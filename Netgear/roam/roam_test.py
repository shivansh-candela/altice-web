""" roam_test.py test will the forced roam method to create and roam number of Wi-Fi stations between two or more APs with the same SSID on the same channel
    cli- python3 roam_test.py --mgr localhost --mgr_port 8080
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.
"""

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
import pdfkit
from lf_report import lf_report
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from datetime import datetime
from lf_graph import lf_bar_graph


class roam_test(LFCliBase):
    def __init__(self, lfclient_host="localhost", lfclient_port=8080, radio=None, sta_prefix=None, start_id=0,
                 num_sta=None,  dut_ssid=None, dut_security=None, dut_passwd=None, band=None, channel=None, roam_configuration=None,
                 roam_interval=None, repeat=None,
                upstream="eth1", _debug_on=False, _exit_on_error=False, _exit_on_fail=False):
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
        self.band = band
        self.channel = channel
        self.repeat = repeat
        self.roam_interval = roam_interval
        self.roam_configuration = roam_configuration
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()

        print("Test is Initialized")

    def precleanup(self):
        self.count = 0
        for rad in self.radio:
            self.count = self.count + 1

            if self.count == 2:
                if self.band[0] == "2.4G":
                    self.sta_prefix = "5G_sta"
                elif self.band[0] == "5G":
                    self.sta_prefix = "2G_sta"
                self.station_list1 = LFUtils.portNameSeries(prefix_=self.sta_prefix, start_id_=self.sta_start_id,
                                                            end_id_=self.num_sta[1] - 1, padding_number_=10000,
                                                            radio=rad)

                # cleanup station list of 5G band when stations created in 2.4G band as well as 5G band at a time
                self.station_profile.cleanup(self.station_list1, delay=1, debug_=self.debug)
                LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                                   port_list=self.station_list1,
                                                   debug=self.debug)
                time.sleep(1)
                return

            self.station_list = LFUtils.portNameSeries(prefix_=self.sta_prefix, start_id_=self.sta_start_id,
                                                       end_id_=self.num_sta[0] - 1, padding_number_=10000,
                                                       radio=rad)

            # cleans stations
            self.station_profile.cleanup(self.station_list, delay=1, debug_=self.debug)
            LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                               port_list=self.station_list,
                                               debug=self.debug)
            time.sleep(1)

        print("precleanup done")

    def build(self):
        #creating station list
        if self.band[0] == "2.4G":
            self.station_list_2G = self.station_list
        if self.band[0] == "5G":
            self.station_list_5G = self.station_list
        if len(self.band) == 2:
            self.station_list_2G = self.station_list.copy()
            self.station_list_5G = self.station_list1.copy()
        self.channels = self.channel.copy()

        # station build
        for rad in self.radio:

            #channel selection
            host = self.host
            base_url = "http://%s:8080" % host
            resource_id = 1  # typically you're using resource 1 in stand alone realm
            lf_r = LFRequest.LFRequest(base_url + "/cli-json/set_wifi_radio")
            lf_r.addPostData({
                "shelf": 1,
                "resource": resource_id,
                "radio": rad,
                "mode": 8,
                "channel": self.channel[0],
            })
            lf_r.jsonPost()
            print("done")
            time.sleep(10)

            self.station_profile.use_security(self.security, self.ssid, self.password)
            self.station_profile.set_number_template("00")

            self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)

            self.station_profile.set_command_param("set_port", "report_timer", 1500)

            # connect station to particular bssid
            #self.station_profile.set_command_param("add_sta", "ap", self.bssid[0])

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
                self.channel[0] = self.channel[1]

        print("Test Build done")

    def roam(self):

        self.total_roaming_pass = 0
        self.total_roaming_fail = 0
        self.twog_station_data = {
            "band":None,
            "stations":[],
            "pass":[],
            "fail":[]
        }
        self.fiveg_station_data = {
            "band": None,
            "stations":[],
            "pass":[],
            "fail":[]
        }
        self.twog_bssid_data = {
            "band":None,
            "bssids":[],
            "pass":[],
            "fail":[]
        }
        self.fiveg_bssid_data = {
            "band":None,
            "bssids":[],
            "pass":[],
            "fail":[]
        }
        frequncies = []
        dict_channel_freq = {
                             "1":2412, "2":2417, "3":2422, "4":2427, "5":2432, "6":2437, "7":2442, "8":2447, "9":2452,
                             "10":2457, "11":2462, "12":2467, "13":2472, "14":2484, "34":5170, "36":5180, "38":5190,
                             "40":5200, "42":5210, "44":5220, "46":5230, "48":5240, "52":5260, "56":5280, "60":5300,
                             "64": 5320, "100":5500, "104":5520, "108":5540, "112":5560, "116":5580, "120":5600, "124":5620,
                             "128":5640, "132":5660, "136":5680, "140":5700, "144":5720, "149":5745, "153":5765, "157":5785,
                             "161": 5805, "165":5825, "169":5845, "173":5865
                             }
        #selecting frequency according to the channel
        for i in self.channels:
            frequncies.append(dict_channel_freq[str(i)])

        extra_data = frequncies
        string_extra_data = 'trigger freq'
        for i in extra_data:
            string_extra_data = string_extra_data + ' ' + str(i)

        # creating scan_wifi command
        self.scan_wifi_data = {
            "shelf": 1,
            "resource": 1,
            "port": None,
            "key": "NA",
            "extra": string_extra_data
        }

        # creating wifi_cli_cmd command
        self.wifi_cli_cmd_data = {
            "shelf": 1,
            "resource": 1,
            "port": None,
            "wpa_cli_cmd": None
        }

        for i in range(self.repeat):

            if len(self.band) == 2:
                self.both_band_roam()
                continue

            elif self.roam_configuration[0][2] == "2.4G":
                station_list = self.station_list_2G[self.roam_configuration[0][0]:self.roam_configuration[0][1]+1]
                bssid_list = self.roam_configuration[0][3:]
            elif self.roam_configuration[0][2] == "5G":
                station_list = self.station_list_5G[self.roam_configuration[0][0]:self.roam_configuration[0][1] + 1]
                bssid_list = self.roam_configuration[0][3:]

            #check first bssid is same as station already connected
            data = self.json_get("ports/list?fields=ap")
            for j in data['interfaces']:
                for k in j:
                    if station_list[0] == k:
                        bssid_first = j[station_list[0]]["ap"]
            if bssid_first.lower() == bssid_list[0].lower():
                bssids = bssid_list.copy()
                bssid_list.pop(0)
                bssid_list.append(bssids[0])

            for j in bssid_list:
                self.scan_wifi_data["port"] = station_list[0][4:]
                self.json_post("/cli-json/scan_wifi", self.scan_wifi_data, suppress_related_commands_=True)
                time.sleep(2)
                for k in station_list:
                    self.wifi_cli_cmd_data["wpa_cli_cmd"] = 'roam ' + j
                    self.wifi_cli_cmd_data["port"] = k[4:]
                    print(self.wifi_cli_cmd_data)
                    self.json_post("/cli-json/wifi_cli_cmd", self.wifi_cli_cmd_data, suppress_related_commands_=True)
                time.sleep(2)
                self.display(station_list, j,self.roam_configuration[0][2])
                time.sleep(self.roam_interval-2)

    def both_band_roam(self):
        for i in self.roam_configuration:
            if i[2] == "2.4G":
                bssid_list_2G = i[3:]
                station_list1 = self.station_list_2G[i[0]:i[1]+1]

                # check first bssid is same as station already connected
                bssid = self.json_get("/port/1/1/2G_sta0000")["interface"]["ap"]
                if bssid.lower() == bssid_list_2G[0].lower():
                    bssids = bssid_list_2G.copy()
                    bssid_list_2G.pop(0)
                    bssid_list_2G.append(bssids[0])
            elif i[2] == "5G":
                bssid_list_5G = i[3:]
                station_list2 = self.station_list_5G[i[0]:i[1]+1]
                bssid = self.json_get("/port/1/1/5G_sta0000")["interface"]["ap"]
                if bssid.lower() == bssid_list_5G[0].lower():
                    bssids = bssid_list_5G.copy()
                    bssid_list_5G.pop(0)
                    bssid_list_5G.append(bssids[0])

        #creating list of both band bssids
        bssid_list_both = []
        for i in range(len(bssid_list_5G)):
            l=[]
            l.append(bssid_list_2G[i])
            l.append(bssid_list_5G[i])
            bssid_list_both.append(l)
        print("bssid list",bssid_list_both)
        for i in bssid_list_both:

            #roam 2.4G stations
            self.scan_wifi_data["port"] = station_list1[0][4:]
            self.json_post("/cli-json/scan_wifi", self.scan_wifi_data, suppress_related_commands_=True)
            time.sleep(2)
            for k in station_list1:
                self.wifi_cli_cmd_data["wpa_cli_cmd"] = 'roam ' + i[0]
                self.wifi_cli_cmd_data["port"] = k[4:]
                print(self.wifi_cli_cmd_data)
                self.json_post("/cli-json/wifi_cli_cmd", self.wifi_cli_cmd_data, suppress_related_commands_=True)

            #roam 5G stations
            self.scan_wifi_data["port"] = station_list2[0][4:]
            self.json_post("/cli-json/scan_wifi", self.scan_wifi_data, suppress_related_commands_=True)
            time.sleep(2)
            for k in station_list2:
                self.wifi_cli_cmd_data["wpa_cli_cmd"] = 'roam ' + i[1]
                self.wifi_cli_cmd_data["port"] = k[4:]
                print(self.wifi_cli_cmd_data)
                self.json_post("/cli-json/wifi_cli_cmd", self.wifi_cli_cmd_data, suppress_related_commands_=True)

            time.sleep(2)
            self.display(station_list1, i[0], "2.4G")
            self.display(station_list2,i[1],"5G")
            time.sleep(self.roam_interval - 2)


    def display(self,station_list,bssid,band):

        pass_count_station = 0
        fail_count_station = 0
        pass_count_bssid = 0
        fail_count_bssid = 0

        data = self.json_get("ports/list?fields=ap")

        #geting bssid of stations from ap field from port manager
        for i in station_list:
            for j in data['interfaces']:
                for k in j:
                    if i == k:
                        ap = j[i]["ap"]

            if ap.lower() == bssid.lower():
                self.total_roaming_pass = self.total_roaming_pass + 1
                pass_count_station = pass_count_station + 1
                pass_count_bssid = pass_count_bssid + 1
                print(i[4:] + " Roamed to bssid " + bssid)
            else:
                self.total_roaming_fail = self.total_roaming_fail + 1
                fail_count_station = fail_count_station + 1
                fail_count_bssid = fail_count_bssid + 1
                print("Roaming failed")

            if band == "2.4G":
                self.twog_station_data["band"] = "2.4G"
                if i not in self.twog_station_data["stations"]:
                    self.twog_station_data["stations"].append(i)
                    self.twog_station_data["pass"].append(pass_count_station)
                    self.twog_station_data["fail"].append(fail_count_station)
                else:
                    station_index = self.twog_station_data["stations"].index(i)
                    self.twog_station_data["pass"][station_index] = self.twog_station_data["pass"][station_index] + pass_count_station
                    self.twog_station_data["fail"][station_index] = self.twog_station_data["fail"][station_index] + fail_count_station

            if band == "5G":
                self.fiveg_station_data["band"] = "5G"
                if i not in self.fiveg_station_data["stations"]:
                    self.fiveg_station_data["stations"].append(i)
                    self.fiveg_station_data["pass"].append(pass_count_station)
                    self.fiveg_station_data["fail"].append(fail_count_station)
                else:
                    station_index = self.fiveg_station_data["stations"].index(i)
                    self.fiveg_station_data["pass"][station_index] = self.fiveg_station_data["pass"][station_index] + pass_count_station
                    self.fiveg_station_data["fail"][station_index] = self.fiveg_station_data["fail"][station_index] + fail_count_station
            pass_count_station = 0
            fail_count_station = 0

        if band == "2.4G":
            self.twog_bssid_data["band"] = "2.4G"
            if bssid not in self.twog_bssid_data["bssids"]:
                self.twog_bssid_data["bssids"].append(bssid)
                self.twog_bssid_data["pass"].append(pass_count_bssid)
                self.twog_bssid_data["fail"].append(fail_count_bssid)
            else:
                bssid_index = self.twog_bssid_data["bssids"].index(bssid)
                self.twog_bssid_data["pass"][bssid_index] = self.twog_bssid_data["pass"][
                                                                    bssid_index] + pass_count_bssid
                self.twog_bssid_data["fail"][bssid_index] = self.twog_bssid_data["fail"][
                                                                    bssid_index] + fail_count_bssid

        if band == "5G":
            self.fiveg_bssid_data["band"] = "5G"
            if bssid not in self.fiveg_bssid_data["bssids"]:
                self.fiveg_bssid_data["bssids"].append(bssid)
                self.fiveg_bssid_data["pass"].append(pass_count_bssid)
                self.fiveg_bssid_data["fail"].append(fail_count_bssid)
            else:
                bssid_index = self.fiveg_bssid_data["bssids"].index(bssid)
                self.fiveg_bssid_data["pass"][bssid_index] = self.fiveg_bssid_data["pass"][
                                                                bssid_index] + pass_count_bssid
                self.fiveg_bssid_data["fail"][bssid_index] = self.fiveg_bssid_data["fail"][
                                                                bssid_index] + fail_count_bssid



    def start(self, print_pass=False, print_fail=False):
        print("Test Started")

    def stop(self):
        self.station_profile.admin_down()

    def postcleanup(self):
        self.station_profile.cleanup(self.station_profile.station_names, delay=1, debug_=self.debug)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)

    def set_values(self):
        if self.band[0] == "2.4G":
            self.sta_prefix = "2G_sta"
        elif self.band[0] == "5G":
            self.sta_prefix = "5G_sta"

