"""
  objective:- Test the Auto Channel Selectionn feature of the AP in 2.4GHz
  run - ./lf_channel_selection_test.py --mgr 192.168.200.34 --iteration 200
"""
import argparse
import sys
import os
import paramiko
import csv
import datetime
from datetime import datetime
import random
from itertools import repeat
from channel_template import *

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

if 'py-json' not in sys.path:
    sys.path.append(os.path.join(os.path.abspath('..'), 'py-json'))
import LANforge
from LANforge.lfcli_base import LFCliBase
from LANforge import LFUtils
import realm
from realm import Realm
import time
from station_profile import StationProfile

#class which will create 3 vap and associate one client each along with some traffic

class ChannelSelectionTest(Realm):
    def __init__(self,
                 host=None,
                 port=None,
                 ssid=None,
                 security=None,
                 radio=None,
                 password=None,
                 vap_list=None,
                 number_template="000",
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False,
                 _dhcp=True,
                 upstream=None,
                 speed_a_min=None,
                 speed_a_maax=None,
                 speed_b_min=None,
                 speed_b_max=None ,
                 dhcp=False,
                 station_list=None):
        super().__init__(host,
                         port)
        self.host = host
        self.port = port
        self.ssid = ssid
        self.security = security
        self.password = password
        self.vap_list = vap_list
        self.radio = radio
        self.number_template = number_template
        self.debug = _debug_on
        self.dhcp = _dhcp
        self._dhcp = dhcp
        self.station_profile = StationProfile(lfclient_url=self.lfclient_url, local_realm=super(), dhcp=False,ssid=self.ssid, ssid_pass=self.password,security=self.security, number_template_=self.number_template)

        #vap profile initialization
        self.vap_profile = self.new_vap_profile()
        self.vap_profile.vap_name = self.vap_list
        self.vap_profile.ssid = self.ssid
        self.vap_profile.security = self.security
        self.vap_profile.ssid_pass = self.password
        self.vap_profile.dhcp = self.dhcp
        if self.debug:
            print("----- VAP List ----- ----- ----- ----- ----- ----- \n")
            print(self.vap_list)
            print("---- ~VAP List ----- ----- ----- ----- ----- ----- \n")

        self.upstream = upstream
        self.speed_a_min = speed_a_min
        self.speed_a_max = speed_a_maax
        self.speed_b_min = speed_b_min
        self.speed_b_max = speed_b_max
        self.station_list = station_list
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.password,
        self.station_profile.security = self.security
        self.cx_profile = self.local_realm.new_l3_cx_profile()
        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.cx_profile.name_prefix ="L3"
        self.cx_profile.side_a_min_bps = speed_a_min
        self.cx_profile.side_a_max_bps = speed_a_maax
        self.cx_profile.side_b_min_bps = speed_b_min
        self.cx_profile.side_b_max_bps = speed_b_max

    def build_vap(self, channel, radio,vap_name):
        vap = vap_name.split(".")
        print(vap[1])
        ip_addr = "192.168." + str(vap[1]) + ".1"
        gateway = "192.168." + str(vap[1]) + ".1"

        self.vap_profile.use_security(self.security, self.ssid, passwd=self.password)
        self.vap_profile.set_command_param("set_port", "resource", int(vap[1]))
        self.vap_profile.set_command_param("set_port", "ip_addr", ip_addr)
        self.vap_profile.set_command_flag("set_port", "ip_address", 1)
        self.vap_profile.set_command_param("set_port", "netmask", "255.255.255.0")
        self.vap_profile.set_command_flag("set_port", "ip_Mask", 1)
        self.vap_profile.set_command_param("set_port", "gateway", gateway)
        self.vap_profile.set_command_flag("set_port", "ip_gateway", 1)
        self.vap_profile.mode = 6
        print("Creating VAP")
        self.vap_profile.create(resource=int(vap[1]), radio=radio, channel=channel, up_=True, debug=False,
                                suppress_related_commands_=True, use_radius=True, hs20_enable=False, use_ht40=False,
                                bridge=False)


    def build_sta(self,sta_name, radio):
        print(sta_name)
        name = sta_name.split(".")
        print(name[1])
        ip_addr = "192.168." + str(name[1]) + ".2"
        gateway = "192.168." + str(name[1]) + ".1"

        self.station_profile.use_security(self.security, self.ssid, self.password)

        self.vap_profile.set_command_param("set_port", "resource", int(name[1]))
        self.station_profile.set_command_param("set_port", "ip_addr", ip_addr)
        self.station_profile.set_command_flag("set_port", "ip_address", 1)
        self.station_profile.set_command_param("set_port", "netmask", "255.255.255.0")
        self.station_profile.set_command_flag("set_port", "ip_Mask", 1)
        self.station_profile.set_command_param("set_port", "gateway", gateway)
        self.station_profile.set_command_flag("set_port", "ip_gateway", 1)
        self.station_profile.desired_add_sta_flags.append("ht40_disable")
        self.station_profile.desired_add_sta_flags_mask.append("ht40_disable")
        self.station_profile.mode = 6
        # self.station_profile.dhcp = False
        # self.local_realm.new_station_profile(dhcp=False)
        self.station_profile.create(radio=radio, sta_names_=[sta_name], debug=self.local_realm.debug)

    def start(self,sta_name):
        self.station_profile.admin_up()
        if self.local_realm.wait_for_ip([sta_name]):
            self.local_realm._pass("All stations got IPs", print_=True)
        else:
            self.local_realm._fail("Stations failed to get IPs", print_=True)

    def create_cx(self, sta_name, vap_name):
        self.cx_profile.create(endp_type="lf_udp", side_a=vap_name, side_b=[sta_name], sleep_time=0)

    def start_cx(self):
        name = self.json_get("endp?fields=name")
        cx_name = []
        for i in [0,2, 4]:
            #print(list(name['endpoint'][i].keys()))
            #print(list(name['endpoint'][i].keys())[0][:13])
            x= list(name['endpoint'][i].keys())[0][:13]
            cx_name.append(x)
        #print("cx name ", cx_name)

        for cx in cx_name:
            self.json_post("/cli-json/set_cx_state", {
                "test_mgr": "default_tm",
                "cx_name": cx,
                "cx_state": "RUNNING"
            }, debug_=self.debug)

    def cleanup_cx(self):
        self.cx_profile.cleanup_prefix()

    def precleanup(self,sta_list, vap_list):
        self.cx_profile.cleanup_prefix()
        for sta in sta_list:
            self.local_realm.rm_port(sta, check_exists=True)
        LFUtils.wait_until_ports_disappear(base_url=self.local_realm.lfclient_url, port_list=sta_list,
                                           debug=self.local_realm.debug)
        for vap in vap_list:
            self.local_realm.rm_port(vap, check_exists=True)
        LFUtils.wait_until_ports_disappear(base_url=self.local_realm.lfclient_url, port_list=vap_list,
                                           debug=self.local_realm.debug)

