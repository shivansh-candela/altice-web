#!/usr/bin/perl -w
#--------------------------------------------------------------------------#
#                    Wifi Portal Login Script                              #
#                                                                          #
#  portal-bot.pl is intended to be a framework for use with a module       #
#  written specificly for the portal you intend to test. Please see        #
#  wifi-portal-bot-creation cookbook for full documentation.               #
#                                                                          #
#  URLs, credentials and ancillary information that does not need to be    #
#  manipulated using the GUI Port tab Batch Modify tool can be placed      #
#  in the file portal_creds.pm. Please consult portal_creds.pm-example     #
#  for an template you can modify; copy the example to portal_creds.pm     #
#  and the file will be incorporated the next time portal-bot.pl runs.     #
#                                                                          #
#  Ensure that 'lanforge.profile' has been sourced in shell when           #
#  executing this from the commandline. This script uses a modified ver    #
#  of libcurl maintained by Candela Technologies. The LD_LIBRARY_PATH must #
#  include /home/lanforge/local/lib for local/bin/curl to work. This is a  #
#  concern when testing the script from command line from portal-bot.bash. #
#  Those libraries are automatically pathed if portal-bot.pl is invoked    #
#  from the LANforge manager.                                              #
#                                                                          #
#  When modifying this script, it is important to NOT CRASH and NOT DIE.   #
#  Script failure will leave the LANforge process hanging for a 120s       #
#  timeout. If you are seeing 'UNHANG' messages in the LANforge Message    #
#  window, your script is either hanging on a curl call that is in the     #
#  middle of a dns timeout, or your script has died before making it to    #
#  signal_exit(). The LANforge process will not interperet system call     #
#  return value, the process listening on mgt_pipe is not the same process #
#  that made the system("./portal-bot.pl ..."); call. If you are on the    #
#  lanforge system, tail these logs:                                       #
#        lanforge_log_1.txt     # wpa_supplicant and invocation log here   #
#        run_client_1.out       # crash messages appear here               #
#        wifi/portal-bot.$dev.log # botlib::logg() messages here           #
#                                                                          #
#--------------------------------------------------------------------------#
# Portal-bot.pl expects the bot:: module to export the following methods:  #
#                                                                          #
#  - bot::find_redirect_url   #  Makes the first http request and          #
#                             #  parses the response for anticiapted       #
#                             #  portal page url. The first http request   #
#                             #  is --start_url (-s)                       #
#                                                                          #
#  - bot::submit_login        #  Uses the --login_form and --login_action  #
#                             #  values to request the login form and      #
#                             #  submit the credentials supplied with the  #
#                             #  --user, --pass options.                   #
#                                                                          #
#  - bot::interpret_login_response                                         #
#                             #  Read the web response after posting to    #
#                             #  --login_action. Look for access granted   #
#                             #  or deny and return value to $::rslt.      #
#                                                                          #
#  - bot::submit_logout       #  Doing logout is one of the more useful    #
#                             #  techniques for releasing a dhcp lease.    #
#                             #  This posts --logout_url and returns       #
#                             #  value to $::rslt if logout successful.    #
#                                                                          #
#--------------------------------------------------------------------------#
#  Forking is manditory if the script is called from the LANforge process. #
#  Not forking will hang the LANforge server. Only disable forking when    #
#  starting script from portal-bot.bash. If invoking script by hand, try:  #
#  lanforge@host $ PBOT_NOFORK=1 PBOT_DEBUG=1 ./portal-bot.pl -b x.pm .... #
#--------------------------------------------------------------------------#


package main;
# do no use Time::HiRes qw(time), module load time too long!
# do not use botlib::date_milli() yet, we haven't loaded it, and
# we want to include latency of all library load times
our $start_at     = `date +%s.%6N`;
our $invoked_at   = 0;
our $use_fork     = 1;
our $explanation  = "";
our $is_verbose   = 0;
$is_verbose       = ( grep {/^-[dv]$/} @ARGV);
our $delays_opt   = "";
our @delays       = ();

if ($::use_fork) {
   if ($ENV{'PBOT_NOFORK'} || $ENV{'PBOT_DEBUG'}) {
      print "Not forking\n" if ($is_verbose);
   }
   else {
      my $cpid = fork();
      if ($cpid > 0) {
         # We are parent process, tell LF our child's pid so it can manage it.
         print "CHILD_PID: $cpid\n";
         exit(0);
      }
   }
}
else {
  # Not forking, print out our own PID for management.
  print "CHILD_PID: $$\n";
}

