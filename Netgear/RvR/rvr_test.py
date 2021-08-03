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
from datetime import datetime


class RvR(Realm):
    def __init__(self, ssid=None, security=None, password=None, create_sta=True, sta_list=None, name_prefix=None,
                 upstream=None, radio="wiphy0", host="localhost", port=8080, mode=0, ap_model="Test", values="0",
                 traffic_type="lf_udp, lf_tcp", serial_number='2222', indices="all", load=500, traffic_direction="download",
                 side_a_min_rate=56, side_a_max_rate=0, side_b_min_rate=56, side_b_max_rate=0, number_template="00000",
                 num_stations=10,
                 test_duration='2m', use_ht160=False, _debug_on=False, _exit_on_error=False, _exit_on_fail=False):
        super().__init__(lfclient_host=host, lfclient_port=port),
        self.upstream = upstream
        self.host = host
        self.port = port
        self.ssid = ssid
        self.security = security
        self.password = password
        self.station_names = sta_list
        self.create_sta = create_sta
        self.num_stations = num_stations
        self.radio = radio
        self.mode = mode
        self.ap_model = ap_model
        self.traffic_type = traffic_type.split(',')
        self.traffic_direction = traffic_direction
        self.load = load
        self.number_template = number_template
        self.debug = _debug_on
        self.name_prefix = name_prefix
        self.test_duration = test_duration

        # initialize station profile
        self.station_profile = self.new_station_profile()
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

        # initialize connection profile
        self.cx_profile = self.new_l3_cx_profile()
        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.cx_profile.name_prefix = self.name_prefix
        self.cx_profile.side_a_min_bps = side_a_min_rate
        self.cx_profile.side_a_max_bps = side_a_max_rate
        self.cx_profile.side_b_min_bps = side_b_min_rate
        self.cx_profile.side_b_max_bps = side_b_max_rate

        # initialize attenuator profile
        self.attenuator_profile = self.new_attenuator_profile()
        self.serial_number = serial_number
        self.indices = indices.split(',')
        self.values = values
        self.initialize_attenuator()

    def initialize_attenuator(self):
        self.attenuator_profile.atten_serno = self.serial_number
        self.attenuator_profile.atten_idx = "all"
        self.attenuator_profile.atten_val = '0'
        self.attenuator_profile.mode = None
        self.attenuator_profile.pulse_width_us5 = None
        self.attenuator_profile.pulse_interval_ms = None,
        self.attenuator_profile.pulse_count = None,
        self.attenuator_profile.pulse_time_ms = None
        self.attenuator_profile.create()
        self.attenuator_profile.show()

    def set_attenuation(self, value):
        self.attenuator_profile.atten_serno = self.serial_number
        self.attenuator_profile.atten_idx = "all"
        self.attenuator_profile.atten_val = value
        self.attenuator_profile.create()
        self.attenuator_profile.show()

    def start_l3(self, print_pass=False, print_fail=False):
        self.cx_profile.start_cx()

    def stop_l3(self):
        self.cx_profile.stop_cx()
        self.station_profile.admin_down()

    def clean_cx_lists(self):
        # Clean out our local lists, this by itself does NOT remove anything from LANforge manager.
        # but, if you are trying to modify existing connections, then clearing these arrays and
        # re-calling 'create' will do the trick.
        self.cx_profile.created_cx.clear()
        self.cx_profile.created_endp.clear()

    def pre_cleanup(self):
        self.cx_profile.cleanup_prefix()
        if self.create_sta:
            for sta in self.station_names:
                self.rm_port(sta, check_exists=True)

    def cleanup(self):
        self.cx_profile.cleanup()
        if self.create_sta:
            self.station_profile.cleanup()
            LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                               port_list=self.station_profile.station_names,
                                               debug=self.debug)

    def start_stations(self):
        self.station_profile.admin_up()
        # check here if upstream port got IP
        temp_stations = self.station_profile.station_names.copy()
        if self.wait_for_ip(temp_stations):
            self._pass("All stations got IPs")
        else:
            self._fail("Stations failed to get IPs")
            self.exit_fail()
        self._pass("PASS: Station build finished")

    def build(self):
        throughput = {}
        self.station_profile.use_security(self.security, self.ssid, self.password)
        self.station_profile.set_number_template(self.number_template)
        print("Creating stations")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.create(radio=self.radio, sta_names_=self.station_names, debug=self.debug)
        self.start_stations()
        self.initialize_attenuator()
        for i in range(len(self.traffic_type)):
            self.cx_profile.create(endp_type=self.traffic_type[i], side_a=self.station_profile.station_names,
                                   side_b=self.upstream,
                                   sleep_time=0)
            self.start_l3()
            time.sleep(int(self.test_duration))
            self.stop_l3()
            throughput[''.join(i)] = self.get_rx_values()
            self.clean_cx_lists()
            self.set_attenuation(self.values[0])

    def get_rx_values(self):
        throughput = {'upload': [], 'download': []}
        for sta in self.cx_profile.created_cx.keys():
            throughput['upload'].append(float(f"{list((self.json_get('/cx/%s?fields=bps+rx+a' % sta)).values())[2]['bps rx a'] / 1000000:.2f}"))
            throughput['download'].append(float(f"{list((self.json_get('/cx/%s?fields=bps+rx+b' % sta)).values())[2]['bps rx b'] / 1000000:.2f}"))
        return throughput


