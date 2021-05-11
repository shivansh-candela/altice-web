#!/usr/bin/env python3

"""throughput.py will create stations and layer-3 traffic to calculate the throughput of AP.

This script will create a VAP and apply some load by creating stations in AP's channel under VAP in order to make the channel
utilized after the channel utilized to specific level again create specific number of stations each with their own set of cross-connects and endpoints.
It will then create layer 3 traffic over a specified amount of time, testing for increased traffic at regular intervals.
This test will pass if all stations increase traffic over the full test duration.

Use './throughput.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
"""

import sys
import os, paramiko, pprint

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

if 'py-json' not in sys.path:
    sys.path.append(os.path.join(os.path.abspath('..'), 'py-json'))

import argparse
from LANforge import LFUtils
from realm import Realm
from LANforge import LFRequest
from station_profile import StationProfile
from LANforge import set_port
import throughput_report
#import create_vap
import time
import datetime

# this class create VAP, station, and traffic
class IPV4VariableTime(Realm):
    def __init__(self, ssid=None,   security=None,       password=None,   sta_list=[],   name_prefix=None,   upstream=None,
                 radio=None,        host="localhost",    port=8080,       mode=0,        ap=None,            side_a_min_rate= 56,
                 side_a_max_rate=0, side_b_min_rate=56,  side_b_max_rate=0,              number_template="00000",
                 test_duration="5m", use_ht160=False,    _debug_on=False,                _exit_on_error=False,
                 _exit_on_fail=False, _vap_radio=None,   _vap_list = '1.1.vap0000', _dhcp = True ):
        super().__init__(lfclient_host=host, lfclient_port=port),
        self.upstream = upstream
        self.host = host
        self.port = port
        self.ssid = ssid
        self.sta_list = sta_list
        self.vap_list = _vap_list
        self.security = security
        self.password = password
        self.radio = radio
        self.vap_radio = _vap_radio
        self.mode = mode
        self.ap = ap
        self.number_template = number_template
        self.debug = _debug_on
        self.name_prefix = name_prefix
        self.test_duration = test_duration
        self._dhcp = _dhcp

        # initializing station profile
        self.station_profile = StationProfile(lfclient_url=self.lfclient_url,   local_realm=super(), debug_=self.debug,     up=False,
                                              dhcp = self._dhcp,                ssid = self.ssid,    ssid_pass = self.password,
                                              security = self.security,         number_template_ = self.number_template,    use_ht160 = use_ht160)#self.new_station_profile()##

        if self.station_profile.use_ht160:
            self.station_profile.mode = 9
        self.station_profile.mode = mode
        if self.ap is not None:
            self.station_profile.set_command_param("add_sta", "ap", self.ap)

        # initializing VAP profile
        self.vap_profile = self.new_vap_profile()
        self.vap_profile.vap_name = self.vap_list
        self.vap_profile.ssid = self.ssid
        self.vap_profile.security = self.security
        self.vap_profile.ssid_pass = self.password
        if self.debug:
            print("----- VAP List ----- ----- ----- ----- ----- ----- \n")
            pprint.pprint(self.vap_list)
            print("---- ~VAP List ----- ----- ----- ----- ----- ----- \n")

        # initializing traffic profile
        self.cx_profile = self.new_l3_cx_profile()
        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.cx_profile.name_prefix = self.name_prefix
        self.cx_profile.side_a_min_bps = side_a_min_rate
        self.cx_profile.side_a_max_bps = side_a_max_rate
        self.cx_profile.side_b_min_bps = side_b_min_rate
        self.cx_profile.side_b_max_bps = side_b_max_rate


    def start(self, print_pass=False, print_fail=False):
        self.station_profile.admin_up() # admin up the stations
        # to-do- check here if upstream port got IP
        temp_stas = self.station_profile.station_names.copy()

        if self.wait_for_ip(temp_stas):
            print("admin-up....")
            self._pass("All stations got IPs")
        else:
            self._fail("Stations failed to get IPs")
            self.exit_fail()
        self.cx_profile.start_cx()  # run the traffic

    def stop(self,trf = True, ad_dwn = True):
        if trf:
            self.cx_profile.stop_cx()   # stop the traffic
        if ad_dwn:
            self.station_profile.admin_down()   # admin down the stations

    def pre_cleanup(self):
        # deleting the previously created traffic, stations
        print("clearing...")
        self.cx_profile.cleanup_prefix()
        for sta in self.sta_list:
            self.rm_port(sta, check_exists=True)

    def cleanup(self):
        self.cx_profile.cleanup()   # clearing the traffic
        self.station_profile.cleanup()
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)

    def build_vaps(self):
        # create VAPs with static IP_addr, netmask, gateway_IP
        self.vap_profile.use_security(self.security, self.ssid, passwd=self.password)
        self.vap_profile.set_command_param("set_port", "ip_addr", "192.168.0.1")
        self.vap_profile.set_command_flag("set_port", "ip_address", 1)
        self.vap_profile.set_command_param("set_port", "netmask", "255.255.255.0")
        self.vap_profile.set_command_flag("set_port", "ip_Mask", 1)
        self.vap_profile.set_command_param("set_port", "gateway", "192.168.0.1")
        self.vap_profile.set_command_flag("set_port", "ip_gateway", 1)
        print("Creating VAPs")
        self.vap_profile.create(resource = 1,   radio = self.vap_radio,     channel = 36,       up_ = True,     debug = False,
                                suppress_related_commands_ = True,          use_radius = True,  hs20_enable = False)
        self._pass("PASS: VAP build finished")

    def build(self):
        # creating stations using static IP and DHCP enabled stations
        self.station_profile.use_security(self.security, self.ssid, self.password)
        self.station_profile.set_number_template(self.number_template)
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        print("Creating stations")
        start_ip = 2
        if self._dhcp:
            self.station_profile.create(radio=self.radio, sta_names_=self.sta_list, debug=self.debug)
        else:
            for sta_name in self.sta_list:
                ip = "192.168.0."+ str(start_ip)
                self.station_profile.set_command_param("set_port", "ip_addr", ip)
                self.station_profile.set_command_flag("set_port", "ip_address", 1)
                self.station_profile.set_command_param("set_port", "netmask", "255.255.255.0")
                self.station_profile.set_command_flag("set_port", "ip_Mask", 1)
                self.station_profile.set_command_param("set_port", "gateway", "192.168.0.1")
                self.station_profile.set_command_flag("set_port", "ip_gateway", 1)

                self.station_profile.create(radio=self.radio, sta_names_=[sta_name], debug=self.debug)
                start_ip += 1
        self.cx_profile.create(endp_type="lf_udp", side_a=self.station_profile.station_names, side_b=self.upstream, sleep_time=0)
        self._pass("PASS: Station build finished")

    def chn_util(self,ssh_root, ssh_passwd):
        # To find the channel utilization
        cmd = 'iwpriv wifi1vap0 get_chutil'     # command to get channel utilization
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ssh_root, 22, 'root', ssh_passwd)
            time.sleep(10)
            stdout = ssh.exec_command(cmd)
            stdout = (((stdout[1].readlines())[0].split(':'))[1].split(' '))[0]
            print(stdout, "----- channel utilization")
            return int(stdout)
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            print("####", e, "####")
            exit(1)
            #return None
        except TimeoutError as e:
            print("####", e, "####")
            exit(1)

    def throughput(self, util, sta_list):
        # bps-rx-a (download) and bps-rx-b(upload) values are taken
        bps_rx_a, bps_rx_b = [],[]

        for sta in self.cx_profile.created_cx.keys():
            if self.cx_profile.side_a_min_bps != '0':
                bps_rx_b.append(float(f"{list((self.json_get('/cx/%s?fields=bps+rx+b' % (sta))).values())[2]['bps rx b']/(1000000):.2f}"))

            if self.cx_profile.side_b_min_bps != '0':
                bps_rx_a.append(float(f"{list((self.json_get('/cx/%s?fields=bps+rx+a' % (sta))).values())[2]['bps rx a']/(100000):.2f}"))

        print(f"bps_rx_a:{bps_rx_a}\nbps_rx_b:{bps_rx_b}")
        '''\ndata-rate-a (100%){}\ndata-rate-a ({}%){}"
              "\ndata-rate-b (100%){}\ndata-rate-b ({}%){}".format(
            bps_rx_a, bps_rx_b, thrp_a,100-util,(thrp_a/100)*(100-util),thrp_b,100-util,(thrp_b/100)*(100-util)))'''

        return bps_rx_a,bps_rx_b

    def re_run_traff(self, adj_trf_rate, add_sub_rate):
        # if channel utilization level is not met re-run the traffic
        print("Re-run the traffic...")
        self.cx_profile.cleanup_prefix()
        time.sleep(.5)
        # give data rate to run the traffic
        if add_sub_rate == "sub":
            self.cx_profile.side_a_min_bps = abs(int(self.cx_profile.side_a_min_bps) - adj_trf_rate)
            self.cx_profile.side_b_min_bps = abs(int(self.cx_profile.side_b_min_bps) - adj_trf_rate)
        elif add_sub_rate == "add":
            self.cx_profile.side_a_min_bps = int(self.cx_profile.side_a_min_bps) + adj_trf_rate
            self.cx_profile.side_b_min_bps = int(self.cx_profile.side_b_min_bps) + adj_trf_rate
        self.cx_profile.created_cx.clear()
        self.cx_profile.create(endp_type="lf_udp", side_a=self.station_profile.station_names, side_b=self.upstream,
                               sleep_time=0)
        self.cx_profile.start_cx()
        print(f"-------side_a_min_bps  {self.cx_profile.side_a_min_bps}\n-------side_b_min_bps  {self.cx_profile.side_b_min_bps}")


    def check_util(self,real_cli_obj = None, util_list = None, real_cli = None, ssh_root = None, ssh_passwd = None,):
        # check the utilization and run the traffic
        bps_rx_a,bps_rx_b = [],[]
        sta_create = 1
        for util in util_list:  #  get throughput for every utilization values
            util = int(util)
            if util <= 25:
                self.cx_profile.side_a_min_bps, self.cx_profile.side_b_min_bps = 3000000, 3000000
            elif 25 < util <= 45:
                self.cx_profile.side_a_min_bps, self.cx_profile.side_b_min_bps = 25000000, 25000000
            elif 45 < util <= 65:
                self.cx_profile.side_a_min_bps, self.cx_profile.side_b_min_bps = 65000000, 65000000
            elif 65 < util <= 85:
                self.cx_profile.side_a_min_bps, self.cx_profile.side_b_min_bps = 80000000, 80000000

            util_flag = 1
            while util_flag:    #loop until the expected channel utilization will get
                util_val = self.chn_util(ssh_root, ssh_passwd)  # find the channel utilization
                if (util - 3) <= util_val <= (util + 3):
                    util_flag = 0
                    if sta_create:
                        sta_create = 0
                        real_cli_obj.build()    # create specified no.of clients once
                    real_cli_obj.start(False, False)
                    time.sleep(60)
                    _bps_rx_a, _bps_rx_b = real_cli_obj.throughput(util,real_cli)
                    bps_rx_a.append(_bps_rx_a)
                    bps_rx_b.append(_bps_rx_b)
                    real_cli_obj.stop(trf=True,ad_dwn=False)
                else:
                    # channel utilization is less than the expected utilization value
                    if util_val < (util - 3):
                        print("less than {}% util...".format(util))
                        if ((util ) - util_val) <= 4:
                            self.re_run_traff(500000, "add")
                        elif ((util ) - util_val) <= 7:
                            self.re_run_traff(1000000, "add")
                        elif ((util ) - util_val) <= 10:
                            self.re_run_traff(1500000, "add")
                        elif (util ) - util_val <= 14:
                            self.re_run_traff(3000000, "add")
                        elif (util ) - util_val > 14:
                            self.re_run_traff(5000000, "add")

                    # channel utilization is less than the expected utilization value
                    elif util_val > (util + 3):
                        print("greater than {}% util...".format(util))
                        if (util_val - (util )) <= 4:
                            self.re_run_traff(500000, "sub")
                        elif (util_val - (util )) <= 7:
                            self.re_run_traff(1000000, "sub")
                        elif (util_val - (util )) <= 10:
                            self.re_run_traff(1500000, "sub")
                        elif util_val - (util ) <= 14:
                            self.re_run_traff(3000000, "sub")
                        elif util_val - (util ) > 14:
                            self.re_run_traff(5000000, "sub")

        print("bps_rx_a ,bps_rx_b",bps_rx_a,bps_rx_b)
        # send all the collected data to genarate report
        throughput_report.thrp_rept(util = util_list, sta_num = real_cli,
                                    bps_rx_a = bps_rx_a, bps_rx_b= bps_rx_b,
                                    tbl_title = "Throughput",
                                    grp_title = "Throughput",
                                    upload = int(real_cli_obj.cx_profile.side_a_min_bps)/1000000,
                                    download = int(real_cli_obj.cx_profile.side_b_min_bps)/1000000,
                                    )