#--------------------------------------------------------------------------#
#                                                                          #
#   Only enable the use statements below if you are fixing the script      #
#   because they add considerable latency to execution. Especially do not  #
#   start using 'use constant foo => n' statements because that forces     #
#   a lengthy load of utf8_heavy.pm somewhere.                            #
#                                                                          #
#--------------------------------------------------------------------------#

if ( defined $ENV{'PBOT_NOFORK'} &&  $ENV{'PBOT_NOFORK'} eq "1") {
   use strict;
   use warnings;
   #use diagnostics;
   use Carp;
   $SIG{ __DIE__ } = sub { Carp::confess( @_ ) };
}
use lib ".";
use botlib qw(dbg dbgdie isBlank signal_exit logg newEvent request delay);
$|=1; #flush stdout immediately

our $no_mgr       =  0;
our $lfmgr_host   = "127.0.0.1"; # use the --no_mgr option to unset this
our $lfmgr_port   = "4001";
our $rslt         = "FAIL";
our $debug        = $ENV{'PBOT_DEBUG'} || 0;
our $verbose      = $ENV{'PBOT_DEBUG'} || 0;
our $dev          = undef;
our $ip4          = undef;
our $ip6          = undef;
our $dns          = undef;
our $mgt_pipe     = undef;
our $ap_url       = undef;
our $login_form   = undef;
our $login_action = undef;
our $logout_url   = undef;
our $start_url    = undef;
our $cookie       = undef; #libcurl cookie storage
our $logfile      = undef;
our $user         = undef;
our $pass         = undef;
our $cust_botlib  = undef; # robot brains
our $do_logout    = 0;
our $dummy_ok     = 0;
our $dummy_fail   = 0;
our $dummy_hang   = 0;
our $is_roaming   = 0;

##------------------------------------------------------------------------
our $usage     = "$0
   -i       <dev>                # required
   --ip4    <ip>                 # required
   --ip6    <ip6>                # required
   --dns    <ip>                 # required
   --mgt    </dev/null | file>   # required
   --no_mgr                      # skips association with manager instance at 127.0.0.1
     # consider this when you need performance, it prohibits sending LANforge events
   --ap_url    <url>             # or -a
   --start_url <url|path>        # or -s if ap_url, use path shorthand
   --login_form <url|path>       # or -n if ap_url, use path shorthand
   --login_action <url|path>     # or -o if ap_url, use path shorthand
   --logout_url <url|path>       # or -t if ap_url, use path shorthand
   --user   <string>             # or -u
   --pass   <string>             # or -p
   --bot    <your_perl.pm>       # or -b customization lib for your portal
   --debug  <yes|no>             # or -d
   --verbose                     # or -v
   --logout                      # skips to logout logic, requires logout_url
   --dummy_ok                    # Skip real logic, just return OK
   --dummy_fail                  # Skip real logic, just return failure
   --dummy_hang                  # Skip real logic, just sleep and do nothing
   --invoked <microsec>          # profiling information
   --roaming                     # or -R, assume auth'd and should not get redirects
   --print                       # print arguments for GUI Port->Misc tab and exit
   --delays <a,b,c,[random]>     # seconds of delay before any POST request,
     # use this to emulate dwell time of user when entering form info
     # random is between {1-119} seconds
     # ranges (E.G.: 4-25) will select a one-time random integer in that range
     # delay[0] used when first requesting start url
     # delay[1] used when first submitting login action
     # delay[2] used when first submitting logout action
     # delay[3+], if set will be used for any other POST submission delay
     # A single digit is a
     # if only one, two, or three delay items provided, the last entry will be
     # used as necessary. To skip a delay, set it to 0 (E.G.: 1,random,0,2).
   -h                            # usage
   ";

# consider using --invoked like this: portal-bot.pl --dummy_ok --invoked `date +%s.%6N`
##-------------------------------------------------------------------------#
#        M  A  I  N                                                        #
##-------------------------------------------------------------------------#

if (@ARGV < 1 ) {
   print $::usage;
   exit 1;
}