class APAutomate():
    def __init__(self, ip , user , pswd):
        self.ip = ip
        self.user = user
        self.pswd = pswd

    def ap_reboot(self):
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(self.ip, port=22, username=self.user, password=self.pswd, banner_timeout=600)
        stdin, stdout, stderr = ssh.exec_command('reboot')
        output = stdout.readlines()
        ssh.close()

    def get_ap_channel(self):
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(self.ip, port=22, username=self.user, password=self.pswd,banner_timeout=600)
        stdin, stdout, stderr = ssh.exec_command('iwlist wifi0vap0 channel')
        output = stdout.readlines()
        ssh.close()
        return output

def main():
    parser = argparse.ArgumentParser(description="SKY UK Channel selection Test Script")
    parser.add_argument('--mgr', help='hostname for where LANforge GUI is running', default='localhost')
    parser.add_argument('--mgr_port',type=int, help='port LANforge GUI HTTP service is running on', default=8080)
    parser.add_argument('--upstream_port', help='non-station port that generates traffic: eg: eth1', default='eth1')
    parser.add_argument('--security1', help='WiFi Security protocol: {open|wep|wpa2|wpa3 for vap1',default='open')
    parser.add_argument('--ssid1', help='WiFi SSID for script object to associate to vap1', default="skyuk1")
    parser.add_argument('--password1', help='WiFi passphrase/password/key for vap1', default='[BLANK]')
    parser.add_argument('--security2', help='WiFi Security protocol: {open|wep|wpa2|wpa3 for vap2',default='open')
    parser.add_argument('--ssid2', help='WiFi SSID for script object to associate to vap2',default='skyuk2')
    parser.add_argument('--password2', help='WiFi passphrase/password/key for vap2', default='[BLANK]')
    parser.add_argument('--security3', help='WiFi Security protocol: {open|wep|wpa2|wpa3 for vap3', default='open')
    parser.add_argument('--ssid3', help='WiFi SSID for script object to associate to vap3', default='skyuk3')
    parser.add_argument('--password3', help='WiFi passphrase/password/key for vap3',default='[BLANK]')
    parser.add_argument('--radios', nargs="+",help='provide hoe many radios test supports',default="6")
    parser.add_argument('--iteration', type=int, help='specify the number of iteration you want to perform test', default=1)
    parser.add_argument('--num_vaps', help='Number of VAPs to Create', default=1)
    parser.add_argument('--num_sta', help='number of stations',default=1)
    parser.add_argument('--vap_rad1',help='vap1 radio',default="1.1.wiphy2")
    parser.add_argument('--vap_rad2', help='vap2 radio',default="1.2.wiphy0")
    parser.add_argument('--vap_rad3', help='vap3 radio',default="1.4.wiphy0")
    parser.add_argument('--sta_rad1',help='station radio for vap1, provide according to resources', default="1.1.wiphy4")
    parser.add_argument('--sta_rad2', help='station radio for vap2, provide according to resources', default="1.2.wiphy1")
    parser.add_argument('--sta_rad3', help='station radio for vap3, provide according to resources', default="1.4.wiphy1")
    parser.add_argument('--ip', type=str, help='AP ip', default='192.168.208.22')
    parser.add_argument('--user', type=str, help='credentials login/username', default='root')
    parser.add_argument('--pswd', type=str, help='credential password', default='Password@123xzsawq@!')
    args = parser.parse_args()

    test_time = datetime.now()
    test_time = test_time.strftime("%b %d %H:%M:%S")
    print("Test started at ", test_time)
    sta_list1 = []
    station_list = []
    if args.radios == "2":
        vap_list = ["vap00"]
        sta1 = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=int(args.num_vaps) - 1,
                                      padding_number_=100,
                                      radio=args.sta_rad1)
        sta_list1.append(sta1)
    elif args.radios == "4":
        vap_list = ["vap00", "vap01"]
        sta1 = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=int(args.num_vaps) - 1,
                                      padding_number_=100,
                                      radio=args.sta_rad1)
        sta_list1.append(sta1)
        sta2 = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=int(args.num_vaps) - 1,
                                      padding_number_=100, radio=args.sta_rad2)
        sta_list1.append(sta2)
    elif args.radios == "6":
        vap_list = ["vap00", "vap01", "vap02"]
        sta1 = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=int(args.num_vaps) - 1,
                                      padding_number_=100,
                                      radio=args.sta_rad1)
        sta_list1.append(sta1)
        sta2 = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=int(args.num_vaps) - 1,
                                      padding_number_=100, radio=args.sta_rad2)
        sta_list1.append(sta2)
        sta3 = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=int(args.num_vaps) - 1,
                                      padding_number_=100, radio=args.sta_rad3)
        sta_list1.append(sta3)
    string1 = ""
    for i in sta_list1:
        string1.join(i)
        station_list.append(string1.join(i))
    #print(station_list)
    #print(vap_list)

    # splitting radio
    rad_1 = args.vap_rad1
    rad1 = rad_1.split(".")
    #print(rad1[2])
    rad_2 = args.vap_rad2
    rad2 = rad_2.split(".")
    #print(rad2[2])
    rad_3 = args.vap_rad3
    rad3 = rad_3.split(".")
    #print(rad3[2])
    # 1.1.vap00
    vap_list_pre = []
    sta_vap = "1." + rad1[1] + "." + vap_list[0]
    vap_list_pre.append(sta_vap)
    #print(sta_vap)
    sta_vap2 = "1." + rad2[1] + "." + vap_list[1]
    vap_list_pre.append(sta_vap2)
    #print(sta_vap2)
    sta_vap3 = "1." + rad3[1] + "." + vap_list[2]
    vap_list_pre.append(sta_vap3)
    #print(sta_vap3)

    # 1.1.sta00
    sta_list_pre =[]
    rad_1a = args.sta_rad1
    rad1a = rad_1a.split(".")
    name1 = "1." + rad1a[1] + ".sta00"
    sta_list_pre.append(name1)
    #print("name1", name1)
    rad_2a = args.sta_rad2
    rad2a = rad_2a.split(".")
    name2 = "1." + rad2a[1] + ".sta00"
    sta_list_pre.append(name2)
    rad_3a = args.sta_rad3
    rad3a = rad_3a.split(".")
    name3 = "1." + rad3a[1] + ".sta00"
    sta_list_pre.append(name3)

    print("cleaning up all connections ")
    ch = ChannelSelectionTest(host=args.mgr, port=8080)
    ch.precleanup(sta_list=sta_list_pre, vap_list= vap_list_pre)
    time.sleep(30)

    print("creating vap on channel ")
    for vap_name in vap_list:
        #print(vap_name)
        if vap_name == "vap00":
            data = {'radio': rad1[2], 'ssid': args.ssid1, 'security': args.security1,
                    'password': args.password1, 'channel': 1, 'vap_name': sta_vap}
        elif vap_name == "vap01":
            data = {'radio': rad2[2], 'ssid': args.ssid2, 'security': args.security2,
                    'password': args.password2, 'channel': 6, 'vap_name': sta_vap2}
        elif vap_name == "vap02":
            data = {'radio': rad3[2], 'ssid': args.ssid3, 'security': args.security2,
                    'password': args.password2, 'channel': 11, 'vap_name': sta_vap3}

        selection = ChannelSelectionTest(host=args.mgr, port=8080, ssid=data['ssid'], security=data['security'],
                                         radio=data['radio'], password=data['password'], vap_list=vap_name,
                                         _dhcp=False)
        selection.build_vap(channel=data['channel'], radio=data['radio'],vap_name=data['vap_name'])

    for sta_name in station_list:
        print("nikita",sta_name)
        if sta_name == name1:
            val = {'ssid': args.ssid1, 'security': args.security1, 'radio': args.sta_rad1,
                   'password': args.password1, 'sta_name': sta_name, 'vap_name': sta_vap}
        elif sta_name == name2:
            val = {'ssid': args.ssid2, 'security': args.security2, 'radio': args.sta_rad2,
                   'password': args.password2, 'sta_name': sta_name,'vap_name': sta_vap2}
        elif sta_name == name3:
            val = {'ssid': args.ssid3, 'security': args.security3, 'radio': args.sta_rad3,
                   'password': args.password3, 'sta_name': sta_name, 'vap_name': sta_vap3}

        station = ChannelSelectionTest(host=args.mgr, port=8080, ssid=val['ssid'], security=val['security'],
                                       radio=val['radio'],
                                       password=val['password'], station_list=val['sta_name'])
        station.build_sta(sta_name=sta_name, radio=val['radio'])
        station.start(sta_name=sta_name)

    #generate iteration
    iteration = args.iteration
    per_col = iteration / 3
    ch1_list = []
    for i in range(0, iteration):
        n = random.randint(1, 5)
        # print(n)
        val = n * 5
        ch1_list.append(val)
    ch6_list = []

    for i in range(0, iteration):
        p = random.randint(1, 5)
        # print(n)
        val = p * 5
        ch6_list.append(val)
    ch11_list = []

    for i in range(0, iteration):
        z = random.randint(1, 5)
        # print(n)
        val = z * 5
        ch11_list.append(val)
    for i in range(0, len(ch1_list)):
        if ch1_list[i] and ch6_list[i] and ch11_list[i]:
            radm = [ch1_list[i], ch6_list[i], ch11_list[i]]
            random_index = random.randrange(len(radm))
            if random_index == 0:
                ch1_list[i] = 0
            elif random_index == 1:
                ch6_list[i] = 0
            else:
                ch11_list[i] = 0
        else:
            continue
    print("channel 1 list = ", ch1_list)
    print("channel 6 list = ", ch6_list)
    print("channel 11 list = ", ch11_list)
    expected = []
    channel_after = []
    final_data = []
    for (a, b, c) in zip(ch1_list, ch6_list, ch11_list):
        print(a, b, c)
        #print(type(a))
        speed1 = str(a)  + "000000"
        speed2 = str(b) + "000000"
        speed3 = str(c) + "000000"
        #print(speed1)
        #print(name1)
        for sta_name in station_list:
            if sta_name == name1:
                val = {'sta_name': sta_name,'vap_name': sta_vap,'speed_a_min': int(speed1), 'speed_a_maax': int(speed1), 'speed_b_min': 0, 'speed_b_max': 0,}
            elif sta_name == name2:
                val = {'sta_name': sta_name,'vap_name': sta_vap2,'speed_a_min': int(speed2), 'speed_a_maax': int(speed2), 'speed_b_min': 0, 'speed_b_max': 0,}
            elif sta_name == name3:
                val = {'sta_name': sta_name,  'vap_name': sta_vap3,'speed_a_min': int(speed3), 'speed_a_maax': int(speed3), 'speed_b_min': 0, 'speed_b_max': 0,}
            station1 = ChannelSelectionTest(host=args.mgr, port=8080, station_list=val['sta_name'],speed_a_min=val['speed_a_min'], speed_a_maax=val['speed_a_maax'],
                                           speed_b_min=val['speed_b_min'],
                                           speed_b_max=val['speed_b_max'])
            station1.create_cx(sta_name=sta_name, vap_name=val['vap_name'])
        station2 = ChannelSelectionTest(host=args.mgr, port=8080)
        station2.start_cx()
        time.sleep(70)
        print("AP reboot ")
        ap = APAutomate(ip=args.ip, user=args.user, pswd=args.pswd)
        ap.ap_reboot()
        time.sleep(120)
        expected_var = ""
        if a < b and a < c:
            expected.append(1)
            expected_var = 1
        elif b < a and b < c:
            expected.append(6)
            expected_var = 6
        elif c < a and c < b:
            expected.append(11)
            expected_var = 11
        elif a == b and a < c:
            expected.append(1)
            expected_var = 1
        elif a == c and a < b:
            expected.append(1)
            expected_var = 1
        elif b == a and b < c:
            expected.append(6)
            expected_var = 6
        elif b == c and b < a:
            expected.append(6)
            expected_var = 6
        elif c == a and c < b:
            expected.append(11)
            expected_var = 11
        elif c == b and c < a:
            expected.append(11)
            expected_var = 11
        elif a == b and b == c:
            expected.append(1)
            expected_var = 1

        #measure channel from ap
        print("now measure channel from ap after reboot ")
        ap_channel = ap.get_ap_channel()
        lst = ap_channel
        x = lst[-2]
        y = x[47:]
        ap_channel_after = y[:len(y) - 2]
        channel_after.append(ap_channel_after)
        print("real ap channel after reboot", ap_channel_after)

        line1={}
        line1["Traffic1"] = str(a)
        line1["Traffic2"] = str(b)
        line1["Traffic3"] = str(c)
        line1["expected channel"] = expected_var
        line1["channel_after"] = ap_channel_after

        final_data.append(line1)
        print("inside iteration data", final_data)
        print("expected innside loop", expected)
        print("channel after list inside loop", channel_after)
        station2.cleanup_cx()

    print("final data", final_data)
    print(" channel after reboot list ", channel_after)
    test_end = datetime.now()
    test_end = test_end.strftime("%b %d %H:%M:%S")
    print("Test ended at ", test_end)
    s1 = test_time
    s2 = test_end  # for example
    FMT = '%b %d %H:%M:%S'
    test_duration = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
    print("total test duration ", test_duration)
    print("test finished")

    expected_list = []
    for i in expected:
        expected_list.append(str(i))
    print("expected channel list", expected_list)
    date = str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
    test_setup_info = {
        "AP Name": "TestAP",
        "SSID": "TestSSID",
        "Test Duration": test_duration
    }
    generate_report(final_data,
                    date,
                    expected_value=expected_list,
                    measured_value=channel_after,
                    test_setup_info=test_setup_info,
                    iteration=args.iteration,
                    graph_path="/home/lanforge/html-reports/skyuk")

if __name__ == '__main__':
    main()


