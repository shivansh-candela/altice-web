""" This script is used for DFS Testing on various radar types and user dependent channels after completion of the test it gives a nice pdf test report under folder html_reports/dfs/
    it uses various input arguments which can be seen by ./x.py --help
    eg - sudo python3 lf_dfs_3.py -i 192.168.208.28 -u root -p Password@123xzsawq@! -mgr localhost -s loadbalance -pwd [BLANK] -sec open -rad wiphy3 -upstream eth1  -m triband --fcctypes FCC0 --channel 52
    date - 11- feb - 2021
    --Nikita Yadav
"""

import os
import paramiko
import time
import argparse
import datetime
import telnetlib
import sys
import logging
import pexpect

from station_layer3 import STATION
from datetime import datetime
from itertools import islice
from html_template import *


if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)
if 'py-json' not in sys.path:
    sys.path.append('../py-json')
import LANforge
from LANforge import LFUtils
from LANforge import lfcli_base
from LANforge.lfcli_base import LFCliBase
from LANforge.LFUtils import *
import realm
from realm import Realm

class DFS_TEST:
    def __init__(self, ip, user, pswd, host, ssid, passwd, security, radio, upstream, fcctype, channel):
        self.ip = ip
        self.user = user
        self.pswd = pswd
        self.host = host
        self.ssid = ssid
        self.passwd = passwd
        self.security = security
        self.radio = radio
        self.upstream= upstream
        self.fcctype = fcctype
        self.channel = channel


    def set_channel_in_ap_at_(self,channel):
        ch = str(channel)
        print("chnnel telnet ",ch)
        x = b"aci-cli aci_wifi_set_channel 1 %s" % ch.encode('ascii') + b"\n"
        print(x)
        tn = telnetlib.Telnet(self.ip)
        tn.read_until(b"Login: ")
        tn.write(self.user.encode("ascii") + b"\n")
        tn.read_until(b"Password: ")
        tn.write(self.pswd.encode('ascii') + b"\n")
        print("successfully connected to %s" % self.ip)
        tn.write(b"sh\n")
        tn.write(x)
        tn.write(b"aci-cli aci_wifi_command_apply 1" + b"\n")
        time.sleep(2)
        output = tn.read_very_eager()
        # print(output)
        return output

    def monitor_station_before(self):
        station_list = LFUtils.port_name_series(prefix="sta",
                                                start_id=0,
                                                end_id=0,
                                                padding_number=10000,
                                                radio=self.radio)
        obj1 = STATION(lfclient_host=self.host, lfclient_port=8080, ssid=self.ssid, paswd=self.passwd, security=self.security, radio=self.radio, upstream=self.upstream, sta_list=station_list)
        var = obj1.json_get("/port/1/1/sta0000?fields=channel")
        var_1 = (var['interface']['channel'])
        return var_1

    def check_primary_channel(self):
        tn = telnetlib.Telnet(self.ip)
        tn.read_until(b"Login: ")
        tn.write(self.user.encode("ascii") + b"\n")
        tn.read_until(b"Password: ")
        tn.write(self.pswd.encode('ascii') + b"\n")
        print("successfully connected to %s" % self.ip)
        tn.write(b"sh\n")
        tn.write(b"wl -i wl1 status\n")

        time.sleep(2)
        output = tn.read_very_eager()
        x = output.decode("utf-8")
        y = x.split(" ")
        ind_var = None
        if "Primary" in y:
            ind_var = y.index("Primary")
        fin_ind = ind_var + 2
        channel = y[fin_ind].rstrip()
        print(channel)
        return channel

    def monitor_station_(self, channel, channel_before):
        station_list = LFUtils.port_name_series(prefix="sta",
                                                start_id=0,
                                                end_id=0,
                                                padding_number=10000,
                                                radio=self.radio)

        obj1 = STATION(lfclient_host=self.host, lfclient_port=8080, ssid=self.ssid, paswd=self.passwd, security=self.security, radio=self.radio, upstream=self.upstream, sta_list=station_list)
        print(channel)
        var = obj1.json_get("/port/1/1/sta0000?fields=channel")
        var_1 = (var['interface']['channel'])
        # print(var_1)

        if var_1 == channel_before:
            print("channel at" + channel)
            return var_1
        else:
            print("wait until channel assigned")
            timeout = time.time() + 60 * 15

            while var_1 != channel:
                var = obj1.json_get("/port/1/1/sta0000?fields=channel")
                var_1 = var['interface']['channel']
                time.sleep(1)
                if time.time() > timeout:
                    var = obj1.json_get("/port/1/1/sta0000?fields=channel")
                    var_1 = var['interface']['channel']
                    break

            return var_1

    def create_station_cx(self):
        cmd = "python3 station_layer3.py -hst localhost -s " + str(self.ssid) + " -pwd " + str(self.passwd) + " -sec " + str(self.security) + " -rad " + str(self.radio) + " -upstream " + str(self.upstream)
        #os.chdir('/home/lanforge/lanforge-scripts/py-scripts')
        os.system(cmd)

    def monitor_untill_channel_assigned(self, host, ssid, passwd, security, radio, upstream):
        self.host = host
        self.ssid = ssid
        self.passwd = passwd
        self.security = security
        self.radio = radio
        self.upstream = upstream
        station_list = LFUtils.port_name_series(prefix="sta",
                                                start_id=0,
                                                end_id=0,
                                                padding_number=10000,
                                                radio=radio)

        obj1 = STATION(lfclient_host=host, lfclient_port=8080, ssid=ssid, paswd=passwd, security=security, radio=radio, upstream=upstream, sta_list=station_list)

        var = obj1.json_get("/port/1/1/sta0000?fields=channel")
        var_1 = (var['interface']['channel'])

        timeout = time.time() + 60 * 15  # 15min
        while var_1 == "-1":
            var = obj1.json_get("/port/1/1/sta0000?fields=channel")
            var_1 = var['interface']['channel']
            time.sleep(1)
            if time.time() > timeout:
                break

        return var_1

    def generate_radar_at_ch(self, width_, interval_, count_, frequency):
        current_time = datetime.now()
        print("Current date and time : ")
        current_time = current_time.strftime("%b %d %H:%M:%S")
        print("time stamp of radar send", current_time)
        # print("width", width_)

        os.chdir('/usr/lib64/python2.7/site-packages/')
        frequency = str(frequency)
        width_ = str(width_)
        interval_ = str(interval_)
        count_ = str(count_)
        command_hackRF = "sudo python lf_hackrf.py --pulse_width " + width_ + " --pulse_interval " + interval_ + " --pulse_count " + count_ + " --sweep_time 1000 --freq " + frequency
        command_hackRF = str(command_hackRF)
        ch = pexpect.spawn(command_hackRF)
        time.sleep(5)
        ch.expect('>>>')
        ch.sendline('s')
        ch.expect('>>>')
        ch.sendline('q')
        time.sleep(1)

        return current_time

    def client_connect_time(self, host, ssid, passwd, security, radio,upstream, channel):
        self.host = host
        self.ssid = ssid
        self.passwd = passwd
        self.security = security
        self.radio = radio
        self.upstream = upstream
        station_list = LFUtils.port_name_series(prefix="sta",
                                                start_id=0,
                                                end_id=0,
                                                padding_number=10000,
                                                radio=radio)
        obj1 = STATION(lfclient_host=host, lfclient_port=8080, ssid=ssid, paswd=passwd, security=security, radio=radio, upstream=upstream, sta_list=station_list)
        var = obj1.json_get("/port/1/1/sta0000?fields=channel")
        var_1 = (var['interface']['channel'])

        timeout_ = time.time() + 60 * 1  # 2min
        while var_1 != "-1":
            var = obj1.json_get("/port/1/1/sta0000?fields=channel")
            var_1 = var['interface']['channel']
            time.sleep(1)
            if time.time() > timeout_:
                break
        if var_1 == "-1":
            current_time = datetime.now()
            print("Current date and time : ")
            disconnect_time = current_time.strftime("%b %d %H:%M:%S")
            print("station disconnection time", disconnect_time)

            timeout = time.time() + 60 * 15  # 15min
            while var_1 == "-1":
                var = obj1.json_get("/port/1/1/sta0000?fields=channel")
                var_1 = var['interface']['channel']
                time.sleep(1)
                if time.time() > timeout:
                    break
            current_time1 = datetime.now()
            print("Current date and time : ")
            connect_time = current_time1.strftime("%b %d %H:%M:%S")
            print("station connection time", connect_time)
            s1 = disconnect_time
            s2 = connect_time  # for example
            FMT = '%b %d %H:%M:%S'
            c_time = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
            print("connection time ", c_time)
            # print("detection time for radar", tdelta)
            # detection_time_lst.append(tdelta)

            lst = str(c_time).split(":")
            seconds = int(lst[0]) * 3600 + int(lst[1]) * 60 + int(lst[2])
            c_time = seconds
            print("connection time ", c_time)
        else:
            disconnect_time = "00:00:00"
            print("station disconnection time", disconnect_time)
            connect_time = "00:00:00"
            print("time at which traffic started", connect_time)
            c_time = 0
            print("connection time ", c_time)

        return c_time

    def channel_after_radar(self, host, ssid, passwd, security, radio, upstream):
        self.host = host
        self.ssid = ssid
        self.passwd = passwd
        self.security = security
        self.radio = radio
        self.upstream = upstream
        station_list = LFUtils.port_name_series(prefix="sta",
                                                start_id=0,
                                                end_id=0,
                                                padding_number=10000,
                                                radio=radio)
        obj1 = STATION(lfclient_host=host, lfclient_port=8080, ssid=ssid, paswd=passwd, security=security, radio=radio, upstream=upstream, sta_list=station_list)
        var = obj1.json_get("/port/1/1/sta0000?fields=channel")
        var_1 = (var['interface']['channel'])
        return var_1

    def monitor_cx(self, host, ssid, passwd, security, radio, upstream):
        self.host = host
        self.ssid = ssid
        self.passwd = passwd
        self.security = security
        self.radio = radio
        self.upstream = upstream
        station_list = LFUtils.port_name_series(prefix="sta",
                                                start_id=0,
                                                end_id=0,
                                                padding_number=10000,
                                                radio=radio)

        obj1 = STATION(lfclient_host=host, lfclient_port=8080, ssid=ssid, paswd=passwd, security=security, radio=radio, upstream=upstream, sta_list=station_list)
        var = obj1.json_get("/cx/L3Teststa0000-0")
        # print(type(var))
        var_1 = (var['L3Teststa0000-0']['state'])
        timeout = time.time() + 60 * 2  # 15min
        while var_1 != "Run":
            var = obj1.json_get("/cx/L3Teststa0000-0")
            # print(type(var))
            var_1 = (var['L3Teststa0000-0']['state'])
            time.sleep(1)
            if time.time() > timeout:
                break
        # print(var_1)
        return var_1

    def monitor_untill_connection_time(self, host, ssid, passwd, security, radio, upstream):
        self.host = host
        self.ssid = ssid
        self.passwd = passwd
        self.security = security
        self.radio = radio
        self.upstream = upstream
        station_list = LFUtils.port_name_series(prefix="sta",
                                                start_id=0,
                                                end_id=0,
                                                padding_number=10000,
                                                radio=radio)
        obj1 = STATION(lfclient_host=host, lfclient_port=8080, ssid=ssid, paswd=passwd, security=security, radio=radio, upstream=upstream, sta_list=station_list)
        var = obj1.json_get("/port/1/1/sta0000?fields=cx%20time%20(us)")
        var_1 = (var['interface']['cx time (us)'])
        return var_1

    def check_Radar_time(self, ip, user, pswd):
        tn = telnetlib.Telnet(ip)
        tn.read_until(b"Login: ")
        tn.write(user.encode("ascii") + b"\n")
        tn.read_until(b"Password: ")
        tn.write(pswd.encode('ascii') + b"\n")
        print("successfully connected to %s" % ip)
        tn.write(b"sh\n")
        tn.write()
        time.sleep(2)
        output = tn.read_very_eager()
        return output

    def ap_reboot(self, ip, user, pswd):
        tn = telnetlib.Telnet(ip)
        tn.read_until(b"Login: ")
        tn.write(user.encode("ascii") + b"\n")
        tn.read_until(b"Password: ")
        tn.write(pswd.encode('ascii') + b"\n")
        print("successfully connected to %s" % ip)
        tn.write(b"sh\n")
        tn.write(b"reboot\n")
        time.sleep(2)
        output = tn.read_very_eager()
        return output