my $show_help =0;
my $just_print=0;
botlib::myoptions( {
   'i|dev|sta=s'     => \$::dev,
   'ip4=s'           => \$::ip4,
   'ip6=s'           => \$::ip6,
   'dns=s'           => \$::dns,
   'mgt=s'           => \$::mgt_pipe,
   'no_mgr'          => \$::no_mgr,
   'a|ap_url=s'      => \$::ap_url,
   's|start_url=s'   => \$::start_url,
   'n|login_form=s'  => \$::login_form,
   'o|login_action=s'=> \$::login_action,
   't|logout_url=s'  => \$::logout_url,
   'u|user=s'        => \$::user,
   'p|pass=s'        => \$::pass,
   'b|bot=s'         => \$::cust_botlib,
   'd|debug'         => \$::debug,
   'v|verbose'       => \$::verbose,
   'logout'          => \$::do_logout,
   'dummy_ok'        => \$::dummy_ok,
   'dummy_fail'      => \$::dummy_fail,
   'dummy_hang'      => \$::dummy_hang,
   'r|roaming'       => \$::is_roaming,
   "invoked=f"       => \$::invoked_at,
   "delays=s"        => \$::delays_opt,
   "print"           => \$just_print,
   'h|help',         => \$show_help
}) || (print $::usage && exit 1);

if ($show_help) {
   print $::usage;
   exit 0;
}

if ($just_print) {
   my %targs = (
      'ap_url'          => $::ap_url,
      'start_url'       => $::start_url,
      'login_form'      => $::login_form,
      'login_action'    => $::login_action,
      'logout_url'      => $::logout_url,
      'user'            => $::user,
      'pass'            => $::pass,
      'bot'             => $::cust_botlib,
      'logout'          => $::do_logout,
      'dummy_ok'        => $::dummy_ok,
      'dummy_fail'      => $::dummy_fail,
      'dummy_hang'      => $::dummy_hang,
      'roaming',        => $::is_roaming,
      'invoked'         => $::invoked_at,
   );
   print "$0";
   for $k (keys %targs) {
      next if (($k =~ /(logout|dummy|roaming|invoked)/) && ($targs{$k} eq "0"));
      print " --".$k." ";
      if (($targs{$k} eq "") || ($targs{$k} =~ / /)) {
         print qq("$targs{$k}");
      }
      else {
         print qq($targs{$k});
      }

   }
   print qq(\n);
   exit 0;
}

use scripts::LANforge::Utils;
use Net::Telnet ();
my $t;
if ($::no_mgr) {
   logg("Disabling manager connection\n");
   $::lfmgr_host = "";
}
if ($::lfmgr_host ne "") {
   logg("Enabling manager connection\n");
   our $utils = new LANforge::Utils();
   $::utils->connect($lfmgr_host, $lfmgr_port);
}

$::cookie    = "/tmp/${dev}_cookie.txt";      # libcurl cookie storage
$::logfile   = "/home/lanforge/wifi/portal-bot.${dev}.log";
unlink($::cookie) if ( -f $::cookie );

#print STDERR "VERBOSE[$::verbose]\n";

# define the bot:: namespace with botlib
# this expects the following methods:
#  - bot::find_redirect_url
#  - bot::submit_login
#  - bot::submit_logout
#  - bot::interpret_login_response
#
if ( ! defined $::cust_botlib || isBlank($::cust_botlib) || !-f $::cust_botlib ) {
   if (!($::dummy_ok || $::dummy_fail || $::dummy_hang)) {
      dbgdie($::dev, "usage", "Please specify portal customization library.(--bot): $::usage" );
   }
}
else {
  dbgdie($::dev, "missing-botlib", "Error importing botlib library [$::cust_botlib]") if( !do $::cust_botlib );
}

##------------------------------------------------------------------------
#  seek credentials for device and invoke ifup_post script
##------------------------------------------------------------------------
my $un = $::user;
my $pd = $::pass;

if ( -f "portal_creds.pm" ) {
   eval "use portal_creds"; #use portal_creds; # holds list of creds to test
   logg("creds has ".@creds::creds." items");

   if ( isBlank($un)             || isBlank($pd)               || isBlank($::start_url)
      || isBlank($::login_form)  || isBlank($::login_action)   || isBlank($::logout_url)) {

      for (my $i = 0; $i< @creds::creds; $i++) {
         next if ($creds::creds[$i]->{"dev"} ne $::dev );

         if (!defined $::user ) {
            $un = $creds::creds[$i]->{"username"};
         }
         if (!defined $::pass) {
            $pd = $creds::creds[$i]->{"passwd"};
         }
         if (!defined $::start_url) {
            $::start_url = $creds::creds[$i]->{"start_url"};
         }
         if (!defined $::login_form) {
            $::login_form = $creds::creds[$i]->{"login_form"};
         }
         if (!defined $::login_action) {
            $::login_action = $creds::creds[$i]->{"login_action"};
         }
         if (!defined $::logout_url) {
            $::logout_url = $creds::creds[$i]->{"logout_url"};
         }

         botlib::logg qq($i dev:${creds::creds[$i]->{dev}} dev[$::dev] user[$un] pass[$pd]);
         last;
      }
   } # endif login credentials had blanks
} # endif conditional use of portal_creds.pm