def main():
    parser = argparse.ArgumentParser(description='''\
    rvr_test.py:
    --------------------
    Generic command layout:
    =====================================================================
    sudo python3 rvr_test.py --mgr localhost --mgr_port 8080 --upstream eth1 --num_stations 40 
    --security WPA2 --ssid NETGEAR73-5G --passwd fancylotus986 --radio wiphy3 --atten_serno 2222 --atten_idx all
    --atten_val 10 --test_duration 1m --ap_name WAX610 ''')
    optional = parser.add_argument_group('optional arguments')
    required = parser.add_argument_group('required arguments')
    optional.add_argument('--mgr', help='hostname for where LANforge GUI is running', default='localhost')
    optional.add_argument('--mgr_port', help='port LANforge GUI HTTP service is running on', default=8080)
    optional.add_argument('--upstream', help='non-station port that generates traffic: <resource>.<port>, '
                                             'e.g: 1.eth1', default='eth1')
    optional.add_argument('--mode', help='Used to force mode of stations', default="0")
    required.add_argument('--radio', help='radio to use for creating clients', default="wiphy0")
    required.add_argument('--ssid', help="ssid for client association with Access Point")
    required.add_argument('--security', help="security type of ssid")
    required.add_argument('--passwd', help="password of ssid")
    required.add_argument('--traffic_type', help='provide the traffic Type lf_udp, lf_tcp', default='lf_udp')
    optional.add_argument('--traffic_direction', help='Traffic direction i.e upload or download or bidirectional', default="download")
    required.add_argument('--load', help='traffic (load) to be created for each client in layer 3', default=500)
    required.add_argument('--test_duration', help='test_duration sets the duration of the test', default="2m")
    optional.add_argument('--create_sta', help='Used to force a connection to a particular AP', default=True)
    optional.add_argument('--sta_names', help='Used to force a connection to a particular AP', default="sta0000")
    optional.add_argument('--ap_name', help="AP Model Name", default="Test-AP")
    required.add_argument('--num_stations', help='number of stations to create', default=10)
    optional.add_argument('-as', '--atten_serno', help='Serial number for requested Attenuator', default='2222')
    optional.add_argument('-ai', '--atten_idx',
                          help='Attenuator index eg. For module 1 = 0,module 2 = 1 --> --atten_idx 0,1',
                          default='all')
    optional.add_argument('-av', '--atten_val',
                          help='Requested attenuation in 1/10ths of dB (ddB) ex:--> --atten_val 0, 10', default='0')
    optional.add_argument('--debug', help="to enable debug", default=False)
    args = parser.parse_args()
    test_start_time = datetime.now().strftime("%b %d %H:%M:%S")
    print("Test started at ", test_start_time)
    print(parser.parse_args())
    if args.test_duration.endswith('s') or args.test_duration.endswith('S'):
        args.test_duration = args.test_duration[0:-1]
    elif args.test_duration.endswith('m') or args.test_duration.endswith('M'):
        args.test_duration = (args.test_duration[0:-1]) * 60
    elif args.test_duration.endswith('h') or args.test_duration.endswith('H'):
        args.test_duration = (args.test_duration[0:-1]) * 60 * 60
    elif args.test_duration.endswith(''):
        args.test_duration = args.test_duration

    if args.atten_val:
        args.atten_val = args.atten_val.split(',')

    if args.traffic_direction == "upload":
        side_b = int(args.load) * 1000000
        side_a = 0
    elif args.traffic_direction == "download":
        side_a = 0
        side_b = int(args.load) * 1000000
    elif args.traffic_direction == "bidirectional":
        side_a = int(args.load) * 1000000
        side_b = int(args.load) * 1000000

    if args.create_sta:
        station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=int(args.num_stations) - 1,
                                              padding_number_=10000,
                                              radio=args.radio)
    else:
        station_list = args.sta_names.split(",")

    rvr_obj = RvR(host=args.mgr,
                  port=args.mgr_port,
                  number_template="0000",
                  sta_list=station_list,
                  create_sta=args.create_sta,
                  num_stations=int(args.num_stations),
                  name_prefix="RvR-",
                  upstream=args.upstream,
                  radio=args.radio,
                  ssid=args.ssid,
                  password=args.passwd,
                  security=args.security,
                  test_duration=args.test_duration,
                  use_ht160=False,
                  load=args.load,
                  side_a_min_rate=side_a,
                  side_b_min_rate=side_b,
                  mode=args.mode,
                  serial_number=args.atten_serno,
                  indices=args.atten_idx,
                  values=args.atten_val,
                  traffic_type=args.traffic_type,
                  traffic_direction=args.traffic_direction,
                  _debug_on=args.debug)

    rvr_obj.pre_cleanup()
    rvr_obj.build()
    rvr_obj.start()
    rvr_obj.cleanup()

    test_end_time = datetime.now().strftime("%b %d %H:%M:%S")
    print("Test ended at: ", test_end_time)


if __name__ == "__main__":
    main()
