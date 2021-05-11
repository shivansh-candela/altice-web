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
import pprint
import paramiko
from create_vap import CreateVAP

class Vap(Realm):
    def __init__(self,
                 _host=None,
                 _port=None,
                 _ssid=None,
                 _security=None,
                 _password=None,
                 _vap_list=None,
                 _number_template="00000",
                 _radio=None,
                 _proxy_str=None,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False,
                 _dhcp=True):
        super().__init__(_host,
                         _port)
        self.host = _host
        self.port = _port
        self.ssid = _ssid
        self.security = _security
        self.password = _password
        self.vap_list = _vap_list
        self.radio = _radio
        self.timeout = 120
        self.number_template = _number_template
        self.debug = _debug_on
        self.dhcp = _dhcp
        self.vap_profile = self.new_vap_profile()
        self.vap_profile.vap_name = self.vap_list
        self.vap_profile.ssid = self.ssid
        self.vap_profile.security = self.security
        self.vap_profile.ssid_pass = self.password
        self.vap_profile.dhcp = self.dhcp
        if self.debug:
            print("----- VAP List ----- ----- ----- ----- ----- ----- \n")
            pprint.pprint(self.vap_list)
            print("---- ~VAP List ----- ----- ----- ----- ----- ----- \n")


    def build(self, channel):
        # Build VAPs
        self.channel = channel
        self.vap_profile.use_security(self.security, self.ssid, passwd=self.password)

        print("Creating VAPs")
        self.vap_profile.create(resource = 1,
                                radio = self.radio,
                                channel = channel,
                                up_ = True,
                                debug = False,
                                suppress_related_commands_ = True,
                                use_radius = True,
                                hs20_enable = False)
        self._pass("PASS: VAP build finished")
    def start(self):
        self.vap_profile.admin_up(1)
    def stop(self):
        self.vap_profile.admin_down(1)

class StationLayer3(Realm):
    def __init__(self, lfclient_host, lfclient_port, ssid, paswd,security, radio,
                 station_list,upstream, speed_a_min,speed_a_maax, speed_b_min, speed_b_max ,name_prefix="L3", _debug_on=False,):
        self.host = lfclient_host
        self.port = lfclient_port
        self.ssid = ssid
        self.debug = _debug_on

        self.paswd = paswd
        self.security = security
        self.radio = radio
        self.station_list = station_list

        self.name_prefix = name_prefix
        self.upstream = upstream
        self.speed_a_min = speed_a_min
        self.speed_a_max = speed_a_maax
        self.speed_b_min = speed_b_min
        self.speed_b_max = speed_b_max



        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.paswd,
        self.station_profile.security = self.security
        self.cx_profile = self.local_realm.new_l3_cx_profile()
        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.cx_profile.name_prefix = self.name_prefix
        self.cx_profile.side_a_min_bps = speed_a_min
        self.cx_profile.side_a_max_bps = speed_a_maax
        self.cx_profile.side_b_min_bps = speed_b_min
        self.cx_profile.side_b_max_bps = speed_b_max

    def precleanup(self, num_sta):
        num_sta = self.num_sta
        station_list = LFUtils.port_name_series(prefix="sta",
                                                start_id=0,
                                                end_id=num_sta - 1,
                                                padding_number=100,
                                                radio=self.radio)
        self.cx_profile.cleanup_prefix()

        for sta in station_list:
            self.local_realm.rm_port(sta, check_exists=True)
        LFUtils.wait_until_ports_disappear(base_url=self.local_realm.lfclient_url, port_list=station_list,
                                           debug=self.local_realm.debug)
        time.sleep(1)

    def build(self, sta_name, traffic_type):
        self.traffic_type = traffic_type
        self.station_profile.use_security(self.security, self.ssid, self.paswd)
        self.station_profile.create(radio=self.radio, sta_names_=[sta_name], debug=self.local_realm.debug)
        self.station_profile.admin_up()
        if self.local_realm.wait_for_ip([sta_name]):
            self.local_realm._pass("All stations got IPs", print_=True)
            if traffic_type == "download":
                self.cx_profile.create(endp_type="lf_udp", side_a=self.upstream, side_b=[sta_name],
                                       sleep_time=0)
            else:
                self.cx_profile.create(endp_type="lf_udp", side_a=[sta_name], side_b=self.upstream,
                                       sleep_time=0)
            self.cx_profile.start_cx()

            return 1
        else:
            self.local_realm._fail("Stations failed to get IPs", print_=True)
            return 0

    def start(self, traffic_type,station_list):
        print(station_list)
        #self.num_sta = num_sta
        self.traffic_type = traffic_type
        self.station_list = station_list
        """station_list = LFUtils.port_name_series(prefix="sta",
                                                start_id=0,
                                                end_id=num_sta - 1,
                                                padding_number=100,
                                                radio=self.radio)"""


        if self.build(station_list, traffic_type=traffic_type) == 0:
            print("station not created")

        else:
            print("station created")

    def stop(self):
        # Bring stations down
        self.station_profile.admin_down()
        self.cx_profile.stop_cx()



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
        #time.sleep(10)


