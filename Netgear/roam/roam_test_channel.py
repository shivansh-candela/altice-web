#!/usr/bin/env python3
#script not completed.
import sys
import json

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
    def __init__(self, lfclient_host="localhost", lfclient_port=8080, radio="wiphy0", sta_prefix="sta", start_id=0,
                 num_sta=None,
                 dut_ssid=None, dut_security=None, dut_passwd=None, bssid=None, roam_num1=None, band=None,
                 upstream="eth1", _debug_on=False, _exit_on_error=False, _exit_on_fail=False):
        super().__init__(lfclient_host, lfclient_port, _debug=_debug_on, _exit_on_fail=_exit_on_fail)
        print("Test is about to start")
        self.host = lfclient_host
        self.port = lfclient_port
        self.radio = radio
        self.band = band
        self.upstream = upstream
        self.sta_prefix = sta_prefix
        self.sta_start_id = start_id
        self.num_sta = num_sta
        self.ssid = dut_ssid
        self.security = dut_security
        self.password = dut_passwd
        self.bssid = bssid
        self.roam_num1 = roam_num1
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()

        print("Test is Initialized")

    def precleanup(self):
        self.count = 0
        for rad in self.radio:
            self.count = self.count + 1

            if self.count == 2:
                self.sta_start_id = self.num_sta
                self.num_sta = 2 * (self.num_sta)
                self.station_list1 = LFUtils.portNameSeries(prefix_=self.sta_prefix, start_id_=self.sta_start_id,
                                                            end_id_=self.num_sta - 1, padding_number_=10000,
                                                            radio=rad)

                # cleanup station list which started sta_id 20
                self.station_profile.cleanup(self.station_list1, delay=1, debug_=self.debug)
                LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                                   port_list=self.station_list1,
                                                   debug=self.debug)
                time.sleep(1)
                return

            self.station_list = LFUtils.portNameSeries(prefix_=self.sta_prefix, start_id_=self.sta_start_id,
                                                       end_id_=self.num_sta - 1, padding_number_=10000,
                                                       radio=rad)

            # cleans stations
            self.station_profile.cleanup(self.station_list, delay=1, debug_=self.debug)
            LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                               port_list=self.station_list,
                                               debug=self.debug)
            time.sleep(1)

        print("precleanup done")

    def build(self):
        # station build
        for rad in self.radio:

            self.station_profile.use_security(self.security, self.ssid, self.password)
            self.station_profile.set_number_template("00")

            self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)

            self.station_profile.set_command_param("set_port", "report_timer", 1500)

            # connect station to particular bssid
            self.station_profile.set_command_param("add_sta", "ap", self.bssid[0])
            print(self.bssid[0])
            self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
            self.station_profile.create(radio=rad, sta_names_=self.station_list, debug=self.debug)
            self.local_realm.wait_until_ports_appear(sta_list=self.station_list)
            self.station_profile.admin_up()
            if self.local_realm.wait_for_ip(self.station_list):
                self._pass("All stations got IPs")
            else:
                self._fail("Stations failed to get IPs")
                exit(1)
            if self.count == 2:
                self.station_list = self.station_list1
                self.bssid[0] = self.bssid[1]
        print("Test Build done")

    def roam(self):
        #self.display("1.1.sta0000",self.bssid[0])
        extra_data = self.roam_num1[1]
        string_extra_data = 'trigger freq'
        for i in extra_data:
            string_extra_data = string_extra_data + ' ' + str(i)
        print(string_extra_data)

        # creating scan_wifi command
        scan_wifi_data = {
            "shelf": 1,
            "resource": 1,
            "port": "sta0000",
            "key": "NA",
            "extra": string_extra_data
        }

        # creating wifi_cli_cmd command
        wifi_cli_cmd_data = {
            "shelf": 1,
            "resource": 1,
            "port": None,
            "wpa_cli_cmd": None
        }

        # list of station names
        list_of_sta = []
        for i in self.station_profile.station_names:
            list_of_sta.append(i[4:])
        print(list_of_sta)

        if self.band == "Both":
            list_of_list_bssid = []
            list_bssid = self.roam_num1[0].copy()
            length = len(list_bssid) //2
            print(list_bssid,length)
            first_list = list_bssid[0:length]
            second_list = list_bssid[length:]
            print(first_list)
            print(second_list)
            first_list.pop(0)
            second_list.pop(0)
            first_list.append(list_bssid[0])
            second_list.append(list_bssid[length])
            list_of_list_bssid.append(first_list)
            list_of_list_bssid.append(second_list)
            print(list_of_list_bssid)


        else:
            # add 1st bssid to last
            list_of_list_bssid = []
            list_bssid = self.roam_num1[0].copy()
            list_bssid.pop(0)
            list_bssid.append(self.roam_num1[0][0])
            list_of_list_bssid.append(list_bssid)
            print(list_of_list_bssid)
        # while True:
        for list_bssid in list_of_list_bssid:
            for i in list_bssid:
                self.json_post("/cli-json/scan_wifi", scan_wifi_data, suppress_related_commands_=True)
                time.sleep(2)
                for j in list_of_sta:
                    wifi_cli_cmd_data["wpa_cli_cmd"] = 'roam ' + i
                    wifi_cli_cmd_data["port"] = j
                    print(wifi_cli_cmd_data)
                    self.json_post("/cli-json/wifi_cli_cmd", wifi_cli_cmd_data, suppress_related_commands_=True)
                    time.sleep(10)
                    self.display("1.1."+j,i)


    def display(self,station_name,bssid):

        data = self.json_get("ports/list?fields=ap")
        for j in data['interfaces']:
            for k in j:
                if station_name == k:
                    ap = j[station_name]["ap"]
        print(ap)
        if ap.lower() == bssid.lower():
            print(station_name[4:] + " Roamed to bssid " + bssid )
        else:
            print("Roaming failed")


    def start(self, print_pass=False, print_fail=False):
        print("Test Started")

        # print(self.station_list)

    def stop(self):
        self.station_profile.admin_down()

    def postcleanup(self):
        self.station_profile.cleanup(self.station_profile.station_names, delay=1, debug_=self.debug)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)

    def set_values(self):
        if self.band == "Both":
            self.num_sta = self.num_sta // 2
        print(self.num_sta)