dbgdie("", "usage", "Please specify device:$::usage")
   if ( !defined $::dev       || isBlank($::dev      ));
dbgdie($::dev, "usage", "Please specify ip4:$::usage") if ( !defined $::ip4 );
dbgdie($::dev, "usage", "Please specify ip6:$::usage") if ( !defined $::ip6 );
dbgdie($::dev, "usage", "Please use either ip4 or ip6:$::usage")
   if (isBlank($::ip6) && isBlank($::ip4));

dbgdie($::dev, "usage", "Please specify dns address:$::usage")
   if ( !defined $::dns       || isBlank($::dns      ));

dbgdie($::dev, "usage", "DNS only has 8.8.8.8!"
   ." Please specify a local nameserver instead of only google.")
   if ( $dns eq "8.8.8.8" );

if ( $dns =~ /^8\.8\.8\.8/ ) {
   logg('DNS starts with 8.8.8.8!'
   .' Please put your local nameserver first,'
   .' you will get a DNS timeout for *.local names.');
}
botlib::parseDelayOptions($::delays_opt);
dbgdie($::dev, "usage", ":delays should be a list of 1 or more non-zero values or 'random': --delays 1,2,33,random")
  if ( ($::delays_opt ne "") && @::delays < 1);

dbgdie($::dev, "usage", "Please specify mgt_pipe address:$::usage")
   if ( !defined $::mgt_pipe  || isBlank($::mgt_pipe ));

if (!($::dummy_ok || $::dummy_fail || $::dummy_hang)) {
   dbgdie($::dev, "usage", "Please specify start_url:$::usage")
      if ( !defined $::start_url || isBlank($::start_url));
   dbgdie($::dev, "usage", "Please specify login_form:$::usage")
      if ( !defined $::login_form || isBlank($::login_form));
   dbgdie($::dev, "usage", "Please specify login_action:$::usage")
      if ( !defined $::login_action || isBlank($::login_action));

   dbgdie($::dev, "usage", "Please specify logout_url:$::usage")
      if ( !defined $::logout_url || isBlank($::logout_url));
   dbgdie($::dev, "usage", "Please specify ap_url:$::usage")
      if ( !defined $::ap_url    || isBlank($::ap_url));
   dbgdie($::dev, "usage", "Please specify user:$::usage")
      if ( !defined $un          || isBlank($un));
   dbgdie($::dev, "usage", "Please specify password:$::usage")
      if ( !defined $pd          || isBlank($pd));
}
else {
  if ( !defined $::start_url || isBlank($::start_url)) {
    $::start_url = "";
  }
}

if (!$::do_logout) {
   unlink($::cookie);
}

# Add logic here to access wifi portal web pages, etc.
# Bind to interface and IP address or it may not work as desired.

$::login_form     = "" if ($::login_form     eq "NA");
$::login_action   = "" if ($::login_action   eq "NA");
$::logout_url     = "" if ($::logout_url     eq "NA");

my $dns_srv = " ";
if ($dns ne "NA") {
  $dns_srv     = " --dns-servers $dns ";
}

my @extended_options=split( "\n", `/home/lanforge/local/bin/curl --help` );
my @dns_opts1 = grep { /dns_interface/ } @extended_options;
my @dns_opts2 = grep { /dns-interface/ } @extended_options;
my $use_dns_under = 0;
if (@dns_opts1 > 0) {
   $use_dns_under = 1;
}
#my @pingargs = ("./vrf_exec.bash", "$::dev", "ping", "-c2", "-i1", "-w3", "-W2", "8.8.8.8");
#my $retval = system(@pingargs);
#$auth_result = "Non-Authenication";
#if($retval == 0){
#   $auth_result = "Authentication";
#}
logg("\nInternet Access: $auth_result\n");
bot::check_authentication($auth_result);
our $curl_args  = "/home/lanforge/local/bin/curl "
   .(($::do_logout)?"-X POST ":"")
   .(($::debug)?"-v ":"")
   ."-sLki "
   ."-c $::cookie "
   ."-b $::cookie "
   ."-4 "
   ."--interface $::dev "
   ."--localaddr $::ip4 "
   .$dns_srv
   .(($use_dns_under)?" --dns_interface":" --dns-interface")." $::dev "
   .(($use_dns_under)?" --dns_ipv4_addr":" --dns-ipv4-addr")." $::ip4 "
   .((defined $bot::extra_args)?$bot::extra_args:"")
   ;
