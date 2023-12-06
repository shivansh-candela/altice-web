#!/usr/bin/env python3
"""
detection_probability_test.py
    --------------------

    Summary :
    ----------
    Detection Probability Test  is compilance to the Dynamic Frequency Selection(DFS) Regulation, it creates regulatory
    specified radar pulses to the DUT repeatedly to measure the probability of detection.

    execution: This script is executed in following way
    1. create a client on 5GHZ band
    2. check if the client is on expected DFS channel or not
    3. if not terminate the script
    4. if yes then it will start sniffer on client channel
    5. once the client is associated respective regulation radar is generated from hackrf
    6. stop sniffer
    7. check for csa frame
    8. report

    ############################################
    # Examples Commands for different scenarios
    ############################################

    --> for full test (all regulation)
       ./detection_probability_test.py  --host 192.168.1.31 --ssid Candela_20MHz --passwd [BLANK] --security open --trials 1   --more_option centre

    *** LEGACY MODE (older) ******

    --> FCC Regulation :

       Try to replace 0 IN FCC0 with 1, 2, 3, 4, 5 and 6

       ./detection_probability_test.py  --host 192.168.200.91 --ssid candelatest --passwd candelatest --security wpa2
       --sniff_radio 1.1.wiphy1 --radio 1.1.wiphy0 --fcctypes FCC0 --channel 52  --trials 1  --desired_detection 60
        --enable_traffic False --static False --more_option centre --bw 20 --lf_hackrf 30a28607 --legacy True

    --> ETSI Regulation

       From ETSI0 to ETSI6

       ./detection_probability_test.py  --host 192.168.200.91 --ssid candelatest --passwd candelatest --security wpa2
       --sniff_radio 1.1.wiphy1 --radio 1.1.wiphy0 --fcctypes ETSI0 --channel 52  --trials 1  --desired_detection 60
        --enable_traffic False --static False --more_option centre --bw 20 --lf_hackrf 30a28607 --legacy True

    --> JAPAN Regulation

       Japan-w53-1/6 and Japan-w56-1/6

       ./detection_probability_test.py  --host 192.168.200.91 --ssid candelatest --passwd candelatest --security wpa2
       --sniff_radio 1.1.wiphy1 --radio 1.1.wiphy0 --fcctypes Japan-w53-1 --channel 52  --trials 1  --desired_detection 60
        --enable_traffic False --static False --more_option centre --bw 20 --lf_hackrf 30a28607 --legacy True

    --> Korea Regulation

       coming soon...

    **** NON LEGACY MODE ****

    --> FCC Regulation

    Try to replace 0 IN FCC0 with 1, 2, 3, 4, 5 and 6

       ./detection_probability_test.py  --host 192.168.200.91 --ssid candelatest --passwd candelatest --security wpa2
       --sniff_radio 1.1.wiphy1 --radio 1.1.wiphy0 --fcctypes FCC0 --channel 52  --trials 1  --desired_detection 60
        --enable_traffic False --static False --more_option centre --bw 20 --lf_hackrf 30a28607 --legacy False

    --> ETSI Regulation

       From ETSI0 to ETSI6

       ./detection_probability_test.py  --host 192.168.200.91 --ssid candelatest --passwd candelatest --security wpa2
       --sniff_radio 1.1.wiphy1 --radio 1.1.wiphy0 --fcctypes ETSI0 --channel 52  --trials 1  --desired_detection 60
        --enable_traffic False --static False --more_option centre --bw 20 --lf_hackrf 30a28607 --legacy False

    --> JAPAN Regulation

       Japan-w53-1/6 and Japan-w56-1/6

       ./detection_probability_test.py  --host 192.168.200.91 --ssid candelatest --passwd candelatest --security wpa2
       --sniff_radio 1.1.wiphy1 --radio 1.1.wiphy0 --fcctypes Japan-w53-1 --channel 52  --trials 1  --desired_detection 60
        --enable_traffic False --static False --more_option centre --bw 20 --lf_hackrf 30a28607 --legacy False

    --> Korea Regulation
       coming soon...

    ===============================================================================
"""