def main():
    # This has --mgr, --mgr_port and --debug
    '''parser = LFCliBase.create_bare_argparse(prog="roam_test.py", formatter_class=argparse.RawTextHelpFormatter,
                                            epilog="About This Script")
    # Adding More Arguments for custom use
    parser.add_argument('--ssid', type=str, help='--ssid', default="roam")
    parser.add_argument('--passwd', type=str, help='--passwd', default="BLANK")
    parser.add_argument('--security', type=str, help='--security', default="open")
    parser.add_argument('--radio', nargs="+", help='--radio to use on LANforge for 2.4G or 5G or Both',
                        default=["wiphy0", "wiphy1"])
    parser.add_argument('--num_stations', type=int, help='--num_client is number of stations', default=6)
    parser.add_argument("--bssids", nargs="+",help='DUT BSSID to which we expect to connect e.g. ["bssid of 2.4G band","bssid of 5G band"]')
    parser.add_argument("--bands", nargs="+", help='Bands e.g.["5G","2.4G","Both"]', default=["2.4G", "5G", "Both"])
    parser.add_argument("--roam_num1", nargs="+", help='list of data e.g:-[[bssids],[frequencies]]',
                        default=[['ac:86:74:8c:ea:42', 'ac:86:74:a4:61:82'], [2412, 2412]])

    args = parser.parse_args()'''

    #Taking input from json file
    with open('roam_config.json') as f:
      data = json.load(f)

    for band in args.bands:
        obj = roam_test(lfclient_host=args.mgr,
                        lfclient_port=args.mgr_port,
                        radio=args.radio,
                        dut_ssid=args.ssid,
                        dut_passwd=args.passwd,
                        dut_security=args.security,
                        num_sta=args.num_stations,
                        bssid=args.bssids,
                        roam_num1=args.roam_num1,
                        band=band,
                        )

        obj.set_values()
        obj.precleanup()
        obj.build()
        obj.start(False, False)
        obj.roam()
        time.sleep(60)
        obj.stop()
        obj.postcleanup()


if __name__ == "__main__":
    main()

