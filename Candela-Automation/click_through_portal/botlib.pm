##----------------------------------------------------------------------------#
##                                                                            #
##   Provides library functions for portal-bot.pl and any bot:: module.       #
##                                                                            #
##----------------------------------------------------------------------------#
package botlib;

if ( defined $ENV{'PBOT_NOFORK'} &&  $ENV{'PBOT_NOFORK'} eq "1") {
   use strict;
   use warnings;
   #use diagnostics;
   use Carp;
   $SIG{ __DIE__ } = sub { Carp::confess( @_ ) };
   use Data::Dumper;
}

our $NL="\n";
use base 'Exporter';
our @EXPORT_OK = qw(dbg isBlank logg signal_exit dbgdie newEvent request getSessionDataFileName loadSessionFile updateSessionFile parseDelayOptions delay);
our $PRIO_INFO = 2;
our $CUSTOM    = 2;

sub dbg {
   my $msg = shift(@_);
   print qq(DEBUG: $msg\n) if ($::debug);
}

sub isBlank {
   my ($m) = @_;
   return ((!defined $m) || ("$m" eq ""));
}

sub getSessionDataFileName {
   dbgdie($::dev, "misconfiguration",
         "botlib::getSessionDataFileName requires bot::module_name defined")
      if (!defined $bot::module_name or "$bot::module_name" eq "" );
   $bot::session_data_file = "wifi/$::dev.portal-".$bot::module_name.".txt";
   return $bot::session_data_file;
}

sub loadSessionFile() {
   my $sess_fn = getSessionDataFileName();
   if ( ! -f $sess_fn ) {
      `touch "$sess_fn"`;
   }
   open(my $fh, "<", $sess_fn)
      or dbgdie($::dev, "lost-bot-session",
         "loadSessionFile: unable to open [$sess_fn] to read session data");
   #print $fh $bot::redir;
   my @lines = <$fh>;
   close $fh;
   my ($k, $v);
   for my $line (@lines) {
      ($k, $v) = $line =~ /([A-Z]+)\s+(.*)$/;
      $::session{$k} = $v;
      dbg("\nSession: key[$k] value[$v]\n");
   }
}

sub updateSessionFile {
   my $rh_new_params = shift;
   my $sess_fn = getSessionDataFileName();
   if (! defined $rh_new_params || (keys %$rh_new_params) < 1) {
      dbg("updateSessionFile: No params to update");
   }
   loadSessionFile(); # updates %::session
   my ($k, $v);
   for $k (keys %$rh_new_params) {
      $::session{ $k } = $rh_new_params->{ $k };
   }
   open(my $fh, ">", $sess_fn)
      or dbgdie($::dev, "lost-bot-session",
         "updateSessionFile: unable to open [$sess_fn] to write session data");
   while( ($k, $v) = each %::session) {
      print $fh "$k $v\n"
   }
   close $fh;
   dbg("\n$sess_fn updated\n");
}

sub defaultRand {
  return 1 + int(rand(118));
}

# expects a,b-c,random comma separated pattersn
# a: integer seconds
# b-c: random range for integer seconds
# random: random 1-119 seconds
# site effect: populates @::delays
sub parseDelayOptions {
  my ($optionstr) = shift;

  return 0
    if (! defined $optionstr || $optionstr eq "");
  my @hunks = split(/,/, $optionstr);
  return 0
    if (@hunks == 0);
  logg("\nParsing delay options: $optionstr\n");
  @::delays = ();
  for my $hunk (@hunks) {
    if ($hunk =~ /^\d+$/) {
      push(@::delays, (0 + $hunk));
    }
    elsif ($hunk =~ /^\d+[-]\d+$/){
      my ($lower, $upper) = $hunk =~ /(\d+)-(\d+)/;
      push(@::delays, randDelay($lower, $upper));
    }
    elsif ($hunk =~ /^rand/i) {
      push(@::delays,  defaultRand())
    }
  }
  logg("\nRandom times are now: ".join(",", @::delays)."\n");
  return 0+(@::delays);
}