import sys
import os
import logging
import importlib
import argparse
import datetime
import time
from datetime import datetime
import pandas as pd
import paramiko
import random
from dateutil import parser

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
                 trials=None,
                 ssh_password=None,
                 ssh_username=None,
                 traffic_type=None,
                 bandwidth=None,
                 ap_name=None,
                 lf_hackrf=None,
                 legacy=None,
                 create_client=None,
                 side_a_min_rate=None,
                 side_a_max_rate=None,
                 side_b_min_rate=None,
                 side_b_max_rate=None,
                 side_a_min_pdu=None,
                 side_b_min_pdu=None
                 ):
        super().__init__(lfclient_host=host,
                         lfclient_port=port)
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
        self.ssh_password = ssh_password
        self.ssh_username = ssh_username
        self.bandwidth = bandwidth
        self.traffic_type = traffic_type
        self.ap_name = ap_name
        self.legacy = legacy
        self.lf_hackrf = lf_hackrf
        self.pcap_name = None
        self.pcap_obj_2 = None
        self.staConnect = sta_connect.StaConnect2(self.host, self.port, outfile="staconnect2.csv")
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.pcap_obj = lf_pcap.LfPcap()
        self.cx_profile = self.new_l3_cx_profile() #create CX profile object
        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.create_client = create_client
        self.cx_profile.side_a_min_bps = side_a_min_rate
        self.cx_profile.side_a_max_bps = side_a_max_rate
        self.cx_profile.side_b_min_bps = side_b_min_rate
        self.cx_profile.side_b_max_bps = side_b_max_rate
        self.cx_profile.side_a_min_pdu = side_a_min_pdu
        self.cx_profile.side_b_min_pdu = side_b_min_pdu
        logging.basicConfig(filename='dpt.log', filemode='w', level=logging.INFO, force=True)
        if self.desired_detection < 60:
            print("please specify desired detection percentage value equal to or greater than the required percentage detection")
            exit(1)

    # get station list
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
                                                     radio=self.sniff_radio, channel=radio_channel,
                                                     monitor_name="monitor", channel_bw="20")
            self.pcap_obj_2.setup(0, 0, 0)
            self.pcap_obj_2.monitor.admin_up()
            print("Waiting until ports appear...")
            x = LFUtils.wait_until_ports_appear(base_url=f"http://{self.host}:{self.port}", port_list="monitor", debug=True, timeout=300)
            if x is True:
                print("monitor is up ")
                print("start sniffing")
                self.pcap_obj_2.monitor.start_sniff(capname=self.pcap_name, duration_sec=duration)
            else:
                print("some problem with monitor not being up")
                exit()
        elif self.more_option == "random":
            self.pcap_obj_2 = sniff_radio.SniffRadio(lfclient_host=self.host, lfclient_port=self.port,
                                                     radio=self.sniff_radio, channel=radio_channel,
                                                     monitor_name="monitor", channel_bw="20")
            self.pcap_obj_2.setup(1, 1, 1)
            self.pcap_obj_2.monitor.admin_up()
            print("Waiting until ports appear...")
            x = LFUtils.wait_until_ports_appear(base_url=f"http://{self.host}:{self.port}", port_list="monitor",
                                                debug=True, timeout=300)
            if x is True:
                print("monitor is up ")
                print("start sniffing")
                self.pcap_obj_2.monitor.start_sniff(capname=self.pcap_name, duration_sec=duration)
            else:
                print("some problem with monitor not being up")
                exit()


    # query station data like channel etc
    def station_data_query(self, station_name="wlan0", query="channel"):
        sta = station_name.split(".")
        url = f"/port/{sta[0]}/{sta[1]}/{sta[2]}?fields={query}"
        response = self.local_realm.json_get(_req_url=url)
        if (response is None) or ("interface" not in response):
            print("station_list: incomplete response:")
            logging.info("station_list: incomplete response:")
            exit(1)
        y = response["interface"][query]
        return y

    def pre_cleanup(self):
        self.cx_profile.cleanup()
        self.cx_profile.cleanup_prefix()

    # create a layer3 connection
    def create_layer3(self, traffic_type, sta_list):
        # checked
        logging.info("station list : " + str(sta_list))

        # create
        print("Creating endpoints")
        logging.info("Creating endpoints")
        self.cx_profile.create(endp_type=traffic_type, side_a=self.upstream,
                               side_b=sta_list, sleep_time=0)
        self.cx_profile.start_cx()

    def stop_l3(self):
        self.cx_profile.stop_cx()

    # create client
    def create_client_(self, start_id=0, sta_prefix="wlan", num_sta=1):
        local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        station_profile = local_realm.new_station_profile()
        sta_list = self.get_station_list()
        if not sta_list:
            print("no stations on lanforge")
            logging.info("no stations on lanforge")
        else:
            print("clean existing station")
            logging.info("clean existing station")
            station_profile.cleanup(sta_list, delay=1)
            LFUtils.wait_until_ports_disappear(base_url=local_realm.lfclient_url,
                                               port_list=sta_list,
                                               debug=True)
            print("pre cleanup done")
            logging.info("pre cleanup done")
        station_list = LFUtils.portNameSeries(prefix_=sta_prefix, start_id_=start_id,
                                              end_id_=num_sta - 1, padding_number_=10000,
                                              radio=self.radio)

        # Setting up static mac
        # https://candelatech.atlassian.net/browse/DFS-161
        station_profile.add_sta_data["mac"] = "a4:6b:b6:40:2f:54"

        station_profile.use_security(self.security, self.ssid, self.passwd)
        station_profile.set_number_template("00")

        station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        station_profile.set_command_flag("set_port", "rpt_timer", 1)
        print("Creating stations.")
        logging.info("Creating stations.")
        station_profile.create(radio=self.radio, sta_names_=station_list)

        print("Waiting for ports to appear")
        logging.info("Waiting for ports to appear")
        local_realm.wait_until_ports_appear(sta_list=station_list)
        station_profile.admin_up()
        print("Waiting for ports to admin up")
        logging.info("Waiting for ports to admin up")
        print(self.static)
        sta_list = self.get_station_list()

        if self.static == "True":
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
        logging.info("wait for ip")
        if local_realm.wait_for_ip(station_list):
            print("All stations got IPs")
            logging.info("All stations got IPs")
            if self.enable_traffic == "True":
                logging.info("create layer3 traffic")
                self.create_layer3(sta_list=sta_list, traffic_type=self.traffic_type)
        else:
            print("Stations failed to get IPs")
            logging.error("Stations failed to get IPs")
            exit(1)

    # this function is used for running hackrf script with different regulation inputs
    def run_hackrf(self, width=None, pri=None, count=None, freq=None, type=None, burst=None, trial_centre=None, trial_low=None,
                   trial_high=None, uut_channel=None, freq_modulatin=None, tx_sample_rate=None, prf_1=None, prf_2=None,
                   prf_3=None, blank_time=None,long_pulse_width=None, chirp_width=None,
                   prf=None,num_con_pair=None ):

        p = paramiko.SSHClient()
        p.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # This script doesn't work for me unless this line is added!
        p.connect(self.host, port=22, username=self.ssh_username, password=self.ssh_password)
        p.get_transport()

        # send frames
        # Execute the first command for scapy logic
        stdin, stdout, stderr = p.exec_command("sudo python scapy_frame.py", get_pty=True)
        stdin.write(str(self.ssh_password) + "\n")
        stdin.flush()
        # Print the output of the first command
        print(stdout.read().decode())
        # time.sleep(1)
        command = None
        if type == "fcc6":
            command = f"nice -19 sudo python3 lf_hackrf_dfs.py --tx_sample_rate 20 --radar_type FCC6,100 --one_burst --log_level debug --lf_hackrf {self.lf_hackrf}"
        if type == "fcc5":
            command = f"nice -19 sudo python3 lf_hackrf_dfs.py --freq {freq} --rf_type --one_burst FCC5,{burst},{trial_centre},{trial_low},{trial_high},{uut_channel},{freq_modulatin},{tx_sample_rate} --log_level debug --lf_hackrf {self.lf_hackrf}"
            print(command)
        if type == "etsi1" or type == "etsi2" or type == "etsi3" or type == "etsi4":
            if type == "etsi1":
                var = "ETSI1"
            if type == "etsi2":
                var = "ETSI2"
            if type == "etsi3":
                var = "ETSI3"
            if type == "etsi4":
                var = "ETSI4"
            command = f"nice -19 sudo python3 lf_hackrf_dfs.py --freq {freq} --rf_type {var},{width},{pri},20 --pulse_count {count} --one_burst --log_level debug --lf_hackrf {self.lf_hackrf}"
            print(command)
        if type == "etsi5" or type == "etsi6":
            if type == "etsi5":
                var = "ETSI5"
            if type == "etsi6":
                var = "ETSI6"
            command = f"nice -19 sudo python3 lf_hackrf_dfs.py --freq {freq} --radar_type {var},{width},{prf_1},{prf_2},{prf_3},20 --log_level debug --one_burst --lf_hackrf {self.lf_hackrf}"
            print(command)
        if type == "legacy":
            command = f"nice -19 sudo python3 lf_hackrf_dfs.py --pulse_width {width} --pulse_interval {pri} --pulse_count {count} --sweep_time 1000 --one_burst --freq {freq} --lf_hackrf {self.lf_hackrf}"
        if type == "legacy_w56-1":
            command = f"nice -19 python3 lf_hackrf_dfs.py --pulse_width {width} --pulse_interval {pri} --pulse_count {count} --tx_sample_rate 2 --sweep_time 1000 --freq {freq} --one_burst --lf_hackrf {self.lf_hackrf}"
        if type == "FCC0" or type == "FCC1" or type == "FCC2" or type == "FCC3" or type == "FCC4" or type == "KOREA" or type == "W56PULSE" or type == "ETSI0":
            if type == "ETSI0":
                command = f"nice -19 python3 lf_hackrf_dfs.py --rf_type {type},{width},{pri},20 --lf_hackrf {self.lf_hackrf} --freq {freq} --one_burst --log_level debug"
            else:
                command = f"nice -19 python3 lf_hackrf_dfs.py --rf_type {type},{width},{pri},{count},20 --lf_hackrf {self.lf_hackrf} --freq {freq} --one_burst --log_level debug"
        if type == "w53-3":
            command = f"nice -19 sudo python3 lf_hackrf_dfs.py --radar_type W53CHIRP,{width},{blank_time},{long_pulse_width},{chirp_width},{prf},{num_con_pair},{freq},20 --one_burst --lf_hackrf {self.lf_hackrf} --log_level debug "
            print(command)
        if type == "w53-1":
            command = f"nice -19 sudo python3 lf_hackrf_dfs.py --rf_type W53PULSE,{width},{prf},{count},20 --freq {freq} --one_burst --lf_hackrf {self.lf_hackrf} --log_level debug"
        # execute second command
        stdin, stdout, stderr = p.exec_command(str(command), get_pty=True)
        stdin.write(str(self.ssh_password) + "\n")
        stdin.flush()
        opt = stdout.readlines()
        opt = "".join(opt)
        print(opt)
        logging.info(opt)
        p.close()

    # stop sniffing
    def stop_sniffer(self):
        print(" stop_sniffer")
        logging.info(" stop_sniffer")
        directory = None
        directory_name = "pcap"
        if directory_name:
            directory = os.path.join("", str(directory_name))
        try:
            if not os.path.exists(directory):
                os.mkdir(directory)
        except Exception as x:
            print(x)
            logging.warning(str(x))

        self.pcap_obj_2.monitor.admin_down()
        self.pcap_obj_2.cleanup()
        lf_report.pull_reports(hostname=self.host, port=22, username=self.ssh_username,
                               password=self.ssh_password,
                               report_location="/home/lanforge/" + self.pcap_name,
                               report_dir="pcap")
        return self.pcap_name

    # a function used for certain value calculation search for its use
    def select_values(self, n, fcc):
        if fcc == "etsi5":
            while True:
                prf_1 = random.randint(300, 400)
                prf_2 = prf_1 + random.randint(20, 50)
                prf_3 = prf_2 + random.randint(20, 50)
                diff_1 = prf_2 - prf_1
                diff_2 = prf_3 - prf_2
                diff_3 = prf_3 - prf_1
                if n == 3:
                    if (300 <= prf_2 <= 400) and (diff_1 in range(20, 50)):
                        if (300 <= prf_3 <= 400) and (diff_2 in range(20, 50)) and (diff_3 in range(20, 50)):
                            return prf_1, prf_2, prf_3
                elif n == 2:
                    if 300 <= prf_2 <= 400:
                        return prf_1, prf_2
        if fcc == "etsi6":
            while True:
                prf_1 = random.randint(400, 1200)
                prf_2 = prf_1 + random.randint(80, 400)
                prf_3 = prf_2 + random.randint(80, 400)
                diff_1 = prf_2 - prf_1
                diff_2 = prf_3 - prf_2
                diff_3 = prf_3 - prf_1
                if n == 3:
                    if (400 <= prf_2 <= 1200) and (diff_1 in range(80, 400)):
                        if (400 <= prf_3 <= 1200) and (diff_2 in range(80, 400)) and (diff_3 in range(80, 400)):
                            return prf_1, prf_2, prf_3
                elif n == 2:
                    if 400 <= prf_2 <= 1200:
                        return prf_1, prf_2

    # main logic used for passing correct value to run hackrf function with respect to regulations
    def main_logic(self, bssid=None):
        main_dict = dict.fromkeys(self.fcctypes)
        print(main_dict)
        logging.info(str(main_dict))
        list_ = []
        for i in range(self.trials + self.extra_trials):
            var = 000
            var_1 = "Trial_" + str(var + i + 1)
            list_.append(var_1)
        sec_dict = dict.fromkeys(list_)
        for i in main_dict:
            main_dict[i] = sec_dict.copy()
        print(main_dict)
        logging.info(str(main_dict))
        width_, interval_, count_ , burst_, trial_centre, trial_low, trial_high, uut_channel, freq_modulatin, tx_sample_rate, prf_1_, prf_2_, prf_3_  = "", "", "", "", "", "", "","", "", "", "", "", ""
        blank_time, long_pulse_width, chirp_width, prf, num_con_pair = "", "", "", "", ""
        fcc1_list = None
        if "FCC1" in self.fcctypes:
            random1 = [518, 538, 558, 578, 598, 618, 638, 658, 678, 698, 718, 738, 758, 778, 798, 818, 838, 858, 878,
                       898, 918, 938, 3066]
            pri1 = random.sample(random1, 15)
            print(pri1)
            print(len(pri1))

            pri2 = []
            for i in range(100):
                randomly = int(random.randint(518, 3066))
                if randomly in pri1:
                    print("ignore")
                else:
                    pri2.append(randomly)
                if len(pri2) >= 15:
                    break
                else:
                    continue
            print(pri2)
            print(len(pri2))
            pri1.extend(pri2)
            print(pri1)
            print(len(pri1))
            fcc1_list = pri1
        print("fcc1_list", fcc1_list)

        for fcc in self.fcctypes:
            for tria in range(self.trials + self.extra_trials):
                print("tria", tria)
                logging.info(str(tria))
                time.sleep(int(self.time_int))
                var = 000
                var_1 = "Trial_" + str(var + tria + 1)
                if fcc == "FCC5":
                    time.sleep(25)
                    new_list = ["Burst", "Trial Centre", "Trial Low", "Trial High","UUT Channel",  "Frequency Modulating", "Tx sample rate", "Detected", "Frequency(KHz)",
                                "Detection Time(sec)"]
                if fcc == "ETSI5" or fcc == "ETSI6":
                    new_list = ["Burst", "prf_1", "prf_2", "prf_3", "Width", "Pulses",   "Detected", "Frequency(KHz)",
                                "Detection Time(sec)"]
                if (fcc == "Japan-w53-3" or fcc == "Japan-w53-4" or fcc == "Japan-w53-5" or fcc == "Japan-w53-6"
                        or fcc == "Japan-w53-7" or fcc ==  "Japan-w53-8"):
                    new_list = ["Burst", "Frequency(KHz)", "Pulse Width", "Blank Time(us)", "Long Pulse Width(us)",
                                "Chirp Width(MHz)", "Pri(Hz)", "No of Continuous Pairs of Pulses", "Detection Time(sec)"]
                if fcc == "Japan-w53-1" or fcc == "Japan-w53-2":
                    new_list = ["Pulses", "Width", "PRF(Hz)", "Detected", "Frequency(KHz)",
                                "Detection Time(sec)"]
                else:
                    new_list = ["Burst", "Pulses", "Width", "PRI(US)", "Detected", "Frequency(KHz)", "Detection Time(sec)"]
                third_dict = dict.fromkeys(new_list)
                main_dict[fcc][var_1] = third_dict.copy()
                print("result data", main_dict)
                logging.info("result data" + str(main_dict))
                # standard = {"FCC0": {"width_": "1", "interval_": "1428", "count_": "18"}, "FCC1": {}}

                if fcc == "FCC0":
                    width_ = "1"
                    interval_ = "1428"
                    count_ = "18"
                elif fcc == "FCC1":
                    if self.trials < 30:
                        print("since given trials are less than 30 TestB is considered")
                        logging.info("since given trials are less than 30 TestB is considered")
                        width_ = "1"
                        interval_ = str(random.randint(518, 3066))
                        formula = ((1 * 19 * 1000000) / (360 * int(interval_)))
                        print(formula)
                        count_ = str(int(formula) + 1)
                        print(count_)
                    else:
                        print("since given trials are greater than or equal to  30 both TestA and TestB is considered")
                        logging.info("since given trials are greater than or equal to  30 both TEstA andTestB is considered")
                        width_ = "1"
                        if tria > 30:
                            interval_ = str(random.randint(518, 3066))
                            formula = ((1 * 19 * 1000000) / (360 * int(interval_)))
                            count_ = str(int(formula)+1)
                        else:
                            interval_1 = fcc1_list[tria]
                            interval_ = str(fcc1_list[tria])
                            formula = ((1 * 19 * 1000000) / (360 * interval_1))
                            count_ = str(int(formula) + 1)
                            print(count_)
                elif fcc == "FCC2":
                    fcc_ra  = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0]
                    width_ = str(random.choice(fcc_ra))
                    interval_ = str(random.randint(150, 230))
                    count_ = str(random.randint(23, 29))
                elif fcc == "FCC3":
                    width_ = str(random.randint(6, 10))
                    interval_ = str(random.randint(200, 500))
                    count_ = str(random.randint(16, 18))
                elif fcc == "FCC4":
                    fcc_ra = [11.0, 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7, 11.8, 11.9,12.0, 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8, 12.9,13.0, 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 13.7, 13.8, 13.9,14.0, 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7, 14.8, 14.9,15.0, 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7, 15.8, 15.9,16.0, 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 16.8, 16.9,17.0, 17.1, 17.2, 17.3, 17.4, 17.5, 17.6, 17.7, 17.8, 17.9,18.0, 18.1, 18.2, 18.3, 18.4, 18.5, 18.6, 18.7, 18.8, 18.9,19.0, 19.1, 19.2, 19.3, 19.4, 19.5, 19.6, 19.7, 19.8, 19.9, 20.0]
                    width_ = str(random.choice(fcc_ra))
                    interval_ = str(random.randint(200, 500))
                    count_ = str(random.randint(12, 16))
                elif fcc == "FCC5":
                    if tria in range(0,10):
                        print(tria)
                        trial_centre = str(1)
                        trial_low = str(0)
                        trial_high = str(0)
                    if tria in range(10,20):
                        print(tria)
                        trial_centre = str(0)
                        trial_low = str(1)
                        trial_high = str(0)
                    if tria in range(20, 31):
                        print(tria)
                        trial_centre = str(0)
                        trial_low = str(0)
                        trial_high = str(1)
                    burst_ = str(random.randint(8, 20))
                    # trial_low = str(1)
                    # trial_high= str(1)
                    uut_channel = str(self.bandwidth)
                    freq_modulatin = str(random.randint(5, 20))
                    tx_sample_rate = str(20)
                elif fcc == "FCC6":
                    width_ = "1"
                    interval_ = "333"
                    count_ = "9"
                elif fcc == "ETSI0":
                    if self.legacy == "True":
                        width_ = "1"
                        interval_ = "1429"
                        count_ = "18"
                    else:
                        width_ = "1"
                        interval_ = "700"
                        count_ = "18"
                elif fcc == "ETSI1":
                    if self.legacy == "True":
                        width_ = str(random.randint(1, 5))
                        interval_ = str(random.randint(1000, 5000))
                        count_ = "10"
                    else:
                        etsi1_width_range = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0]
                        random_number = random.choice(etsi1_width_range)
                        width_ = random_number
                        interval_ = str(random.randint(200, 1000))
                        tx_sample_rate = "8"
                        count_ = "10"
                elif fcc == "ETSI2":
                    if self.legacy == "True":
                        width_ = str(random.randint(1, 15))
                        interval_ = str(random.randint(625, 5000))
                        count_ = "15"
                    else:
                        etsi2_width_range = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9.0, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 10.0, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9, 11.0, 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7, 11.8, 11.9, 12.0, 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8, 12.9, 13.0, 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 13.7, 13.8, 13.9, 14.0, 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7, 14.8, 14.9, 15.0]
                        random_number = random.choice(etsi2_width_range)
                        width_ = random_number
                        interval_ = str(random.randint(200, 1600))
                        tx_sample_rate = "8"
                        count_ = "15"
                elif fcc == "ETSI3":
                    if self.legacy == "True":
                        width_ = str(random.randint(1, 15))
                        interval_ = str(random.randint(250, 435))
                        count_ = "25"
                    else:
                        etsi3_width_range = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9,
                                             2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4,
                                             3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9,
                                             5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4,
                                             6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9,
                                             8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9.0, 9.1, 9.2, 9.3, 9.4,
                                             9.5, 9.6, 9.7, 9.8, 9.9, 10.0, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7,
                                             10.8, 10.9, 11.0, 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7, 11.8, 11.9,
                                             12.0, 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8, 12.9, 13.0, 13.1,
                                             13.2, 13.3, 13.4, 13.5, 13.6, 13.7, 13.8, 13.9, 14.0, 14.1, 14.2, 14.3,
                                             14.4, 14.5, 14.6, 14.7, 14.8, 14.9, 15.0]
                        random_number = random.choice(etsi3_width_range)
                        width_ = random_number
                        interval_ = str(random.randint(2300, 4000))
                        tx_sample_rate = "8"
                        count_ = "25"
                elif fcc == "ETSI4":
                    width_ = str(random.randint(20, 30))
                    interval_ = str(random.randint(2000, 4000))
                    count_ = "20"
                elif fcc == "ETSI5":
                    if self.legacy == "True":
                        width_ = str(random.randint(1, 2))
                        interval_ = str(random.randint(2500, 3333))
                        count_ = "10"
                    else:
                        etsi5_pulse_width_range = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9,2.0]
                        random_number = random.choice(etsi5_pulse_width_range)
                        width_ = str(random_number)
                        pulse_burst = random.randint(2, 3)
                        if pulse_burst == 2:
                            count_ = "20"
                            prf_1, prf_2 = self.select_values(n=2, fcc="etsi5")
                            print(f"prf_1: {prf_1}")
                            print(f"prf_2: {prf_2}")
                            prf_3 = 0

                        elif pulse_burst == 3:
                            count_ = "30"
                            prf_1, prf_2, prf_3 = self.select_values(n=3, fcc="etsi5")
                            print(f"prf_1: {prf_1}")
                            print(f"prf_2: {prf_2}")
                            print(f"prf_3: {prf_3}")

                        prf_1_ = prf_1
                        prf_2_ = prf_2
                        prf_3_ = prf_3
                        burst_ = pulse_burst

                elif fcc == "ETSI6":
                    if self.legacy == "True":
                        width_ = str(random.randint(1, 2))
                        interval_ = str(random.randint(833, 2500))
                        count_ = "15"
                    else:
                        etsi6_pulse_width_range = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8,
                                                   1.9, 2.0]
                        random_number = random.choice(etsi6_pulse_width_range)
                        width_ = str(random_number)
                        pulse_burst = random.randint(2, 3)
                        if pulse_burst == 2:
                            count_ = "30"
                            prf_1, prf_2 = self.select_values(n=2, fcc="etsi6")
                            print(f"prf_1: {prf_1}")
                            print(f"prf_2: {prf_2}")
                            prf_3 = 0

                        elif pulse_burst == 3:
                            count_ = "45"
                            prf_1, prf_2, prf_3 = self.select_values(n=3, fcc="etsi6")
                            print(f"prf_1: {prf_1}")
                            print(f"prf_2: {prf_2}")
                            print(f"prf_3: {prf_3}")

                        prf_1_ = prf_1
                        prf_2_ = prf_2
                        prf_3_ = prf_3
                        burst_ = pulse_burst

                elif fcc == "Japan-w53-1":
                    w53 = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
                           2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6,
                           3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0]
                    random_number = random.choice(w53)
                    width_ = random_number
                    prf = random.randint(200, 1000)
                    count_ = random.randint(10, 40)
                    tx_sample_rate = 20
                elif fcc == "Japan-w53-2":
                    w53 = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
                                         2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6,
                                         3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2,
                                         5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8,
                                         6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4,
                                         8.5, 8.6, 8.7, 8.8, 8.9, 9.0, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9,
                                         10.0, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9, 11.0, 11.1, 11.2,
                                         11.3, 11.4, 11.5, 11.6, 11.7, 11.8, 11.9, 12.0, 12.1, 12.2, 12.3, 12.4, 12.5,
                                         12.6, 12.7, 12.8, 12.9, 13.0, 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 13.7, 13.8,
                                         13.9, 14.0, 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7, 14.8, 14.9, 15.0]

                    random_number = random.choice(w53)
                    width_ = random_number
                    prf = random.randint(200, 1600)
                    count_ = random.randint(15, 40)
                    tx_sample_rate = 20
                elif (fcc == "Japan-w53-3" or fcc == "Japan-w53-4" or fcc == "Japan-w53-5" or fcc == "Japan-w53-6"
                      or fcc == "Japan-w53-7" or fcc == "Japan-w53-8"):
                    if fcc == "Japan-w53-5" or fcc == "Japan-w53-6" or fcc == "Japan-w53-7" or fcc == "Japan-w53-8":
                        w53__width_range = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
                        random_number = random.choice(w53__width_range)
                        width_ = random_number
                        blank_time = random.randint(50, 240)
                        long_pulse_width = random.randint(30, 32)

                        if fcc == "Japan-w53-5":
                            prf = random.randint(1114, 1118)
                            num_con_pair = random.randint(30, 40)
                        elif fcc == "Japan-w53-6":
                            prf = random.randint(928, 932)
                            num_con_pair = random.randint(25, 40)
                        elif fcc == "Japan-w53-7":
                            prf = random.randint(886, 890)
                            num_con_pair = random.randint(24, 40)
                        elif fcc == "Japan-w53-8":
                            prf = random.randint(738, 742)
                            num_con_pair = random.randint(20, 40)

                    else:
                        w53_3_width_range = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
                                             2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6,
                                             3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0]
                        random_number = random.choice(w53_3_width_range)
                        width_ = random_number
                        blank_time = random.randint(70, 120)
                        long_pulse_width = random.randint(20, 110)
                    if fcc == "Japan-w53-4":
                        prf = random.randint(200, 1600)
                        num_con_pair = random.randint(int(min(max(22, (0.026 * prf)), 30)), 40)
                    elif fcc == "Japan-w53-3":
                        prf = random.randint(200, 1000)
                        num_con_pair = random.randint(int(min(max(22, (0.026 * prf)), 30)), 40)
                    chirp_width_range = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
                    chirp_width = random.choice(chirp_width_range)
                    tx_sample_rate = "20"
                elif fcc == "korea_1":
                    if self.legacy == "True":
                        width_ = 1
                        interval_ = 1429
                        count_ = 18
                    else:
                        width_ = 1
                        interval_ = 700
                        count_ = 18
                elif fcc == "korea_2":
                    if self.legacy == "True":
                        width_ = 1
                        interval_ = 556
                        count_ = 10
                    else:
                        width_ = 1
                        interval_ = 1800
                        count_ = 10
                elif fcc == "korea_3":
                    if self.legacy == "True":
                        width_ = 2
                        interval_ = 3030
                        count_ = 70
                    else:
                        width_ = 2
                        interval_ = 330
                        count_ = 70
                elif fcc == "Japan-w56-1":
                    if self.legacy == "True":
                        width_ = 0.5
                        interval_ = 1389 #This is PRI, i.e. PRI = 1389
                        count_ = 18
                    else:
                        width_ = 0.5
                        interval_ = 720 #This is PRF, i.e. PRF = 720
                        count_ = 18
                elif fcc == "Japan-w56-2":
                    if self.legacy == "True":
                        width_ = 1
                        interval_ = 1429
                        count_ = 18
                    else:
                        width_ = 1
                        interval_ = 700
                        count_ = 18
                elif fcc == "Japan-w56-3":
                    if self.legacy == "True":
                        width_ = 2
                        interval_ = 4000
                        count_ = 18
                    else:
                        width_ = 2
                        interval_ = 250
                        count_ = 18
                elif fcc == "Japan-w56-4":
                    if self.legacy == "True":
                        width_ = str(random.randint(1, 5))
                        interval_ = str(random.randint(150, 230))
                        count_ = str(random.randint(23, 29))
                    else:
                        w53_3_width_range = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
                                             2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5,
                                             3.6,
                                             3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0]
                        random_number = random.choice(w53_3_width_range)
                        width_ = random_number
                        interval_ = random.randint(4347, 6667)
                        count_ = random.randint(23, 29)
                elif fcc == "Japan-w56-5":
                    if self.legacy == "True":
                        width_ = str(random.randint(6, 10))
                        interval_ = str(random.randint(200, 500))
                        count_ = str(random.randint(16, 18))
                    else:
                        w53_3_width_range = [6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9.0, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 10.0]
                        random_number = random.choice(w53_3_width_range)
                        width_ = random_number
                        interval_ = random.randint(2000, 5000)
                        count_ = random.randint(16, 18)
                elif fcc == "Japan-w56-6":
                    if self.legacy == "True":
                        width_ = str(random.randint(11, 20))
                        interval_ = str(random.randint(200, 500))
                        count_ = str(random.randint(12, 16))
                    else:
                        w53_3_width_range = [11.0, 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7, 11.8, 11.9,
                                            12.0, 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8, 12.9,
                                            13.0, 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 13.7, 13.8, 13.9,
                                            14.0, 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7, 14.8, 14.9,
                                            15.0, 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7, 15.8, 15.9,
                                            16.0, 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 16.8, 16.9,
                                            17.0, 17.1, 17.2, 17.3, 17.4, 17.5, 17.6, 17.7, 17.8, 17.9,
                                            18.0, 18.1, 18.2, 18.3, 18.4, 18.5, 18.6, 18.7, 18.8, 18.9,
                                            19.0, 19.1, 19.2, 19.3, 19.4, 19.5, 19.6, 19.7, 19.8, 19.9,
                                            20.0]
                        random_number = random.choice(w53_3_width_range)
                        width_ = random_number
                        interval_ = random.randint(2000, 5000)
                        count_ = random.randint(12, 16)
                if fcc == "FCC5":
                    print(burst_)
                    main_dict[fcc][var_1]["Burst"] = burst_
                    main_dict[fcc][var_1]["Trial Centre"] = trial_centre
                    main_dict[fcc][var_1]["Trial Low"] = trial_low
                    main_dict[fcc][var_1]["Trial High"] = trial_high
                    main_dict[fcc][var_1]["UUT Channel"] = uut_channel
                    main_dict[fcc][var_1]["Frequency Modulating"] = freq_modulatin
                    main_dict[fcc][var_1]["Tx sample rate"] = tx_sample_rate
                if fcc == "FCC6":
                    main_dict[fcc][var_1]["Burst"] = "100"
                    main_dict[fcc][var_1]["Pulses"] = count_
                    main_dict[fcc][var_1]["Width"] = width_
                    main_dict[fcc][var_1]["PRI(US)"] = interval_
                if (fcc == "FCC0" or fcc == "FCC1" or fcc == "FCC2" or fcc == "FCC3" or fcc == "FCC4"
                        or fcc == "ETSI0" or fcc == "ETSI1"or fcc == "ETSI2" or fcc == "ETSI3" or fcc == "ETSI4"
                        or fcc == "Japan-w56-1" or fcc == "Japan-w56-2" or fcc == "Japan-w56-3"or fcc == "Japan-w56-4" or fcc == "Japan-w56-5" or fcc == "Japan-w56-6"
                        or fcc == "korea_1" or fcc == "korea_2" or fcc == "korea_3"
                ):
                    main_dict[fcc][var_1]["Burst"] = "1"
                    main_dict[fcc][var_1]["Pulses"] = count_
                    main_dict[fcc][var_1]["Width"] = width_
                    main_dict[fcc][var_1]["PRI(US)"] = interval_
                if fcc == "ETSI5" or fcc == "ETSI6":
                    main_dict[fcc][var_1]["Burst"] = burst_
                    main_dict[fcc][var_1]["Pulses"] = count_
                    main_dict[fcc][var_1]["Width"] = width_
                    main_dict[fcc][var_1]["prf_1"] = prf_1_
                    main_dict[fcc][var_1]["prf_2"] = prf_2_
                    main_dict[fcc][var_1]["prf_3"] = prf_3_
                if fcc == "Japan-w53-3" or fcc == "Japan-w53-4" or fcc == "Japan-w53-5" or fcc == "Japan-w53-6" or fcc == "Japan-w53-7" or fcc == "Japan-w53-8":
                    main_dict[fcc][var_1]["Burst"] = "1"
                    main_dict[fcc][var_1]["Width"] = width_
                    main_dict[fcc][var_1]["Blank Time(us)"] = blank_time
                    main_dict[fcc][var_1]["Long Pulse Width(us)"] = long_pulse_width
                    main_dict[fcc][var_1]["Chirp Width(MHz)"] = chirp_width
                    main_dict[fcc][var_1]["Pri(Hz)"] = prf
                    main_dict[fcc][var_1]["No of Continuous Pairs of Pulses"] = num_con_pair
                if fcc == "Japan-w53-1" or fcc == "Japan-w53-2":
                    main_dict[fcc][var_1]["Width"] = width_
                    main_dict[fcc][var_1]["Pulses"] = count_
                    main_dict[fcc][var_1]["PRF(Hz)"] = prf

                if self.more_option == "centre":
                    if self.bandwidth == "20":
                        frequency = {"52": "5260000", "56": "5280000", "60": "5300000", "64": "5320000",
                                     "100": "5500000",
                                     "104": "5520000", "108": "5540000", "112": "5560000", "116": "5580000",
                                     "120": "5600000",
                                     "124": "5620000",
                                     "128": "5640000", "132": "5660000", "136": "5680000", "140": "5700000",
                                     "144": "5720000"}

                    elif self.bandwidth == "40":
                        frequency = {"52": "5270000", "54": "5270000", "56": "5270000", "60": "5310000",
                                     "62": "5310000", "64": "5310000",
                                     "100": "5510000", "102": "5510000",
                                     "104": "5510000", "108": "5550000", "110": "5550000",
                                     "112": "5550000", "116": "5590000", "118": "5590000",
                                     "120": "5590000", "124": "5630000", "126": "5630000",
                                     "128": "5630000", "132": "5670000", "134": "5670000",
                                     "136": "5670000", "140": "5710000", "142": "5710000",
                                     "144": "5710000"}

                    elif self.bandwidth == "80":
                        frequency = {"52": "5290000", "54": "5290000", "56": "5290000", "58": "5290000",
                                     "60": "5290000", "62": "5290000", "64": "5290000",
                                     "100": "5530000", "102": "5530000", "104": "5530000", "106": "5530000",
                                     "108": "5530000", "110": "5530000",
                                     "112": "5530000", "116": "5610000", "118": "5610000",
                                     "120": "5610000", "122": "5610000", "124": "5610000", "126": "5610000",
                                     "128": "5610000", "132": "5690000", "134": "5690000",
                                     "136": "5690000", "138": "5690000", "140": "5690000", "142": "5690000",
                                     "144": "5690000"}

                    elif self.bandwidth == "160":
                        frequency = {"36": "5250000", "40": "5250000", "44": "5250000", "48": "5250000",
                                     "52": "5250000", "56": "5250000", "60": "5250000",
                                     "64": "5250000", "100": "5570000", "104": "5570000", "108": "5570000",
                                     "112": "5570000", "116": "5570000", "120": "5570000", "124": "5570000",
                                     "128": "5570000"}

                if self.more_option == "random":
                    if self.bandwidth == "20":

                        frequency = {"52": str(random.randint(5250, 5270)), "54": str(random.randint(5250, 5290)),
                                     "56": str(random.randint(5270, 5290)), "58": str(random.randint(5250, 5330)),
                                     "60": str(random.randint(5290, 5310)), "62": str(random.randint(5290, 5330)),
                                     "64": str(random.randint(5310, 5330)), "100": str(random.randint(5490, 5510)),
                                     "102": str(random.randint(5490, 5530)), "104": str(random.randint(5510, 5530)),
                                     "108": str(random.randint(5530, 5550)), "110": str(random.randint(5530, 5570)),
                                     "112": str(random.randint(5550, 5570)), "116": str(random.randint(5570, 5590)),
                                     "118": str(random.randint(5570, 5610)), "122": str(random.randint(5570, 5650)),
                                     "120": str(random.randint(5590, 5610)),
                                     "124": str(random.randint(5610, 5630)), "126": str(random.randint(5610, 5650)),
                                     "128": str(random.randint(5630, 5650)), "132": str(random.randint(5650, 5670)),
                                     "134": str(random.randint(5650, 5690)),
                                     "136": str(random.randint(5670, 5690)), "138": str(random.randint(5650, 5730)),
                                     "140": str(random.randint(5690, 5710)), "144": str(random.randint(5710, 5730))}

                    elif self.bandwidth == "40":
                        frequency = {"52": str(random.randint(5250, 5290)), "54": str(random.randint(5250, 5290)),
                                     "56": str(random.randint(5250, 5290)), "58": str(random.randint(5250, 5330)),
                                     "60": str(random.randint(5290, 5330)), "62": str(random.randint(5290, 5330)),
                                     "64": str(random.randint(5290, 5330)), "100": str(random.randint(5490, 5530)),
                                     "102": str(random.randint(5490, 5530)), "104": str(random.randint(5490, 5530)),
                                     "108": str(random.randint(5530, 5570)), "110": str(random.randint(5530, 5570)),
                                     "112": str(random.randint(5530, 5570)), "116": str(random.randint(5570, 5610)),
                                     "118": str(random.randint(5570, 5610)), "122": str(random.randint(5570, 5650)),
                                     "120": str(random.randint(5570, 5610)),
                                     "124": str(random.randint(5610, 5650)), "126": str(random.randint(5610, 5650)),
                                     "128": str(random.randint(5610, 5650)), "132": str(random.randint(5650, 5690)),
                                     "134": str(random.randint(5650, 5690)),
                                     "136": str(random.randint(5650, 5690)),
                                     "140": str(random.randint(5690, 5730)), "144": str(random.randint(5690, 5730))}

                    elif self.bandwidth == "80":
                        frequency = {"52": str(random.randint(5250, 5330)), "54": str(random.randint(5250, 5330)),
                                     "56": str(random.randint(5250, 5330)), "58": str(random.randint(5250, 5330)),
                                     "60": str(random.randint(5250, 5330)), "62": str(random.randint(5250, 5330)),
                                     "64": str(random.randint(5250, 5330)), "100": str(random.randint(5490, 5570)),
                                     "102": str(random.randint(5490, 5570)), "104": str(random.randint(5490, 5570)),
                                     "108": str(random.randint(5490, 5570)), "110": str(random.randint(5490, 5570)),
                                     "112": str(random.randint(5490, 5570)), "116": str(random.randint(5570, 5650)),
                                     "118": str(random.randint(5570, 5650)), "122": str(random.randint(5570, 5650)),
                                     "120": str(random.randint(5570, 5650)),
                                     "124": str(random.randint(5570, 5650)), "126": str(random.randint(5570, 5650)),
                                     "128": str(random.randint(5570, 5650)), "132": str(random.randint(5650, 5730)),
                                     "134": str(random.randint(5650, 5730)),
                                     "136": str(random.randint(5650, 5730)), "138": str(random.randint(5650, 5730)),
                                     "140": str(random.randint(5650, 5730)), "144": str(random.randint(5650, 5730))}

                    elif self.bandwidth == "160":
                        frequency = {"36": str(random.randint(5250, 5350)), "40": str(random.randint(5250, 5350)),
                                     "44": str(random.randint(5250, 5350)), "48": str(random.randint(5250, 5350)),
                                     "52": str(random.randint(5250, 5350)), "56": str(random.randint(5250, 5350)),
                                     "60": str(random.randint(5250, 5350)), "64": str(random.randint(5250, 5350)),
                                     "100": str(random.randint(5490, 5650)), "104": str(random.randint(5490, 5650)),
                                     "108": str(random.randint(5490, 5650)), "112": str(random.randint(5490, 5650)),
                                     "116": str(random.randint(5490, 5650)), "120": str(random.randint(5490, 5650)),
                                     "124": str(random.randint(5490, 5650)), "128": str(random.randint(5490, 5650))}

                print(str(int(frequency[str(self.channel)]) * 1000))
                if self.more_option == "centre":
                    main_dict[fcc][var_1]["Frequency(KHz)"] = str(frequency[str(self.channel)])
                elif self.more_option == "random":
                    main_dict[fcc][var_1]["Frequency(KHz)"] = str(int(frequency[str(self.channel)]) * 1000)

                print("starting sniffer")
                logging.info("starting sniffer")
                self.start_sniffer(radio_channel=self.channel, radio=self.sniff_radio,
                                   test_name="dfs_csa_" + str(fcc) + "_" + str(var_1) + "_channel" + str(
                                       self.channel) + "_")
                time.sleep(1)
                print("generate radar")
                logging.info("generate radar")

                if self.more_option == "centre":
                    if fcc == "FCC6":
                        self.run_hackrf(type="fcc6", freq=str(frequency[str(self.channel)]))
                    # else:
                    #     self.run_hackrf(width=width_, pri=interval_, count=count_, freq=str(frequency[str(self.channel)]))
                    if fcc == "FCC5":
                        self.run_hackrf(type="fcc5", freq=str(frequency[str(self.channel)]), burst=burst_, trial_centre=trial_centre, trial_low=trial_low,
                                        trial_high=trial_high, uut_channel=uut_channel, freq_modulatin=freq_modulatin, tx_sample_rate=tx_sample_rate)
                    if fcc == "FCC0" or fcc == "FCC1" or fcc == "FCC2" or fcc == "FCC3" or fcc == "FCC4" or fcc == "ETSI0" or fcc == "ETSI1" or fcc == "ETSI2" or fcc == "ETSI3" or fcc == "ETSI4"\
                            or fcc == "korea_1" or fcc == "korea_2"  or fcc == "korea_3":
                        if self.legacy == "True":
                            self.run_hackrf(type="legacy", width=width_, pri=interval_, count=count_, freq=str(frequency[str(self.channel)]))
                        else:
                            if fcc == "FCC0":
                                var = "FCC0"
                            if fcc == "FCC1":
                                var = "FCC1"
                            if fcc == "FCC2":
                                var = "FCC2"
                            if fcc == "FCC3":
                                var = "FCC3"
                            if fcc == "FCC4":
                                var = "FCC4"
                            if fcc == "korea_1" or fcc == "korea_2" or fcc == "korea_3":
                                var = "KOREA"
                            if fcc == "ETSI0":
                                var =  "ETSI0"
                            if fcc == "ETSI1":
                                var = "etsi1"
                            if fcc == "ETSI2":
                                var = "etsi2"
                            if fcc == "ETSI3":
                                var = "etsi3"
                            if fcc == "ETSI4":
                                var = "etsi4"
                            self.run_hackrf(type=var, width=width_, pri=interval_, count=count_,
                                                freq=str(frequency[str(self.channel)]))

                    if fcc == "ETSI5" or fcc == "ETSI6":
                        if fcc == "ETSI5":
                            self.run_hackrf(type="etsi5", width=width_, prf_1=prf_1_, prf_2 = prf_2_, prf_3 = prf_3_,
                                        freq=str(frequency[str(self.channel)]), count=count_)
                        if fcc == "ETSI6":
                            self.run_hackrf(type="etsi6", width=width_, prf_1=prf_1_, prf_2=prf_2_, prf_3=prf_3_,
                                            freq=str(frequency[str(self.channel)]), count=count_)
                    if fcc == "Japan-w53-3" or fcc == "Japan-w53-4" or fcc == "Japan-w53-5" or fcc == "Japan-w53-6" or fcc ==  "Japan-w53-7" or fcc == "Japan-w53-8":
                        self.run_hackrf(type="w53-3", width=width_, blank_time=blank_time,
                                        long_pulse_width=long_pulse_width, chirp_width=chirp_width,
                                        prf=prf, num_con_pair=num_con_pair,
                                        freq=str(frequency[str(self.channel)])[:4])
                    if fcc == "Japan-w53-1" or fcc == "Japan-w53-2":
                        self.run_hackrf(type="w53-1", width=width_, prf=prf, count=count_,
                                        freq=str(frequency[str(self.channel)]))
                    if fcc == "Japan-w56-1" or fcc == "Japan-w56-2" or fcc == "Japan-w56-3" or fcc == "Japan-w56-4" or fcc == "Japan-w56-5" or fcc == "Japan-w56-6":
                        if self.legacy == "True":
                            if fcc == "Japan-w56-1":
                                self.run_hackrf(type="legacy_w56-1", width=width_, pri=interval_, count=count_, freq=str(frequency[str(self.channel)]))
                            else:
                                self.run_hackrf(type="legacy", width=width_, pri=interval_, count=count_, freq=str(frequency[str(self.channel)]))
                        else:
                            var = "W56PULSE"
                            self.run_hackrf(type=var, width=width_, pri=interval_, count=count_,
                                            freq=str(frequency[str(self.channel)]))

                elif self.more_option == "random":
                    if fcc == "FCC5":
                        self.run_hackrf(type="fcc5", freq=str(int(frequency[str(self.channel)]) * 1000))
                    else:
                        self.run_hackrf(width=width_, pri=interval_, count=count_,
                                        freq=str(frequency[str(self.channel)]))
                    if fcc == "FCC6":
                        self.run_hackrf(type="fcc6", freq=str(int(frequency[str(self.channel)]) * 1000))
                    else:
                        self.run_hackrf(width=width_, pri=interval_, count=count_,
                                        freq=str(int(frequency[str(self.channel)]) * 1000))

                print("stop sniffer")
                time.sleep(5)
                file_name_ = self.stop_sniffer()
                file_name = "./pcap/" + str(file_name_)
                print("pcap file name", file_name)
                logging.info("pcap file name" + str(file_name))

                # pcap read logic

                # check for scapy frame

                scapy_frame = self.pcap_obj.check_frame_present(pcap_file=str(file_name), filter="(wlan.sa == 00:11:22:33:44:55)")
                print("scapy frame +", scapy_frame)
                scapy_frame_time_ = None
                if len(scapy_frame) != 0 and scapy_frame != "empty":
                    print("scapy frame  is present")
                    logging.info("scapy frame  is present")

                    scapy_frame_time = self.pcap_obj.read_arrival_time(
                        pcap_file=str(file_name),
                        filter="(wlan.sa == 00:11:22:33:44:55)")
                    print("scapy frame  time is ", scapy_frame_time)
                    logging.info("csa frame  time is " + str(scapy_frame_time))
                    scapy_time = str(scapy_frame_time)

                try:
                    csa_frame = self.pcap_obj.check_frame_present(
                        pcap_file=str(file_name),
                        filter="(wlan.csa.channel_switch.count && wlan.ssid == %s &&  wlan.bssid == %s)" % (
                        str(self.ssid), str(bssid)))
                except Exception as Except:
                    print(f"FAILED with exception: {Except}")

                print("csa frame", csa_frame)
                logging.info("csa frame" + str(csa_frame))
                if len(csa_frame) != 0 and csa_frame != "empty":
                    print("csa frame  is present")
                    logging.info("csa frame  is present")
                    print("radar detected")
                    logging.info("radar detected")
                    main_dict[fcc][var_1]["Detected"] = "YES"
                    csa_frame_time = self.pcap_obj.read_arrival_time(
                        pcap_file=str(file_name),
                        filter="(wlan.csa.channel_switch.count && wlan.ssid == %s &&  wlan.bssid == %s)" % (
                        str(self.ssid), str(bssid)))

                    print("csa frame  time is ", csa_frame_time)
                    logging.info("csa frame  time is " + str(csa_frame_time))
                    csa_time = str(csa_frame_time)
                    csa_frame_time_ = None

                    print("csa fra")
                    print(scapy_frame_time_)
                    print(type(scapy_frame_time_))
                    print("csa_frame,", csa_frame_time_)
                    print(type(csa_frame_time_))
                    print("calculate detection time")
                    logging.info("calculate detection time")
                    csa_datetime = parser.parse(csa_frame_time)
                    scapy_datetime = parser.parse(scapy_frame_time)

                    # Calculate the time difference
                    time_difference = round((csa_datetime - scapy_datetime).total_seconds(), 1)

                    print(time_difference)

                    print("detection time ", time_difference)
                    logging.info("detection time " + str(time_difference))
                    main_dict[fcc][var_1]["Detection Time(sec)"] = time_difference

                else:
                    print("csa frame is not present")
                    logging.info("csa frame is not present")
                    print("radar not detected")
                    logging.info("radar not detected")
                    main_dict[fcc][var_1]["Detected"] = "NO"
                    main_dict[fcc][var_1]["Detection Time(sec)"] = "NA"

                print(main_dict)
                logging.info(str(main_dict))
                if str(tria + 1) == str(self.trials):
                    print("check desired trials percentage")
                    logging.info("check desired trials percentage")
                    detection_list = []
                    for i in main_dict[fcc]:
                        print(i)
                        if main_dict[fcc][i] is None:
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
        logging.info("final dict" + str(main_dict))
        return main_dict

    # this is called first
    def run(self):
        print(self.enable_traffic)
        print(self.fcctypes)
        if self.create_client == "True":
            print("clean all stations before the test")
            logging.info("clean all stations before the test")
            self.pre_cleanup()

            print("create client")
            logging.info("create client")
            self.create_client_()
        else:
            print("client already exists")
        print("check if station is at expected channel")
        logging.info("check if station is at expected channel")
        sta_list = self.get_station_list()
        channel = self.station_data_query(station_name=sta_list[0], query="channel")
        bssid = self.station_data_query(station_name=sta_list[0], query="ap")
        print(bssid)
        logging.info(str(bssid))
        # channel = self.station_data_query(station_name="wlan0000", query="channel")
        if channel == self.channel:
            print("station is at expected channel")
            logging.info("station is at expected channel")
        else:
            print("station is not at expected channel")
            logging.error("station is not at expected channel")
            exit(1)

        test_time = datetime.now()
        test_time = test_time.strftime("%b %d %H:%M:%S")
        print("Radar Test started at ", test_time)
        logging.info("Radar Test started at " + str(test_time))

        print("run particular logic for given  trials")
        logging.info("run particular logic for given  trials")
        main = self.main_logic(bssid=bssid)

        test_end = datetime.now()
        test_end = test_end.strftime("%b %d %H:%M:%S")
        print("Test ended at ", test_end)
        logging.info("Test ended at " + str(test_end))
        logging.info("Test ended at " + test_end)
        s1 = test_time
        s2 = test_end  # for example
        FMT = '%b %d %H:%M:%S'
        test_duration = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
        logging.info("test duration" + str(test_duration))
        self.generate_report(test_duration=test_duration, main_dict=main)
        self.stop_l3()

    # graphing function
    def generate_graph(self, data):
        obj = lf_graph.lf_stacked_graph(_data_set=data, _xaxis_name="", _yaxis_name="", _enable_csv=False,
                                        _remove_border=True)
        img = obj.build_stacked_graph()
        return img

    # report generation function
    def generate_report(self, test_duration=None, main_dict=None):

        print("test duration", test_duration)
        lst =[]
        for i in self.fcctypes:
            print(i)
            if "FCC" in i:
                if len(lst) == 0:
                    lst.append("FCC")
                else:
                    for x in lst:
                        if "FCC" in lst:
                            pass
                        else:
                            lst.append("FCC")

            elif "ETSI" in i:
                if len(lst) == 0:
                    lst.append("ETSI")
                else:
                    for x in lst:
                        if "ETSI" in lst:
                            pass
                        else:
                            lst.append("ETSI")
            elif "Japan" in i:
                if len(lst) == 0:
                    lst.append("Japan")
                else:
                    for x in lst:
                        if "Japan" in lst:
                            print("yo")
                            pass
                        else:
                            print("b")
                            lst.append("Japan")
            elif "Korea" in i:
                if len(lst) == 0:
                    lst.append("Korea")
                else:
                    for x in lst:
                        if "Korea" in lst:
                            pass
                        else:
                            lst.append("Korea")
        print(lst)

        var_name = "_".join(lst)
        report = lf_report_pdf.lf_report(_path="",
                                         _results_dir_name=f"{var_name}_ch{self.channel}_bw{self.bandwidth}_Detection Probability Test",
                                         _output_html="dpt.html",
                                         _output_pdf=f"{var_name}_ch{self.channel}_bw{self.bandwidth}_dpt.pdf")
        # self.test_duration = "xyz"
        date = str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
        report_path = report.get_report_path()
        print(report_path)
        report.move_data(directory_name="pcap")

        test_setup_info = {
            "DUT Name": self.ap_name,
            "SSID": self.ssid,
            "Test Duration": test_duration,
        }
        report.set_title("Detection Probability Test Report")
        report.set_date(date)
        report.build_banner_cover()
        report.set_table_title("Test Setup Information")
        report.build_table_title()

        report.test_setup_table(value="Device under test", test_setup_data=test_setup_info)

        report.set_obj_html("Objective", "Detection Probability Test  is compilance to the Dynamic Frequency Selection"
                                         " (DFS) Regulation, it creates regulatory specified radar pulses "
                                         " to the DUT repeatedly to measure the probability "
                                         "of detection.")
        report.build_objective()
        report.set_obj_html("Result Summary",
                            "The below graph provides information regarding detection probability percentage for various RADAR Types.")
        report.build_objective()
        graph_dict = dict.fromkeys(self.fcctypes)
        for fcc in self.fcctypes:
            detection_list = []
            for i in main_dict[fcc]:
                if main_dict[fcc][i] is None:
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
                percent = round(((m / len(detection_list)) * 100), 1)
                print(percent)
                graph_dict[fcc] = percent

        print("graph dict", graph_dict)
        logging.info("graph dict" + str(graph_dict))

        graph2 = self.generate_graph(data=graph_dict)
        # graph1 = self.generate_per_station_graph()
        report.set_graph_image(graph2)
        report.move_graph_image()
        report.build_graph_without_border()

        # various atandards
        required_percent = {"FCC0": "60%", "FCC1": "60%", "FCC2": "60%", "FCC3": "60%", "FCC4": "60%", "FCC5": "70%",
                            "FCC6": "70%",
                            "ETSI0": "NA", "ETSI1": "60%", "ETSI2": "60%", "ETSI3": "60%", "ETSI4": "60%",
                            "ETSI5": "60%", "ETSI6": "60%",
                            "korea_1": "60%", "korea_2": "60%", "korea_3": "60%",
                            "Japan-w53-1": "60%", "Japan-w53-3": "60%",  "Japan-w53-4": "60%",  "Japan-w53-7": "60%",
                            "Japan-w53-8": "60%",
                            "Japan-w53-6": "60%", "Japan-w53-5": "60%",
                            "Japan-w53-2": "60%", "Japan-w56-1": "60%",  "Japan-w56-2": "60%", "Japan-w56-3": "60%",
                            "Japan-w56-4": "60%", "Japan-w56-5": "60%", "Japan-w56-6": "60%"}

        report.set_obj_html("Summary Table",
                            "The below table provides detailed information regarding detection probability percentage for various RADAR Types.")
        report.build_objective()
        wave, desired_per, pd_per, pd_req, tring, avg_detect, result = [], [], [], [], [], [], []

        for fcc in self.fcctypes:
            wave.append(fcc)
            desired_per.append(self.desired_detection)

            # PD LOGIC
            detection_list = []
            for i in main_dict[fcc]:
                if main_dict[fcc][i] is None:
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
            length = []
            for i in main_dict[fcc]:
                if main_dict[fcc][i] is None:
                    print("\n")
                else:
                    length.append(i)
            tring.append(len(length))

            # average detection time
            detection_list = []
            for i in main_dict[fcc]:
                if main_dict[fcc][i] is None:
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
            # "Desired Percentage %" :desired_per,
            "Required Detection Percentage %": pd_req,
            "Num Trials": tring,
            "Average Detect Time (secs)": avg_detect,
            "Result": result,
        }
        test_setup = pd.DataFrame(table_1)
        report.set_table_dataframe(test_setup)
        report.build_table()

        x = list(main_dict.keys())
        print(x)
        main_list = []
        if ("FCC1" in x) and ("FCC2" in x) and ("FCC3" in x) and ("FCC4" in x):
            print(" FCC1, FCC2, FCC3 and FCC4 is present")
            n_tri = []
            main_list.append("FCC1")
            main_list.append("FCC2")
            main_list.append("FCC3")
            main_list.append("FCC4")
            sucess_det, average_det = [], []
            for i in main_list:
                y = list(main_dict[i].keys())
                n_tri.append(len(y))
                print("y", y)
                lst2 = []
                for z in y:
                    lst2.append(main_dict[i][z]["Detected"])
                print("lst2", lst2)
                sucess_det.append(lst2.count("YES"))

            print(n_tri)
            print(sucess_det)

            # average
            for m, n in zip(sucess_det, n_tri):
                avg = (m / n) * 100
                average_det.append(round(avg, 2))
            print(average_det)
            # aggregate
            sum = 0
            for i in average_det:
                sum = sum + i

            aggregate = (sum / 400) * 100
            print(aggregate)

            report.set_obj_html("Aggregate of short pulse type 1-4",
                                "The aggregate is the average of the percentage of successful detections of"
                                " Short Pulse Radar Types 1-4.  For example, the following table indicates how "
                                " the aggregate of percentage of successful detections is computed. For the current run aggregate is equal to " + str(round(aggregate, 2)) + " %")
            report.build_objective()

            table_2 = {
                "Radar Type": main_list,
                "No. of Trials": n_tri,
                "Number of Successful Detections %": sucess_det,
                "Minimum Percentage of Successful Detection": average_det,
            }
            test_setup = pd.DataFrame(table_2)
            report.set_table_dataframe(test_setup)
            report.build_table()


        report.set_obj_html("Detailed Result Table",
                            "The below tables provides detailed information for per trials run for each RADAR Types")
        report.build_objective()
        for fcc in self.fcctypes:
            report.set_obj_html("Detailed Result Table for " + str(fcc),
                                "The below table provides detailed information for per trials run for " + str(
                                    fcc) + " RADAR Type")
            report.build_objective()
            if fcc == "FCC5":
                Trials, burst, trial_centre, trial_low, trial_high, uut_channel, freq_modulatin, tx_sample_rate, detect,frequency, det_time = [], [], [], [], [], [], [], [], [], [], []

            if fcc == "ETSI5" or fcc == "ETSI6":
                Trials, burst, pulse, width, prf_1, prf_2, prf_3, detect, frequency, det_time = [], [], [], [], [], [], [], [], [], []
            if fcc == "Japan-w53-3" or fcc == "Japan-w53-4" or fcc == "Japan-w53-5" or fcc == "Japan-w53-6" or fcc ==  "Japan-w53-7" or fcc ==  "Japan-w53-8":
                Trials, burst, width, blank_t, long_pulse_wdth, chirp_width, pri, no_c_pulse,  detect, frequency, det_time = [], [], [], [], [], [], [], [], [], [], []
            if fcc == "Japan-w53-1" or fcc == "Japan-w53-2":
                Trials, pulse, width, prf, detect, frequency, det_time = [], [], [], [], [], [], []
            else:
                Trials, burst, pulse, width, pri, detect, frequency, det_time = [], [], [], [], [], [], [], []

            for i in main_dict[fcc]:
                if main_dict[fcc][i] is None:
                    print("ignore")
                if fcc == "FCC5":
                    Trials.append(i)
                    burst.append(main_dict[fcc][i]['Burst'])
                    trial_centre.append(main_dict[fcc][i]['Trial Centre'])
                    trial_low.append(main_dict[fcc][i]['Trial Low'])
                    trial_high.append(main_dict[fcc][i]['Trial High'])
                    uut_channel.append(main_dict[fcc][i]['UUT Channel'])
                    freq_modulatin.append(main_dict[fcc][i]['Frequency Modulating'])
                    tx_sample_rate.append(main_dict[fcc][i]['Tx sample rate'])
                    detect.append(main_dict[fcc][i]['Detected'])
                    frequency.append(main_dict[fcc][i]['Frequency(KHz)'])
                    det_time.append(main_dict[fcc][i]['Detection Time(sec)'])
                elif fcc == "ETSI5" or fcc == "ETSI6":
                    Trials.append(i)
                    burst.append(main_dict[fcc][i]['Burst'])
                    pulse.append(main_dict[fcc][i]['Pulses'])
                    width.append(main_dict[fcc][i]['Width'])
                    prf_1.append(main_dict[fcc][i]['prf_1'])
                    prf_2.append(main_dict[fcc][i]['prf_2'])
                    prf_3.append(main_dict[fcc][i]['prf_3'])
                    detect.append(main_dict[fcc][i]['Detected'])
                    frequency.append(main_dict[fcc][i]['Frequency(KHz)'])
                    det_time.append(main_dict[fcc][i]['Detection Time(sec)'])
                elif fcc == "Japan-w53-3" or fcc == "Japan-w53-4" or fcc == "Japan-w53-5" or fcc == "Japan-w53-6" or fcc ==  "Japan-w53-7" or fcc ==  "Japan-w53-8":
                    Trials.append(i)
                    burst.append(main_dict[fcc][i]['Burst'])
                    width.append(main_dict[fcc][i]['Width'])
                    blank_t.append(main_dict[fcc][i]["Blank Time(us)"])
                    long_pulse_wdth.append(main_dict[fcc][i]["Long Pulse Width(us)"])
                    chirp_width.append(main_dict[fcc][i]["Chirp Width(MHz)"])
                    pri.append(main_dict[fcc][i][ "Pri(Hz)"])
                    no_c_pulse.append(main_dict[fcc][i]["No of Continuous Pairs of Pulses"])
                    detect.append(main_dict[fcc][i]['Detected'])
                    frequency.append(main_dict[fcc][i]['Frequency(KHz)'])
                    det_time.append(main_dict[fcc][i]['Detection Time(sec)'])
                elif fcc == "Japan-w53-1" or fcc == "Japan-w53-2":
                    Trials.append(i)
                    pulse.append(main_dict[fcc][i]['Pulses'])
                    width.append(main_dict[fcc][i]['Width'])
                    prf.append(main_dict[fcc][i]['PRF(Hz)'])
                    detect.append(main_dict[fcc][i]['Detected'])
                    frequency.append(main_dict[fcc][i]['Frequency(KHz)'])
                    det_time.append(main_dict[fcc][i]['Detection Time(sec)'])
                else:
                    Trials.append(i)
                    burst.append(main_dict[fcc][i]['Burst'])
                    pulse.append(main_dict[fcc][i]['Pulses'])
                    width.append(main_dict[fcc][i]['Width'])
                    pri.append(main_dict[fcc][i]['PRI(US)'])
                    detect.append(main_dict[fcc][i]['Detected'])
                    frequency.append(main_dict[fcc][i]['Frequency(KHz)'])
                    det_time.append(main_dict[fcc][i]['Detection Time(sec)'])

            print("trial", Trials)
            if fcc == "FCC5":
                table_2 = {
                    "Trials": Trials,
                    "Num Bursts": burst,
                    "Trial centre": trial_centre,
                    "Trial Low": trial_low,
                    "Trial High": trial_high,
                    "UUT Channel": uut_channel,
                    "Freq Modulating": freq_modulatin,
                    "TX Sample Rate": tx_sample_rate,
                    "Detected": detect,
                    "Frequency (KHz)": frequency,
                    "Detection Time (secs)": det_time
                }
            elif fcc == "FCC0" or fcc == "FCC1" or fcc == "FCC2" or fcc == "FCC3" or fcc == "FCC4":
                table_2 = {
                    "Trials": Trials,
                    "Num Bursts": burst,
                    "Num Pulses": pulse,
                    "Pulse Width (μs)": width,
                    "PRI (μs)": pri,
                    "Detected": detect,
                    "Frequency (KHz)": frequency,
                    "Detection Time (secs)": det_time
                }
            elif fcc == "ETSI5" or fcc == "ETSI6":
                table_2 = {
                    "Trials": Trials,
                    "Num Bursts": burst,
                    "Num Pulses": pulse,
                    "Pulse Width (μs)": width,
                    "PRI_1 (Hz)": prf_1,
                    "PRI_2 (Hz)": prf_2,
                    "PRI_3 (Hz)": prf_3,
                    "Detected": detect,
                    "Frequency (KHz)": frequency,
                    "Detection Time (secs)": det_time
                }
            elif fcc == "Japan-w53-3" or fcc == "Japan-w53-4" or fcc == "Japan-w53-5" or fcc == "Japan-w53-6" or fcc ==  "Japan-w53-7" or fcc ==  "Japan-w53-8":
                table_2 = {
                    "Trials": Trials,
                    "Num Bursts": burst,
                    "Pulse Width (μs)": width,
                    "Blank Time (μs)": blank_t,
                    "Long Pulse Width (μs)": long_pulse_wdth,
                    "Chirp Width(MHz)": chirp_width,
                    "PRF (Hz)": pri,
                    "No of Continuous Pairs of Pulses": no_c_pulse,
                    "Detected": detect,
                    "Frequency (KHz)": frequency,
                    "Detection Time (secs)": det_time
                }
            elif fcc == "Japan-w53-1" or fcc == "Japan-w53-2":
                table_2 = {
                    "Trials": Trials,
                    "Num Pulses": pulse,
                    "Pulse Width (μs)": width,
                    "PRF (Hz)": prf,
                    "Detected": detect,
                    "Frequency (KHz)": frequency,
                    "Detection Time (secs)": det_time
                }
            else:
                # Japan-56-1,2,3,4,5,6 & Korea 1,2,3 & ETSI-0,1,2,3,4
                table_2 = {
                    "Trials": Trials,
                    "Num Bursts": burst,
                    "Num Pulses": pulse,
                    "Pulse Width (μs)": width,
                    "PRF (Hz)": pri,
                    "Detected": detect,
                    "Frequency (KHz)": frequency,
                    "Detection Time (secs)": det_time
                }
            test_setup_ = pd.DataFrame(table_2)
            report.set_table_dataframe(test_setup_)
            report.build_table()

        freq_option = None
        if self.more_option == "centre":
            freq_option = "Stay at centre freq for all Trials"
        elif self.more_option == "random":
            freq_option = "Stay at random frequency between the bandwidth for all trials"

        tx_power = {"52": "-41.17", "56": "41.92", "60": "-41.91", "64": "-41.31", "100": "-38.61", "104":"-39.06",
                    "108": "-39.77", "112":"-40.27", "116": "-40.22", "120": "-39.44", "124": "-38.75",
                    "128": "-38.32", "132": "-38.87", "136": "-39.77", "140": "-39.97", "144": "-40.03"}
        test_input_infor = {
            "Parameters": "Values",
            "LANforge ip": self.host,
            "LANforge port": self.port,
            "Radar Types": self.fcctypes,
            "Radar Hardware": "ct712",
            "Freq Channel Number": self.channel,
            "Bandwidth": self.bandwidth + " (MHz)",
            "Tx Power of radar in dbm": tx_power[str(self.channel)],
            "Desired Pass Percentage": str(self.desired_detection) + str("%"),
            "Max Number of extra trials": self.extra_trials,
            "Time interval between Trials (secs)": self.time_int,
            "Run Traffic": self.enable_traffic,
            "Frequency step option": freq_option,
            "Contact": "<a href='mailto:support@candelatech.com'>support@candelatech.com</a>"
        }
        report.set_table_title("Test basic Information")
        report.build_table_title()
        report.test_setup_table(value="Information", test_setup_data=test_input_infor)

        report.build_footer()
        report.write_html()
        report.write_pdf_with_timestamp(_page_size='A4', _orientation='Portrait')
        report.move_data(directory="log", _file_name="dpt.log" )
        # report.move_data(_file_name="dpt.log")