def main():
    # This has --mgr, --mgr_port and --debug
    parser = LFCliBase.create_bare_argparse(prog="roam_test.py", formatter_class=argparse.RawTextHelpFormatter,
                                            epilog="About This Script")


    args = parser.parse_args()

    # 1st time stamp for test duration
    time_stamp1 = datetime.now()

    #Taking input from json file
    radios = []
    channels = []
    num_of_stations = []
    bands = []

    with open('roam_config.json') as f:
      file_data = json.load(f)

    roam_interval = file_data["roam interval"]
    repeat = file_data["repeat"]
    ap_name = file_data["ap name"]
    roam_configuration = file_data["roaming_configuration"]
    for i in list(file_data.keys()):
      if i == "2.4G client":
        num_of_stations.append(file_data["2.4G client"])
        bands.append("2.4G")
      if i == "5G client":
        num_of_stations.append(file_data["5G client"])
        bands.append("5G")
      if i == "2.4G radio":
        radios.append(file_data["2.4G radio"])
      if i == "5G radio":
        radios.append(file_data["5G radio"])
      if i == "2.4G channel":
        channels.append(file_data["2.4G channel"])
      if i == "5G channel":
        channels.append(file_data["5G channel"])

    #for num_stations in num_of_stations:
    obj = roam_test(lfclient_host = args.mgr,
                    lfclient_port = args.mgr_port,
                    radio = radios,
                    dut_ssid = file_data["ssid"],
                    dut_passwd = file_data["passwd"],
                    dut_security = file_data["security"],
                    num_sta = num_of_stations,
                    band = bands,
                    channel = channels,
                    roam_configuration = roam_configuration,
                    repeat = repeat,
                    roam_interval = roam_interval
                    )

    obj.set_values()
    obj.precleanup()
    obj.build()
    obj.start(False, False)
    obj.roam()
    #time.sleep(60)
    obj.stop()
    obj.postcleanup()

    # 2nd time stamp for test duration
    time_stamp2 = datetime.now()

    # total time for test duration
    test_duration = str(time_stamp2 - time_stamp1)[:-7]

    test_setup_data = {
    'Device Under Test': ap_name,
    'SSID': [file_data["ssid"]]

    }

    #adding number of stations in dict for showing in report
    for i in bands:
        if i == "2.4G":
            test_setup_data["Number of 2.4Ghz Stations"] = [file_data["2.4G client"]]
        if i == "5G":
            test_setup_data["Number of 5Ghz Stations"] = [file_data["5G client"]]

    test_setup_data["Roam configuration repeat"] = [repeat]
    test_setup_data["Test Duration"] = test_duration

    test_setup = pd.DataFrame(test_setup_data)

    date = str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]

    report = lf_report(_results_dir_name = "roam_test")
    report.set_title("Roam Test")
    report.set_date(date)
    report.build_banner()
    report.set_obj_html("Objective",
                        "This test uses the forced roam method to create and roam number of Wi-Fi stations between two or more APs with the same SSID on the same channel.")
    report.build_objective()
    report.set_table_title("Test Setup Information")
    report.build_table_title()
    report.set_table_dataframe(test_setup)
    report.build_table()
    twog_station_data = obj.twog_station_data
    fiveg_station_data = obj.fiveg_station_data
    twog_bssid_data = obj.twog_bssid_data
    fiveg_bssid_data = obj.fiveg_bssid_data
    total_roam = {
        "pass":[obj.total_roaming_pass],
        "fail":[obj.total_roaming_fail],
        "x_axis":[""],
        "x_axis_name":"Total roam",
        "y_axis_name":"Amount",
        "image_name":"total_roam_image",
        "title":"Total Roams - All Stations",
        "objective":"The below graph shows the total number of success and failure roams for all the connected station within the test duration."
    }

    num = 0
    whole_data_dict = {}
    num = num + 1
    whole_data_dict[num] = total_roam
    if twog_station_data["band"] == "2.4G":
        x_axis = []
        for i in range(len(twog_station_data["stations"])):
            x_axis.append(i)
        twog_station_data["x_axis"] = x_axis
        twog_station_data["x_axis_name"] = "Stations"
        twog_station_data["y_axis_name"] = "Amount"
        twog_station_data["image_name"] = "twog_station_image"
        twog_station_data["title"] = "Success/Failure Roams - 2.4Ghz Stations"
        twog_station_data["objective"] = "The below graph shows the number of success and failure roams for all 2.4GHz WiFi stations."
        num = num + 1
        whole_data_dict[num] = twog_station_data
        twog_bssid_data["x_axis"] = twog_bssid_data["bssids"]
        twog_bssid_data["x_axis_name"] = "BSSID"
        twog_bssid_data["y_axis_name"] = "Amount"
        twog_bssid_data["image_name"] = "twog_bssid_image"
        twog_bssid_data["title"] = "Success/Failure Roams - 2.4Ghz BSSID's"
        twog_bssid_data["objective"] = "The below graph shows how many roams succeeded and fail on all 2.4Ghz BSSID's."
        num = num + 1
        whole_data_dict[num] = twog_bssid_data
    if fiveg_station_data["band"] == "5G":
        x_axis = []
        for i in range(len(fiveg_station_data["stations"])):
            x_axis.append(i)
        fiveg_station_data["x_axis"] = x_axis
        fiveg_station_data["x_axis_name"] = "Stations"
        fiveg_station_data["y_axis_name"] = "Amount"
        fiveg_station_data["image_name"] = "fiveg_station_image"
        fiveg_station_data["title"] = "Success/Failure Roams - 5Ghz Stations"
        fiveg_station_data["objective"] = "The below graph shows the number of success and failure roams for all 5GHz WiFi stations."
        num = num + 1
        whole_data_dict[num] = fiveg_station_data
        fiveg_bssid_data["x_axis"] = fiveg_bssid_data["bssids"]
        fiveg_bssid_data["x_axis_name"] = "BSSID"
        fiveg_bssid_data["y_axis_name"] = "Amount"
        fiveg_bssid_data["image_name"] = "fiveg_bssid_image"
        fiveg_bssid_data["title"] = "Success/Failure Roams - 5Ghz BSSID's"
        fiveg_bssid_data["objective"] = "The below graph shows how many roams succeeded and fail on all 5Ghz BSSID's."
        num = num + 1
        whole_data_dict[num] = fiveg_bssid_data
    print("whole data:",whole_data_dict)
    for i in whole_data_dict:

        success = whole_data_dict[i]["pass"]
        fail = whole_data_dict[i]["fail"]
        set_xaxis = whole_data_dict[i]["x_axis"]
        dataset = [success,fail]
        # test lf_graph in report
        x_axis_values = set_xaxis

        report.set_obj_html(whole_data_dict[i]["title"],whole_data_dict[i]["objective"])
        report.build_objective()

        graph = lf_bar_graph(_data_set=dataset,
                             _xaxis_name=whole_data_dict[i]["x_axis_name"],
                             _yaxis_name=whole_data_dict[i]["y_axis_name"],
                             _xaxis_categories=x_axis_values,
                             _label=["Success","Fail"],
                             _graph_image_name=whole_data_dict[i]["image_name"],
                             _figsize=(18, 6),
                             _color=["g", "r"],
                             _display_value=True,
                             _step=None,
                             _color_edge=None)

        graph_png = graph.build_bar_graph()

        print("graph name {}".format(graph_png))

        report.set_graph_image(graph_png)
        # need to move the graph image to the results
        report.move_graph_image()

        report.build_graph()

    '''input_setup = pd.DataFrame({
        'Information': [],
        "Contact support@candelatech.com": []

    })
    report.set_table_title("Input Setup Information")
    report.build_table_title()

    report.set_table_dataframe(input_setup)
    report.build_table()'''

    html_file = report.write_html()
    print("returned file {}".format(html_file))
    print(html_file)
    report.write_pdf()


if __name__ == "__main__":
    main()

