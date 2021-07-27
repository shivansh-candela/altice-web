#!/usr/bin/env python3

"""
NAME: rvr_test.py

PURPOSE: rvr_test.py will measure the performance of stations over a certain distance of the DUT. Distance is emulated 
        using programmable attenuators and throughput test is run at each distance/RSSI step.

EXAMPLE:
python3 rvr_test.py --mgr 192.168.200.21 --mgr_port 8080 -u eth1 --num_stations 1
--radio wiphy1 --ssid TestAP5-71 --passwd lanforge --security wpa2 --mode 11 --a_min 1000000 --b_min 1000000 --traffic_type lf_udp

python3 rvr_test.py --num_stations 1 --radio wiphy1 --ssid ct523c-vap --passwd ct523c-vap --security wpa2 --mode 11 --a_min 1000000 --b_min 1000000 --traffic_type lf_udp


Use './rvr_test.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
"""

import sys
import os

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

if 'py-json' not in sys.path:
    sys.path.append(os.path.join(os.path.abspath('..'), 'py-json'))

import argparse
from LANforge import LFUtils
from realm import Realm
import time
import datetime


class rvr_test(Realm):
    def __init__(self,
                 ssid=None,
                 security=None,
                 password=None,
                 create_sta=True,
                 sta_list=None,
                 name_prefix=None,
                 upstream=None,
                 radio="wiphy0",
                 host="localhost",
                 port=8080,
                 mode=0,
                 ap_model="",
                 traffic_type=None,
                 side_a_min_rate=56, side_a_max_rate=0,
                 side_b_min_rate=56, side_b_max_rate=0,
                 number_template="00000",
                 test_duration="2m",
                 use_ht160=False,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super.__init__(lfclient_host=host, lfclilent_port=port),
        self.upstream = upstream
        self.host = host
        self.port = port
        self.ssid = ssid
        self.security = security
        self.password = password
        self.sta_list = sta_list
        self.create_sta = create_sta
        self.radio = radio
        self.mode = mode
        self.upload = side_a_min_rate
        self.download = side_b_min_rate
        self.ap_model = ap_model
        self.traffic_type = traffic_type
        self.number_template = number_template
        self.debug = _debug_on
        self.name_prefix = name_prefix
        self.test_duration = test_duration
        self.station_profile = self.new_station_profile()
        self.cx_profile = self.new_l3_cx_profile()
        self.station_profile.lfclient_url = self.lfclient_url
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.password
        self.station_profile.security = self.security
        self.station_profile.number_template_ = self.number_template
        self.station_profile.debug = self.debug
        self.station_profile.use_ht160 = use_ht160
        if self.station_profile.use_ht160:
            self.station_profile.mode = 9
        self.station_profile.mode = mode
        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.cx_profile.name_prefix = self.name_prefix
        self.cx_profile.side_a_min_bps = side_a_min_rate
        self.cx_profile.side_a_max_bps = side_a_max_rate
        self.cx_profile.side_b_min_bps = side_b_min_rate
        self.cx_profile.side_b_max_bps = side_b_max_rate

    def start(self, print_pass=False, print_fail=False):
        self.cx_profile.start_cx()

    def stop(self):
        self.cx_profile.stop_cx()
        self.station_profile.admin_down()

    def pre_cleanup(self):
        self.cx_profile.cleanup_prefix()
        if self.create_sta:
            for sta in self.sta_list:
                self.rm_port(sta, check_exists=True)

    def cleanup(self):
        self.cx_profile.cleanup()
        if self.create_sta:
            self.station_profile.cleanup()
            LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                               port_list=self.station_profile.station_names,
                                               debug=self.debug)

    def build(self):
        self.station_profile.use_security(self.security,
                                          self.ssid,
                                          self.password)
        self.station_profile.set_number_template(self.number_template)
        print("Creating stations")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.create(radio=self.radio,
                                    sta_names_=self.sta_list,
                                    debug=self.debug)
        self.cx_profile.create(endp_type="lf_udp",
                               side_a=self.station_profile.station_names,
                               side_b=self.upstream,
                               sleep_time=0)
        self._pass("PASS: Station build finished")


def main():
    parser = Realm.create_basic_argparse(
        prog='rvr_test.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
            Create stations and endpoints and runs L3 traffic with various IP type of service(BK |  BE | Video | Voice)
            ''',
        description='''\
rvr_test.py:
--------------------
Generic command layout:

python3 ./rvr_test.py
    --radio_2g wiphy0
    --radio_5g wiphy1
    --num_stations 32
    --security {open|wep|wpa|wpa2|wpa3}
    --ssid netgear
    --password admin123
    --upload 3000
    --download 1000
    --debug
    --ap_name Netgear RC6700
    --upstream_port eth1        (upstream Port)
    --traffic_type lf_udp       (traffic type, lf_udp | lf_tcp)
    --test_duration 5m          (duration to run traffic 5m --> 5 Minutes)
    --create_sta False          (False, means it will not create stations and use the sta_names specified below)
    --sta_names sta000,sta001,sta002 (used if --create_sta is False, comma separated names of stations)
    ''')
    parser.add_argument('--mode', help='Used to force mode of stations', default="0")
    parser.add_argument('--traffic_type', help='Select the Traffic Type [lf_udp, lf_tcp]', required=True)
    parser.add_argument('--upload', help='--upload bps rate minimum for endpoint_a (upload rate) ', default=256000)
    parser.add_argument('--download', help='--download bps rate minimum for endpoint_b (download rate)', default=256000)
    parser.add_argument('--test_duration', help='--test_duration sets the duration of the test', default="2m")
    parser.add_argument('--create_sta', help='Used to force a connection to a particular AP', default=True)
    parser.add_argument('--sta_names', help='Used to force a connection to a particular AP', default="sta0000")
    parser.add_argument('--ap_name', help="AP Model Name", default="Test-AP")
    args = parser.parse_args()

    if args.create_sta:
        station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=int(args.num_stations) - 1,
                                              padding_number_=10000,
                                              radio=args.radio_5g)
    else:
        station_list = args.sta_names.split(",")

    rvrTest = rvr_test(host=args.mgr,
                       port=args.mgr_port,
                       number_template="0000",
                       sta_list=station_list,
                       create_sta=args.create_sta,
                       name_prefix="TOS-",
                       upstream=args.upstream_port,
                       ssid=args.ssid,
                       password=args.passwd,
                       security=args.security,
                       test_duration=args.test_duration,
                       use_ht160=False,
                       side_a_min_rate=args.upload,
                       side_b_min_rate=args.download,
                       mode=args.mode,
                       traffic_type=args.traffic_type,
                       _debug_on=args.debug)

    rvrTest.pre_cleanup()
    rvrTest.build()
    rvrTest.start()
    rvrTest.cleanup()