dbg "Curl_args: $::curl_args";

if ($::do_logout) {
   if ($::dummy_ok) {
      $::rslt = "OK -LOGOUT (Dummy)";
   }
   elsif ($::dummy_fail) {
      $::rslt = "FAIL -LOGOUT (Dummy)";
   }
   elsif ($::dummy_hang) {
      sleep(5000);
   }
   else {
      my @response_logout_page    = ();
      #request({'curl_args'  => $::curl_args,
      #         'delay'       => "0,0",
      #          'url'        => $::start_url},
      #          \@response_logout_page);
      #my ($redirect_url_logout, $gw_id_logout)  = bot::find_redirect_url( \@response_logout_page);
      #$::logout_url = $::ap_url.$::logout_url."?".$gw_id_logout;
      #logg( "logout_url: $::logout_url");
      #$::rslt = bot::submit_logout($::logout_url)
   }
}
else {
   if ($::dummy_ok) {
      $::rslt = "OK (Dummy)";
   }
   elsif ($::dummy_fail) {
      $::rslt = "FAIL (Dummy)";
   }
   elsif ($::dummy_hang) {
      sleep(5000);
   }
   else {
      logg("\nrequesting start_url using: $::curl_args $::start_url\n");

      my $curl_start_at    = botlib::time_milli();
      #my @response_page    = split(/\n/, `$::curl_args "$::start_url"`);
      my @response_page    = ();
      request({'curl_args'  => $::curl_args,
              'delay'       => "0,0",
               'url'        => $::start_url,
               'print'     => 0},
               \@response_page);
      my $curl_delta       = botlib::time_milli() - $curl_start_at;
      logg(sprintf "first_page_load time: %0.6f\n", $curl_delta);
      botlib::newEvent("first_page_load", $curl_delta, $::dev);
      dbg("recieved page:\n".join("\n", @response_page)."\n");
      #logg("@response_page");
      if ($::is_roaming) {
         # indicates we have already logged in and should not expect a redirect.
         # if we get a redirect, we need to signal fail
         my @location_s=grep(/^Location: /, @response_page);
         if (@location_s > 0) {
            logg("Redirected while roaming:");
            logg(join("\n", @location_s));
            $::rslt = "FAIL -Redirected while roaming";
         }
         else {
            $::rslt = "OK";
         }
      }
      else {
         #use bot qw(find_redirect_url submit_login interpret_login_response);
         my ($url, $redirect_url, $gw_id)  = bot::find_redirect_url( \@response_page);
         logg("redirect_url $redirect_url\n");
         my @firefox_url = split / /, $url;
         my @split_url  = split /wifidog/, $redirect_url;

         delay(0, 1)
            if (@delays>0);
         my $ra_login_response = bot::submit_login($redirect_url,
                                                   $un,
                                                   $pd,
                                                   $redirect_url.$::login_form,
                                                   $redirect_url.$::login_action."?".$gw_id,
                                                   $gw_id);
         logg "ra_login_r: ".join("\n", @$ra_login_response)."\n";
         $::rslt = bot::interpret_login_response($ra_login_response);
         my $token_url = $split_url[0] . "cpUserInfo";
         my @response_token    = ();
         request({'curl_args'  => $::curl_args,
                  'delay'       => "0,0",
                  'method'    => "POST",
                  'post_data'       => '{"mac":"xyz","randomId":"xyz","gw_id":"xyz"}',
                  'url'        => $token_url,
                  'print'     => 1},
                \@response_token);
         my @found      = grep(/randomId/, @response_token);
         my $url_token = $found[0];
         my @spliturl = split /,/, $url_token;
         my $spliturl1 = $spliturl[1];
         my @randomid_val = split /:/, $spliturl1;
         my $token_val = $randomid_val[1];
         $token_val =~ s/[^a-zA-Z0-9]*//g;
         $port = $redirect_url;
         $port =~ s/3001/2060/ig;
         my @ret_response4 = bot::simple_get($port . "auth?token=" . $token_val,1);

         delay(0, 1)
            if (@delays>0);

         my @ret_response8 = bot::simple_get("http://www.isro.com/",1);
         my @found_data      = grep(/ISRO.COM/, @ret_response8);
         my @rslt_data = bot::interpret_autoredirect_response($found_data[0]);
      }
   }
}


logg("result for $::dev: $::rslt");
signal_exit($::dev, $::rslt, $::mgt_pipe);


###
###
###
