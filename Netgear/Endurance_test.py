#!/usr/bin/env python3

"""test_generic.py will create stations and endpoints to generate traffic based on a command-line specified command type.

This script will create a variable number of stations to test generic endpoints. Multiple command types can be tested
including ping, speedtest, generic types. The test will check the last-result attribute for different things
depending on what test is being run. Ping will test for successful pings, speedtest will test for download
speed, upload speed, and ping time, generic will test for successful generic commands

Use './test_generic.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
"""

import pprint
import sys
import os

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

if 'py-json' not in sys.path:
    sys.path.append(os.path.join(os.path.abspath('..'), 'py-json'))

import argparse
from LANforge.lfcli_base import LFCliBase
from LANforge import LFUtils
import realm
import time
import datetime
import json
import re

import paramiko
import schedule
import time
import threading
from Endurance_html_report import *

# from multicast_profile import MULTICASTProfile
from create_station import CreateStation


class GenTest(LFCliBase):
    def __init__(self, ssid1, security1, passwd1, ssid2, security2, passwd2, station_list1_wiphy0, station_list2_wiphy0,
                 station_list1_wiphy1, station_list2_wiphy1, client, name_prefix,
                 upstream, host="localhost",
                 port=8080,
                 number_template="000", test_duration="5m", type="lfping", dest=None, cmd=None,
                 interval=1, radio1="wiphy0", radio2="wiphy1", speedtest_min_up=None, speedtest_min_dl=None,
                 speedtest_max_ping=None,
                 traffic_type="lf_udp", side_a_speed="0M", side_b_speed="10M",
                 file_output=None,
                 loop_count=None,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False):
        super().__init__(host, port, _local_realm=realm.Realm(host, port), _debug=_debug_on,
                         _halt_on_error=_exit_on_error, _exit_on_fail=_exit_on_fail)
        self.ssid1 = ssid1
        self.radio1 = radio1
        self.security1 = security1
        self.passwd1 = passwd1
        self.upstream = upstream
        self.station_list1_wiphy0 = station_list1_wiphy0
        self.station_list2_wiphy0 = station_list2_wiphy0
        self.ssid2 = ssid2
        self.radio2 = radio2
        self.security2 = security2
        self.passwd2 = passwd2
        self.station_list1_wiphy1 = station_list1_wiphy1
        self.station_list2_wiphy1 = station_list2_wiphy1
        self.number_template = number_template
        self.name_prefix = name_prefix
        self.test_duration = test_duration
        self.side_a_min_speed = side_a_speed
        self.side_b_min_speed = side_b_speed
        self.l3_traffictype = traffic_type
        self.ips_list = []
        self.temp_stas6 = []
        if (speedtest_min_up is not None):
            self.speedtest_min_up = float(speedtest_min_up)
        if (speedtest_min_dl is not None):
            self.speedtest_min_dl = float(speedtest_min_dl)
        if (speedtest_max_ping is not None):
            self.speedtest_max_ping = float(speedtest_max_ping)
        self.debug = _debug_on
        if (client is not None):
            self.client_name = client

        self.station_profile1 = self.local_realm.new_station_profile()
        self.station_profile2 = self.local_realm.new_station_profile()
        self.station_profile3 = self.local_realm.new_station_profile()
        self.station_profile4 = self.local_realm.new_station_profile()

        self.station_profile1.lfclient_url = self.lfclient_url
        self.station_profile1.ssid = self.ssid1
        self.station_profile1.ssid_pass = self.passwd1
        self.station_profile1.security = self.security1
        self.station_profile1.number_template_ = self.number_template
        self.station_profile1.mode = 6

        self.station_profile2.lfclient_url = self.lfclient_url
        self.station_profile2.ssid = self.ssid2
        self.station_profile2.ssid_pass = self.passwd2
        self.station_profile2.security = self.security2
        self.station_profile2.number_template_ = self.number_template
        self.station_profile2.mode = 6

        self.station_profile3.lfclient_url = self.lfclient_url
        self.station_profile3.ssid = self.ssid1
        self.station_profile3.ssid_pass = self.passwd1
        self.station_profile3.security = self.security1
        self.station_profile3.number_template_ = self.number_template
        self.station_profile3.mode = 10

        self.station_profile4.lfclient_url = self.lfclient_url
        self.station_profile4.ssid = self.ssid2
        self.station_profile4.ssid_pass = self.passwd2
        self.station_profile4.security = self.security2
        self.station_profile4.number_template_ = self.number_template
        self.station_profile4.mode = 10

        time.sleep(2)

        self.generic_endps_profile = self.local_realm.new_generic_endp_profile()

        self.generic_endps_profile.name = name_prefix
        self.generic_endps_profile.type = type
        # self.generic_endps_profile.dest = self.ips_list[0]
        self.generic_endps_profile.cmd = cmd
        self.generic_endps_profile.interval = interval
        self.generic_endps_profile.file_output = file_output
        self.generic_endps_profile.loop_count = loop_count

        time.sleep(2)
        self.l3_cx_profile = self.local_realm.new_l3_cx_profile()

        self.l3_cx_profile.side_a_min_bps = int(side_a_speed)
        self.l3_cx_profile.side_b_min_bps = int(side_b_speed)
        self.l3_cx_profile.traffic_type = traffic_type

        self.multicast = self.local_realm.new_multicast_profile()

        # self.l3_cx_profile.upstream = upstream

    def collect_ip(self):
        temp_stas1 = self.station_profile1.station_names.copy()
        temp_stas2 = self.station_profile2.station_names.copy()
        temp_stas3 = self.station_profile3.station_names.copy()
        temp_stas4 = self.station_profile4.station_names.copy()
        temp_stas5 = temp_stas1 + temp_stas2 + temp_stas3 + temp_stas4
        self.temp_stas6 = temp_stas5.copy()
        temp_stas5.append(self.upstream)
        print(self.temp_stas6)

        for sta_eid in temp_stas5:
            eid = self.local_realm.name_to_eid(sta_eid)
            response = super().json_get("/port/%s/%s/%s?fields=alias,ip,port+type,ipv6+address" %
                                        (eid[0], eid[1], eid[2]))
            v = response['interface']
            if v['ip']:
                self.ips_list.append(v['ip'])

    def choose_ping_command(self):
        # self.generic_endps_profile.dest = self.ips_list[1]
        print("In Ping command...........")
        gen_results = self.json_get("generic/list?fields=name,last+results", debug_=self.debug)
        if self.debug:
            print(gen_results)
        if gen_results['endpoints'] is not None:
            for name in gen_results['endpoints']:
                for k, v in name.items():
                    if v['name'] in self.generic_endps_profile.created_endp and not v['name'].endswith('1'):
                        if v['last results'] != "" and "Unreachable" not in v['last results']:
                            return True, v['name']
                        else:
                            return False, v['name']

    def choose_lfcurl_command(self):
        gen_results = self.json_get("generic/list?fields=name,last+results", debug_=self.debug)
        if self.debug:
            print(gen_results)
        if gen_results['endpoints'] is not None:
            for name in gen_results['endpoints']:
                for k, v in name.items():
                    if v['name'] != '':
                        results = v['last results'].split()
                        if 'Finished' in v['last results']:
                            if results[1][:-1] == results[2]:
                                return True, v['name']
                            else:
                                return False, v['name']

    def choose_iperf3_command(self):
        gen_results = self.json_get("generic/list?fields=name,last+results", debug_=self.debug)
        if gen_results['endpoints'] is not None:
            pprint.pprint(gen_results['endpoints'])
            # for name in gen_results['endpoints']:
            # pprint.pprint(name.items)
            # for k,v in name.items():
        exit(1)

    def choose_speedtest_command(self):
        gen_results = self.json_get("generic/list?fields=name,last+results", debug_=self.debug)
        if gen_results['endpoints'] is not None:
            for name in gen_results['endpoints']:
                for k, v in name.items():
                    if v['last results'] is not None and v['name'] in self.generic_endps_profile.created_endp and v[
                        'last results'] != '':
                        last_results = json.loads(v['last results'])
                        if last_results['download'] is None and last_results['upload'] is None and last_results[
                            'ping'] is None:
                            return False, v['name']
                        elif last_results['download'] >= self.speedtest_min_dl and \
                                last_results['upload'] >= self.speedtest_min_up and \
                                last_results['ping'] <= self.speedtest_max_ping:
                            return True, v['name']

    def choose_generic_command(self):
        gen_results = self.json_get("generic/list?fields=name,last+results", debug_=self.debug)
        if (gen_results['endpoints'] is not None):
            for name in gen_results['endpoints']:
                for k, v in name.items():
                    if v['name'] in self.generic_endps_profile.created_endp and not v['name'].endswith('1'):
                        if v['last results'] != "" and "not known" not in v['last results']:
                            return True, v['name']
                        else:
                            return False, v['name']

    def start_ping(self):

        self.generic_endps_profile.start_cx()
        # cur_time = datetime.datetime.now()
        passes = 0
        expected_passes = 0
        # self.generic_endps_profile.start_cx()
        # time.sleep(15)
        # end_time = self.local_realm.parse_time(self.test_duration) + cur_time
        print("Starting Test...")
        result = False

        if self.generic_endps_profile.type == "lfping":
            result = self.choose_ping_command()
        elif self.generic_endps_profile.type == "iperf3":
            result = self.choose_iperf3_command()
        time.sleep(1)

    def start_stations(self):
        self.station_profile1.admin_up()
        self.station_profile2.admin_up()
        self.station_profile3.admin_up()
        self.station_profile4.admin_up()
        temp_stas1 = []
        temp_stas2 = []
        for station in self.station_list1_wiphy0.copy():
            temp_stas1.append(self.local_realm.name_to_eid(station)[2])
        for station in self.station_list2_wiphy0.copy():
            temp_stas1.append(self.local_realm.name_to_eid(station)[2])
        for station in self.station_list1_wiphy1.copy():
            temp_stas2.append(self.local_realm.name_to_eid(station)[2])
        for station in self.station_list2_wiphy1.copy():
            temp_stas2.append(self.local_realm.name_to_eid(station)[2])
        if self.debug:
            pprint.pprint(self.station_profile.station_names)
        LFUtils.wait_until_ports_admin_up(base_url=self.lfclient_url, port_list=self.station_profile1.station_names)
        LFUtils.wait_until_ports_admin_up(base_url=self.lfclient_url, port_list=self.station_profile2.station_names)
        LFUtils.wait_until_ports_admin_up(base_url=self.lfclient_url, port_list=self.station_profile3.station_names)
        LFUtils.wait_until_ports_admin_up(base_url=self.lfclient_url, port_list=self.station_profile4.station_names)
        if self.local_realm.wait_for_ip(temp_stas1):
            self._pass("All stations got IPs")
        else:
            self._fail("Stations failed to get IPs")
            self.exit_fail()
        if self.local_realm.wait_for_ip(temp_stas2):
            self._pass("All stations got IPs")
        else:
            self._fail("Stations failed to get IPs")
            self.exit_fail()
        self.collect_ip()

    def start_l3(self):
        self.l3_cx_profile.start_cx()

    def start_multi(self):
        self.multicast.start_mc()

    def stop(self):
        print("Stopping Test...")
        self.generic_endps_profile.stop_cx()
        self.station_profile.admin_down()

    def stop_multi(self):
        print("STOPPING MULTICAST TRAFFIC....")
        self.multicast.stop_mc()

    def stop_l3(self):
        print("STOPPING LAYER3 TRAFFIC....")
        self.l3_cx_profile.stop_cx()

    def stop_ping(self):
        print("STOPPING PING SESSIONS....")
        self.generic_endps_profile.stop_cx()

    def build_stations(self):
        self.station_profile1.use_security(self.security1, self.ssid1, self.passwd1)
        self.station_profile1.set_number_template(self.number_template)
        print("Creating stations 1,2")
        self.station_profile1.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile1.set_command_param("set_port", "report_timer", 1500)
        self.station_profile1.set_command_flag("set_port", "rpt_timer", 1)

        self.station_profile1.create(radio=self.radio1, sta_names_=self.station_list1_wiphy0, debug=self.debug)
        self.station_profile2.use_security(self.security2, self.ssid2, self.passwd2)
        self.station_profile2.set_number_template(self.number_template)
        print("Creating stations 5,6")
        self.station_profile2.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile2.set_command_param("set_port", "report_timer", 1500)
        self.station_profile2.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile2.create(radio=self.radio1, sta_names_=self.station_list2_wiphy0, debug=self.debug)

        self.station_profile3.use_security(self.security1, self.ssid1, self.passwd1)
        self.station_profile3.set_number_template(self.number_template)
        print("Creating stations 3,4")
        self.station_profile3.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile3.set_command_param("set_port", "report_timer", 1500)
        self.station_profile3.set_command_flag("set_port", "rpt_timer", 1)

        self.station_profile3.create(radio=self.radio2, sta_names_=self.station_list1_wiphy1, debug=self.debug)

        self.station_profile4.use_security(self.security2, self.ssid2, self.passwd2)
        self.station_profile4.set_number_template(self.number_template)
        print("Creating stations 7,8")
        self.station_profile4.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile4.set_command_param("set_port", "report_timer", 1500)
        self.station_profile4.set_command_flag("set_port", "rpt_timer", 1)

        self.station_profile4.create(radio=self.radio2, sta_names_=self.station_list2_wiphy1, debug=self.debug)

        self._pass("PASS: Station build finished")

    def build_multi(self):
        self.multicast.create_mc_tx("mc_udp", "1.1.sta01", mcast_group="224.1.0.1", mcast_dest_port=8001)
        self.multicast.create_mc_rx("mc_udp", "1.1.sta02", mcast_group="224.1.0.1", mcast_dest_port=8001)
        self.multicast.create_mc_tx("mc_udp", "1.1.sta03", mcast_group="224.1.0.2", mcast_dest_port=8002)
        self.multicast.create_mc_rx("mc_udp", "1.1.sta04", mcast_group="224.1.0.2", mcast_dest_port=8002)
        self.multicast.create_mc_tx("mc_udp", "1.1.sta05", mcast_group="224.1.0.3", mcast_dest_port=8003)
        self.multicast.create_mc_rx("mc_udp", "1.1.sta06", mcast_group="224.1.0.3", mcast_dest_port=8003)
        self.multicast.create_mc_tx("mc_udp", "1.1.sta07", mcast_group="224.1.0.4", mcast_dest_port=8004)
        self.multicast.create_mc_rx("mc_udp", "1.1.sta08", mcast_group="224.1.0.4", mcast_dest_port=8004)

        self.multicast.create_mc_tx("mc_udp", "1.1.sta01", mcast_group="224.1.0.5", mcast_dest_port=8005)
        self.multicast.create_mc_rx("mc_udp", "1.1.sta03", mcast_group="224.1.0.5", mcast_dest_port=8005)
        self.multicast.create_mc_tx("mc_udp", "1.1.sta04", mcast_group="224.1.0.6", mcast_dest_port=8006)
        self.multicast.create_mc_rx("mc_udp", "1.1.sta02", mcast_group="224.1.0.6", mcast_dest_port=8006)
        self.multicast.create_mc_tx("mc_udp", "1.1.sta05", mcast_group="224.1.0.7", mcast_dest_port=8007)
        self.multicast.create_mc_rx("mc_udp", "1.1.sta07", mcast_group="224.1.0.7", mcast_dest_port=8007)
        self.multicast.create_mc_tx("mc_udp", "1.1.sta08", mcast_group="224.1.0.8", mcast_dest_port=8008)
        self.multicast.create_mc_rx("mc_udp", "1.1.sta06", mcast_group="224.1.0.8", mcast_dest_port=8008)

        self.multicast.create_mc_tx("mc_udp", "1.1.sta01", mcast_group="224.1.1.0", mcast_dest_port=8011)
        self.multicast.create_mc_rx("mc_udp", "1.1.sta06", mcast_group="224.1.1.0", mcast_dest_port=8012)
        self.multicast.create_mc_tx("mc_udp", "1.1.sta05", mcast_group="224.1.1.2", mcast_dest_port=8013)
        self.multicast.create_mc_rx("mc_udp", "1.1.sta02", mcast_group="224.1.1.2", mcast_dest_port=8013)

        self.multicast.create_mc_tx("mc_udp", "1.1.sta07", mcast_group="224.1.2.3", mcast_dest_port=8014)
        self.multicast.create_mc_rx("mc_udp", "1.1.sta01", mcast_group="224.1.2.3", mcast_dest_port=8014)
        self.multicast.create_mc_tx("mc_udp", "1.1.sta05", mcast_group="224.1.2.4", mcast_dest_port=8015)
        self.multicast.create_mc_rx("mc_udp", "1.1.sta03", mcast_group="224.1.2.4", mcast_dest_port=8015)

        self.multicast.create_mc_tx("mc_udp", "1.1.eth1", mcast_group="224.1.2.5", mcast_dest_port=8016)
        for sta in self.temp_stas6:
            self.multicast.create_mc_rx("mc_udp", sta, mcast_group="224.1.2.5", mcast_dest_port=8016)

        for serv in self.temp_stas6:
            self.multicast.create_mc_tx("mc_udp", serv, mcast_group="224.1.2.6", mcast_dest_port=8017)
        self.multicast.create_mc_rx("mc_udp", "1.1.eth1", mcast_group="224.1.2.6", mcast_dest_port=8017)

    def build_l3(self):

        self.l3_cx_profile.create_cx(endp_type=self.l3_cx_profile.traffic_type, side_a="1.1.sta02",
                                     side_b="1.1.sta01", count=2, sleep_time=0)
        self.l3_cx_profile.create_cx(endp_type=self.l3_cx_profile.traffic_type, side_a="1.1.sta04",
                                     side_b="1.1.sta03", count=2, sleep_time=0)
        self.l3_cx_profile.create_cx(endp_type=self.l3_cx_profile.traffic_type, side_a="1.1.sta06",
                                     side_b="1.1.sta05", count=2, sleep_time=0)
        self.l3_cx_profile.create_cx(endp_type=self.l3_cx_profile.traffic_type, side_a="1.1.sta08",
                                     side_b="1.1.sta07", count=2, sleep_time=0)

        self.l3_cx_profile.create_cx(endp_type=self.l3_cx_profile.traffic_type, side_a="1.1.sta02",
                                     side_b="1.1.sta03", count=2, sleep_time=0)
        self.l3_cx_profile.create_cx(endp_type=self.l3_cx_profile.traffic_type, side_a="1.1.sta04",
                                     side_b="1.1.sta01", count=2, sleep_time=0)
        self.l3_cx_profile.create_cx(endp_type=self.l3_cx_profile.traffic_type, side_a="1.1.sta06",
                                     side_b="1.1.sta07", count=2, sleep_time=0)
        self.l3_cx_profile.create_cx(endp_type=self.l3_cx_profile.traffic_type, side_a="1.1.sta08",
                                     side_b="1.1.sta05", count=2, sleep_time=0)

        self.l3_cx_profile.create_cx(endp_type=self.l3_cx_profile.traffic_type, side_a="1.1.sta06",
                                     side_b="1.1.sta02", count=2, sleep_time=0)
        self.l3_cx_profile.create_cx(endp_type=self.l3_cx_profile.traffic_type, side_a="1.1.sta04",
                                     side_b="1.1.sta07", count=2, sleep_time=0)

        self.l3_cx_profile.create_cx(endp_type=self.l3_cx_profile.traffic_type, side_a="1.1.sta08",
                                     side_b="1.1.sta02", count=2, sleep_time=0)
        self.l3_cx_profile.create_cx(endp_type=self.l3_cx_profile.traffic_type, side_a="1.1.sta06",
                                     side_b="1.1.sta04", count=2, sleep_time=0)

        self.l3_cx_profile.side_a_min_bps = int(self.side_a_min_speed)
        self.l3_cx_profile.side_b_min_bps = 0
        self.l3_cx_profile.traffic_type = "lf_tcp"
        self.l3_cx_profile.create_cx(endp_type=self.l3_cx_profile.traffic_type, side_a="1.1.eth1",
                                     side_b=self.temp_stas6, count=2, sleep_time=0)

        self.l3_cx_profile.side_a_min_bps = 0
        self.l3_cx_profile.side_b_min_bps = int(self.side_b_min_speed)
        self.l3_cx_profile.traffic_type = "lf_tcp"
        self.l3_cx_profile.create_cx(endp_type=self.l3_cx_profile.traffic_type, side_a="1.1.eth1",
                                     side_b=self.temp_stas6, count=2, sleep_time=0)

    def build_ping(self):

        self.generic_endps_profile.create_gen("1.1.sta01", self.ips_list[1], "a", sleep_time=.5)
        self.generic_endps_profile.create_gen("1.1.sta03", self.ips_list[5], "b", sleep_time=.5)
        self.generic_endps_profile.create_gen("1.1.sta05", self.ips_list[3], "c", sleep_time=.5)
        self.generic_endps_profile.create_gen("1.1.sta07", self.ips_list[7], "d", sleep_time=.5)

        self.generic_endps_profile.create_gen("1.1.sta01", self.ips_list[4], "e", sleep_time=.5)
        self.generic_endps_profile.create_gen("1.1.sta04", self.ips_list[1], "f", sleep_time=.5)
        self.generic_endps_profile.create_gen("1.1.sta05", self.ips_list[6], "g", sleep_time=.5)
        self.generic_endps_profile.create_gen("1.1.sta08", self.ips_list[3], "h", sleep_time=.5)

        self.generic_endps_profile.create_gen("1.1.sta01", self.ips_list[2], "i", sleep_time=.5)
        self.generic_endps_profile.create_gen("1.1.sta03", self.ips_list[7], "j", sleep_time=.5)

        self.generic_endps_profile.create_gen("1.1.sta01", self.ips_list[6], "k", sleep_time=.5)
        self.generic_endps_profile.create_gen("1.1.sta03", self.ips_list[2], "l", sleep_time=.5)

        print(self.ips_list[0:8])
        self.generic_endps_profile.create_gen("1.1.eth1", self.ips_list[0:8], "m", sleep_time=.5)

        self.generic_endps_profile.create_gen(self.temp_stas6, self.ips_list[8], "n", sleep_time=.5)

    def cleanup(self, sta_list):
        self.generic_endps_profile.cleanup()
        self.station_profile.cleanup(sta_list)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=sta_list, debug=self.debug)

    def client_disconnection_check(self):
        temp_stas1 = self.station_profile1.station_names.copy()
        temp_stas2 = self.station_profile2.station_names.copy()
        temp_stas3 = temp_stas1 + temp_stas2

        l1 = ["0.0.0.0", "NA", " "]
        # temp_stas1.append(self.upstream)
        for sta_eid in temp_stas3:
            eid = self.local_realm.name_to_eid(sta_eid)
            response = super().json_get("/port/%s/%s/%s?fields=alias,ip,port+type,ipv6+address" %
                                        (eid[0], eid[1], eid[2]))
            v = response['interface']
            if v['ip'] in l1:
                return False
            else:
                return True

    def traffic_check(self):
        states_list = ["PHANTOM", "FTM_WAIT"]
        for station in self.l3_cx_profile.created_cx:
            var = super().json_get("/cx/%s?fields=state,bps rx a,bps rx b" % station)
            state_data = var['interface']
            if state_data['state'] in states_list:
                return False
            elif state_data['state'] == "Run":
                print(1)

        pass

    def ap_memory_check(self):

        pass


