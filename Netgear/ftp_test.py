""" ftp_test.py will create stations and endpoints to generate and verify layer-4 traffic over an ftp connection.
    find out download/upload time of each client according to file size.
    This script will monitor the bytes-rd attribute of the endpoints.
    Use './ftp_test.py --help' to see command line usage and options
    -Jitendrakumar Kushavah
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.
"""
import sys
from ftp_html import *
import paramiko
if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)
if 'py-json' not in sys.path:
    sys.path.append('../py-json')

from LANforge import LFUtils
from LANforge.lfcli_base import LFCliBase
from LANforge.LFUtils import *
import realm
import argparse
from datetime import datetime
import time
import os

class ftp_test(LFCliBase):
    def __init__(self, lfclient_host="localhost", lfclient_port=8080, sta_prefix="sta", start_id=0, num_sta= None,
                 dut_ssid=None,dut_security=None, dut_passwd=None, file_size=None, band=None,
                 upstream="eth1",_debug_on=False, _exit_on_error=False,  _exit_on_fail=False, direction= None):
        super().__init__(lfclient_host, lfclient_port, _debug=_debug_on, _exit_on_fail=_exit_on_fail)
        print("Test is about to start")
        self.host = lfclient_host
        self.port = lfclient_port
        #self.radio = radio
        self.upstream = upstream
        self.sta_prefix = sta_prefix
        self.sta_start_id = start_id
        self.num_sta = num_sta
        self.ssid = dut_ssid
        self.security = dut_security
        self.password = dut_passwd
        self.requests_per_ten = 1
        self.band=band
        self.file_size=file_size
        self.direction=direction
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()
        self.cx_profile = self.local_realm.new_http_profile()
        self.port_util = realm.PortUtils(self.local_realm)
        self.cx_profile.requests_per_ten = self.requests_per_ten

        print("Test is Initialized")

    def set_values(self):
        #This method will set values according user input

        if self.band == "5G":
            self.radio = ["wiphy0"]
            if self.file_size == "2MB":

                #providing time duration for Pass or fail criteria
                self.duration = self.convert_min_in_time(1)
            elif self.file_size == "500MB":
                self.duration = self.convert_min_in_time(30)
            elif self.file_size == "1000MB":
                self.duration = self.convert_min_in_time(50)
            else:
                self.duration = self.convert_min_in_time(10)
        elif self.band == "2.4G":
            self.radio = ["wiphy1"]
            if self.file_size == "2MB":
                self.duration = self.convert_min_in_time(2)
            elif self.file_size == "500MB":
                self.duration = self.convert_min_in_time(60)
            elif self.file_size == "1000MB":
                self.duration = self.convert_min_in_time(80)
            else:
                 self.duration = self.convert_min_in_time(10)
        elif self.band == "Both":
            self.radio = ["wiphy0", "wiphy1"]

            #if Both then number of stations are half for 2.4G and half for 5G
            self.num_sta = self.num_sta // 2
            print(self.num_sta)
            if self.file_size == "2MB":
                self.duration = self.convert_min_in_time(2)
            elif self.file_size == "500MB":
                self.duration = self.convert_min_in_time(60)
            elif self.file_size == "1000MB":
                self.duration = self.convert_min_in_time(80)
            else:
                 self.duration = self.convert_min_in_time(10)
        
        self.file_size_bytes=int(self.convert_file_size_in_Bytes(self.file_size))
    

    def precleanup(self):
        self.count=0

        #delete everything in the GUI before starting the script
        try:
            self.local_realm.load("BLANK")
        except:
            print("Couldn't load 'BLANK' Test configurations")

        for rad in self.radio:
            if rad == "wiphy0":

                #select mode(All stations will connects to 5G)
                self.station_profile.mode = 10
                self.count=self.count+1

            elif rad == "wiphy1":

                # select mode(All stations will connects to 2.4G)
                self.station_profile.mode = 6
                self.count = self.count + 1

            #check Both band if both band then for 2G station id start with 20
            if self.count == 2:
                self.sta_start_id = self.num_sta
                self.num_sta = 2 * (self.num_sta)

                #if Both band then first 20 stations will connects to 5G
                self.station_profile.mode = 10
                self.cx_profile.cleanup()

                #create station list with sta_id 20
                self.station_list1 = LFUtils.portNameSeries(prefix_=self.sta_prefix, start_id_=self.sta_start_id,
                                                           end_id_=self.num_sta - 1, padding_number_=10000,
                                                           radio=rad)

                #cleanup station list which started sta_id 20
                self.station_profile.cleanup(self.station_list1, debug_=self.debug)
                LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                                   port_list=self.station_list,
                                                   debug=self.debug)
                return
            #clean layer4 ftp traffic
            self.cx_profile.cleanup()
            self.station_list = LFUtils.portNameSeries(prefix_=self.sta_prefix, start_id_=self.sta_start_id,
                                                       end_id_=self.num_sta - 1, padding_number_=10000,
                                                       radio=rad)

            #cleans stations
            self.station_profile.cleanup(self.station_list , delay=1, debug_=self.debug)
            LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                               port_list=self.station_list,
                                               debug=self.debug)
            time.sleep(1)

        print("precleanup done")

    def build(self):

        #set ftp
        self.port_util.set_ftp(port_name=self.local_realm.name_to_eid(self.upstream)[2], resource=1, on=True)

        for rad in self.radio:

            #station build
            self.station_profile.use_security(self.security, self.ssid, self.password)
            self.station_profile.set_number_template("00")
            self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
            self.station_profile.set_command_param("set_port", "report_timer", 1500)
            self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
            self.station_profile.create(radio=rad, sta_names_=self.station_list, debug=self.debug)
            self.local_realm.wait_until_ports_appear(sta_list=self.station_list)
            self.station_profile.admin_up()
            if self.local_realm.wait_for_ip(self.station_list):
                self._pass("All stations got IPs")
            else:
                self._fail("Stations failed to get IPs")
                exit(1)
            #building layer4
            self.cx_profile.direction ="dl"
            self.cx_profile.dest = "/dev/null"
            print('Direction:',self.direction)

            if self.direction == "Download":
                
                #data from GUI for find out ip addr of upstream port
                data = self.json_get("ports/list?fields=IP")

                for i in data["interfaces"]:
                    for j in i:
                        if "1.1." + self.upstream == j:
                            ip_upstream = i["1.1." + self.upstream]['ip']
            

                self.cx_profile.create(ports=self.station_profile.station_names, ftp_ip = ip_upstream + "/Netgear.txt",
                                        sleep_time=.5,debug_=self.debug,suppress_related_commands_=True, ftp=True, user="lanforge",
                                        passwd="lanforge", source="")


            elif self.direction == "Upload":
                dict_sta_and_ip = {}

                #data from GUI for find out ip addr of each station
                data = self.json_get("ports/list?fields=IP")

                # This loop for find out proper ip addr and station name
                for i in self.station_list:
                    for j in data['interfaces']:
                        for k in j:
                            if i == k:
                                dict_sta_and_ip[k] = j[i]['ip']



                #list of ip addr of all stations
                ip = list(dict_sta_and_ip.values())

                eth_list = []
                client_list = []

                #list of all stations
                for i in range(len(self.station_list)):
                    client_list.append(self.station_list[i][4:])

                #list of upstream port
                eth_list.append(self.upstream)

                #create layer for connection for upload
                for client_num in range(len(self.station_list)):
                    self.cx_profile.create(ports=eth_list, ftp_ip=ip[client_num] + "/Netgear.txt", sleep_time=.5,
                                           debug_=self.debug, suppress_related_commands_=True, ftp=True,
                                           user="lanforge", passwd="lanforge",
                                           source="", upload_name=client_list[client_num])

            #check Both band present then build stations with another station list
            if self.count == 2:
                self.station_list = self.station_list1

                # if Both band then another 20 stations will connects to 2.4G
                self.station_profile.mode = 6
        print("Test Build done")

    def start(self, print_pass=False, print_fail=False):
        for rad in self.radio:
            self.cx_profile.start_cx()

        print("Test Started")


    def stop(self):
        self.cx_profile.stop_cx()
        self.station_profile.admin_down()

    def postcleanup(self):
        self.cx_profile.cleanup()
        self.local_realm.load("BLANK")
        self.station_profile.cleanup(self.station_profile.station_names, delay=1, debug_=self.debug)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                   debug=self.debug)

    #Create file for given file size
    def file_create(self):
        if os.path.isfile("/home/lanforge/Netgear.txt"):
            os.remove("/home/lanforge/Netgear.txt")
        os.system("fallocate -l " +self.file_size +" /home/lanforge/Netgear.txt")
        print("File creation done", self.file_size)

    #convert file size MB or GB into Bytes
    def convert_file_size_in_Bytes(self,size):
        if (size.endswith("MB")) or (size.endswith("Mb")) or (size.endswith("GB")) or (size.endswith("Gb")):
            if (size.endswith("MB")) or (size.endswith("Mb")):
                return float(size[:-2]) * 10**6
            elif (size.endswith("GB")) or (size.endswith("Gb")):
                return float(size[:-2]) * 10**9


    def my_monitor(self,time1):
        #data in json format
        data = self.json_get("layer4/list?fields=bytes-rd")

        #list of layer 4 connections name
        self.data1 = []
        for i in range(self.num_sta):
            self.data1.append((str(list(data['endpoint'][i].keys())))[2:-2])
        #print(self.data1)

        data2 = self.data1
        list_of_time = []
        list1 = []
        list2 = []

        for i in range(self.num_sta):
            list_of_time.append(0)
        while list_of_time.count(0) != 0:

            #run script upto given time
            if str(datetime.now()- time1) >= self.duration:
                break

            for i in range(self.num_sta):
                data = self.json_get("layer4/list?fields=bytes-rd")

                #reading uc-avg data in json format
                uc_avg= self.json_get("layer4/list?fields=uc-avg")
                if data['endpoint'][i][data2[i]]['bytes-rd'] <= self.file_size_bytes:
                    data = self.json_get("layer4/list?fields=bytes-rd")
                if data['endpoint'][i][data2[i]]['bytes-rd'] >= self.file_size_bytes:
                    list1.append(i)
                    if list1.count(i) == 1:
                        list2.append(i)
                        list1 = list2

                        #stop station after download or upload file with particular size
                        self.json_post("/cli-json/set_cx_state", {
                            "test_mgr": "default_tm",
                            "cx_name": "CX_" + data2[i],
                            "cx_state": "STOPPED"
                        }, debug_=self.debug)

                        list_of_time[i] = round(int(uc_avg['endpoint'][i][data2[i]]['uc-avg'])/1000,1)
            time.sleep(0.5)

        #return list of download/upload time in seconds
        return list_of_time

    #Method for arrange ftp download/upload time data in dictionary
    def ftp_test_data(self, list_time, pass_fail, bands, file_sizes, directions, num_stations):

        #creating dictionary for single iteration
        create_dict={}

        create_dict["band"] = self.band
        create_dict["direction"] = self.direction
        create_dict["file_size"] = self.file_size
        create_dict["time"] = list_time
        create_dict["duration"] = self.time_test
        create_dict["result"] = pass_fail
        create_dict["bands"] = bands
        create_dict["file_sizes"] = file_sizes
        create_dict["directions"] = directions
        create_dict["num_stations"] = num_stations 

        return  create_dict

    #Method for AP reboot
    def ap_reboot(self, ip, user, pswd):

        print("starting AP reboot")

        # creating shh client object we use this object to connect to router
        ssh = paramiko.SSHClient()

        # automatically adds the missing host key
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=22, username=user, password=pswd, banner_timeout=600)
        stdin, stdout, stderr = ssh.exec_command('reboot')
        output = stdout.readlines()
        ssh.close()
        # print('\n'.join(output))

        time.sleep(180)
        print("AP rebooted")

    def convert_min_in_time(self,total_minutes):

        #saving time in minutus
        self.time_test = total_minutes

        # Get hours with floor division
        hours = total_minutes // 60

        # Get additional minutes with modulus
        minutes = total_minutes % 60

        # Create time as a string
        time_string = str("%d:%02d" % (divmod(total_minutes, 60))) + ":00" + ":000000"

        return time_string

    def pass_fail_check(self,time_list):
        if time_list.count(0) == 0:
            return "Pass"
        else:
            return "Fail"