def main():
    optional = []
    required = []
    optional.append({'name': '--mode', 'help': 'Used to force mode of stations'})
    optional.append({'name': '--ap', 'help': 'Used to force a connection to a particular AP'})
    optional.append({'name': '--test_duration', 'help': '--test_duration sets the duration of the test', 'default': "2m"})
    optional.append({'name':'--num_vaps', 'help':'Number of VAPs to Create', 'default': 1})
    required.append({'name':'--vap_radio', 'help':'VAP radio', 'default': "wiphy3"})
    optional.append({'name':'--util', 'help':'channel utilization','default': "20,40"})
    required.append({'name':'--ip_ntgr','help':"IP of netgear AP", 'default': '192.168.208.13'})
    required.append({'name':'--ssh_passwd','help':'ssh password', 'default': 'Password@123xzsawq@!'})
    optional.append({'name': '--upload_ntgr', 'help': '--a_min bps rate minimum for side_a of netgear', 'default': 10000000})
    optional.append({'name': '--download_ntgr', 'help': '--b_min bps rate minimum for side_b of netgear', 'default': 10000000})
    parser = Realm.create_basic_argparse(
        prog='throughput.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
            Measure the throughput for no.of clients when the channel was already utilized by specific load
            ''',
        description='''\
throughput.py:
--------------------
Generic command layout:

python3 ./throughput.py
    --upstream_port eth1
    --vap_radio wiphy0
    --radio wiphy1
    --num_stations 32
    --num_vaps 1
    --security {open|wep|wpa|wpa2|wpa3}
    --ssid netgear
    --password admin123
    --test_duration 2m (default)
    --upload_ntgr 3000000
    --download_ntgr 1000000
    --util 20,40,60
    --ip_ntgr 192.168.208.22
    --ssh_passwd Password@123xzsawq@!
    --debug
===============================================================================
    ''', more_optional=optional, more_required = required)

    args = parser.parse_args()

    util_list = args.util.split(',') # eg: --util 20,40 is changes to [20,40]

    num_sta = lambda ars: ars if (ars != None) else 40    # if num station is None by deafault it create 2 stations

    # 4 stations created under VAP by default
    station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_= 3 , padding_number_=10000, radio=args.radio)
    # no.of vap name list
    vap_list = LFUtils.port_name_series(prefix="vap", start_id=0, end_id= int(args.num_vaps) - 1, padding_number=10000, radio=args.vap_radio)
    print(station_list,'\n',vap_list)
    # traffic data rate for stations under vap
    vap_sta_upload, vap_sta_download = 3000000, 3000000

    # create stations and run traffic under VAP
    ip_var_test = IPV4VariableTime(host=args.mgr,           port=args.mgr_port,         number_template="0000",
                                   sta_list=station_list,   name_prefix="VT",           upstream="1.1."+vap_list[0],
                                   ssid="testchannel",          password='[BLANK]',       radio=args.radio,
                                   security='open',         test_duration=args.test_duration,
                                   use_ht160=False,         side_a_min_rate= vap_sta_upload,
                                   side_b_min_rate=vap_sta_download,
                                   mode=args.mode,          ap=args.ap,                 _debug_on=args.debug,
                                   _vap_list = vap_list[0], _vap_radio = args.vap_radio, _dhcp = False)

    # ip_var_test.stop()
    # time.sleep(30)
    ip_var_test.build_vaps()  # create VAPs
    ip_var_test.pre_cleanup() # clear existing clients
    ip_var_test.build()     # create Stations and traffic

    if not ip_var_test.passes():
        print(ip_var_test.get_fail_message())
        ip_var_test.exit_fail()

    try:
        layer3connections = ','.join([[*x.keys()][0] for x in ip_var_test.json_get('endp')['endpoint']])
    except:
        raise ValueError('Try setting the upstream port flag if your device does not have an eth1 port')

    ip_var_test.start(False, False)  # start the traffic and admin-up the sta

    station_list1 = LFUtils.portNameSeries(prefix_="Thsta", start_id_=0, end_id_=int(num_sta(args.num_stations))-1, padding_number_=10000,
                                           radio=args.radio)
    print(station_list1,"station list for netgear AP.....")
    ip_var_test1 = IPV4VariableTime(host=args.mgr,          port=args.mgr_port,         number_template="0000",
                                    sta_list=station_list1, name_prefix="Thrp",         upstream=args.upstream_port,
                                    ssid= args.ssid,   password=args.passwd,       radio=args.radio,
                                    security=args.security,                        test_duration=args.test_duration,
                                    use_ht160=False,        side_a_min_rate=args.upload_ntgr,    side_b_min_rate=args.download_ntgr,
                                    mode=args.mode,         ap=args.ap,             _debug_on=args.debug,   _dhcp = True)

    ip_var_test1.pre_cleanup()  # clean the existing sta and traffics
    # check the channel utilization
    ip_var_test.check_util(real_cli_obj = ip_var_test1, util_list = util_list,
                           real_cli = station_list1,
                           ssh_root = args.ip_ntgr, ssh_passwd = args.ssh_passwd,)


    #ip_var_test.stop()
    #ip_var_test1.stop()
    if not ip_var_test.passes():
        print(ip_var_test.get_fail_message())
        ip_var_test.exit_fail()
    time.sleep(5)
    ip_var_test1.cleanup()
    ip_var_test.cleanup()
    if ip_var_test.passes():
        ip_var_test.exit_success()


if __name__ == "__main__":
    main()
