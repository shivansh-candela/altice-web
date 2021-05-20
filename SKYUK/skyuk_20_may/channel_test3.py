"""
>python channel_test.py --mgr 192.168.200.34  --upstream_port enp26s0 --num_vaps 1  --vap_rad1 wiphy2 --sta_rad1 wiphy4 --num_sta 1 --ip 192.168.208.22 --user root --pswd Password@123xzsawq@!
"""
import argparse
import sys
import os
import paramiko
import csv
import datetime
from datetime import datetime

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
        if self.station_list == "sta00" or self.station_list == "sta01":

            self.station_profile.resource = 1
        elif self.station_list == "sta02":
            self.station_profile.resource = 2


        self.cx_profile = self.local_realm.new_l3_cx_profile()
        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.cx_profile.name_prefix ="L3"
        self.cx_profile.side_a_min_bps = speed_a_min
        self.cx_profile.side_a_max_bps = speed_a_maax
        self.cx_profile.side_b_min_bps = speed_b_min
        self.cx_profile.side_b_max_bps = speed_b_max

    def build_vap(self, channel, radio, ip_addr, netmask, gateway):

        #intializing vap
        if self.vap_list == "vap00":
            self.vap_profile.use_security(self.security, self.ssid, passwd=self.password)
            self.vap_profile.set_command_param("set_port", "resource", 1)
            self.vap_profile.set_command_param("set_port", "ip_addr", str(ip_addr))
            self.vap_profile.set_command_flag("set_port", "ip_address", 1)
            self.vap_profile.set_command_param("set_port", "netmask", str(netmask) )
            self.vap_profile.set_command_flag("set_port", "ip_Mask", 1)
            self.vap_profile.set_command_param("set_port", "gateway", str(gateway))
            self.vap_profile.set_command_flag("set_port", "ip_gateway", 1)
            self.vap_profile.mode = 6
        elif self.vap_list == "vap01":
            self.vap_profile.use_security(self.security, self.ssid, passwd=self.password)
            self.vap_profile.set_command_param("set_port", "resource", 2)

            self.vap_profile.set_command_param("set_port", "ip_addr", str(ip_addr))
            self.vap_profile.set_command_flag("set_port", "ip_address", 1)
            self.vap_profile.set_command_param("set_port", "netmask", str(netmask))
            self.vap_profile.set_command_flag("set_port", "ip_Mask", 1)
            self.vap_profile.set_command_param("set_port", "gateway", str(gateway))
            self.vap_profile.set_command_flag("set_port", "ip_gateway", 1)
            self.vap_profile.mode = 6

        elif self.vap_list == "vap02":
            self.vap_profile.use_security(self.security, self.ssid, passwd=self.password)
            self.vap_profile.set_command_param("set_port", "resource", 4)

            self.vap_profile.set_command_param("set_port", "ip_addr", str(ip_addr))
            self.vap_profile.set_command_flag("set_port", "ip_address", 1)
            self.vap_profile.set_command_param("set_port", "netmask", str(netmask))
            self.vap_profile.set_command_flag("set_port", "ip_Mask", 1)
            self.vap_profile.set_command_param("set_port", "gateway", str(gateway))
            self.vap_profile.set_command_flag("set_port", "ip_gateway", 1)
            self.vap_profile.mode = 6



        #self.vap_profile.set_command_flag("set_port")

        print(self.vap_list)
        if self.vap_list == "vap00" :
            print("Creating VAP")
            self.vap_profile.create(resource=1 ,radio=radio, channel=channel, up_=True, debug=False,
                                    suppress_related_commands_=True, use_radius=True, hs20_enable=False)
        elif self.vap_list == "vap01":
            print("Creating VAP at second lanforge")
            self.vap_profile.create(resource=2, radio=radio, channel=channel, up_=True, debug=False,
                                    suppress_related_commands_=True, use_radius=True, hs20_enable=False)
        elif self.vap_list == "vap02":
            print("Creating VAP at third lanforge")
            self.vap_profile.create(resource=4, radio=radio, channel=channel, up_=True, debug=False,
                                    suppress_related_commands_=True, use_radius=True, hs20_enable=False)



        self._pass("PASS: VAP build finished")

    def build_sta(self,sta_name, radio, ip_addr, gateway):
        print(self.station_list)
        self.station_profile.use_security(self.security, self.ssid, self.password)

        if self.station_list == "1.1.sta00" :

            self.vap_profile.set_command_param("set_port", "resource", 1)
            self.station_profile.set_command_param("set_port", "ip_addr", ip_addr)
            self.station_profile.set_command_flag("set_port", "ip_address", 1)
            self.station_profile.set_command_param("set_port", "netmask", "255.255.255.0")
            self.station_profile.set_command_flag("set_port", "ip_Mask", 1)
            self.station_profile.set_command_param("set_port", "gateway", gateway)
            self.station_profile.set_command_flag("set_port", "ip_gateway", 1)
            #self.station_profile.dhcp = False
            #self.local_realm.new_station_profile(dhcp=False)
            self.station_profile.create(radio=radio, sta_names_=[sta_name], debug=self.local_realm.debug)
        elif self.station_list == "1.2.sta00":
            self.vap_profile.set_command_param("set_port", "resource", 2)
            self.station_profile.set_command_param("set_port", "ip_addr", ip_addr)
            self.station_profile.set_command_flag("set_port", "ip_address", 1)
            self.station_profile.set_command_param("set_port", "netmask", "255.255.255.0")
            self.station_profile.set_command_flag("set_port", "ip_Mask", 1)
            self.station_profile.set_command_param("set_port", "gateway", gateway)
            self.station_profile.set_command_flag("set_port", "ip_gateway", 1)

            self.station_profile.create(radio=radio, sta_names_=[sta_name], debug=self.local_realm.debug)
        elif self.station_list == "1.4.sta00":
            self.vap_profile.set_command_param("set_port", "resource", 4)
            self.station_profile.set_command_param("set_port", "ip_addr", ip_addr)
            self.station_profile.set_command_flag("set_port", "ip_address", 1)
            self.station_profile.set_command_param("set_port", "netmask", "255.255.255.0")
            self.station_profile.set_command_flag("set_port", "ip_Mask", 1)
            self.station_profile.set_command_param("set_port", "gateway", gateway)
            self.station_profile.set_command_flag("set_port", "ip_gateway", 1)

            self.station_profile.create(radio=radio, sta_names_=[sta_name], debug=self.local_realm.debug)


    def start(self,sta_name):
        self.station_profile.admin_up()
        if self.local_realm.wait_for_ip([sta_name]):
            self.local_realm._pass("All stations got IPs", print_=True)
        else:
            self.local_realm._fail("Stations failed to get IPs", print_=True)

    def create_cx(self, sta_name, vap_name):
        print(sta_name)
        print("vap name in cx ", vap_name)

        self.cx_profile.create(endp_type="lf_udp", side_a=vap_name, side_b=[sta_name], sleep_time=0)
        #time.sleep(10)
        self.cx_profile.stop_cx()
        time.sleep(2)
        self.cx_profile.start_cx()

    def precleanup(self,):

        station_list = ["1.1.sta00", "1.2.sta00", "1.4.sta00"]
        for sta in station_list:
            self.local_realm.rm_port(sta, check_exists=True)
        LFUtils.wait_until_ports_disappear(base_url=self.local_realm.lfclient_url, port_list=station_list,
                                           debug=self.local_realm.debug)
        vap_list = ["1.1.vap00", "1.2.vap01", "1.4.vap02"]
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
        ssh.connect(self.ip, port=22, username=self.user, password=self.pswd)
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
    parser.add_argument('--radios', nargs="+",help='provide hoe many radios test supports', default=["2", "4", "6"])

    parser.add_argument('--num_vaps', help='Number of VAPs to Create')
    parser.add_argument('--vap_rad1',help='vap1 radio')
    parser.add_argument('--vap_rad2', help='vap2 radio')
    parser.add_argument('--vap_rad3', help='vap3 radio')

    parser.add_argument('--sta_rad1',help='station radio for vap1')
    parser.add_argument('--sta_rad2', help='station radio for vap2')
    parser.add_argument('--sta_rad3', help='station radio for vap3')

    parser.add_argument('--num_sta',help='number of stations')

    parser.add_argument('--ip', type=str, help='AP ip', default='192.168.208.22')
    parser.add_argument('--user', type=str, help='credentials login/username', default='root')
    parser.add_argument('--pswd', type=str, help='credential password', default='Password@123xzsawq@!')
    args = parser.parse_args()

    test_time = datetime.now()
    test_time = test_time.strftime("%b %d %H:%M:%S")
    print("Test started at ", test_time)

    with open("skyukreq.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        data = list(reader)
        row_count = len(data)
        #print(row_count)
        count = row_count

    expected_channel = []
    channel_after =[]

    final_data = []

    for line in csv.DictReader(open('skyukreq.csv')):

        #print(type(line['channel1']))
        # print(line['Channel6'])
        # print(line['Channel 11'])
        print(line["Expected channel"])
        if line['channel1'] == "0.9":
            speed1 = "900000"
        else:
            speed1 = str(line['channel1']) + "000000"
        if line['Channel6'] == "0.9":
            speed2 = "900000"
        else:
            speed2 = str(line['Channel6']) + "000000"
        if line['Channel 11'] == "0.9":
            speed3 = "900000"
        else:
            speed3 = str(line['Channel 11']) + "000000"

        expected_channel.append(line["Expected channel"])


        speed3 = str(line['Channel 11']) + "000000"
        print(speed1)
        print(speed2)
        print(speed3)

        print("cleaning up all connections ")
        ch = ChannelSelectionTest(host=args.mgr, port=8080)
        ch.precleanup()
        time.sleep(30)
        print("creating vap on channel ")
        # vap_list1=[]
        # vap_list=[]
        # vap1 = LFUtils.portNameSeries(prefix_="vap", start_id_=0, end_id_=int(args.num_vaps) - 1,padding_number_=100,radio="1.1.wiphy2")
        # vap_list1.append(vap1)
        # vap2 = LFUtils.portNameSeries(prefix_="vap", start_id_=0, end_id_=int(args.num_vaps) - 1,
        #                                   padding_number_=100, radio="1.2.wiphy0")
        # vap_list1.append(vap2)
        # string1 = ""
        # for i in vap_list1:
        #     string1.join(i)
        #     vap_list.append(string1.join(i))
        vap_list = ["vap00", "vap01", "vap02"]
        print(vap_list)

        for vap_name in vap_list:
            print(vap_name)
            if vap_name == "vap00":
                data = {'radio': "wiphy2", 'ip_addr': "192.168.1.1", 'netmask': "255.255.255.0",
                        'gateway': "192.168.1.1", 'ssid': args.ssid1, 'security': args.security1,
                        'password': args.password1, 'channel': 1}
            elif vap_name == "vap01":
                data = {'radio': "wiphy0", 'ip_addr': "192.168.2.1", 'netmask': "255.255.255.0",
                        'gateway': "192.168.2.1", 'ssid': args.ssid2, 'security': args.security2,
                        'password': args.password2, 'channel': 6}
            elif vap_name == "vap02":
                data = {'radio': "wiphy0", 'ip_addr': "192.168.3.1", 'netmask': "255.255.255.0",
                        'gateway': "192.168.23.1", 'ssid': args.ssid3, 'security': args.security2,
                        'password': args.password2, 'channel': 11}



            selection = ChannelSelectionTest(host=args.mgr, port=8080, ssid=data['ssid'], security=data['security'],
                                             radio=data['radio'], password=data['password'], vap_list=vap_name,
                                             _dhcp=False)
            selection.build_vap(channel=data['channel'], radio=data['radio'], ip_addr=data['ip_addr'],
                                netmask=data['netmask'], gateway=data['gateway'])
            time.sleep(40)
        # #time.sleep(40)
        sta_list1 = []
        station_list=[]
        sta1 = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=int(args.num_vaps) - 1,padding_number_=100,radio="1.1.wiphy1")
        sta_list1.append(sta1)
        sta2 = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=int(args.num_vaps) - 1,
                                          padding_number_=100, radio="1.2.wiphy1")
        sta_list1.append(sta2)
        sta3 = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=int(args.num_vaps) - 1,
                                      padding_number_=100, radio="1.4.wiphy1")
        sta_list1.append(sta3)
        string1 = ""
        for i in sta_list1:
            string1.join(i)
            station_list.append(string1.join(i))
        print(station_list)

        # station_list = ["sta02"]
        for sta_name in station_list:
            if sta_name == "1.1.sta00":
                val = {'ssid': args.ssid1, 'security': args.security1, 'radio': "1.1.wiphy4",
                       'password': args.password1, 'sta_name': sta_name, 'upstream': args.upstream_port,
                       'speed_a_min': int(speed1), 'speed_a_maax': int(speed1), 'speed_b_min': 0, 'speed_b_max': 0,
                       'ip_addr': "192.168.1.2", 'gateway': "192.168.1.1", 'vap_name': '1.1.vap00 '}
            elif sta_name == "1.2.sta00":
                val = {'ssid': args.ssid2, 'security': args.security2, 'radio': "1.2.wiphy1",
                       'password': args.password2, 'sta_name': sta_name, 'upstream': args.upstream_port,
                       'speed_a_min': int(speed2), 'speed_a_maax': int(speed2), 'speed_b_min': 0, 'speed_b_max': 0,
                       'ip_addr': "192.168.2.2", 'gateway': "192.168.2.1", 'vap_name': '1.2.vap01'}
            elif sta_name == "1.4.sta00":
                val = {'ssid': args.ssid3, 'security': args.security3, 'radio': "1.4.wiphy1",
                       'password': args.password3, 'sta_name': sta_name, 'upstream': args.upstream_port,
                       'speed_a_min': 50000000, 'speed_a_maax': 50000000, 'speed_b_min': 0, 'speed_b_max': 0,
                       'ip_addr': "192.168.3.2", 'gateway': "192.168.3.1", 'vap_name': '1.4.vap02'}

            station = ChannelSelectionTest(host=args.mgr, port=8080, ssid=val['ssid'], security=val['security'],
                                           radio=val['radio'],
                                           password=val['password'], station_list=val['sta_name'],
                                           upstream=val['upstream'],
                                           speed_a_min=val['speed_a_min'], speed_a_maax=val['speed_a_maax'],
                                           speed_b_min=val['speed_b_min'],
                                           speed_b_max=val['speed_b_max'], _dhcp=False)
            station.build_sta(sta_name=sta_name, radio=val['radio'], ip_addr=val['ip_addr'], gateway=val['gateway'])
            station.start(sta_name=sta_name)
            station.create_cx(sta_name=sta_name, vap_name=val['vap_name'])
            time.sleep(60)
        print("AP reboot ")
        ap = APAutomate(ip=args.ip, user=args.user, pswd=args.pswd)
        ap.ap_reboot()
        time.sleep(180)

        # measure channel from ap
        print("now measure channel from ap after reboot ")
        ap_channel = ap.get_ap_channel()
        lst = ap_channel
        x = lst[-2]
        y = x[47:]
        ap_channel_after = y[:len(y) - 2]
        channel_after.append(ap_channel_after)
        print("real ap channel after reboot", ap_channel_after)
        line1={}
        line1["Traffic1"] = line['channel1']
        line1["Traffic2"] = line['Channel6']
        line1["Traffic3"] = line['Channel 11']
        line1["expected channel"] = line["Expected channel"]
        line1["channel_after"] = ap_channel_after

        final_data.append(line1)
        print("inside iteration data", final_data)
        print("expected innside loop", expected_channel)
        print("channel after list inside loop", channel_after)

    print("final data", final_data)
    print("expected channel list ", expected_channel)
    print(" channel after reboot list ", channel_after)
    test_end = datetime.now()
    test_end = test_end.strftime("%b %d %H:%M:%S")
    print("Test ended at ", test_end)
    s1 = test_time
    s2 = test_end  # for example
    FMT = '%b %d %H:%M:%S'
    test_duration = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
    print("total test duration ", test_duration)

if __name__ == '__main__':
    main()

