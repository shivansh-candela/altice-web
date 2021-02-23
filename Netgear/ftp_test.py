#ftp download and upload
import sys
if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)
if 'py-json' not in sys.path:
    sys.path.append('../py-json')

from LANforge import LFUtils
from LANforge import lfcli_base
from LANforge.lfcli_base import LFCliBase
from LANforge.LFUtils import *
import realm
from realm import Realm
import argparse
import datetime
import time
import os

class ftp_test(LFCliBase):
    
     obj = ftp_test(lfclient_host=args.mgr,
                    lfclient_port=args.mgr_port,
                    dut_ssid=args.ssid,
                    dut_passwd=args.passwd,
                    dut_security=args.security,
                    num_sta=args.client,
                    file_size=args.file_size,
                    direction=args.direction            

    def __init__(self, lfclient_host="localhost", lfclient_port=8080,dut_radio=None, sta_prefix="sta", start_id=0, num_sta= None, radio=None,
                 dut_ssid=None,dut_security=None, dut_passwd=None, file_size=None,upstream="eth1",_debug_on=False, _exit_on_error=False,  _exit_on_fail=False, direction= None):
        super().__init__(lfclient_host, lfclient_port, _debug=_debug_on, _halt_on_error=_exit_on_error, _exit_on_fail=_exit_on_fail)
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
        self.requests_per_ten = 600
        self.file_size=file_size
        self.direction=direction
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()
        self.cx_profile = self.local_realm.new_http_profile()
        self.port_util = realm.PortUtils(self.local_realm)
        self.cx_profile.requests_per_ten = self.requests_per_ten
        self.station_profile.mode = 0

        print("Test is Initialized")


    def precleanup(self):

        #clean layer4 ftp traffic
        self.cx_profile.cleanup()
        self.station_list = LFUtils.portNameSeries(prefix_=self.sta_prefix, start_id_=self.sta_start_id,
                                                   end_id_=self.num_sta - 1, padding_number_=10000,
                                                   radio=self.radio)

        #cleans stations
        self.station_profile.cleanup(self.station_list , debug_=self.debug)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                           port_list=self.station_list,
                                           debug=self.debug)
        time.sleep(1)
        print("precleanup done")

    def build(self):

        #set ftp
        self.port_util.set_ftp(port_name=self.local_realm.name_to_eid(self.upstream_port)[2], resource=1, on=True)

        #station build
        self.station_profile.use_security(self.security, self.ssid, self.password)
        self.station_profile.set_number_template("00")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.create(radio=self.radio, sta_names_=self.station_list, debug=self.debug)
        self.local_realm.wait_until_ports_appear(sta_list=self.station_list)

        #building layer4
        self.cx_profile.direction ="dl"
        self.cx_profile.dest = "/dev/null"

        if self.direction == "download":
            self.cx_profile.create(ports=self.station_profile.station_names, ftp_ip="192.168.1.59/jk.txt",
                                    sleep_time=.5,debug_=self.debug,suppress_related_commands_=True, ftp=True, user="lanforge",
                                    passwd="lanforge", source="")
        elif self.direction == "upload":
            data1 = []
            data2 = {}

            #reading data for getting ip"s of stations
            data = self.json_get("ports/list?fields=IP")

            for i in range(len(self.sta_list) + 6):
                #getting station names as keys from json data
                data1.append((str(list(data['interfaces'][i].keys())))[2:-2])

                #creating dictionary of station name and ip's
                data2[data1[i]] = data['interfaces'][i][data1[i]]['ip']

            #dictionary of stations name and ip"s
            dict_sta_ip = dict(list(data2.items())[6:])

            print(dict_sta_ip)

            #list of ip's
            ip = list(dict_sta_ip.values())

            eth_list = []
            for client_num in range(len(self.station_list)):
                eth_list.append(self.upstream_port)
            for client_num in range(len(self.station_list)):
                self.cx_profile.create(ports=eth_list, ftp_ip=ip[client_num] + "/jk.txt", sleep_time=.5,
                                       debug_=self.debug, suppress_related_commands_=True, ftp=True,
                                       user="lanforge", passwd="lanforge",
                                       source="")
        print("Test Build done")

    def start(self, print_pass=False, print_fail=False):
        self.cx_profile.start_cx()
        self.station_profile.admin_up()
        temp_stas = self.station_profile.station_names.copy()
        temp_stas.append(self.upstream)
        if (self.local_realm.wait_for_ip(temp_stas)):
            self._pass("All stations got IPs", print_pass)
        else:
            self._fail("Stations failed to get IPs", print_fail)
            exit(1)

        print("Test Started")


    def stop(self):
        self.cx_profile.stop_cx()
        self.station_profile.admin_down()

    def postcleanup(self):
        self.cx_profile.cleanup()
        self.station_profile.cleanup()
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                   debug=self.debug)

    def file_create(self):
        if self.file_size == "200MB":
            size_in_bytes=200000000
        elif self.file_size == "500MB":
            size_in_bytes=500000000
        else:
            size_in_bytes = 1000000000

        if os.path.isfile("/home/lanforge/Netgear.txt"):
            os.remove("/home/lanforge/Netgear.txt")
        file_data=b"0"
        with open("Netgear.txt","wb") as f:
            num_chars= size_in_bytes
            f.write(file_data * num_chars)

    def my_monitor(self):
        #data in json format
        data = self.json_get("layer4/list?fields=bytes-rd")
        print(data)

        #list of layer 4 connections name
        self.data1 = []
        for i in range(len(self.sta_list)):
            self.data1.append((str(list(data['endpoint'][i].keys())))[2:-2])
        print(self.data1)

        data2 = self.data1
        list_of_time = []
        list1 = []
        list2 = []
        if self.file_size == "200MB":
            size_in_bytes=200000000
        elif self.file_size == "500MB":
            size_in_bytes=500000000
        else:
            size_in_bytes = 1000000000

        for i in range(len(self.sta_list)):
            list_of_time.append(0)
        while list_of_time.count(0) != 0:
            for i in range(len(self.sta_list)):
                data = self.json_get("layer4/list?fields=bytes-rd")
                if data['endpoint'][i][data2[i]]['bytes-rd'] <= size_in_bytes:
                    # print(data['endpoint'][i][data1[i]]['bytes-rd'])
                    data = self.json_get("layer4/list?fields=bytes-rd")
                if data['endpoint'][i][data2[i]]['bytes-rd'] >= size_in_bytes:
                    list1.append(i)
                    if list1.count(i) == 1:
                        list2.append(i)
                        list1 = list2
                        # print(data['endpoint'][i][data1[i]]['bytes-rd'])
                        print("download ", i, "station")
                        self.json_post("/cli-json/set_cx_state", {
                            "test_mgr": "default_tm",
                            "cx_name": "CX_" + data2[i],
                            "cx_state": "STOPPED"
                        }, debug_=self.debug)
                        list_of_time[i] = datetime.now()
            time.sleep(1)
        return list_of_time

    def time_calculate(self,time_list,time1):
        dw_time_list=[]
        for i in range(len(self.sta_list)):
            dw_time_list.append(str(time_list[i]-time1)[:-7])
        print("dw_time_list",dw_time_list)
        output_data = {}
        for i in range(len(self.sta_list)):
            output_data[self.data1[i]] = dw_time_list[i]
        return output_data

    def speed_calculate(self,dict_time):
        list_time=list(dict_time.values())
        speed_list=[]
        for i in range(len(dict_time)):
            h,m,s=list_time[i].split(":")
            seconds=total = (int(h) * 3600 + int(m) * 60 + int(s))
            speed_list.append((200000000//seconds)/10**2)
        return speed_list

    def write_file_csv(self, dict_data, speed_list):
        fields = ['Name', 'Download time(H:M:S)', 'Speed(Megabytes/Sec)']
        list1 = list(dict_data.keys())
        list2 = list(dict_data.values())
        list_data = []
        l = []

        #create list of list
        for i in range(len(dict_data)):
            l.extend([list1[i], list2[i], speed_list[i]])
            list_data.append(l)
            l = []

        filename = "download.csv"
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(list_data)


    def ap_reboot(self, ip, user, pswd):
        self.ip = ip
        self.user = user
        self.pswd = pswd

        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(ip, port=22, username=user, password=pswd, banner_timeout=600)

        stdin, stdout, stderr = ssh.exec_command('reboot')
        output = stdout.readlines()
        ssh.close()
        # print('\n'.join(output))
        time.sleep(10)
def main():
    # This has --mgr, --mgr_port and --debug
    parser = LFCliBase.create_bare_argparse(prog="netgear-ftp", formatter_class=argparse.RawTextHelpFormatter, epilog="About This Script")
    # Adding More Arguments for custom use
    parser.add_argument('--ssid',nargs="+" ,help='--ssid', default="TestAP")
    parser.add_argument('--passwd',nargs="+", help='--passwd', default="BLANK")
    parser.add_argument('--security', nargs="+",help='--security', default="open")
    parser.add_argument('--radios',nargs="+",help='--radio to use on LANforge for 5G and 2G', default=["wiphy0","wiphy1"])
    
    # Test variables
    parser.add_argument('--directions', nargs="+",help='--List with Upload and Download Options', default=["Upload", "Download"])
    parser.add_argument('--file_sizes', nargs="+",help='--File Size defaults ["200MB","500MB","1GB"]', default=["200MB","500MB","1000MB"])
    parser.add_argument('--clients', nargs="+", help='--num_client is number of stations', default=[40, ])
    
    args = parser.parse_args()
    print(args)

    #For all combinations of directions, file size and client counts, run the test
    for direction in args.directions:
        for file_size in args.file_sizes:
            for radio in args.radios :
                # Start Test
                obj = ftp_test(lfclient_host=args.mgr,
                    lfclient_port=args.mgr_port,
                    dut_ssid=args.ssid,
                    dut_passwd=args.passwd,
                    dut_security=args.security,
                    num_sta= args.client,
                    radio=radio,
                    file_size=file_size,
                    direction=direction                      
                   )
    
    obj.precleanup()
    obj.ap_reboot()
    obj.build()
    obj.start()
    if not obj.passes():
        print(obj.get_fail_message())
        exit(1)

    #First time stamp
    time1 = datetime.now()

    obj.start(False, False)

    #return list of download completed time
    time_list = obj.my_monitor()

    #return dictionary of station name and download time
    dict_time_list = obj.time_calculate(time_list, time1)
    print("download time=", dict_time_list)

    #return list of speed of station
    speed_list = obj.speed_calculate(dict_time_list)
    print("speed_list", speed_list)

    #create csv file of data
    obj.write_file_csv(dict_time_list, speed_list)

    obj.stop()
    obj.postcleanup()
    obj.stop()


if __name__ == '__main__':
    main()