# randDelay(a, b) returns random int between a, b
# randDelay(b) returns random int between 1, b
# randDelay(b,b) return b
sub randDelay {
  my ($lower, $upper) = @_;
  dbgdie($::dev, "botlib::randDelay called without arguments")
    if (!defined $lower);
  if (!defined $upper) {
    $upper = 0 + $lower;
    $lower = 1;
  }
  return $upper
    if ($upper == $lower); #this is a stupid conditon to be in
  my $rund = int(rand($upper - $lower) + $lower);
  return $rund;
}
# expects (number) or (number, preferred)
sub delay {
  my $delay       = 0;
  my $pref_index  = -1;
  if (@_ == 2) {
    $delay        = shift;
    $pref_index   = shift;
    if ($pref_index < @::delays) {
      $delay      = $::delays[$pref_index];
      logg("delay: There are ".(@::delays)." delay entries, delay $pref_index: $delay seconds\n");
    }
    else {
      $delay      = $::delays[$#::delays];
      logg("delay: There are ".(@::delays)." delay entries, chose ".$#::delays.": $delay seconds\n");
    }
  }
  else {
    $delay        = shift;
  }

  return
    if ($delay < 1);
  logg("Delaying $delay seconds\n");
  sleep($delay);
}

sub request {
   my $rh_args       = shift;
   my $ra_result     = shift;
   #print Dumper($rh_args);

   dbgdie($::dev, "script-error", "failed to pass hash of arguments to botlib::request()")
      unless( exists $rh_args->{'curl_args'} );
   my $curl_args     = $rh_args->{'curl_args'};

   dbgdie($::dev, "script-error", "failed to pass ref to result lines to botlib::request()")
      if ( !defined $ra_result );

   dbgdie($::dev, "script-error", "failed to pass url to botlib::request()")
      unless( exists $rh_args->{'url'} );

   my $delay          = 0;
   my $delay_index    = -1;
   if (defined $rh_args->{'delay'} && ($rh_args->{'delay'} ne "")) {
     if ($rh_args->{'delay'} =~ /^\d+$/) {
       $delay         = 0 + $rh_args->{'delay'};
     }
     elsif ($rh_args->{'delay'} =~ /^\d+,\d+$/) {
       ($delay, $delay_index) = $rh_args->{'delay'} =~ /^(\d+)[,](\d+)$/;
     }
     elsif ($rh_args->{'delay'} =~ /^rand/i){
       $delay         = randDelay();
     }
     elsif ($rh_args->{'delay'} =~ /^\d+[-]\d+$/) {
       my ($lower, $upper) = $rh_args->{'delay'} =~ /^(\d+)[-](\d+)$/;
       $delay        = randDelay($lower, $upper);
     }
     else {
       logg("request: ignoring delay [".$rh_args->{'delay'}."]\n");
     }
   }
   my $url           = $rh_args->{'url'};
   my $method        = (defined $rh_args->{'method'})      ? $rh_args->{'method'}    : 'GET';
   my $post_data     = (defined $rh_args->{'post_data'})   ? $rh_args->{'post_data'} : '';
   my $result_s      = "";
   my @result_lines  = ();
   my $X             = qq(-X $method);
   my $data          = (!isBlank($post_data))              ? qq(-d '$post_data')     : '';
   my $cmd           = qq($curl_args $X $data '$url');
   if ($delay_index >= 0) {
      logg("request: default_delay[$delay] [$delay_index]\n");
      delay($delay, $delay_index);
   }
   else {
     logg("request: delay[$delay]\n");
     delay($delay)
   }
   logg("\nSubmitting: $cmd\n");
   @{$ra_result}     = split(/\r?\n/, `$cmd`);
   if (exists $rh_args->{'print'}  && $rh_args->{'print'} == 1) {
      logg("\n".join("\nPAGE> ", @$ra_result)."\n");
   }
   my @badness       = grep {/HTTP.1\.1 (400|401|402|404|500) /} @$ra_result;
   if (@badness > 0 ) {
      my ($http_err_code) = $badness[0] =~/HTTP.1\.1 (400|401|402|404|500) /;

      if ((defined bot::get_explanation) && (defined $::explanation)) {
         $::explanation = bot::get_explanation($ra_result);
      }
      else {
         $::explanation = "failed-page-request";
      }
      my $now = `date +%s.%6N`; #::mtime();
      my $elapsed = $now - $::start_at;
      my $latency = ($::invoked_at != 0) ? ($now - $::invoked_at) : ($elapsed);
      #newEvent("HTTP[$http_err_code] $::explanation", $latency, $::dev);
      dbgdie($::dev, "HTTP[$http_err_code] ".$::explanation, join("\nError> ", @badness));
   }
   1;
}

sub time_milli {
   return 0 + `date +%s.%6N`;
}

sub newEvent {
   my $descr   = shift;
   my $delta   = shift;
   my $actor   = shift;
   my $msg     = sprintf("%s %0.6f", $descr, $delta);
   logg("newEvent $descr $delta $actor\n");
   if ($::lfmgr_host ne "") {
      $::utils->doAsyncCmd(qq[add_event new '$msg' $PRIO_INFO $actor]);
   }
}

sub myoptions {
   my $rh_option_map = shift;
   my $i             = 0;
   my $matched       = "";
   my $switch        = 0;
   my $istuple       = 0;
   my $value         = "";
   my $format        = "";
   my @def_opts      = keys %$rh_option_map;
   my $pipesplit     = quotemeta("|");

   foreach my $arg (@ARGV) {
      #print "$i myoptions: $arg $NL";

      if ($arg =~ /^-[a-z]$/) {
         $switch = 1;
      }
      elsif ($arg =~ /^--[a-z]{2,}.+$/) {
         $switch = 1;
      }
      else {
         $switch = 0;
      }

      if ($switch) {
         ($arg) = ($arg =~ /^-{1,2}(.*)$/);
         $value   = "";
         $format  = "";
      }
      else {
         $value   = $arg;
      }
      #print "arg[$arg] switch[$switch]$NL";
      if ($arg =~ /[=]/) {
         $istuple = 1;
      }
      else {
         $istuple = 0;
      }

      #print "istuple: $istuple$NL";
      if ($istuple) {
         my @hunks = split("=", $arg);
         $value = $hunks[1];
      }

      #print "> arg[$arg] switch[$switch] value[$value] matched[$matched]$NL";
      if ($switch gt 0) { # look through defined options for matching thingy
         #print "looking thru @def_opts$NL";
         foreach my $def_opt (@def_opts) {
            my $short_opt = $def_opt;
            #print "Evaluating key[$def_opt]$NL";
            $format="";
            if ($def_opt =~ m/.*?[=][sfi]$/ ) {
               ($short_opt, $format) = ($def_opt =~ /^(.*?)[=](.)$/);
               #print "found format[$format]$NL";
            }

            my @variations    = split($pipesplit, $short_opt);
            #print "found variations[@variations]$NL";
            foreach my $opt_variation (@variations) {
               #print "does $opt_variation match $arg?$NL";
               if ($opt_variation eq $arg) {
                  $matched    = $def_opt;
                  $value      = 1 if ($format eq "");
                  #print "! arg[$arg] switch[$switch] value[$value] matched[$matched]$NL";
                  last;
               }
            }
            if($matched ne "") {
               #print "matched[$matched]$NL";
               #print "@ arg[$arg] switch[$switch] value[$value] matched[$matched]$NL";
               last;
            }
         }
      }
      #print "< arg[$arg] switch[$switch] value[$value] matched[$matched]$NL";
      #print "matched: $matched format: $format$NL";
      if ($value ne "" && $format ne "") {
         $value = sprintf("%s", $value) if ($format eq "s");
         $value = sprintf("%f", $value) if ($format eq "f");
         $value = sprintf("%d", $value) if ($format eq "i");
      }
      #print "% arg[$arg] switch[$switch] value[$value] matched[$matched]$NL";
      #print "matched[$matched] value[$value]$NL";
      if ( $matched ne "" && $value ne "") {
         my $rv_option = $rh_option_map->{ $matched };
         $$rv_option = $value;
         #print "Just set $matched to $value $NL";
         $format  = "";
         $value   = "";
         $matched = "";
         $istuple = 0;
         $switch  = 0;
      }
      $i++;
   }
   # pad set items
   foreach my $def_opt (@def_opts) {
      my $rv_option = $rh_option_map->{ $def_opt };
      if ( ! defined $$rv_option ) {
         $$rv_option = $value;
      }
   }
   return 1;
} # ~myoptions


sub logg {
   if ($::is_verbose) {
      for my $line (@_) {
         print STDERR $line;
      }
   }
   if (! isBlank( $::logfile)) {
      open( my $lf, ">>", $::logfile )
         || signal_exit($::dev, "FAIL-Unable to open logfile[$::logfile]", $::mgt_pipe );

      for my $line (@_) {
         print $lf $line.$NL;
         #print "INF: $line".NL if( $::verbose );
      }
      close( $lf );
   }
   if (defined $::mgt_pipe && $::mgt_pipe ne "/dev/null") {
      open(my $FD, ">", "$::mgt_pipe") || die $!;
      for my $line (@_) {
         print $FD "gossip $::dev $line\n";
      }
      close $FD;
   }
}

##------------------------------------------------------------------------
# this signals back to LANforge
sub signal_exit {
   print STDERR ("misconfigured signal_exit call\n") unless (@_ > 2);
   my $dev        = shift @_;
   my $rslt       = shift @_;
   my $mgt_pipe   = shift @_;
   print STDERR ( "signal_exit usage: mgt_pipe, result\n")
      unless( $dev && $mgt_pipe && $rslt);
   my $now = `date +%s.%6N`; #::mtime();
   my $elapsed = $now - $::start_at;
   my $latency = ($::invoked_at != 0) ? ($now - $::invoked_at) : ($elapsed);

   # Let LANforge know how long it took us to complete this command.
   # The syntax is specific, so do not change.  This should be last,
   # as LANforge will clip this from messages seen by the user and report
   # the timestamp by other means.
   #$rslt .= "(invoked=$::invoked_at now=$now latency=$latency elapsed=$elapsed)";
   #$rslt .= sprintf("(elapsed=%5f ltc=%5f)", $elapsed, $latency);
   $rslt .= "(elapsed=$elapsed $latency)";

   #"$dev RESULT: ".$rslt;
   if (!$::debug && defined $::mgt_pipe && $::mgt_pipe ne "/dev/null") {
      open(my $FD, ">", "$mgt_pipe") || die $!;
      $rslt =~ s/'/"/g; # Make sure we don't have single quotes, messes up CLI parser
      print $FD "admin ifup_post_complete $dev '$rslt'\n";
      close $FD;
   }
   #if ($::debug || !defined $::mgt_pipe || $::mgt_pipe eq "/dev/null" ) {
      print "portal-bot result for $dev: " . $rslt . "\n";
   #}
   exit 0;
}
##------------------------------------------------------------------------

sub dbgdie {
   my $dev        = shift @_;
   my $failcode   = shift @_;
   my $msg        = shift @_;
   logg( "lanforge management pipe misconfigured, set: mgt_pipe\n" )
      unless ($::mgt_pipe);
   logg( "dbgdie requires dev, failcode, msg" )
      unless ($::dev && $failcode && $msg);
   dbg("dbgdie: $failcode $msg\n");
   logg("ERROR: $failcode $msg\n");
   my $now = `date +%s.%6N`;
   my $elapsed = $now - $::start_at;
   my $latency = ($::invoked_at != 0) ? ($now - $::invoked_at) : ($elapsed);

   newEvent("$failcode $msg", $latency, $::dev);
   signal_exit($dev, "FAIL:$failcode $msg", $::mgt_pipe);
}

1;