def main():
    description = """
    detection_probability_test.py
    --------------------

    Summary :
    ----------
    Detection Probability Test  is compilance to the Dynamic Frequency Selection(DFS_Object) Regulation, it creates regulatory
    specified radar pulses to the DUT repeatedly to measure the probability of detection.

    execution: This script is executed in following way
    1. create a client on 5GHZ band
    2. check if the client is on expected DFS_Object channel or not
    3. if not terminate the script
    4. if yes then it will start sniffer on client channel
    5. once the client is associated respective regulation radar is generated from hackrf
    6. stop sniffer
    7. check for csa frame 
    8. report 

    ############################################
    # Examples Commands for different scenarios 
    ############################################

    --> for full test (all regulation)
       ./detection_probability_test.py  --host 192.168.1.31 --ssid Candela_20MHz --passwd [BLANK] --security open --trials 1   --more_option centre 

    *** LEGACY MODE (older) ******        

    --> FCC Regulation :

       Try to replace 0 IN FCC0 with 1, 2, 3, 4, 5 and 6

       ./detection_probability_test.py  --host 192.168.200.91 --ssid candelatest --passwd candelatest --security wpa2 
       --sniff_radio 1.1.wiphy1 --radio 1.1.wiphy0 --fcctypes FCC0 --channel 52  --trials 1  --desired_detection 60
        --enable_traffic False --static False --more_option centre --bw 20 --lf_hackrf 30a28607 --legacy True

    --> ETSI Regulation

       From ETSI0 to ETSI6

       ./detection_probability_test.py  --host 192.168.200.91 --ssid candelatest --passwd candelatest --security wpa2 
       --sniff_radio 1.1.wiphy1 --radio 1.1.wiphy0 --fcctypes ETSI0 --channel 52  --trials 1  --desired_detection 60
        --enable_traffic False --static False --more_option centre --bw 20 --lf_hackrf 30a28607 --legacy True

    --> JAPAN Regulation

       Japan-w53-1/6 and Japan-w56-1/6

       ./detection_probability_test.py  --host 192.168.200.91 --ssid candelatest --passwd candelatest --security wpa2 
       --sniff_radio 1.1.wiphy1 --radio 1.1.wiphy0 --fcctypes Japan-w53-1 --channel 52  --trials 1  --desired_detection 60
        --enable_traffic False --static False --more_option centre --bw 20 --lf_hackrf 30a28607 --legacy True

    --> Korea Regulation
       coming soon...

    **** NON LEGACY MODE ****

    --> FCC Regulation

    Try to replace 0 IN FCC0 with 1, 2, 3, 4, 5 and 6

       ./detection_probability_test.py  --host 192.168.200.91 --ssid candelatest --passwd candelatest --security wpa2 
       --sniff_radio 1.1.wiphy1 --radio 1.1.wiphy0 --fcctypes FCC0 --channel 52  --trials 1  --desired_detection 60
        --enable_traffic False --static False --more_option centre --bw 20 --lf_hackrf 30a28607 --legacy False

    --> ETSI Regulation

       From ETSI0 to ETSI6

       ./detection_probability_test.py  --host 192.168.200.91 --ssid candelatest --passwd candelatest --security wpa2 
       --sniff_radio 1.1.wiphy1 --radio 1.1.wiphy0 --fcctypes ETSI0 --channel 52  --trials 1  --desired_detection 60
        --enable_traffic False --static False --more_option centre --bw 20 --lf_hackrf 30a28607 --legacy False

    --> JAPAN Regulation

       Japan-w53-1/6 and Japan-w56-1/6

       ./detection_probability_test.py  --host 192.168.200.91 --ssid candelatest --passwd candelatest --security wpa2 
       --sniff_radio 1.1.wiphy1 --radio 1.1.wiphy0 --fcctypes Japan-w53-1 --channel 52  --trials 1  --desired_detection 60
        --enable_traffic False --static False --more_option centre --bw 20 --lf_hackrf 30a28607 --legacy False

    --> Korea Regulation
       coming soon...

    ===============================================================================  
    """
    parser = argparse.ArgumentParser(
        prog='detection_probability_test.py',
        formatter_class=argparse.RawTextHelpFormatter,
        description=description)

    parser.add_argument("--host", help='specify the GUI ip to connect to', default='192.168.1.31')
    parser.add_argument("--port", help='specify scripting port of LANforge', default=8080)
    parser.add_argument('--ssid', type=str, help='ssid for client')
    parser.add_argument('--passwd', type=str, help='password to connect to ssid', default='[BLANK]')
    parser.add_argument('--security', type=str, help='security', default='open')
    parser.add_argument('--radio', type=str, help='radio at which client will be connected', default='1.1.wiphy1')
    parser.add_argument("--sniff_radio", help='radio at which wireshark will be started', default="1.1.wiphy0")
    parser.add_argument("--static", help='True if client will be created with static ip', default=True)
    parser.add_argument("--static_ip", help='if static option is True provide static ip to client',
                        default="192.168.2.100")
    parser.add_argument("--ip_mask", help='if static is true provide ip mask to client', default="255.255.255.0")
    parser.add_argument("--gateway_ip", help='if static is true provide gateway ip', default="192.168.2.50")
    parser.add_argument('--upstream', type=str, help='provide eth1/eth2', default='eth1')
    parser.add_argument('--fcctypes', nargs="+",
                        help='types needed to be tested FCC0/FCC1/FCC2/FCC3/FCC4/FCC5/ETSI0/ETSI1/ETSI2/ETSI3/ETSI4/ETSI5/ETSI6/Japan-W53-1/Japan-W53-2/Japan-w53-3/Japan-w53-4/Japan-w53-5/Japan-w53-6',
                        default=["FCC0", "FCC1", "FCC2", "FCC3", "FCC4", "ETSI0", "ETSI1", "ETSI2", "ETSI3", "ETSI4",
                                 "ETSI5", "ETSI6", "Japan-W53-1", "Japan-W53-2", "Japan-w53-3", "Japan-w53-4",
                                 "Japan-w53-5",
                                 "Japan-w53-6", "Japan-w53-7", "Japan-w53-8", "Japan-w56-1",
                                 "Japan-w56-2", "Japan-w56-3", "Japan-w56-4",
                                 "Japan-w56-5", "Japan-w56-6",
                                 "korea_1", "korea_2", "korea_3"])
    parser.add_argument('--channel', type=str,
                        help='channel options need to be tested 52, 56, 60, 64, 100, 104, 108, 112, 116, 120, 124 ,128, 132, 136, 140',
                        default="100")
    parser.add_argument("--enable_traffic",
                        help='set to True if traffic needs to be added while testing', default=False)
    parser.add_argument("--trials", type=int,
                        help='provide the number of trials you want to test default is 30', default=30)
    parser.add_argument("--desired_detection", type=int,
                        help='provide the percentage value for desired detection eg 80, which means 80%%', default=80)
    parser.add_argument("--extra_trials", type=int,
                        help='provide the number of extra trials need to be performed if the test doesnot reach the expected or desired value',
                        default=0)
    parser.add_argument("--more_option",
                        help='select from the list of more options which test you need to perform shift, centre, random',
                        default="centre")
    parser.add_argument("--time_int", help='provide time interval in seconds between each trials', default="0")
    parser.add_argument("--ssh_username", help='provide username for doing ssh into LANforge', default="lanforge")
    parser.add_argument("--ssh_password", help='provide password for doing ssh into LANforge', default="lanforge")
    parser.add_argument("--bw",
                        help='provide bandwidth over which you want to start test eith 20/40/80 Mhz', default="20")
    parser.add_argument("--traffic_type", help='mention the traffic type you want to run eg lf_udp', default="lf_udp")
    parser.add_argument("--ap_name", help='provide model of dut', default="Test_AP")
    parser.add_argument("--tx_power", help='manually provide tx power of radar sent')
    parser.add_argument("--lf_hackrf", help='provide serial number og tx hackrf eg 30a28607')
    parser.add_argument("--legacy", help='stores true for legacy mode by default', default=True)
    parser.add_argument("--create_client", help='stores True/False if client creation is needed', default=False)
    parser.add_argument("--side_a_min_rate", type=int, help='for layer3 provide side a min tx rate', default=1000000)
    parser.add_argument("--side_a_max_rate", type=int,  help='for layer3 provide side a max tx rate', default=0)
    parser.add_argument("--side_b_min_rate",type=int,  help='for layer3 provide side b min tx rate', default=1000000)
    parser.add_argument("--side_b_max_rate", type=int, help='for layer3 provide side b max tx rate', default=0)
    parser.add_argument("--side_a_min_pdu", type=int, help='for layer3 provide side a min pdu size', default=1250)
    parser.add_argument("--side_b_min_pdu", type=int, help='for layer3 provide side b min pdu size', default=1250)
    parser.add_argument("--postcleanup", action='store_true')

    args = parser.parse_args()
    DFS_Object = DfsTest(host=args.host,
                  port=args.port,
                  ssid=args.ssid,
                  passwd=args.passwd,
                  security=args.security,
                  radio=args.radio,
                  upstream=args.upstream,
                  fcctypes=args.fcctypes,
                  channel=args.channel,
                  sniff_radio=args.sniff_radio,
                  static=args.static,
                  static_ip=args.static_ip,
                  ip_mask=args.ip_mask,
                  gateway_ip=args.gateway_ip,
                  enable_traffic=args.enable_traffic,
                  desired_detection=args.desired_detection,
                  extra_trials=args.extra_trials,
                  more_option=args.more_option,
                  time_int=args.time_int,
                  trials=args.trials,
                  ssh_username=args.ssh_username,
                  ssh_password=args.ssh_password,
                  traffic_type=args.traffic_type,
                  bandwidth=args.bw,
                  ap_name=args.ap_name,
                  lf_hackrf=args.lf_hackrf,
                  legacy=args.legacy,
                  create_client=args.create_client,
                  side_a_min_rate=args.side_a_min_rate,
                  side_a_max_rate=args.side_a_max_rate,
                  side_b_min_rate=args.side_b_min_rate,
                  side_b_max_rate=args.side_b_max_rate,
                  side_a_min_pdu=args.side_a_min_pdu,
                  side_b_min_pdu=args.side_b_min_pdu
                  )

    DFS_Object.run()

    if args.postcleanup:
        DFS_Object.pre_cleanup()

if __name__ == '__main__':
    main()