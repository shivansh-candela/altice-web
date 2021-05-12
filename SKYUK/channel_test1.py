"""
python channel_test1.py --mgr 192.168.200.34 --ssid1 skyuk --security1 open --password1 [BLANK] --num_vaps 3 --vap_rad1 wiphy2 --ssid2 skyuk2 --security2 open --password2 [BLANK] --vap_rad2 wiphy4 --ssid3 skyuk3 --security3 open --password3 [BLANK] --vap_rad3 wiphy6 --num_sta 3 --upstream_port enp26s0 --sta_rad1 wiphy0 --sta_rad2 wiphy1 --sta_rad3 wiphy5
"""
import argparse
import sys
import os

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
        self.station_profile = self.local_realm.new_station_profile()
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

    def build_vap(self, channel, radio, ip_addr, netmask, gateway):

        #intializing vap
        self.vap_profile.use_security(self.security, self.ssid, passwd=self.password)
        #,"192.168.1.1"
        self.vap_profile.set_command_param("set_port", "ip_addr", str(ip_addr))
        self.vap_profile.set_command_flag("set_port", "ip_address", 1)
        #"255.255.255.0"
        self.vap_profile.set_command_param("set_port", "netmask", str(netmask) )
        self.vap_profile.set_command_flag("set_port", "ip_Mask", 1)
        #"192.168.1.1"
        self.vap_profile.set_command_param("set_port", "gateway", str(gateway))
        self.vap_profile.set_command_flag("set_port", "ip_gateway", 1)

        print("Creating VAPs")
        self.vap_profile.create(resource=1, radio=radio, channel=channel, up_=True, debug=False,
                                suppress_related_commands_=True, use_radius=True, hs20_enable=False)
        self._pass("PASS: VAP build finished")

    def build_sta(self,sta_name, radio, ip_addr, gateway):
        self.station_profile.use_security(self.security, self.ssid, self.password)
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
        self.cx_profile.create(endp_type="lf_udp", side_a="1.1."+str(vap_name), side_b=[sta_name], sleep_time=0)
        time.sleep(10)
        self.cx_profile.start_cx()


def main():

    parser = argparse.ArgumentParser(description="SKY UK Channel selection Test Script")
    parser.add_argument('--mgr', help='hostname for where LANforge GUI is running', default='localhost')
    parser.add_argument('--mgr_port', help='port LANforge GUI HTTP service is running on', default=8080)
    parser.add_argument('--upstream_port', help='non-station port that generates traffic: eg: eth1', default='eth1')
    parser.add_argument('--security1', help='WiFi Security protocol: {open|wep|wpa2|wpa3 for vap1')
    parser.add_argument('--ssid1', help='WiFi SSID for script object to associate to vap1')
    parser.add_argument('--password1', help='WiFi passphrase/password/key for vap1')

    parser.add_argument('--security2', help='WiFi Security protocol: {open|wep|wpa2|wpa3 for vap2')
    parser.add_argument('--ssid2', help='WiFi SSID for script object to associate to vap2')
    parser.add_argument('--password2', help='WiFi passphrase/password/key for vap2')

    parser.add_argument('--security3', help='WiFi Security protocol: {open|wep|wpa2|wpa3 for vap3')
    parser.add_argument('--ssid3', help='WiFi SSID for script object to associate to vap3')
    parser.add_argument('--password3', help='WiFi passphrase/password/key for vap3')

    parser.add_argument('--num_vaps', help='Number of VAPs to Create')
    parser.add_argument('--vap_rad1',help='vap1 radio')
    parser.add_argument('--vap_rad2', help='vap2 radio')
    parser.add_argument('--vap_rad3', help='vap3 radio')

    parser.add_argument('--sta_rad1',help='station radio for vap1')
    parser.add_argument('--sta_rad2', help='station radio for vap2')
    parser.add_argument('--sta_rad3', help='station radio for vap3')

    parser.add_argument('--num_sta',help='number of stations')
    args = parser.parse_args()

    vap_list = LFUtils.port_name_series(prefix="vap", start_id=0, end_id=int(args.num_vaps) - 1, padding_number=100, radio="wiphy2")
    print(vap_list)

    for vap_name in vap_list:
        if vap_name=="1.1.vap00":
            radio=args.vap_rad1
            ip_addr="192.168.1.1"
            netask="255.255.255.0"
            gateway="192.168.1.1"
            ssid=args.ssid1
            security=args.security1
            password=args.password1
            channel=1
        elif vap_name=="1.1.vap01":
            radio = args.vap_rad2
            ip_addr = "192.168.2.1"
            netask = "255.255.255.0"
            gateway = "192.168.2.1"
            ssid = args.ssid2
            security = args.security2
            password = args.password2
            channel=6
        elif vap_name=="1.1.vap02":
            radio = args.vap_rad3
            ip_addr = "192.168.3.1"
            netask = "255.255.255.0"
            gateway = "192.168.3.1"
            ssid = args.ssid3
            security = args.security3
            password = args.password3
            channel=11

        selection = ChannelSelectionTest(host=args.mgr, port=8080, ssid=ssid, security=security, radio=radio, password=password, vap_list=vap_name, _dhcp=False)
        selection.build_vap(channel=channel, radio=radio,ip_addr=ip_addr, netmask=netask, gateway=gateway)

    time.sleep(40)

    station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=int(args.num_sta) - 1,
                                          padding_number_=100)
    print(station_list)
    for sta_name in station_list:
        if sta_name == "sta00":
            ssid = args.ssid1
            security = args.security1
            radio = args.sta_rad1
            password = args.password1
            sta_name = sta_name
            upstream = args.upstream_port
            speed_a_min = 10000000
            speed_a_maax = 10000000
            speed_b_min = 0
            speed_b_max = 0
            ip_addr = "192.168.1.2"
            gateway = "192.168.1.1"
            vap_name = "1.1.vap00"
        elif sta_name == "sta01":
            ssid = args.ssid2
            security = args.security2
            radio = args.sta_rad2
            password = args.password2
            sta_name = sta_name
            upstream = args.upstream_port
            speed_a_min = 60000000
            speed_a_maax = 60000000
            speed_b_min = 0
            speed_b_max = 0
            ip_addr = "192.168.2.2"
            gateway = "192.168.2.1"
            vap_name = "1.1.vap01"
        elif sta_name == "sta02":
            ssid = args.ssid3
            security = args.security3
            radio = args.sta_rad3
            password = args.password3
            sta_name = sta_name
            upstream = args.upstream_port
            speed_a_min = 50000000
            speed_a_maax = 50000000
            speed_b_min = 0
            speed_b_max = 0
            ip_addr = "192.168.3.2"
            gateway = "192.168.3.1"
            vap_name = "1.1.vap02"

        station = ChannelSelectionTest(host=args.mgr, port=8080, ssid=ssid, security=security, radio=radio,
                                       password=password, station_list=sta_name, upstream=upstream,
                                       speed_a_min=speed_a_min, speed_a_maax=speed_a_maax, speed_b_min=speed_b_min,
                                       speed_b_max=speed_b_max, _dhcp=False)
        station.build_sta(sta_name=sta_name, radio=radio, ip_addr=ip_addr, gateway=gateway)
        station.start(sta_name=sta_name)
        station.create_cx(sta_name=sta_name, vap_name=vap_name)

    #exit()



if __name__ == '__main__':
    main()