#!/usr/bin/env python3
"""
 NOTE : Detection Probability Test  is compilance to the Dynamic Frequency Selection(DFS) Regulation, it creates regulatory specified radar pulses
                                         to the DUT repeatedly to measure the probability
                                         of detection.

 run : - python3 lf_detection_probability_test.py  --host 192.168.1.31 --ssid Candela_20MHz --passwd [BLANK] --security open --trials 1   --more_option centre --fcctypes FCC0

"""

import sys
import os
import logging
import importlib
import argparse
import time
import datetime
from datetime import datetime
import pandas as pd
import paramiko
import matplotlib.pyplot as plt
import random

if sys.version_info[0] != 3:
    logging.critical("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
sniff_radio = importlib.import_module("py-scripts.lf_sniff_radio")
sta_connect = importlib.import_module("py-scripts.sta_connect2")
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")
lf_clean = importlib.import_module("py-scripts.lf_cleanup")
cv_test_reports = importlib.import_module("py-json.cv_test_reports")
lf_report = cv_test_reports.lanforge_reports
lf_report_pdf = importlib.import_module("py-scripts.lf_report")
lf_pcap = importlib.import_module("py-scripts.lf_pcap")
lf_graph = importlib.import_module("py-scripts.lf_graph")


class DfsTest(Realm):
    def __init__(self,
                 host=None,
                 port=None,
                 ssid=None,
                 passwd=None,
                 security=None,
                 radio=None,
                 upstream=None,
                 fcctypes=None,
                 channel=None,
                 sniff_radio=None,
                 static=None,
                 static_ip=None,
                 ip_mask=None,
                 gateway_ip=None,
                 enable_traffic=None,
                 desired_detection=None,
                 extra_trials=None,
                 more_option=None,
                 time_int=None,
                 trials=None
                 ):
        super().__init__(host, port)
        self.host = host
        self.port = port
        self.ssid = ssid
        self.passwd = passwd
        self.security = security
        self.radio = radio
        self.upstream = upstream
        self.fcctypes = fcctypes
        self.channel = channel
        self.sniff_radio = sniff_radio
        self.static = static
        self.static_ip = static_ip
        self.ip_mask = ip_mask
        self.gateway_ip = gateway_ip
        self.enable_traffic = enable_traffic
        self.desired_detection = desired_detection
        self.extra_trials = extra_trials
        self.more_option = more_option
        self.time_int = time_int
        self.trials = trials
        self.pcap_name = None
        self.pcap_obj_2 = None
        self.staConnect = sta_connect.StaConnect2(self.host, self.port, outfile="staconnect2.csv")
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.pcap_obj = lf_pcap.LfPcap()

    def get_station_list(self):
        sta = self.staConnect.station_list()
        if sta == "no response":
            return "no response"
        sta_list = []
        for i in sta:
            for j in i:
                sta_list.append(j)
        return sta_list

    # set channel to parent radio and start sniffing
    def start_sniffer(self, radio_channel=None, radio=None, test_name="dfs_csa_", duration=60):
        self.pcap_name = test_name + str(datetime.now().strftime("%Y-%m-%d-%H-%M")).replace(':', '-') + ".pcap"
        if self.more_option == "centre":
            self.pcap_obj_2 = sniff_radio.SniffRadio(lfclient_host=self.host, lfclient_port=self.port,
                                                 radio=self.sniff_radio, channel=radio_channel, monitor_name="monitor", channel_bw="20")
            self.pcap_obj_2.setup(0, 0, 0)
            time.sleep(5)
            self.pcap_obj_2.monitor.admin_up()
            time.sleep(5)
            self.pcap_obj_2.monitor.start_sniff(capname=self.pcap_name, duration_sec=duration)
        elif self.more_option == "random":
            self.pcap_obj_2 = sniff_radio.SniffRadio(lfclient_host=self.host, lfclient_port=self.port,
                                                     radio=self.sniff_radio, channel=radio_channel,
                                                     monitor_name="monitor", channel_bw="20")
            self.pcap_obj_2.setup(1, 1, 1)
            time.sleep(5)
            self.pcap_obj_2.monitor.admin_up()
            time.sleep(5)
            self.pcap_obj_2.monitor.start_sniff(capname=self.pcap_name, duration_sec=duration)


    def station_data_query(self, station_name="wlan0", query="channel"):
        # print(station_name)
        sta = station_name.split(".")
        url = f"/port/{sta[0]}/{sta[1]}/{sta[2]}?fields={query}"
        # print("url//////", url)
        response = self.local_realm.json_get(_req_url=url)
        # print("response: ", response)
        if (response is None) or ("interface" not in response):
            print("station_list: incomplete response:")
            # pprint(response)
            exit(1)
        y = response["interface"][query]
        # print(y)
        return y

    def precleanup(self):
        obj = lf_clean.lf_clean(host=self.host,
                                port=self.port,
                                clean_cxs=True,
                                clean_endp=True)
        obj.resource = "all"
        obj.cxs_clean()
        # obj.sta_clean()
        obj.port_mgr_clean()

    def create_client(self, start_id=0, sta_prefix="wlan", num_sta=1):

        local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        station_profile = local_realm.new_station_profile()

        sta_list = self.get_station_list()
        # print(sta_list)
        if not sta_list:
            print("no stations on lanforge")
        else:
            print("clean existing station")
            station_profile.cleanup(sta_list, delay=1)
            LFUtils.wait_until_ports_disappear(base_url=local_realm.lfclient_url,
                                               port_list=sta_list,
                                               debug=True)
            # time.sleep(2)
            print("pre cleanup done")
        station_list = LFUtils.portNameSeries(prefix_=sta_prefix, start_id_=start_id,
                                              end_id_=num_sta - 1, padding_number_=10000,
                                              radio=self.radio)
        station_profile.use_security(self.security, self.ssid, self.passwd)
        station_profile.set_number_template("00")

        station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        station_profile.set_command_flag("set_port", "rpt_timer", 1)
        print("Creating stations.")
        station_profile.create(radio=self.radio, sta_names_=station_list)

        print("Waiting for ports to appear")
        local_realm.wait_until_ports_appear(sta_list=station_list)
        station_profile.admin_up()
        print("Waiting for ports to admin up")

        if self.static:
            sta_list = self.get_station_list()
            port = self.station_data_query(station_name=sta_list[0], query="port")
            port_ = port.split(".")
            set_port = {
                "shelf": port_[0],
                "resource": port_[1],
                "port": port_[2],
                "ip_addr": self.static_ip,
                "netmask": self.ip_mask,
                "gateway": self.gateway_ip,
                "cmd_flags": "NA",
                "current_flags": "NA",
                "mac": "NA",
                "mtu": "NA",
                "tx_queue_len": "NA",
                "alias": "NA",
                "interest": "8552366108"
            }
            self.local_realm.json_post("/cli-json/set_port", set_port)
        print("wait for ip")
        if local_realm.wait_for_ip(station_list):
            print("All stations got IPs")
            return True
        else:
            print("Stations failed to get IPs")
            exit(1)
            return False

    def run_hackrf(self, width=1, pri=1428, count=18, freq=None):
        p = paramiko.SSHClient()
        p.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())  # This script doesn't work for me unless this line is added!
        p.connect(self.host, port=22, username="lanforge", password="lanforge")
        p.get_transport()
        command = "sudo python lf_hackrf.py --pulse_width " + str(width) + " --pulse_interval " + str(pri) + " --pulse_count " + str(count) + " --sweep_time 1000 --freq " + str(freq) + " --one_burst"
        stdin, stdout, stderr = p.exec_command(str(command), get_pty=True)
        stdin.write("lanforge\n")
        stdin.flush()
        opt = stdout.readlines()
        opt = "".join(opt)
        print(opt)
        p.close()

        # return current_time

    def stop_sniffer(self):
        print("in stop_sniffer")
        directory = None
        directory_name = "pcap"
        if directory_name:
            directory = os.path.join("", str(directory_name))
        try:

            if not os.path.exists(directory):
                os.mkdir(directory)
        except Exception as x:
            print(x)

        self.pcap_obj_2.monitor.admin_down()
        time.sleep(2)
        self.pcap_obj_2.cleanup()
        lf_report.pull_reports(hostname=self.host, port=22, username="lanforge",
                               password="lanforge",
                               report_location="/home/lanforge/" + self.pcap_name,
                               report_dir="pcap")
        time.sleep(10)

        return self.pcap_name

    def main_logic(self, bssid=None):
        main_dict = dict.fromkeys(self.fcctypes)
        print(main_dict)
        list_ = []
        for i in range(self.trials + self.extra_trials):
            var = 000
            var_1 = "Trial_" + str(var + i + 1)
            list_.append(var_1)
        sec_dict = dict.fromkeys(list_)
        for i in main_dict:
            main_dict[i] = sec_dict.copy()
        print(main_dict)
        width_, interval_, count_ = "", "", ""
        for fcc in self.fcctypes:
            for tria in range(self.trials + self.extra_trials):
                var = 000
                var_1 = "Trial_" + str(var + tria + 1)
                new_list = ["Burst", "Pulses", "Width", "PRI(US)", "Detected", "Frequency(MHz)", "Detection Time(sec)"]
                third_dict = dict.fromkeys(new_list)
                main_dict[fcc][var_1] = third_dict.copy()
                print(main_dict)

                # standard = {"FCC0": {"width_": "1", "interval_": "1428", "count_": "18"}, "FCC1": {}}

                if fcc == "FCC0":
                    width_ = "1"
                    interval_ = "1428"
                    count_ = "18"
                elif fcc == "FCC1":
                    width_ = "1"
                    interval_ = str(random.randint(518, 3066))
                    # interval_ = "1163"
                    count_ = str(random.randint(17, 102))
                elif fcc == "FCC2":
                    width_ = str(random.randint(1, 5))
                    interval_ = str(random.randint(150, 230))
                    count_ = str(random.randint(23, 29))
                elif fcc == "FCC3":
                    width_ = str(random.randint(6, 10))
                    interval_ = str(random.randint(200, 500))
                    count_ = str(random.randint(16, 18))
                elif fcc == "FCC4":
                    width_ = str(random.randint(11, 12))
                    interval_ = str(random.randint(200, 500))
                    count_ = str(random.randint(12, 16))
                # elif fcc == "FCC5":
                #     width_ = "70"
                #     interval_ = "1975"
                #     count_ = "3"
                elif fcc == "ETSI0":
                    width_ = "1"
                    interval_ = "1429"
                    count_ = "18"
                elif fcc == "ETSI1":
                    width_ = str(random.randint(1, 5))
                    interval_ = str(random.randint(1000, 5000))
                    count_ = "10"
                elif fcc == "ETSI2":
                    width_ = str(random.randint(1, 15))
                    interval_ = str(random.randint(625, 5000))
                    count_ = "15"
                elif fcc == "ETSI3":
                    width_ = str(random.randint(1, 15))
                    interval_ = str(random.randint(250, 435))
                    count_ = "25"
                elif fcc == "ETSI4":
                    width_ = str(random.randint(20, 30))
                    interval_ = str(random.randint(250, 500))
                    count_ = "20"
                elif fcc == "ETSI5":
                    width_ = str(random.randint(1, 2))
                    interval_ = str(random.randint(2500, 3333))
                    count_ = "10"
                elif fcc == "ETSI6":
                    width_ = str(random.randint(1, 2))
                    interval_ = str(random.randint(833, 2500))
                    count_ = "15"
                elif fcc == "Japan-W53-1":
                    width_ = 1
                    interval_ = 1428
                    count_ = 18
                elif fcc == "Japan-W53-2":
                    width_ = random.randint(1, 15)
                    interval_ = 3846
                    count_ = 18
                elif fcc == "korea_1":
                    width_ = 1
                    interval_ = 1429
                    count_ = 18
                elif fcc == "korea_2":
                    width_ = 1
                    interval_ = 556
                    count_ = 10
                elif fcc == "korea_3":
                    width_ = 2
                    interval_ = 3030
                    count_ = 70
                elif fcc == "Japan-W56-2":
                    width_ = 1
                    interval_ = 1429
                    count_ = 18
                elif fcc == "Japan-W56-3":
                    width_ = 2
                    interval_ = 4000
                    count_ = 18
                elif fcc == "Japan-W56-4":
                    width_ = str(random.randint(1, 5))
                    interval_  = str(random.randint(150, 230))
                    count_ = str(random.randint(23, 29))
                elif fcc == "Japan-W56-5":
                    width_ = str(random.randint(6, 10))
                    interval_ = str(random.randint(200, 500))
                    count_ = str(random.randint(16, 18))
                elif fcc == "Japan-W56-6":
                    width_ = str(random.randint(11, 20))
                    interval_ = str(random.randint(200, 500))
                    count_ = str(random.randint(12, 16))


                main_dict[fcc][var_1]["Burst"] = "1"
                main_dict[fcc][var_1]["Pulses"] = count_
                main_dict[fcc][var_1]["Width"] = width_
                main_dict[fcc][var_1]["PRI(US)"] = interval_

                if self.more_option == "centre":
                    frequency = {"52": "5260000", "56": "5280000", "60": "5300000", "64": "5320000", "100": "5500000",
                                 "104": "5520000", "108": "5540000", "112": "5560000", "116": "5580000", "120": "5600000",
                                 "124": "5620000",
                                 "128": "5640000", "132": "5660000", "136": "5680000", "140": "5700000"}
                if self.more_option == "random":
                    frequency = {"52": "5260000", "56": "5280000", "60": "5300000", "64": "5320000", "100": str(random.randint(5490, 5510)),
                                 "104": "5520000", "108": "5540000", "112": "5560000", "116": "5580000",
                                 "120": "5600000",
                                 "124": "5620000",
                                 "128": "5640000", "132": "5660000", "136": "5680000", "140": "5700000"}
                print(str(int(frequency[str(self.channel)]) * 1000))
                if self.more_option == "centre":
                    main_dict[fcc][var_1]["Frequency(MHz)"] = str(frequency[str(self.channel)])
                elif self.more_option == "random":
                    main_dict[fcc][var_1]["Frequency(MHz)"] = str(int(frequency[str(self.channel)]) * 1000)

                print("starting sniffer")
                self.start_sniffer(radio_channel=self.channel, radio=self.sniff_radio,
                                   test_name="dfs_csa_" + str(fcc) + "_" + str(var_1) + "_channel" + str(self.channel) + "_")
                print("generate radar")
                if self.more_option == "centre":
                    self.run_hackrf(width=width_, pri=interval_, count=count_, freq=str(frequency[str(self.channel)]))
                elif self.more_option == "random":
                    self.run_hackrf(width=width_, pri=interval_, count=count_,
                                    freq=str(int(frequency[str(self.channel)]) * 1000))

                current_time = datetime.now()
                print("Current date and time : ")
                current_time = current_time.strftime("%b %d, %Y  %H:%M:%S")
                print("time stamp of radar send", current_time)
                time.sleep(15)
                print("stop sniffer")
                file_name_ = self.stop_sniffer()
                file_name = "./pcap/" + str(file_name_)
                print("pcap file name", file_name)

                # pcap read logic

                csa_frame = self.pcap_obj.check_frame_present(
                    pcap_file=str(file_name),
                    filter="(wlan.csa.channel_switch.count == 4 && wlan.ssid == %s &&  wlan.bssid == %s)" % (str(self.ssid), str(bssid)))
                print("csa frame", csa_frame)
                if len(csa_frame) != 0 and csa_frame != "empty":
                    print("csa frame  is present")
                    print("radar detected")
                    main_dict[fcc][var_1]["Detected"] = "YES"
                    csa_frame_time = self.pcap_obj.read_arrival_time(
                        pcap_file=str(file_name),
                        filter="(wlan.csa.channel_switch.count == 4 && wlan.ssid == %s &&  wlan.bssid == %s)" % (str(self.ssid), str(bssid)))
                    print("csa frame  time is ", csa_frame_time)
                    csa_time = str(csa_frame_time)
                    csa_frame_time_ = None
                    for i in csa_time:
                        if i == ".":
                            print("yes")
                            ind = csa_time.index(".")
                            csa_frame_time_ = csa_time[:ind]
                    print("csa time", csa_frame_time_)

                    print("calculate detection time")
                    FMT = '%b %d, %Y %H:%M:%S'
                    c_time = datetime.strptime(csa_frame_time_, FMT) - datetime.strptime(current_time, FMT)
                    print("detection time ", c_time)
                    lst = str(c_time).split(":")
                    seconds = int(lst[0]) * 3600 + int(lst[1]) * 60 + int(lst[2])
                    d_time = seconds
                    print("detection time ", d_time)
                    main_dict[fcc][var_1]["Detection Time(sec)"] = d_time

                else:
                    print("csa frame is not present")
                    print("radar not detected")
                    main_dict[fcc][var_1]["Detected"] = "NO"
                    main_dict[fcc][var_1]["Detection Time(sec)"] = "NA"


                print(main_dict)
                if str(tria+1) == str(self.trials):
                    print("check desired trials percentage")
                    detection_list = []
                    for i in main_dict[fcc]:
                        print(i)
                        if main_dict[fcc][i] == None:
                            print("/n")
                        else:
                            detection_list.append(main_dict[fcc][i]["Detected"])
                    print("detection list", detection_list)
                    m = None
                    for i in detection_list:
                        if i == 'YES':
                            m = detection_list.count("YES")
                            print(m)
                        else:
                            if len(detection_list) == 1:
                                m = 0
                                print("\n")
                    result1 = all(element == "NO" for element in detection_list)
                    if result1:
                        m = 0
                    if len(detection_list) == 0:
                        print("/n")
                    else:
                        percent = (m / len(detection_list)) * 100
                        print(percent)
                        if percent < float(self.desired_detection):
                             continue
                        else:
                            break

        print("final dict", main_dict)
        return main_dict

    def run(self):
        print(self.fcctypes)
        test_time = datetime.now()
        test_time = test_time.strftime("%b %d %H:%M:%S")
        print("Test started at ", test_time)
        logging.info("Test started at " + str(test_time))

        print("clean all stations before the test")
        self.precleanup()

        print("create client")
        self.create_client()
        print("check if station is at expected channel")
        sta_list = self.get_station_list()
        channel = self.station_data_query(station_name=sta_list[0], query="channel")
        bssid = self.station_data_query(station_name=sta_list[0], query="ap")
        print(bssid)
        # channel = self.station_data_query(station_name="wlan0000", query="channel")
        if channel == self.channel:
            print("station is at expected channel")
        else:
            print("station is not at expected channel")
            exit(1)

        print("run particular logic for given  trials")
        main = self.main_logic(bssid=bssid)

        test_end = datetime.now()
        test_end = test_end.strftime("%b %d %H:%M:%S")
        print("Test ended at ", test_end)
        logging.info("Test ended at " + test_end)
        s1 = test_time
        s2 = test_end  # for example
        FMT = '%b %d %H:%M:%S'
        test_duration = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
        self.generate_report(test_duration= test_duration, main_dict=main)

    def test_graph(self, graph_dict=None):
        self.graph_image_name = "overall"
        x = []
        for i in graph_dict:
            x.append(i)
        pass_per =[]
        fail_per = []
        for i in graph_dict:

            pass_per.append(graph_dict[i])
            fail_per.append(round((float(100 - graph_dict[i])), 1))

        plt.rcParams["figure.figsize"] = [15, 7]
        plt.rcParams["figure.autolayout"] = True

        year =x
        issues_addressed = pass_per
        issues_pending =fail_per

        b1 = plt.barh(year, issues_addressed, color="green")

        b2 = plt.barh(year, issues_pending, left=issues_addressed, color="red")
        for i, v in enumerate(issues_addressed):
            if v != 0:
                plt.text(v * 0.45, i + .145, "%s%s" % (v, "%"), color='white', fontweight='bold', fontsize=10,
                         ha='center', va='center')
        for i, v in enumerate(issues_pending):
            if v != 0:
                plt.text(v * 0.45 + issues_addressed[i], i + .145, "%s%s" % (v, "%"), color='white', fontweight='bold',
                         fontsize=10,
                         ha='center', va='center')

        plt.legend([b1, b2], ["PASS", "FAIL"], title="Issues", bbox_to_anchor=(1.05, 1.0), loc="upper left")
        plt.xticks([])
        plt.savefig("%s.png" % self.graph_image_name, dpi=96)
        return "%s.png" % self.graph_image_name

    def generate_report(self, test_duration=None,  main_dict=None):
        print("test duration", test_duration)
        report = lf_report_pdf.lf_report(_path="", _results_dir_name="Detection Probability Test", _output_html="dpt.html",
                                         _output_pdf="dpt.pdf")
        # self.test_duration = "xyz"
        date = str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
        report_path = report.get_report_path()
        print(report_path)
        report.move_data(directory_name="pcap")

        test_setup_info = {
            "DUT Name": "NXP_AP",
            "SSID": self.ssid,
            "Test Duration": test_duration,
        }
        report.set_title("Detection Probability Test Report")
        report.set_date(date)
        report.build_banner()
        report.set_table_title("Test Setup Information")
        report.build_table_title()

        report.test_setup_table(value="Device under test", test_setup_data=test_setup_info)

        report.set_obj_html("Objective", "Detection Probability Test  is compilance to the Dynamic Frequency Selection"
                                         " (DFS) Regulation, it creates regulatory specified radar pulses "
                                         " to the DUT repeatedly to measure the probability "
                                         "of detection.")
        report.build_objective()
        report.set_obj_html("Result Summary", "The below graph provides information regarding detection probability percentage for various RADAR Types.")
        report.build_objective()
        graph_dict = dict.fromkeys(self.fcctypes)
        for fcc in self.fcctypes:
            detection_list = []
            for i in main_dict[fcc]:
                if main_dict[fcc][i] == None:
                    print("/n")
                else:
                    detection_list.append(main_dict[fcc][i]["Detected"])
            print("detection list", detection_list)
            m = None
            for i in detection_list:
                if i == 'YES':
                    m = detection_list.count("YES")
                    print(m)
                else:
                    if len(detection_list) == 1:
                        m = 0
                        print("\n")
            result1 = all(element == "NO" for element in detection_list)
            if result1:
                m = 0
            if len(detection_list) == 0:
                print("/n")
                graph_dict[fcc] = "0"

            else:
                percent = round(((m / len(detection_list)) * 100) , 1)
                print(percent)
                graph_dict[fcc] = percent

        print("graph dict", graph_dict)

        graph2 = self.test_graph(graph_dict=graph_dict)
        # graph1 = self.generate_per_station_graph()
        report.set_graph_image(graph2)
        report.move_graph_image()
        report.build_graph()

        # various atandards
        required_percent = {"FCC0": "60%", "FCC1":"60%", "FCC2": "60%", "FCC3": "60%", "FCC4": "80%", "FCC5": "70%",
                            "ETSI0": "NA", "ETSI1": "60%", "ETSI2": "60%", "ETSI3": "60%", "ETSI4": "60%", "ETSI5": "60%", "ETSI6": "60%",
                            "korea_1": "60%", "korea_2": "60%", "korea_3": "60%",
                            "Japan-W53-1": "60%", "Japan-W53-2": "60%", "Japan-W56-2": "60%", "Japan-W56-3": "60%", "Japan-W56-4": "60%", "Japan-W56-5": "60%", "Japan-W56-6": "60%"}


        report.set_obj_html("Summary Table",
                            "The below table provides detailed information regarding detection probability percentage for various RADAR Types.")
        report.build_objective()
        wave, pd_per, pd_req, tring, avg_detect, result = [], [], [], [], [], []

        for fcc in self.fcctypes:
            wave.append(fcc)

            # PD LOGIC
            detection_list = []
            for i in main_dict[fcc]:
                if main_dict[fcc][i] == None:
                    print("/n")
                else:
                    detection_list.append(main_dict[fcc][i]["Detected"])
            print("detection list", detection_list)
            m = None
            for i in detection_list:
                if i == 'YES':
                    m = detection_list.count("YES")
                    print(m)
                else:
                    if len(detection_list) == 1:
                        m = 0
                        print("\n")
                result1 = all(element == "NO" for element in detection_list)
                if result1:
                    m = 0
            if len(detection_list) == 0:
                print("/n")
                pd_per.append("0")
            else:
                percent = round(((m / len(detection_list)) * 100), 1)
                print(percent)
                pd_per.append(percent)
                if percent >= self.desired_detection:
                    result.append("PASSED")
                else:
                    result.append("FAILED")

            pd_req.append(required_percent[fcc])
            length= []
            for i in main_dict[fcc]:
                if main_dict[fcc][i] == None:
                    print("\n")
                else:
                    length.append(i)
            tring.append(len(length))

            # average detection time
            detection_list = []
            for i in main_dict[fcc]:
                if main_dict[fcc][i] == None:
                    print("/n")
                else:
                    detection_list.append(main_dict[fcc][i]['Detection Time(sec)'])
            print("detection list", detection_list)
            result1 = all(element == "NA" for element in detection_list)
            if len(detection_list) == 0:
                print("/n")
                avg_detect.append("0")
            else:
                if result1:
                    avg_detect.append(0)
                else:

                    sum = 0
                    for i in detection_list:
                        val = None
                        if i == "NA":
                            val = 0
                        else:
                            val = i

                        sum = sum + int(val)

                    av = round((sum / len(detection_list)), 1)
                    print(av)
                    avg_detect.append(av)
        table_1 = {
            "WaveForm Name": wave,
            "Pd %": pd_per,
            "Pd Required Percentage %": pd_req,
            "Num Trials": tring,
            "Average Detect Time (secs)": avg_detect,
            "Result": result,
        }
        test_setup = pd.DataFrame(table_1)
        report.set_table_dataframe(test_setup)
        report.build_table()

        report.set_obj_html("Detailed Result Table",
                            "The below tables provides detailed information for per trials run for each RADAR Types")
        report.build_objective()
        for fcc in self.fcctypes:
            report.set_obj_html("Detailed Result Table for " + str(fcc),
                                "The below table provides detailed information for per trials run for " + str(fcc) + "RADAR Type")
            report.build_objective()

            Trials, burst, pulse, width, pri, detect, frequency, det_time = [], [],[], [], [], [], [], []

            for i in main_dict[fcc]:
                if main_dict[fcc][i] == None:
                    print("ignore")

                else:
                    Trials.append(i)
                    burst.append(main_dict[fcc][i]['Burst'])
                    pulse.append(main_dict[fcc][i]['Pulses'])
                    width.append(main_dict[fcc][i]['Width'])
                    pri.append(main_dict[fcc][i]['PRI(US)'])
                    detect.append(main_dict[fcc][i]['Detected'])
                    frequency.append(main_dict[fcc][i]['Frequency(MHz)'])
                    det_time.append(main_dict[fcc][i]['Detection Time(sec)'])

            print("trial", Trials)
            table_2 = {
                "Trials": Trials,
                "Num Bursts": burst,
                "Num Pulses": pulse,
                "Pulse Width (us)": width,
                "PRI(us)": pri,
                "Detected": detect,
                "Frequency (MHz)": frequency,
                "Detection Time(secs)": det_time
            }
            test_setup_ = pd.DataFrame(table_2)
            report.set_table_dataframe(test_setup_)
            report.build_table()

        freq_option= None
        if self.more_option == "centre":
            freq_option = "Stay at centre freq for all Trials"
        elif self.more_option == "random":
            freq_option = "Stay at random frequency between the bandwidth for all trials"
        test_input_infor = {
            "Parameters": "Values",
            "LANforge ip": self.host,
            "LANforge port": self.port,
            "Radar Types": self.fcctypes,
            "Radar Hardware": "ct712",
            "Freq Channel Number": self.channel,
            "Desired Pass Percentage": str(self.desired_detection) + str("%"),
            "Max Number of extra trials": self.extra_trials,
            "Time interval between Trials (secs)": "2",
            "Run Traffic": False,
            "Frequency step option": freq_option,
            "Contact": "support@candelatech.com"
        }
        report.set_table_title("Test basic Information")
        report.build_table_title()
        report.test_setup_table(value="Information", test_setup_data=test_input_infor)

        report.build_footer()
        report.write_html()
        report.write_pdf_with_timestamp(_page_size='A4', _orientation='Landscape')



