import sys
import os
import importlib
import argparse
import time
import shlex
import logging

logger = logging.getLogger(__name__)

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
cv_test_manager = importlib.import_module("py-json.cv_test_manager")
cv_test = cv_test_manager.cv_test
wifi_monitor_profile = importlib.import_module("py-json.wifi_monitor_profile")
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")
# sniff_radio = importlib.import_module("py-scripts.lf_sniff_radio")
set_wifi_radio = importlib.import_module("py-json.LANforge.set_wifi_radio")
set_radio_mode = set_wifi_radio.set_radio_mode

class LargeClients(cv_test):
    def __init__(self,
                 lfmgr="localhost",
                 port="8080",
                 _debug_on=False,
                 ):
        super().__init__(
            lfclient_host=lfmgr,
            lfclient_port=port,
            debug_=_debug_on
        )
        self.lfmgr = lfmgr
        self.port = port

    def load_apply_scenario(self, scenario):
        self.sync_cv()  # chamberview sync
        time.sleep(2)
        print("Applying scenario")
        self.apply_cv_scenario(scenario)  # Apply scenario
        self.show_text_blob(None, None, False)  # Show changes on GUI
        self.apply_cv_scenario(scenario)  # Apply scenario
        self.build_cv_scenario()  # build scenario

class RadioSniff(Realm):
    def __init__(self,
                 lfclient_host="localhost",
                 lfclient_port=8080,
                 radio="wiphy0",
                 outfile="/home/lanforge/test_pcap.pcap",
                 duration=60,
                 channel=None,
                 channel_freq=None,
                 # channel_bw=None,
                 center_freq=None,
                 radio_mode="AUTO",
                 debug_on_=True,
                 monitor_name=None,
                 # sniff_snapshot_bytes=None,
                 # sniff_flags=None
                 ):
        super().__init__(lfclient_host, lfclient_port)
        self.lfclient_host = lfclient_host
        self.lfclient_port = lfclient_port
        self.debug = debug_on_
        self.local_realm = realm.Realm(lfclient_host=self.lfclient_host,
                                       lfclient_port=self.lfclient_port,
                                       debug_=self.debug)
        self.monitor = self.new_wifi_monitor_profile()
        self.outfile = outfile
        self.radio = radio
        self.channel = channel
        self.channel_freq = channel_freq
        # self.channel_bw = channel_bw
        self.center_freq = center_freq
        self.duration = duration
        self.mode = radio_mode
        self.monitor_name = monitor_name
        self.monitor_info = ''
        # self.sniff_snapshot_bytes = sniff_snapshot_bytes  # default to max size
        # self.sniff_flags = sniff_flags  # will default to dumpcap, see wifi_monitor_profile::SNIFF_X constants
        if self.channel_freq is not None:
            self.freq = self.channel_freq
            logger.info("channel frequency {freq}".format(freq=self.channel_freq))
        # conversion of 6e channel to frequency
        # ch_6e = (f - 5000 )  / 5
        # f = (ch_6e * 5) + 5000
        elif self.channel is not None:
            if self.channel != 'AUTO':
                if 'e' in self.channel:
                    channel_6e = self.channel.replace('e', '')
                    self.freq = ((int(channel_6e) + 190) * 5) + 5000
                    lf_6e_chan = int(channel_6e) + 190
                    logger.info("6e_chan: {chan} lf_6e_chan: {lf_chan} frequency: {freq}".format(chan=self.channel, lf_chan=lf_6e_chan, freq=self.freq))
                    self.channel = lf_6e_chan
                else:
                    if int(self.channel) <= 13:
                        # channel 1 is 2412 ,
                        self.freq = 2407 + int(self.channel) * 5
                    elif int(self.channel) == 14:
                        self.freq = 2484
                    # 5g or 6g Candela numbering
                    else:
                        self.freq = int(self.channel) * 5 + 5000
                    logger.info("channel: {chan}  frequency: {freq}".format(chan=self.channel, freq=self.freq))

    def setup(self, data):
        self.monitor.create(radio_=self.radio, channel=self.channel, frequency=self.freq, mode=self.mode,
                            name_=self.monitor_name, data_input=data)






def main():
    parser = cv_test.create_basic_argparse(
        prog='large_clients_test.py',
        formatter_class=argparse.RawTextHelpFormatter,
        )
    parser.add_argument(
        "--scenario",
        type=str,
        help="Name of the scenario that we want to load and apply"

    )
    #parser.add_argument('--radio', type=str, help='--radio: Radio to sniff', default="wiphy0")
    parser.add_argument('--outfile', type=str, help='--outfile: give the filename with path',
                        default="/home/lanforge/test_pcap.pcap")
    # parser.add_argument('--duration', type=int, help='--duration duration in sec, for which you want to capture',
    #                     default=60)
    parser.add_argument('--channel', type=str, help='''
                                        --channel Set channel pn selected Radio, the channel [52, 56 ...]
                                        channel will get converted to the control frequency.
                                        Must enter Channel
                                        ''',
                        default='36')
    parser.add_argument('--channel_freq', type=str, help='''
                                       --channel_freq  this is the frequency that the channel operates at
                                       Must enter --channel or --channel_freq
                                       --channel_freq takes presidence if both entered if value not zero
                                       ''')
    parser.add_argument('--radio_mode', type=str, help='--radio_mode select the radio mode [AUTO, 802.11a, 802.11b, '
                                                       '802.11ab ...]', default="AUTO")
    parser.add_argument('--monitor_name', type=str, help='Wi-Fi monitor name', default="sniffer0")
    parser.add_argument('--sniff_bytes', default=None,
                        help='keep this many bytes per packet, helps to reduce overall capture size')
    parser.add_argument('--sniff_using', default=None,
                        help="""Default sniffer is wireshark, which is only useful from a desktop setting.
                            Combine options with a comma: dumpcap,mate_xterm
            tshark:             headless tshark utility
            dumpcap:            headless dumpcap utility
            mate_terminal:      make tshark/dumpcap interactive in a MATE terminal
            mate_xterm:         make tshark/dumpcap interactive in an xterm
            mate_kill_dumpcap:  kill previously issued dumpcap""")
    args = parser.parse_args()
    large_clients = LargeClients(lfmgr=args.mgr,
                                 _debug_on=args.debug,
                                 port=args.mgr_port,
                                 )
    large_clients.load_apply_scenario(scenario=args.scenario)
    obj = RadioSniff(lfclient_host=args.mgr,
                     lfclient_port=args.mgr_port,
                     radio=args.radio,
                     outfile=args.outfile,
                     channel=args.channel,
                     channel_freq=args.channel_freq,
                     radio_mode=args.radio_mode,
                     monitor_name=args.monitor_name,
                     )
    data = {
        "shelf": 1,
        "resource": 1,
        "radio": args.radio,
        "channel": args.channel,
        "flags": 184614912
    }
    obj.setup(data)
if __name__ == "__main__":
    main()