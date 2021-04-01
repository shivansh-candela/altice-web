"""how to run - --mgr 192.168.200.13 --upstream_port eth2 --num_stations 40 --security open --ssid Nikita --passwd [BLANK] --target_per_ten 1 """
import sys
if 'py-json' not in sys.path:
    sys.path.append('../py-json')
from LANforge import LFUtils
from LANforge import lfcli_base
from LANforge.lfcli_base import LFCliBase
from LANforge.LFUtils import *
import realm
from realm import Realm
from realm import PortUtils
import argparse
import datetime
import time
import os
from webpage_report import *

class HTTPDOWNLOAD(Realm):
    def __init__(self, lfclient_host, lfclient_port, upstream, num_sta, security, ssid, password, url, target_per_ten, bands,start_id=0, _debug_on=False, _exit_on_error=False, _exit_on_fail=False):
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
        self.bands = bands
        print("in",bands)


        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()
        self.http_profile = self.local_realm.new_http_profile()
        self.http_profile.requests_per_ten = self.target_per_ten

        self.http_profile.url = self.url
        #self.http_profile.direction = 'dl'
        #self.http_profile.dest = '/dev/null'
        self.port_util = PortUtils(self.local_realm)
        self.http_profile.debug = _debug_on
        self.created_cx = {}
        #print("hi",radio)

    def set_values(self):
        # This method will set values according user input
        if self.bands == "5G":
            self.radio = ["wiphy0"]
            print("hi", self.radio)
        elif self.bands == "2.4G":
            self.radio = ["wiphy1"]
        elif self.bands == "Both":
            self.radio = ["wiphy0", "wiphy1"]
            print("hello", self.radio)
            self.num_sta = self.num_sta // 2

    def precleanup(self):
        self.count = 0
        try:
            self.local_realm.load("BLANK")
        except:
            print("couldn't load 'BLANK' Test Configuration")

        #print("hi", self.radio)
        for rad in self.radio:
            if rad == "wiphy0":
                # select an mode
                self.station_profile.mode = 10
                self.count = self.count + 1
            elif rad == "wiphy1":
                # select an mode
                self.station_profile.mode = 6
                self.count = self.count + 1
            # check Both band if both band then for 2G station id start with 20
            if self.count == 2:
                self.sta_start_id = self.num_sta
                self.num_sta = 2 * (self.num_sta)
                self.station_profile.mode = 10
                self.http_profile.cleanup()
                # create station list with sta_id 20

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

        for rad in self.radio:

            # station build
            self.station_profile.use_security(self.security, self.ssid, self.password)
            #self.station_profile.set_nustation_listmber_template("00")
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
            self.http_profile.create(ports=self.station_profile.station_names, sleep_time=.5,
                                     suppress_related_commands_=None, http=True,
                                     http_ip='192.168.208.202/webpagetesting.html')
            if self.count == 2:
                self.station_list = self.station_list1
                self.station_profile.mode = 6
        print("Test Build done")

    def start(self, print_pass=False, print_fail=False):
        print("Test Started")
        for rad in self.radio:
            self.http_profile.start_cx()

    def my_monitor(self):
        # data in json format
        data = self.local_realm.json_get("layer4/list?fields=uc-avg")
        data1 = []
        for i in range(len(data['endpoint'])):
            data1.append(str(list(data['endpoint'][i]))[2:-2])
        #print(data1)
        data2 = []
        for i in range(self.num_sta):
            data = self.local_realm.json_get("layer4/list?fields=uc-avg")
            #print(type(data['endpoint'][i][data1[i]]['uc-avg']))
            data2.append((data['endpoint'][i][data1[i]]['uc-avg']))

        #print("downloading time for all clients", data2)
        return data2
    def postcleanup(self):
        # for rad in self.radio
        self.http_profile.cleanup()
        self.station_profile.cleanup()
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)
def main():
    parser = argparse.ArgumentParser(description="Netgear webpage download Test Script")
    parser.add_argument('--mgr', help='hostname for where LANforge GUI is running', default='localhost')
    parser.add_argument('--mgr_port', help='port LANforge GUI HTTP service is running on', default=8080)
    parser.add_argument('--upstream_port', help='non-station port that generates traffic: eg: eth1', default='eth2')
    parser.add_argument('--num_stations', type=int, help='number of stations to create', default=1)
    #parser.add_argument('--radio', help='wiphy radio eg wiphy0', default='wiphy0')
    parser.add_argument('--security', help='WiFi Security protocol: {open|wep|wpa2|wpa3')
    parser.add_argument('--ssid', help='WiFi SSID for script object to associate to')
    parser.add_argument('--passwd', help='WiFi passphrase/password/key')
    parser.add_argument('--url', help='url on which you want to test HTTP')
    parser.add_argument('--target_per_ten', help='number of request per 10 minutes', default=100)
    parser.add_argument('--bands', nargs="+", help='--bands', default=["5G", "2.4G", "Both"])

    args = parser.parse_args()
    test_time = datetime.now()
    test_time = test_time.strftime("%b %d %H:%M:%S")
    print("Test started at ", test_time)
    """list5G = []
    list2G = []
    Both = []
    dict_keys = []
    dict_keys.extend(args.bands)
    #print(dict_keys)
    final_dict = dict.fromkeys(dict_keys)
    #print(final_dict)
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
    for bands in args.bands:
        http = HTTPDOWNLOAD(lfclient_host=args.mgr, lfclient_port=args.mgr_port,
                                upstream=args.upstream_port, num_sta=args.num_stations,
                                security=args.security,
                                ssid=args.ssid, password=args.passwd,
                                url=args.url, target_per_ten=args.target_per_ten,
                                bands=bands)
        http.set_values()
        http.precleanup()
        http.build()
        http.start()
        time.sleep(90)
        value = http.my_monitor()
        print("hi", value)
        #print(type(value))
        if bands == "5G":
            list5G.extend(value)
            #print("5G", list5G)
            final_dict['5G']['dl_time']=list5G
            min5.append(min(list5G))
            final_dict['5G']['min'] = min5
            max5.append(max(list5G))
            final_dict['5G']['max'] = max5
            avg5.append((sum(list5G) / 40 ))
            final_dict['5G']['avg'] = avg5
        elif bands == "2.4G":
            list2G.extend(value)
            print("2.4G", list2G)
            final_dict['2.4G']['dl_time'] = list2G
            min2.append(min(list2G))
            final_dict['2.4G']['min'] = min2
            max2.append(max(list2G))
            final_dict['2.4G']['max'] = max2
            avg2.append((sum(list2G) / 40 ))
            final_dict['2.4G']['avg'] = avg2
        elif bands == "Both":
            Both.extend(value)
            print("both", Both)
            final_dict['Both']['dl_time'] = Both
            min_both.append(min(Both))
            final_dict['Both']['min'] = min_both
            max_both.append(max(Both))
            final_dict['Both']['max'] = max_both
            avg_both.append((sum(Both) / 40 ))
            final_dict['Both']['avg'] = avg_both
    print("final list", final_dict)"""
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
    test_setup_info = {
        "AP Name": "WAC550",
        "SSID": args.ssid,
        "Test Duration": test_duration
    }
    input_setup_info = {
        "Contact": "support@candelatech.com"
    }
    result_data= {'5G': {'dl_time': [4340.0, 8839.0, 8791.0, 21684.0, 21751.0, 24364.0, 23468.0, 24124.0, 21777.0, 19207.0, 18648.0, 22455.0, 22336.0, 23934.0, 21399.0, 23753.0, 12710.0, 23106.0, 23274.0, 23504.0, 22602.0, 23327.0, 16480.0, 22186.0, 20049.0, 15550.0, 22759.0, 22688.0, 20029.0, 15926.0, 22445.0, 21651.0, 21665.0, 13764.0, 16350.0, 13496.0, 13818.0, 14687.0, 17213.0, 13693.0], 'min': [4340.0], 'max': [24364.0], 'avg': [19096.05]}, '2.4G': {'dl_time': [81702.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 17186.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 56628.0, 54969.0, 80200.0, 0.0, 62977.0, 0.0, 75654.0, 0.0, 0.0, 17339.0, 11116.0, 0.0, 14578.0, 11438.0, 15462.0, 13841.0, 14810.0, 14234.0, 16704.0, 14606.0, 12161.0, 0.0, 18978.0, 0.0], 'min': [0.0], 'max': [81702.0], 'avg': [15114.575]}, 'Both': {'dl_time': [2916.0, 6322.0, 6456.0, 6834.0, 10353.0, 10718.0, 10830.0, 9495.0, 11167.0, 9392.0, 10779.0, 10658.0, 10992.0, 10510.0, 8343.0, 8737.0, 8836.0, 8871.0, 9176.0, 10180.0, 0.0, 0.0, 75126.0, 0.0, 0.0, 79886.0, 77712.0, 0.0, 89331.0, 0.0, 75184.0, 0.0, 0.0, 0.0, 0.0, 57581.0, 0.0, 0.0, 0.0, 0.0], 'min': [0.0], 'max': [89331.0], 'avg': [15909.625]}}
    generate_report(result_data= result_data,
                    date=date,
                    test_setup_info= test_setup_info,
                    input_setup_info=input_setup_info,
                    graph_path="/home/lanforge/html-reports/Loadbalancing")

if __name__ == '__main__':
    main()