def main():
    # This has --mgr, --mgr_port and --debug
    parser = LFCliBase.create_bare_argparse(prog="ftp_test.py", formatter_class=argparse.RawTextHelpFormatter, epilog="About This Script")
    # Adding More Arguments for custom use
    parser.add_argument('--ssid',type=str, help='--ssid', default="TestAP-Jitendra")
    parser.add_argument('--passwd',type=str, help='--passwd', default="BLANK")
    parser.add_argument('--security', type=str, help='--security', default="open")
    parser.add_argument('--ap_name', type=str, help='--ap_name', default="R7800")
    parser.add_argument('--ap_ip', type=str, help='--ap_ip', default="192.168.213.90")
    
    # Test variables
    parser.add_argument('--bands', nargs="+", help='--bands defaults ["5G","2.4G","Both"]', default=["5G","2.4G","Both"])
    parser.add_argument('--directions', nargs="+", help='--directions defaults ["Download","Upload"]', default=["Download","Upload"])
    parser.add_argument('--file_sizes', nargs="+", help='--File Size defaults ["2MB","500MB","1000MB"]', default=["2MB","500MB","1000MB"])
    parser.add_argument('--num_stations', type=int, help='--num_stations is number of stations', default=40)
    
    args = parser.parse_args()

    # 1st time stamp for test duration
    time_stamp1 = datetime.now()

    #use for creating ftp_test dictionary
    iteraration_num=0

    #empty dictionary for whole test data
    ftp_data={}

    #For all combinations ftp_data of directions, file size and client counts, run the test
    for band in args.bands:
        for direction in args.directions:
            for file_size in args.file_sizes:
                # Start Test
                obj = ftp_test(lfclient_host=args.mgr,
                    lfclient_port=args.mgr_port,
                    dut_ssid=args.ssid,
                    dut_passwd=args.passwd,
                    dut_security=args.security,
                    num_sta= args.num_stations,
                    band=band,
                    file_size=file_size,
                    direction=direction
                   )

                iteraration_num=iteraration_num+1
                obj.file_create()
                obj.set_values()
                obj.precleanup()
                #if file_size != "2MB":
                    #obj.ap_reboot("192.168.213.190","root","Password@123xzsawq@!")
                obj.build()
                if not obj.passes():
                    print(obj.get_fail_message())
                    exit(1)

                #First time stamp
                time1 = datetime.now()
            
                obj.start(False, False)
            
                #return list of download/upload completed time stamp
                time_list = obj.my_monitor(time1)

                # check pass or fail
                pass_fail = obj.pass_fail_check(time_list)

                #dictionary of whole data
                ftp_data[iteraration_num] = obj.ftp_test_data(time_list,pass_fail,args.bands,args.file_sizes,args.directions,args.num_stations)

                obj.stop()
                obj.postcleanup()

    #2nd time stamp for test duration
    time_stamp2 = datetime.now()

    #total time for test duration
    test_duration = str(time_stamp2 - time_stamp1)[:-7]


    date = str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]

    test_setup_info = {
        "AP Name": args.ap_name,
        "SSID": args.ssid,
        "Number of Stations": args.num_stations,
        "Test Duration": test_duration
    }

    input_setup_info = {
        "IP": args.ap_ip ,
        "user": "root",
        "Contact": "support@candelatech.com"
    }
    generate_report(ftp_data,
                    date,
                    test_setup_info,
                    input_setup_info,
                    graph_path="/home/lanforge/html-reports/FTP-Test")


if __name__ == '__main__':
    main()

