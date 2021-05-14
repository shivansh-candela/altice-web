"""
This script will create 40 clients on 5Ghz , 2.4Ghz and Both and generate layer4 traffic on LANforge ,The Webpage Download Test is designed to test the performance of the  Access Point.The goal is to  check whether the
webpage loading time meets the expectation when clients connected on single radio as well as dual radio.

how to run -
sudo python3 web.py --upstream_port eth1 --num_stations 40 --security open --ssid ASUSAP --passwd [BLANK] --target_per_ten 1 --bands 5G  --file_size 10Mb  --fiveg_radio wiphy0 --twog_radio wiphy1 --duration 1
Copyright 2021 Candela Technologies Inc
04 - April - 2021
"""

import sys
import argparse
from datetime import datetime
import time
import os
import paramiko

if 'py-json' not in sys.path:
    sys.path.append('../py-json')
from LANforge import LFUtils
from LANforge import lfcli_base
from LANforge.lfcli_base import LFCliBase
from LANforge.LFUtils import *
import realm
from realm import Realm
from realm import PortUtils
from webpage_report import *

class HTTPDOWNLOAD(Realm):
    def __init__(self, lfclient_host, lfclient_port, upstream, num_sta, security, ssid, password, url,
                 target_per_ten, file_size, bands, start_id=0, _debug_on=False, _exit_on_error=False,
                 _exit_on_fail=False):
        self.host = lfclient_host
        self.port = lfclient_port
        self.upstream = upstream
        self.num_sta = num_sta
        #self.radio = radio
        self.security = security
        self.ssid = ssid
        self.sta_start_id = start_id
        self.password = password
        self.url = url
        self.target_per_ten = target_per_ten
        self.file_size = file_size
        self.bands = bands
        self.debug = _debug_on
        print(bands)

        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()
        self.http_profile = self.local_realm.new_http_profile()
        self.http_profile.requests_per_ten = self.target_per_ten
        self.http_profile.url = self.url
        self.port_util = PortUtils(self.local_realm)
        self.http_profile.debug = _debug_on
        self.created_cx = {}

    def set_values(self,radio1, radio2):
        # This method will set values according user input
        if self.bands == "5G":
            self.radio = [radio1]
            print("hi", self.radio)
        elif self.bands == "2.4G":
            self.radio = [radio2]
        elif self.bands == "Both":
            self.radio = [radio1, radio2]
            print("hello", self.radio)
            self.num_sta = self.num_sta // 2

    def precleanup(self, radio1, radio2):
        self.count = 0
        try:
            self.local_realm.load("BLANK")
        except:
            print("couldn't load 'BLANK' Test Configuration")

        print("hi", self.radio)
        if self.bands == "5G":
            self.radio = [radio1]
        elif self.bands == "2.4G":
            self.radio = [radio2]
        elif self.bands == "Both":
            self.radio = [radio1, radio2]
            print("hello", self.radio)

        for rad in self.radio:
            print("radio", rad)
            if rad == radio1:
                # select an mode
                self.station_profile.mode = 10
                self.count = self.count + 1
            elif rad == radio2:
                # select an mode
                self.station_profile.mode = 6
                self.count = self.count + 1

            if self.count == 2:
                self.sta_start_id = self.num_sta
                self.num_sta = 2 * (self.num_sta)
                self.station_profile.mode = 10
                self.http_profile.cleanup()
                self.station_list1 = LFUtils.portNameSeries(prefix_="sta", start_id_=self.sta_start_id,
                                                            end_id_=self.num_sta - 1, padding_number_=10000,
                                                            radio=rad)
                # cleanup station list which started sta_id 20
                self.station_profile.cleanup(self.station_list1, debug_=self.local_realm.debug)
                LFUtils.wait_until_ports_disappear(base_url=self.local_realm.lfclient_url,
                                                   port_list=self.station_list,
                                                   debug=self.local_realm.debug)
                return
            # clean dlayer4 ftp traffic
            self.http_profile.cleanup()
            self.station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=self.sta_start_id,
                                                       end_id_=self.num_sta - 1, padding_number_=10000,
                                                       radio=rad)
            # cleans stations
            self.station_profile.cleanup(self.station_list, delay=1, debug_=self.local_realm.debug)
            LFUtils.wait_until_ports_disappear(base_url=self.local_realm.lfclient_url,
                                               port_list=self.station_list,
                                               debug=self.local_realm.debug)
            time.sleep(1)
        print("precleanup done")

    def build(self):
        self.port_util.set_http(port_name=self.local_realm.name_to_eid(self.upstream)[2], resource=1, on=True)
        data = {
            "shelf": 1,
            "resource": 1,
            "port": "eth1",
            "current_flags": 2147483648,
            "interest": 16384

        }
        url = "/cli-json/set_port"
        self.local_realm.json_post(url, data, debug_=True)
        time.sleep(10)

        for rad in self.radio:

            # station build
            self.station_profile.use_security(self.security, self.ssid, self.password)
            # self.station_profile.set_nustation_listmber_template("00")
            self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
            self.station_profile.set_command_param("set_port", "report_timer", 1500)
            self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
            self.station_profile.create(radio=rad, sta_names_=self.station_list, debug=self.local_realm.debug)
            self.local_realm.wait_until_ports_appear(sta_list=self.station_list)
            self.station_profile.admin_up()
            if self.local_realm.wait_for_ip(self.station_list):
                self.local_realm._pass("All stations got IPs")
            else:
                self.local_realm._fail("Stations failed to get IPs")
            # building layer4
            self.http_profile.direction = 'dl'
            self.http_profile.dest = '/dev/null'
            data = self.local_realm.json_get("ports/list?fields=IP")

            for i in data["interfaces"]:
                for j in i:
                    if "1.1." + self.upstream == j:
                        ip_upstream = i["1.1." + self.upstream]['ip']
            self.http_profile.create(ports=self.station_profile.station_names, sleep_time=.5,
                                     suppress_related_commands_=None, http=True,
                                     http_ip=ip_upstream + "/webpage.html")
            if self.count == 2:
                self.station_list = self.station_list1
                self.station_profile.mode = 6
        print("Test Build done")

    def start(self, print_pass=False, print_fail=False):
        print("Test Started")
        self.http_profile.start_cx()
        try:
            for i in self.http_profile.created_cx.keys():
                while self.local_realm.json_get("/cx/" + i).get(i).get('state') != 'Run':
                    continue
        except Exception as e:
            pass

    def my_monitor(self):
        # data in json format
        data = self.local_realm.json_get("layer4/list?fields=uc-avg")
        data1 = []
        for i in range(len(data['endpoint'])):
            data1.append(str(list(data['endpoint'][i]))[2:-2])
        # print(data1)
        data2 = []
        for i in range(self.num_sta):
            data = self.local_realm.json_get("layer4/list?fields=uc-avg")
            # print(type(data['endpoint'][i][data1[i]]['uc-avg']))
            data2.append((data['endpoint'][i][data1[i]]['uc-avg']))

        # print("downloading time for all clients", data2)
        return data2

    def postcleanup(self):
        # for rad in self.radio
        self.http_profile.cleanup()
        self.station_profile.cleanup()
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)

    def file_create(self):
        os.chdir('/usr/local/lanforge/nginx/html/')
        if os.path.isfile("/usr/local/lanforge/nginx/html/webpage.html"):
            os.system("sudo rm /usr/local/lanforge/nginx/html/webpage.html")
        os.system("sudo fallocate -l " + self.file_size + " /usr/local/lanforge/nginx/html/webpage.html")
        print("File creation done", self.file_size)