def run():
    parser = argparse.ArgumentParser(description="Netgear AP DFS Test Script")
    parser.add_argument('--ip', type=str, help='AP ip', default="192.168.200.22")
    parser.add_argument('--user', type=str, help='credentials login/username', default="admin")
    parser.add_argument('--pswd', type=str, help='credential password', default="Password@123")
    parser.add_argument('--mgr', type=str, help='host name', default="localhost")
    parser.add_argument('--ssid', type=str, help='ssid for client',default="skydfs_5")
    parser.add_argument('--passwd', type=str, help='password to connect to ssid', default='[BLANK]')
    parser.add_argument( '--security', type=str, help='security', default='open')
    parser.add_argument('--radio', type=str, help='radio at which client will be connected', default='wiphy2')
    parser.add_argument('--upstream', type=str, help='provide eth1/eth2', default='eth1')
    parser.add_argument('-n', '--name', type=str, help='Type Name of AP on which test is performed')
    parser.add_argument('--fcctypes', nargs="+",
                        default=["FCC0", "FCC1", "FCC2", "FCC3", "FCC4", "FCC5", "ETSI1", "ETSI2", "ETSI3", "ETSI4",
                                 "ETSI5", "ETSI6"],
                        help='types needed to be tested {FCC0/FCC1/FCC2/FCC3/FCC4/FCC5/ETSI1/ETSI2/ETSI3/ETSI4/ETSI5/ETSI6}')
    parser.add_argument('--channel', nargs="+",
                        default=[52, 56, 60, 64, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140],
                        help='channel options need to be tested {52, 56, 60, 64, 100, 104, 108, 112, 116, 120, 124 ,128, 132, 136, 140}')
    # parser.add_argument('--model', type=str, help="provide type of AP model such as triband or dual band", default="dual")

    # script starts
    date1 = str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
    main_path = "/home/lanforge/html-reports/DFS_log"
    report_root = "/home/lanforge/html-reports/DFS_log" + "/" + str(date1)
    new_path = report_root + "/dfs.log"
    if path.exists(main_path):
        os.mkdir(report_root)
        print("Reports Root is Created")
    else:
        os.mkdir(main_path)
        os.mkdir(report_root)
        print("Reports Root is created")
    logging.basicConfig(filename=new_path, filemode='a',
                        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    """logging.basicConfig(filename='/home/lanforge/html-reports/dfs/dfs.log', filemode='w',
                        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')"""
    logging.warning('Test Started')
    test_time = datetime.now()
    test_time = test_time.strftime("%b %d %H:%M:%S")
    print("Test started at ", test_time)
    cmd = "Test started at " + str(test_time)
    logging.warning(str(cmd))
    # class instance
    args = parser.parse_args()
    dfs = DFS_TEST(ip=args.ip, user=args.user, pswd=args.pswd, host=args.mgr, ssid=args.ssid, passwd=args.passwd, security=args.security, radio=args.radio, upstream=args.upstream, fcctype=args.fcctypes,
                   channel=args.channel)

    # To create a stations
    channel_list = args.channel
    dfs.set_channel_in_ap_at_(channel=channel_list[0])
    time.sleep(30)
    # "FCC0", "FCC1", "FCC2", "FCC3", "FCC4", "FCC5", "ETSI1", "ETSI2", "ETSI3", "ETSI4", "ETSI5", "ETSI6"
    fcc_types = args.fcctypes
    result_data = dict.fromkeys(fcc_types)
    # set channel
    width_ = ""
    interval_ = ""
    count_ = ""

    logging.warning("creating station and generating traffic")
    dfs.create_station_cx()
    for fcc in fcc_types:
        if fcc == "FCC0":
            width = "1"
            interval = "1428"
            count = "18"
            width_ = width
            print("width", width_)
            interval_ = interval
            count_ = count
        elif fcc == "FCC1":
            width = "1"
            interval = "1163"
            count = "18"
            width_ = width
            interval_ = interval
            count_ = count
        elif fcc == "FCC2":
            width = "2"
            interval = "208"
            count = "28"
            width_ = width
            interval_ = interval
            count_ = count
        elif fcc == "FCC3":
            width = "7"
            interval = "365"
            count = "16"
            width_ = width
            interval_ = interval
            count_ = count
        elif fcc == "FCC4":
            width = "16"
            interval = "271"
            count = "12"
            width_ = width
            interval_ = interval
            count_ = count
        elif fcc == "FCC5":
            width = "70"
            interval = "1975"
            count = "3"
            width_ = width
            interval_ = interval
            count_ = count
        elif fcc == "ETSI1":
            width = "5"
            interval = "342"
            count = "10"
            width_ = width
            interval_ = interval
            count_ = count
        elif fcc == "ETSI2":
            width = "2"
            interval = "1271"
            count = "15"
            width_ = width
            interval_ = interval
            count_ = count
        elif fcc == "ETSI3":
            width = "15"
            interval = "3280"
            count = "25"
            width_ = width
            interval_ = interval
            count_ = count
        elif fcc == "ETSI4":
            width = "24"
            interval = "2477"
            count = "20"
            width_ = width
            interval_ = interval
            count_ = count
        elif fcc == "ETSI5":
            width = "1"
            interval = "356"
            count = "10"
            width_ = width
            interval_ = interval
            count_ = count
        elif fcc == "ETSI6":
            width = "2"
            interval = "1091"
            count = "15"
            width_ = width
            interval_ = interval
            count_ = count
        print(fcc)

        switched_ch_lst = []
        detection_time_lst = []
        connection_time_lst = []
        radar_lst = []

        # channel_list = ["52", "56", "60", "64", "100", "104", "108", "112", "116", "120", "124", "128", "132", "136",
        #                 "140"]
        channel_values = args.channel
        # print(channel_values)

        result_data[fcc] = dict.fromkeys(["switched_ch_lst", "radar_lst"])

        result_data[fcc]["switched_ch_lst"] = []
        result_data[fcc]["radar_lst"] = []

        # print("under", result_data)

        for channel_s in channel_values:

            print("set channel to ", channel_s)
            x = "set channel to " + str(channel_s)
            logging.warning(str(x))
            # monitor channel
            channel_before = dfs.monitor_station_before()
            print("channel before ", channel_before)
            print("set channel in ap")
            dfs.set_channel_in_ap_at_(channel=channel_s)
            print("channel set checking....")
            logging.warning('channel set checking....')

            print("now check primary channel from ap")
            primary_channel = dfs.check_primary_channel()
            print("after setting the command the ap is at channel ", primary_channel)
            print("now checking channel from lanforge")
            monitoring_station = dfs.monitor_station_(channel=str(channel_s), channel_before=channel_before)
            monitoring_station = str(monitoring_station)
            print(("channel set to ", monitoring_station))
            y = "channel set to " + str(monitoring_station)
            logging.warning(str(y))

            channel_s = str(channel_s)

            if monitoring_station == channel_s:
                print("station allocated to " + monitoring_station)
                z = "station allocated to " + str(monitoring_station)
                logging.warning(str(z))

                print("now generate radar on " + channel_s)
                q = "now generate radar on " + str(channel_s)
                logging.warning(str(q))

                frequency = {"52": "5260000", "56": "5280000", "60": "5300000", "64": "5320000", "100": "5500000",
                             "104": "5520000", "108": "5540000", "112": "5560000", "116": "5580000", "120": "5600000",
                             "124": "5620000",
                             "128": "5640000", "132": "5660000", "136": "5680000", "140": "5700000"}

                # now radar generate
                generating_radar = dfs.generate_radar_at_ch(width_, interval_, count_, frequency[channel_s])

                client_connection_time = dfs.client_connect_time(args.mgr, args.ssid, args.passwd, args.security,
                                                                 args.radio, args.upstream,  channel_s)
                print("client connection time ", client_connection_time)
                w = "client connection time " + str(client_connection_time)
                logging.warning(str(w))
                # connection_time_lst.append(client_connection_time)

                time.sleep(2)
                detecting_radar_channel = dfs.channel_after_radar(args.mgr, args.ssid, args.passwd,
                                                                  args.security,
                                                                  args.radio, args.upstream)
                if channel_s != detecting_radar_channel:
                    print("Radar detected on channel " + channel_s)
                    data = "YES"
                    radar_lst.append(data)
                    logging.warning("YES")
                    if data == "YES":

                        print("checking channel assigned...")

                        # print("after radar channel is at ", detecting_radar_channel)

                        if detecting_radar_channel == "-1" or detecting_radar_channel == "AUTO" or detecting_radar_channel == channel_s:
                            print("TEST Fail")
                            logging.warning("Test FAIL")
                            switched_ch_lst.append("X")
                            logging.warning("radar detected but  no switch")

                            continue
                        else:
                            print("Test Pass")
                            logging.warning("TEST PASS ")
                            pass_fail = "PASS"

                            ch_af_radar = detecting_radar_channel
                            print("after radar channel is at ", ch_af_radar)
                            Y = "after radar channel is at " + str(ch_af_radar)
                            logging.warning(str(Y))
                            switched_ch_lst.append(ch_af_radar)
                else:
                    data = "NO"
                    pass_fail = "FAIL"
                    radar_lst.append(data)
                    switched_ch_lst.append(" - ")
            else:
                # monitoring_station = str(monitoring_station)
                radar_lst.append("N/A")
                switched_ch_lst.append("N/A")


            print("switched channel list ", switched_ch_lst)
            s = "switched channel list " + str(switched_ch_lst)
            logging.warning(str(s))
            print("radar detection list", radar_lst)
            r = "radar detection list" + str(radar_lst)
            logging.warning(str(r))


        result_data[fcc]["switched_ch_lst"] = switched_ch_lst
        result_data[fcc]["radar_lst"] = radar_lst

        print("result ", result_data)
        res = "result " + str(result_data)
        logging.warning(str(res))
        # time.sleep(1800)
        logging.warning("Doing AP reboot ")
        print("Doing AP reboot ")
        dfs.ap_reboot(args.ip, args.user, args.pswd)
        print("wait for 4 mins")
        time.sleep(240)

    print("final result", result_data)
    res = "final result " + str(result_data)

    logging.warning(str(res))
    print("Test Finished")
    test_end = datetime.now()
    test_end = test_end.strftime("%b %d %H:%M:%S")
    print("Test ended at ", test_end)

    s1 = test_time
    s2 = test_end  # for example
    FMT = '%b %d %H:%M:%S'
    test_duration = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
    print("total test duration ", test_duration)

    # # Try changing values for the same
    date = str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
    model_name = "skyAP"
    test_setup_info = {
        "AP Name": model_name,
        "SSID": args.ssid,
        "Number of Stations": "1",
        "Test Duration": test_duration
    }

    input_setup_info = {
        "IP": args.ip,
        "user": args.user,
        "Radartypes": args.fcctypes,
        "Channel": args.channel,
        "Contact": "support@candelatech.com"
    }
    print("going to generate report")
    generate_report(result_data,
                    date,
                    test_setup_info,
                    input_setup_info,
                    test_channel=channel_values,
                    graph_path="/home/lanforge/html-reports/dfs")

    graph_path = "/home/lanforge/html-reports/dfs"

if __name__ == '__main__':
    run()