def main():
    parser = argparse.ArgumentParser(description="SKY UK Channel selection Test Script")
    parser.add_argument('--mgr', help='hostname for where LANforge GUI is running', default='localhost')
    parser.add_argument('--mgr_port', help='port LANforge GUI HTTP service is running on', default=8080)
    parser.add_argument('--upstream_port', help='non-station port that generates traffic: eg: eth1', default='eth1')
    parser.add_argument('--num_stations', type=int, help='number of stations to create', default=1)

    parser.add_argument('--security', help='WiFi Security protocol: {open|wep|wpa2|wpa3 for vap1')
    parser.add_argument('--security1', help='WiFi Security protocol: {open|wep|wpa2|wpa3 for vap2')
    parser.add_argument('--security2', help='WiFi Security protocol: {open|wep|wpa2|wpa3 for vap3')

    parser.add_argument('--ssid', help='WiFi SSID for script object to associate to vap1')
    parser.add_argument('--ssid1', help='WiFi SSID for script object to associate to vap2')
    parser.add_argument('--ssid2', help='WiFi SSID for script object to associate to vap3')

    parser.add_argument('--passwd', help='WiFi passphrase/password/key for vap1')
    parser.add_argument('--passwd1', help='WiFi passphrase/password/key for vap2')
    parser.add_argument('--passwd2', help='WiFi passphrase/password/key for vap3')

    parser.add_argument('--num_vaps', help='Number of VAPs to Create')
    parser.add_argument('--radio', type=str, help='provide radio for vap1')
    parser.add_argument('--radio1', type=str, help='provide radio for station1')
    parser.add_argument('--radio2', type=str, help='provide radio for vap2')
    parser.add_argument('--radio4', type=str, help='provide radio for vap3')

    parser.add_argument('--radio3', type=str, help='provide radio for station2')
    parser.add_argument('--radio5', type=str, help='provide radio for station3')
    parser.add_argument( '--ip', type=str, help='AP ip')
    parser.add_argument('--user', type=str, help='credentials login/username')
    parser.add_argument('--pswd', type=str, help='credential password')
    args = parser.parse_args()
    print("creating vap")
    vap_list = LFUtils.port_name_series(prefix="vap",
                                        start_id=0,
                                        end_id=int(args.num_vaps) - 1,
                                        padding_number=100,
                                        radio=args.radio)
    for vap_name in vap_list:
        print(vap_name)
        if vap_name == '1.1.vap00':
            ssid = args.ssid
            passwd = args.passwd
            security = args.security
            radio = args.radio
        elif vap_name == '1.1.vap01':
            ssid = args.ssid1
            passwd = args.passwd1
            security = args.security1
            radio = args.radio2
        elif vap_name == '1.1.vap02':
            ssid = args.ssid2
            passwd = args.passwd2
            security = args.security2
            radio = args.radio4


        vap = Vap(_host=args.mgr,
                   _port=args.mgr_port,
                   _ssid=ssid,
                   _password=passwd,
                   _security=security,
                   _vap_list=vap_name,
                   _radio=radio)
        #vap.build(channel=1)

        if vap_name == '1.1.vap00':
            vap.build(channel=1)
        if vap_name == '1.1.vap01':
            vap.build(channel=6)
        if vap_name == '1.1.vap02':
            vap.build(channel=11)

    time.sleep(20)


    #creating station
    station_list = LFUtils.port_name_series(prefix="sta",
                                            start_id=0,
                                            end_id=args.num_stations - 1,
                                            padding_number=100,
                                            radio=args.radio)
    print("Stationlist ", station_list)

    for sta_name in station_list:
        print(sta_name)
        if sta_name == '1.1.sta00':
            #print(':radio')
            rad = args.radio1
            print(rad)
            ssid = args.ssid
            security = args.security
            passwd = args.passwd
            speed_a_min = 10000000
            speed_a_maax = 10000000
            speed_b_min = 0
            speed_b_max = 0
        elif sta_name == '1.1.sta01':
            rad = args.radio3
            ssid = args.ssid1
            security = args.security1
            passwd = args.passwd1
            speed_a_min = 60000000
            speed_a_maax = 60000000
            speed_b_min = 0
            speed_b_max = 0
        elif sta_name == '1.1.sta02':
            rad = args.radio5
            ssid = args.ssid2
            security = args.security2
            passwd = args.passwd2
            speed_a_min = 50000000
            speed_a_maax = 50000000
            speed_b_min = 0
            speed_b_max = 0

        print(sta_name)
        station = StationLayer3(lfclient_host=args.mgr,lfclient_port=args.mgr_port,
                                    ssid=ssid,security=security,
                                    paswd=passwd,radio=rad,
                                    station_list=sta_name, upstream=args.upstream_port,speed_a_min=speed_a_min,speed_a_maax=speed_a_maax,
                                    speed_b_min=speed_b_min, speed_b_max=speed_b_max)

        station.start(traffic_type="download", station_list=sta_name)


    time.sleep(20)


    print("doing ap reboot")
    ap = AP_automate(args.ip, args.user, args.pswd)
    ap.ap_reboot(args.ip, args.user, args.pswd)
    time.sleep(300)

    #after that creating station with real ap ssid to check on which channel it is being

    print("check channel ")
    var = station.local_realm.json_get("/port/1/1/sta0000?fields=channel")
    var_1 = (var['interface']['channel'])
    print("measured channel is", var_1)

if __name__ == '__main__':
    main()