def main():
    parser = LFCliBase.create_basic_argparse(
        prog='test_generic.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''Create generic endpoints and test for their ability to execute chosen commands\n''')

    parser.add_argument('--ssid1', help='WiFi SSID for script objects to associate to')
    parser.add_argument('--passwd1', help='WiFi passphrase/password/key', default="[BLANK]")
    parser.add_argument('--security1', help='WiFi Security protocol: < open | wep | wpa | wpa2 | wpa3 >',
                        default="open")
    parser.add_argument('--ssid2', help='WiFi SSID for script objects to associate to')
    parser.add_argument('--passwd2', help='WiFi passphrase/password/key', default="[BLANK]")
    parser.add_argument('--security2', help='WiFi Security protocol: < open | wep | wpa | wpa2 | wpa3 >',
                        default="open")
    parser.add_argument('--radio1', help='1st radio on which stations to be created',
                        default="wiphy0")
    parser.add_argument('--radio2', help='2nd radio on which stations to be created',
                        default="wiphy1")
    parser.add_argument('--type', help='type of command to run: generic, lfping, iperf3-client, iperf3-server, lfcurl',
                        default="lfping")
    parser.add_argument('--cmd', help='specifies command to be run by generic type endp', default='')
    parser.add_argument('--dest', help='destination IP for command', default="10.40.0.1")
    parser.add_argument('--test_duration', help='duration of the test eg: 30s, 2m, 4h', default="5m")
    parser.add_argument('--interval', help='interval to use when running lfping (1s, 1m)', default=1)
    parser.add_argument('--speedtest_min_up', help='sets the minimum upload threshold for the speedtest type',
                        default=None)
    parser.add_argument('--speedtest_min_dl', help='sets the minimum download threshold for the speedtest type',
                        default=None)
    parser.add_argument('--speedtest_max_ping', help='sets the minimum ping threshold for the speedtest type',
                        default=None)
    parser.add_argument('--client', help='client to the iperf3 server', default=None)
    parser.add_argument('--file_output', help='location to output results of lf_curl, absolute path preferred',
                        default=None)
    parser.add_argument('--loop_count', help='determines the number of loops to use in lf_curl', default=None)
    parser.add_argument('--side_a_min_speed', help='--speed you want to monitor traffic with (max is 10G)',
                        default="0M")
    parser.add_argument('--side_b_min_speed', help='--speed you want to monitor traffic with (max is 10G)',
                        default="10M")
    parser.add_argument('--traffic_type', help='--traffic_type is used for traffic type (lf_udp, lf_tcp)',
                        default="lf_udp")

    args = parser.parse_args()
    num_sta = 2
    if (args.num_stations is not None) and (int(args.num_stations) > 0):
        num_stations_converted = int(args.num_stations)
        num_sta = num_stations_converted

    station_list1_wiphy0 = LFUtils.portNameSeries(radio=args.radio1,
                                                  prefix_="sta",
                                                  start_id_=1,
                                                  end_id_=2,
                                                  padding_number_=100)
    station_list2_wiphy0 = LFUtils.portNameSeries(radio=args.radio1,
                                                  prefix_="sta",
                                                  start_id_=5,
                                                  end_id_=6,
                                                  padding_number_=100)
    station_list1_wiphy1 = LFUtils.portNameSeries(radio=args.radio2,
                                                  prefix_="sta",
                                                  start_id_=3,
                                                  end_id_=4,
                                                  padding_number_=100)
    station_list2_wiphy1 = LFUtils.portNameSeries(radio=args.radio2,
                                                  prefix_="sta",
                                                  start_id_=7,
                                                  end_id_=8,
                                                  padding_number_=100)

    generic_test = GenTest(host=args.mgr, port=args.mgr_port,
                           number_template="00",
                           radio1=args.radio1,
                           station_list1_wiphy0=station_list1_wiphy0,
                           station_list2_wiphy0=station_list2_wiphy0,
                           security1=args.security1,
                           radio2=args.radio2,
                           station_list1_wiphy1=station_list1_wiphy1,
                           station_list2_wiphy1=station_list2_wiphy1,
                           security2=args.security2,
                           name_prefix="GT",
                           type=args.type,
                           dest=args.dest,
                           cmd=args.cmd,
                           interval=1,
                           ssid1=args.ssid1,
                           passwd1=args.passwd1,
                           ssid2=args.ssid2,
                           passwd2=args.passwd2,
                           upstream=args.upstream_port,
                           test_duration=args.test_duration,
                           speedtest_min_up=args.speedtest_min_up,
                           speedtest_min_dl=args.speedtest_min_dl,
                           speedtest_max_ping=args.speedtest_max_ping,
                           file_output=args.file_output,
                           loop_count=args.loop_count,
                           client=args.client,
                           traffic_type=args.traffic_type,
                           side_a_speed=args.side_a_min_speed,
                           side_b_speed=args.side_b_min_speed,

                           _debug_on=args.debug)

    # generic_test.cleanup(station_list)
    generic_test.build_stations()
    generic_test.start_stations()
    # generic_test.build_multi()
    # generic_test.start_multi()
    generic_test.build_ping()
    generic_test.start_ping()
    generic_test.build_l3()
    generic_test.start_l3()

    start_time = datetime.datetime.now()

    end_time = realm.Realm.parse_time(args.test_duration) + start_time

    print(start_time)
    print(end_time)

    ip = "192.168.215.186"

    user = "root"

    passwd = "Password@123()opklnm"

    ssh = paramiko.SSHClient()

    print("started")
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port=22, username=user, password=passwd, banner_timeout=600)

    wifi_tx_rx_data = {}
    eth_tx_rx_data = {}
    Time_stamp = []
    def stats_ap():
        t = threading.Timer(60, stats_ap)
        t.start()
        start_time = datetime.datetime.now()
        if start_time > end_time:
            t.cancel()
        list_1 = ["apstats -a|grep -i 'Tx Data Bytes'", "apstats -a|grep -i 'Rx Data Bytes'",
                  "cat /proc/net/dev | grep -i eth0 | awk '{print $10}'",
                  "cat /proc/net/dev | grep -i eth0 | awk '{print $10}'",
                  "cat /proc/meminfo | grep -i MemAvail", 'cat /proc/meminfo |grep -i memfree',
                  "mpstat"]
        list_2 = ['Tx_Data_Bytes', 'Rx_Data_Bytes', 'eth_Tx_Data_Bytes', 'eth_Rx_Data_Bytes', 'Memory_Available',
                  'Free_Memory', 'cpu_stat']

        wifi_Tx_Data_Bytes = []
        wifi_Rx_Data_Bytes = []
        eth_Tx_Data_Bytes = []
        eth_Rx_Data_Bytes = []
        free_mem=[]
        avail_mem=[]
        cpu_time=[]
        data = {}
        data1 = {}
        global wifi_tx_rx_data
        global eth_tx_rx_data
        global Time_stamp
        global memory_cpu_utili
        pattern = "\d+"
        for ii, j in zip(list_1, list_2):
            stdin, stdout, stderr = ssh.exec_command(ii)
            output = stdout.readlines()
            data[j] = output
        for m in data:
            if m in list_2:
                if m != 'cpu_stat':
                    mm = re.findall(pattern, data[m][0])
                    data1[m] = int(mm[0])
                    if m == 'Tx_Data_Bytes':
                        wifi_Tx_Data_Bytes.append(int(mm[0]))
                    elif m == 'Rx_Data_Bytes':
                        wifi_Rx_Data_Bytes.append(int(mm[0]))
                    elif m == 'eth_Tx_Data_Bytes':
                        eth_Tx_Data_Bytes.append(int(mm[0]))
                    elif m == 'eth_Rx_Data_Bytes':
                        eth_Rx_Data_Bytes.append(int(mm[0]))
                    elif m == 'Memory_Available':
                        free_mem.append()

                elif m == 'cpu_stat':
                    k = data[m][3]
                    kk = k.split('   ')
                    data1[m] = float(kk[-1].replace("\n", ''))
                    data1['Time'] = kk[0]
                    Time_stamp.append(kk[0])

        print(data1)
        print(wifi_Tx_Data_Bytes)
        print(wifi_Rx_Data_Bytes)
        print(eth_Tx_Data_Bytes)
        print(eth_Rx_Data_Bytes)

        wifi_tx_rx_data = {'wifi_tx_data_byes': wifi_Tx_Data_Bytes, 'wifi_rx_data_bytes': wifi_Rx_Data_Bytes}
        eth_tx_rx_data = {'eth_tx_data_bytes': eth_Tx_Data_Bytes, 'eth_rx_data_bytes': eth_Rx_Data_Bytes}
        memory_cpu_utili = {"free mem": [],"avail mem": [],"cpu time": []}



    stats_ap()

    while start_time < end_time:
        start_time = datetime.datetime.now()

    # t.cancel()
    print("Test Completed will stop all the traffic")
    generic_test.stop_l3()
    # generic_test.stop_multi()
    generic_test.stop_ping()

    generate_report(Time_stamp, wifi_tx_rx_data, eth_tx_rx_data)

    '''
    if not generic_test.passes():
        print(generic_test.get_fail_message())
        generic_test.exit_fail()
    generic_test.start_cx()
    exit(1)
    if not generic_test.passes():
        print(generic_test.get_fail_message())
        generic_test.exit_fail()
    generic_test.stop()
    time.sleep(30)
    generic_test.cleanup(station_list)
    if generic_test.passes():
        generic_test.exit_success()
    '''


if __name__ == "__main__":
    main()