class AP_automate:
    def __init__(self, ap_ip, user, pswd):
        self.ap_ip = ap_ip
        self.user = user
        self.pswd = pswd

    def get_ap_model(self, ap_ip, user, pswd):
        self.ap_ip = ap_ip
        self.user = user
        self.pswd = pswd
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(ap_ip, port=22, username=user, password=pswd)
        stdin, stdout, stderr = ssh.exec_command('printmd')
        output = stdout.readlines()
        ssh.close()
        return output


def main():
    parser = argparse.ArgumentParser(description="Netgear webpage download Test Script")
    parser.add_argument('--mgr', help='hostname for where LANforge GUI is running', default='localhost')
    parser.add_argument('--mgr_port', help='port LANforge GUI HTTP service is running on', default=8080)
    parser.add_argument('--upstream_port', help='non-station port that generates traffic: eg: eth1', default='eth2')
    parser.add_argument('--num_stations', type=int, help='number of stations to create', default=1)
    parser.add_argument('--twog_radio', help='specify radio for 2.4G clients', default='wiphy3')
    parser.add_argument('--fiveg_radio', help='specify radio for 5 GHz client', default='wiphy0')
    parser.add_argument('--security', help='WiFi Security protocol: {open|wep|wpa2|wpa3')
    parser.add_argument('--ssid', help='WiFi SSID for script object to associate to')
    parser.add_argument('--passwd', help='WiFi passphrase/password/key')
    parser.add_argument('--target_per_ten', help='number of request per 10 minutes', default=100)
    parser.add_argument('--file_size', type=str, help='specify the size of file you want to download', default='5Mb')
    parser.add_argument('--bands', nargs="+", help='--bands', default=["5G", "2.4G", "Both"])
    parser.add_argument('--ap_ip', type=str, help="mention th AP ip for ssh ", default="192.168.208.201")
    parser.add_argument('--user', type=str, help='credentials ap login/username', default='root')
    parser.add_argument('--pswd', type=str, help='credential password', default='Netgear@123xzsawq@!')
    parser.add_argument('--duration', type=int, help='time to run traffic')

    args = parser.parse_args()
    test_time = datetime.now()
    test_time = test_time.strftime("%b %d %H:%M:%S")
    print("Test started at ", test_time)
    list5G = []
    list2G = []
    Both = []
    dict_keys = []
    dict_keys.extend(args.bands)
    # print(dict_keys)
    final_dict = dict.fromkeys(dict_keys)
    # print(final_dict)
    dict1_keys = ['dl_time', 'min', 'max', 'avg']
    for i in final_dict:
        final_dict[i] = dict.fromkeys(dict1_keys)
    print(final_dict)
    min5 = []
    min2 = []
    min_both = []
    max5 = []
    max2 = []
    max_both = []
    avg2 = []
    avg5 = []
    avg_both = []

    ap = AP_automate(args.ap_ip, args.user, args.pswd)
    for bands in args.bands:
        http = HTTPDOWNLOAD(lfclient_host=args.mgr, lfclient_port=args.mgr_port,
                            upstream=args.upstream_port, num_sta=args.num_stations,
                            security=args.security,
                            ssid=args.ssid, password=args.passwd,
                            url=args.url, target_per_ten=args.target_per_ten,
                            file_size=args.file_size, bands=bands)
        http.file_create()
        http.set_values(radio1=args.fiveg_radio,radio2=args.twog_radio)
        http.precleanup(radio1=args.fiveg_radio,radio2=args.twog_radio)
        http.build()
        http.start()
        duration = args.duration
        duration = 60 * duration
        print("time in seconds ", duration)
        time.sleep(duration)
        value = http.my_monitor()
        #print("hi", value)
        # print(type(value))
        if bands == "5G":
            list5G.extend(value)
            # print("5G", list5G)
            final_dict['5G']['dl_time'] = list5G
            min5.append(min(list5G))
            final_dict['5G']['min'] = min5
            max5.append(max(list5G))
            final_dict['5G']['max'] = max5
            avg5.append((sum(list5G) / 40))
            final_dict['5G']['avg'] = avg5
        elif bands == "2.4G":
            list2G.extend(value)
            print("2.4G", list2G)
            final_dict['2.4G']['dl_time'] = list2G
            min2.append(min(list2G))
            final_dict['2.4G']['min'] = min2
            max2.append(max(list2G))
            final_dict['2.4G']['max'] = max2
            avg2.append((sum(list2G) / 40))
            final_dict['2.4G']['avg'] = avg2
        elif bands == "Both":
            Both.extend(value)
            print("both", Both)
            final_dict['Both']['dl_time'] = Both
            min_both.append(min(Both))
            final_dict['Both']['min'] = min_both
            max_both.append(max(Both))
            final_dict['Both']['max'] = max_both
            avg_both.append((sum(Both) / 40))
            final_dict['Both']['avg'] = avg_both
    print("final list", final_dict)
    print("Test Finished")
    test_end = datetime.now()
    test_end = test_end.strftime("%b %d %H:%M:%S")
    print("Test ended at ", test_end)
    s1 = test_time
    s2 = test_end  # for example
    FMT = '%b %d %H:%M:%S'
    test_duration = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
    print("total test duration ", test_duration)
    date = str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
    # model = ap.get_ap_model(args.ap_ip, args.user, args.pswd)
    # model_name = model[0][12:]
    test_setup_info = {
        "AP Name": "R7800",
        "SSID": args.ssid,
        "Test Duration": test_duration
    }
    input_setup_info = {
        "Contact": "support@candelatech.com"
    }
    band = args.bands

    generate_report(final_dict,
                    date,
                    test_setup_info,
                    input_setup_info,
                    band,
                    graph_path="/home/lanforge/html-reports/Webpage")

if __name__ == '__main__':
    main()