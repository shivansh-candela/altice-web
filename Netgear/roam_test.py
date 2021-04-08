#!/usr/bin/env python3

import sys

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

if 'py-json' not in sys.path:
    sys.path.append('../py-json')

import argparse
from LANforge.lfcli_base import LFCliBase
from LANforge.LFUtils import *
from LANforge import LFUtils
import realm
import time
import datetime


class roam_test(LFCliBase):
    def __init__(self, lfclient_host="localhost", lfclient_port=8080, radio="wiphy0", sta_prefix="sta", start_id=0, num_sta= None,
                 dut_ssid=None, dut_security=None, dut_passwd=None, bssid=None,roam_num1=None,
                 upstream="eth1",_debug_on=False, _exit_on_error=False,  _exit_on_fail=False):
        super().__init__(lfclient_host, lfclient_port, _debug=_debug_on, _exit_on_fail=_exit_on_fail)
        print("Test is about to start")
        self.host = lfclient_host
        self.port = lfclient_port
        self.radio = radio
        self.upstream = upstream
        self.sta_prefix = sta_prefix
        self.sta_start_id = start_id
        self.num_sta = num_sta
        self.ssid = dut_ssid
        self.security = dut_security
        self.password = dut_passwd
        self.bssid=bssid
        self.roam_num1=roam_num1
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()

        print("Test is Initialized")

    def precleanup(self):
        self.station_list = LFUtils.portNameSeries(prefix_=self.sta_prefix, start_id_=self.sta_start_id,
                                                   end_id_=self.num_sta - 1, padding_number_=10000,
                                                   radio=self.radio)

        # cleans stations
        self.station_profile.cleanup(self.station_list, delay=1, debug_=self.debug)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                           port_list=self.station_list,
                                           debug=self.debug)
        time.sleep(1)

        print("precleanup done")

    def build(self):
        # station build
        self.station_profile.use_security(self.security, self.ssid, self.password)
        self.station_profile.set_number_template("00")

        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)

        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_param("add_sta", "ap", self.bssid)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.create(radio=self.radio, sta_names_=self.station_list, debug=self.debug)
        self.local_realm.wait_until_ports_appear(sta_list=self.station_list)
        print("Test Build done")

    def roam(self):
        extra_data=self.roam_num1[3]
        string_extra_data='trigger freq'
        for i in extra_data:
            string_extra_data=string_extra_data+' '+str(i)
        print(string_extra_data)

        #creating scan_wifi command
        scan_wifi_data = {
            "shelf": 1,
            "resource": 1,
            "port": "sta0000",
            "key": "NA",
            "extra": string_extra_data
        }

        #creating wifi_cli_cmd command
        wifi_cli_cmd_data = {
            "shelf": 1,
            "resource": 1,
            "port": "sta0000",
            "wpa_cli_cmd": None
        }
        while True:
            for i in self.roam_num1[2]:
                self.json_post("/cli-json/scan_wifi", scan_wifi_data, suppress_related_commands_=True)
                time.sleep(2)
                wifi_cli_cmd_data["wpa_cli_cmd"]='roam '+ i
                print(wifi_cli_cmd_data)
                self.json_post("/cli-json/wifi_cli_cmd", wifi_cli_cmd_data, suppress_related_commands_=True)
                time.sleep(10)


    def start(self, print_pass=False, print_fail=False):
       print("Test Started")
       self.station_profile.admin_up()
       if self.local_realm.wait_for_ip(self.station_list):
           self._pass("All stations got IPs")
       else:
           self._fail("Stations failed to get IPs")
           exit(1)
       print(self.station_list)

    def stop(self):
        self.station_profile.admin_down()

    def postcleanup(self):
        self.station_profile.cleanup(self.station_profile.station_names, delay=1, debug_=self.debug)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)


def main():
    # This has --mgr, --mgr_port and --debug
    parser = LFCliBase.create_bare_argparse(prog="roam_test.py", formatter_class=argparse.RawTextHelpFormatter,
                                            epilog="About This Script")
    # Adding More Arguments for custom use
    parser.add_argument('--ssid', type=str, help='--ssid', default="roam")
    parser.add_argument('--passwd', type=str, help='--passwd', default="BLANK")
    parser.add_argument('--security', type=str, help='--security', default="open")
    parser.add_argument('--radio', help='--radio to use on LANforge', default="wiphy0")
    parser.add_argument('--num_stations', type=int, help='--num_client is number of stations', default=1)
    parser.add_argument("--bssid", type=str, help='DUT BSSID to which we expect to connect',default="ac:86:74:a4:61:82")
    parser.add_argument("--roam_num1", nargs="+", help='list of data e.g:-[ssid,band,[bssids],[frequencies]]',
                        default=["roam","2.4G",['ac:86:74:a4:61:82','ac:86:74:8c:ea:42'],[2412,2462]])

    args = parser.parse_args()
    obj = roam_test(lfclient_host=args.mgr,
                   lfclient_port=args.mgr_port,
                   radio=args.radio,
                   dut_ssid=args.ssid,
                   dut_passwd=args.passwd,
                   dut_security=args.security,
                   num_sta=args.num_stations,
                   bssid=args.bssid,
                   roam_num1=args.roam_num1
                   )


    obj.precleanup()

    obj.build()
    obj.start(False, False)
    obj.roam()
    #obj.stop()
    #obj.postcleanup()




if __name__ == "__main__":
    main()
