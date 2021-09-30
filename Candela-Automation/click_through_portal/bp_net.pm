##----------------------------------------------------------------------------#
##                                                                            #
##   Basic-Portal portal-bot module. Use the --bot/-b switch                  #
##   from the portal-bot.pl command line; EG:                                 #
##   portal-bot.pl -b bp.pm ...                                               #
##                                                                            #
##   It is absolutely necessary that no code in bot:: modules endangers the   #
##   operation of the portal-bot script. Do not call die() or exit().         #
##   Communicate your displeasure using logg(), dbgdie() or signal_exit().    #
##----------------------------------------------------------------------------#
package bot;
use Data::Dumper qw(Dumper);
# do not turn on debugging by default when doing performance monitoring
# all perl includes have a startup cost to them
if ( defined $ENV{'PBOT_NOFORK'} &&  $ENV{'PBOT_NOFORK'} eq "1") {
   use strict;
   use warnings;
   #use diagnostics;
   use Carp;
   #use Data::Dumper;
   $SIG{ __DIE__ } = sub { Carp::confess( @_ ) };
}

use URI::Escape;
use botlib qw(dbg isBlank logg signal_exit dbgdie newEvent request delay);
use Exporter;
our @EXPORT_OK = qw(find_redirect_url check_authentication simple_get simple_post submit_login submit_logout interpret_login_response interpret_autoredirect_response get_explanation);

# this demonstrates handling: Redirect 302 /start /login.php
sub find_redirect_url {
   my $curl_delta = botlib::time_milli() - $::start_at;
   my $ra_page    = shift;
   my @found      = grep {/^Location: /} @$ra_page;
   my $redir      = undef;
   my $extract_url    = $found[0];
   my @split_url  = split /&/, $extract_url;
   my $gw_id1      = $split_url[2];
   if ($extract_url =~ /microsoft.com/){
       my $session_retain = "success";
       newEvent("session retain: $session_retain", $curl_delta, $::dev);
   }
   else{   
       my $session_retain = "Fail";
       newEvent("session retain: $session_retain", $curl_delta, $::dev);
   }
   return (@found, $::ap_url, $gw_id1);
}

sub simple_get {
   my $url = shift;
   my $print = shift;
   my @ra_response = ();
   request({'curl_args'  => $::curl_args,
            'url'       => $url,
            'method'    => 'GET',
            'print'     => $print},
            \@ra_response);
   #logg(join("\nSG>", @$ra_response))
   #   if ($print);
   return @ra_response;
   
}


sub simple_post {
   my $url = shift;
   my $print = shift;
   my @ra_response = ();
   request({'curl_args'  => $::curl_args,
            'url'       => $url,
            'method'    => 'POST',
            'print'     => $print},
            \@ra_response);
   #logg(join("\nSG>", @$ra_response))
   #   if ($print);
   return @ra_response;
   
}
sub check_authentication {
   my $auth_ok = shift;
   my $curl_delta = botlib::time_milli() - $::start_at;
   newEvent("Internet Access: $auth_ok", $curl_delta, $::dev);
}


sub submit_login {
   my $base_redir = shift;
   my $user_name  = shift;
   my $passwd     = shift;
   my $get_url    = shift;
   my $post_url   = shift;

   my $post_data  = "";
   my @response   = ();
   request({'curl_args' => $::curl_args,
            'url'       => $post_url,
            'method'    => 'GET',
            'post_data' => $post_data,
            'print'     => 0},         # turns on debugging
            \@response);

#   # example of chosing a delay near the end of the list that might not be there
#   request({'curl_args' => $::curl_args,
#            'url'       => "$post_url?asdf=3",
#            'delay'     => '0,3',
#            'method'    => 'GET',
#            'print'     => 1},         # turns on debugging
#            \@response);
#
   my $curl_delta = botlib::time_milli() - $::start_at;
   newEvent("submit_login", $curl_delta, $::dev);
   if (@response < 1) {
   newEvent("auto redirection webpage: FAIL", $curl_delta, $::dev);   
   dbgdie($::dev, 'empty-response', 'No data found in login post response');
   }

   return \@response;
}

# set the ::rslt variable
sub interpret_login_response {
   my $ra_response   = shift @_;
   my $curl_delta    = botlib::time_milli() - $::start_at;
   #logg( "INTERPRET given ".join("\n", @$ra_response));

   my @found         = grep (/Login Successful/i, @$ra_response);
   logg("found ref to data? ".join("\n", @found));

   if (@found < 1) {
      newEvent("auto redirection webpage: FAIL", $curl_delta, $::dev);   
      dbgdie($::dev, "on-login-submit", "access-granted not found");
   }
   my $result        = $::rslt; # presumably FAIL
   if ($found[0] =~ /Login Successful/ ) {
      $result        = "OK"; # infers login
      newEvent("portal_login: $result", $curl_delta, $::dev);

   }
   else {
      $result        = "FAIL -LOGIN-incorrect_passwd"; # infers login
      $::explanation = get_explanation($ra_response);
      newEvent("portal_login: $result $::explanation", $curl_delta, $::dev);
   }

   return $result;
}

sub interpret_autoredirect_response {
   my $auto_response   = shift;
   my $curl_delta    = botlib::time_milli() - $::start_at;
   #logg( "INTERPRET given ".join("\n", @$ra_response));

   if ($auto_response =~ /ISRO.COM/){
      my $result        = "OK";
      newEvent("auto redirection webpage: $result", $curl_delta, $::dev);
   }
   else {
      my $result        = "FAIL"; # infers login
      newEvent("auto redirection webpage: $result", $curl_delta, $::dev);
   }
   #print("$result");
   return $result;
}

# only place -LOGOUT is needed in response is for logout, other values infer login
sub submit_logout {
   my $out_url = shift @_;



   if (!defined $out_url || isBlank($out_url)){
      newEvent("auto redirection webpage: FAIL", $curl_delta, $::dev);   
      dbgdie($::dev, "usage", "submit_logout missing logout_url");
}
   $out_url       =~ s/!/%21/g;
   my @response   = ();
   request({'curl_args' => $::curl_args,
            'url'       => $out_url,
            'delay'     => '0,2',
            'post_data' => ""},
            \@response);

   my $curl_delta = botlib::time_milli() - $::start_at;
   my @found      = grep {/Login Successful/i} @response;
   if (@found > 0 ) {
      $::rslt     = "OK -LOGOUT";
   }
   else {
      $::rslt     = "FAIL -LOGOUT";
      $::explanation = get_explanation(\@response);
   }
   botlib::newEvent("submit_logout: $::rslt $::explanation", $curl_delta, $::dev);
   return $::rslt;
}

sub get_explanation {
   $ra_result        = shift;
   my $expl          = "unknown";
   my $err_code      = "NA";
   my $err_msg       = "NA";
   for $line (@$ra_result) {
      dbg("get_explanation: $line");
      next unless ($line =~ /^X-err-/);
      ($err_code) = $line =~ /^X-err-no: (.*)$/
         if ($line =~ /^X-err-no: /);
      ($err_msg ) = $line =~ /^X-err-msg: (.*)$/
         if ($line =~ /^X-err-msg: /);
   }
   #dbg Dumper($err_code);
   #dbg Dumper($err_msg);
   if ((defined $err_code) && ($err_code ne "")
      || (defined $err_msg) && ($err_msg ne "")) {
      $expl = $err_code.",".$err_msg;
   }
   else {
      logg("get_explanation: incomplete error data");
   }
   return $expl;
}

1;
