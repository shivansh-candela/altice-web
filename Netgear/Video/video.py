""" how to run - python3 lf_webpage.py --mgr localhost --upstream_port eth1 --num_stations 40 --security open --ssid Nikita --passwd [BLANK]
 --target_per_ten 1 --url 192.168.212.225/webpagetesting.html  --bands 5G"""
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
#from datetime import datetime
import time
import os
import paramiko
from itertools import groupby
#from webpage_report import *

class VideoStreaming(Realm):
    def __init__(self, lfclient_host, lfclient_port, upstream, num_sta, security, ssid, password, url,
                 target_per_ten, max_speed,file_size, bands,start_id=0, _debug_on=False, _exit_on_error=False, _exit_on_fail=False):
        self.host = lfclient_host
        self.port = lfclient_port
        self.lfclient_url = "http://%s:%s" % (lfclient_host, lfclient_port)
        self.proxy = {}
        self.exit_on_error = _exit_on_error
        self.exit_on_fail = _exit_on_fail
        self.upstream = upstream
        self.num_sta = num_sta
        #self.radio = radio
        self.security = security
        self.ssid = ssid
        self.sta_start_id = start_id
        self.password = password
        self.url = url
        self.target_per_ten = target_per_ten
        self.max_speed = max_speed
        self.file_size = file_size
        self.bands = bands
        print("in",bands)
        self.debug = _debug_on


        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()
        self.station_profile.debug = self.debug
        self.http_profile = self.local_realm.new_http_profile()
        self.http_profile.requests_per_ten = self.target_per_ten
        self.http_profile.max_speed = self.max_speed

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
                                     http_ip=self.url)

            if self.count == 2:
                self.station_list = self.station_list1
                self.station_profile.mode = 8
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
        print("Test Started")

    def monitor(self,
                duration_sec,
                monitor_interval,
                created_cx,
                col_names,
                iterations):
        #sta_list = self.station_list

        try:
            duration_sec = Realm.parse_time(duration_sec).seconds
        except:
            if (duration_sec is None) or (duration_sec <= 1):
                raise ValueError("L4CXProfile::monitor wants duration_sec > 1 second")
            if (duration_sec <= monitor_interval):
                raise ValueError("L4CXProfile::monitor wants duration_sec > monitor_interval")
        if created_cx == None:
            raise ValueError("Monitor needs a list of Layer 4 connections")
        if (monitor_interval is None) or (monitor_interval < 1):
            raise ValueError("L4CXProfile::monitor wants monitor_interval >= 1 second")

        #assign column names
        if col_names is not None and len(col_names) > 0:
            print(col_names)
            header_row=col_names
            print("hi",header_row)
        else:
            header_row=list((list(self.json_get("/layer4/all")['endpoint'][0].values())[0].keys()))
            print(header_row)

        #monitor columns
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(seconds=duration_sec)
        #sleep_interval = round(duration_sec // 5)

        rx_rate = []
        for test in range(1 + iterations):
            while datetime.datetime.now() < end_time:
                if col_names is None:
                    response = self.json_get("/layer4/all")
                else:
                    fields = ",".join(col_names)
                    created_cx_ = ",".join(created_cx)

                    response = self.json_get("/layer4/%s?fields=%s" % (created_cx_, fields))
                    print(response['endpoint'])
                    endpt = response['endpoint']
                    for i in endpt:
                        print(list(i.keys()))
                        name = list(i.keys())[0]
                        print(i[name]['rx rate'])
                        rx_rate.append(i[name]['rx rate'])

                time.sleep(monitor_interval)

        #rx_rate list is calculated
        print("rx rate values are ", rx_rate)

        return rx_rate

    """def my_monitor(self):
        # data in json format
        data1 = []
        #for j in range(3600):

        data = self.local_realm.json_get("layer4/list?fields=rx rate")

        for i in range(len(data['endpoint'])):
            data1.append(str(list(data['endpoint'][i]))[2:-2])
        time.sleep(1)
        print("only data", data1)
        data2 = []
        for i in range(self.num_sta):
            data = self.local_realm.json_get("layer4/list?fields=rx rate")
            #print(type(data['endpoint'][i][data1[i]]['uc-avg']))
            data2.append((data['endpoint'][i][data1[i]]['rx rate']))

        print(data2)
        #print("downloading time for all clients", data2)
        return data2"""
    def postcleanup(self):
        # for rad in self.radio
        self.http_profile.cleanup()
        self.station_profile.cleanup()
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)

    def file_create(self):
        os.chdir('/usr/local/lanforge/nginx/html/')
        if os.path.isfile("/usr/local/lanforge/nginx/html/video.txt"):
            os.system("sudo rm /usr/local/lanforge/nginx/html/video.txt")
        os.system("sudo fallocate -l " + self.file_size + " /usr/local/lanforge/nginx/html/video.txt")
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
    parser = argparse.ArgumentParser(description="Netgear Video streaming Test Script")
    parser.add_argument('--mgr', help='hostname for where LANforge GUI is running', default='localhost')
    parser.add_argument('--mgr_port', help='port LANforge GUI HTTP service is running on', default=8080)
    parser.add_argument('--upstream_port', help='non-station port that generates traffic: eg: eth1', default='eth1')
    parser.add_argument('--num_stations', type=int, help='number of stations to create', default=1)
    parser.add_argument('--security', help='WiFi Security protocol: {open|wep|wpa2|wpa3')
    parser.add_argument('--ssid', help='WiFi SSID for script object to associate to')
    parser.add_argument('--passwd', help='WiFi passphrase/password/key')
    parser.add_argument('--url', type=str, help='url on which you want to test HTTP')
    parser.add_argument('--target_per_ten', help='number of request per 10 minutes', default=100)
    parser.add_argument('--max_speed', nargs="+", help='provide the maximum speed',
                        default=[1000000, 2000000, 3000000, 4000000, 5000000])
    parser.add_argument('--bands', nargs="+", help='--bands', default=["5G",  "Both"])
    parser.add_argument('--file_size',type=str, help='specify the size of file you want to download', default='10Mb')
    parser.add_argument('--duration', type=int, help='mention the time interval you want to check the values for cx in secs', default=2)
    parser.add_argument('--ap_ip', type=str, help="mention th AP ip for ssh ", default="192.168.208.201")
    parser.add_argument('--user', type=str, help='credentials ap login/username', default='root')
    parser.add_argument( '--pswd', type=str, help='credential password', default='Netgear@123xzsawq@!')


    args = parser.parse_args()
    ap = AP_automate(args.ap_ip, args.user, args.pswd)
    speed_dict = {}
    print(type(args.max_speed))

    speed_dict = dict.fromkeys(args.max_speed)
    print(speed_dict)


    for bands in args.bands:
        for speed in args.max_speed:
            http = VideoStreaming(lfclient_host=args.mgr, lfclient_port=args.mgr_port,
                                    upstream=args.upstream_port, num_sta=args.num_stations,
                                    security=args.security,
                                    ssid=args.ssid, password=args.passwd,
                                    url=args.url, target_per_ten=args.target_per_ten, max_speed=speed,
                                    file_size=args.file_size,bands=bands, _debug_on=True)
            # calculate threshold
            number = speed
            print(int(number))
            per = 0.7 * float(number)
            print(int(per))
            threshold = int(per)
            print("threshold is", threshold)

            #http.file_create()
            http.set_values()
            http.precleanup()
            time.sleep(2)

            time.sleep(6)
            http.build()
            time.sleep(20)
            http.start()
            time.sleep(20)
            layer4connections = []
            for i in http.json_get('/layer4/')['endpoint']:
                #print(list(i.keys())[0])
                layer4connections.append(list(i.keys())[0])
            print(layer4connections)


            rx_rate = http.monitor(duration_sec=args.duration,
                                   monitor_interval=1,
                                   col_names=['rx rate'],
                                   created_cx=layer4connections,
                                   iterations=0)
            print("list of rx rate", rx_rate)

            # divide the list into number of endpoints, Yield successive n-sized chunks from l.
            def divide_chunks(l, n):

                # looping till length l
                for i in range(0, len(l), n):
                    yield l[i:i + n]

            # How many elements each list should have
            n = args.num_stations

            divided_list= list(divide_chunks(rx_rate, n))
            print(divided_list)

            #creating number of endpoints name  list
            num_sta = args.num_stations
            endp_name_lst = []
            for i in range(0, num_sta):
                var = "endp" + str(i)
                endp_name_lst.append(var)

            print(endp_name_lst)
            #dictionary of name list
            endp_dict = dict.fromkeys(endp_name_lst)
            print(endp_dict)
            for i in endp_dict:
                endp_dict[i] = []

            for i in divided_list:
                for index, key in enumerate(endp_dict):
                    # print(index, key)
                    endp_dict[key].append(i[index])

            print(endp_dict)
            #print(endp_dict['endp0'])

            # print(endp_dict['endp0'])
            final_data = dict.fromkeys(endp_dict.keys())
            for k in endp_dict.keys():
                grouped_L = [(k, sum(1 for i in g)) for k, g in groupby(endp_dict[k])]
                flag = 0
                for i in grouped_L:  #
                    if not i[0]:
                        if i[1] >= 5:
                            # print(i)
                            # print(i[1]/5)
                            flag += i[1] / 5  # flag = flag + i[1]/5
                            # print(flag)
                final_data[k] = int(flag)
                # print(flag)
            print("number of buffers in all endpoints",final_data)

            print(speed)
            print(type(speed))

            if speed == '1000000':
                print("yes")
                speed_dict['1000000'] = final_data
            elif speed == '2000000':
                speed_dict['2000000'] = final_data
            elif speed == '3000000':
                speed_dict['3000000'] = final_data
            elif speed == '4000000':
                speed_dict['4000000'] = final_data
            elif speed  == '5000000':
                speed_dict['5000000'] = final_data

    print(speed_dict)







if __name__ == '__main__':
    main()