def main():
    desc = """ detection probability  test 
        
        """
    parser = argparse.ArgumentParser(
        prog=__file__,
        formatter_class=argparse.RawTextHelpFormatter,
        description=desc)

    parser.add_argument("--host", default='192.168.1.31',
                        help='specify the GUI ip to connect to')

    parser.add_argument("--port", default=8080, help="specify scripting port of LANforge")

    parser.add_argument('--ssid', type=str, help='ssid for client')

    parser.add_argument('--passwd', type=str, help='password to connect to ssid', default='[BLANK]')

    parser.add_argument('--security', type=str, help='security', default='open')

    parser.add_argument('--radio', type=str, help='radio at which client will be connected', default='1.1.wiphy1')

    parser.add_argument("--sniff_radio", default="1.1.wiphy0", help="radio at which wireshark will be started")

    parser.add_argument("--static", default=True, help="True if client will be created with static ip")

    parser.add_argument("--static_ip", default="192.168.2.100", help="if static option is True provide static ip to client")

    parser.add_argument("--ip_mask", default="255.255.255.0", help="if static is true provide ip mask to client")

    parser.add_argument("--gateway_ip", default="192.168.2.50", help="if static is true provide gateway ip")

    parser.add_argument('--upstream', type=str, help='provide eth1/eth2', default='eth1')

    parser.add_argument('--fcctypes', nargs="+",
                        default=["FCC0", "FCC1", "FCC2", "FCC3", "FCC4", "ETSI0", "ETSI1", "ETSI2", "ETSI3", "ETSI4",
                                 "ETSI5", "ETSI6", "Japan-W53-1","Japan-W56-2", "Japan-W56-3", "Japan-W56-4", "Japan-W56-5", "Japan-W56-6",
                                 "korea_1",  "korea_2",  "korea_3"],
                        help='types needed to be tested {FCC0/FCC1/FCC2/FCC3/FCC4/FCC5/ETSI1/ETSI2/ETSI3/ETSI4/ETSI5/ETSI6}')

    parser.add_argument('--channel', type=str, default="100",
                        help='channel options need to be tested {52, 56, 60, 64, 100, 104, 108, 112, 116, 120, 124 ,128, 132, 136, 140}')

    parser.add_argument("--enable_traffic", default=False, help="set to True if traffic needs to be added while testing")

    parser.add_argument("--trials", type=int, default=30, help="provide the number of trials you want to test default is 30")

    parser.add_argument("--desired_detection", type=int, default=80, help="provide the percentage value for desired detection eg 80, which means 80%")

    parser.add_argument("--extra_trials", type=int, default=0, help="provide the number of extra trials need to be performed if the test doesnot reach the expected"
                                                                    "or desired value")

    parser.add_argument("--more_option", default="centre", help="select from the list of more options "
                                                                             "which test you need to perform [shift, centre, random]")

    parser.add_argument("--time_int", default="0", help="provide time interval in seconds between each trials")



    args = parser.parse_args()
    obj = DfsTest(host=args.host,
                  port=args.port,
                  ssid=args.ssid,
                  passwd=args.passwd,
                  security=args.security,
                  radio=args.radio,
                  upstream=args.upstream,
                  fcctypes=args.fcctypes,
                  channel=args.channel,
                  sniff_radio = args.sniff_radio,
                  static = args.static,
                  static_ip = args.static_ip,
                  ip_mask = args.ip_mask,
                  gateway_ip = args.gateway_ip,
                  enable_traffic=args.enable_traffic,
                  desired_detection = args.desired_detection,
                  extra_trials = args.extra_trials,
                  more_option = args.more_option,
                  time_int = args.time_int,
                  trials = args.trials)
    obj.run()

if __name__ == '__main__':
    main()