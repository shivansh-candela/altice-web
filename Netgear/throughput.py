#!/usr/bin/env python3

"""throughput.py will create stations and layer-3 traffic to measure the throughput of AP.

This script will create a VAP and apply some load by creating stations of AP's channel under VAP in order to make the channel
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


class IPV4VariableTime(Realm):
    def __init__(self, ssid=None,   security=None,       password=None,   sta_list=[],   name_prefix=None,   upstream=None,
                 radio=None,        host="localhost",    port=8080,       mode=0,        ap=None,            side_a_min_rate= 56,
                 side_a_max_rate=0, side_b_min_rate=56,  side_b_max_rate=0,              number_template="00000",
                 test_duration="5m", use_ht160=False,    _debug_on=False,                _exit_on_error=False,
                 _exit_on_fail=False, _vap_radio=None,   _vap_list = '1.1.vap0000', _dhcp = True ):
        super().__init__(lfclient_host=host, lfclient_port=port),
        #self.l3cxprofile = self.new_l3_cx_profile()
        self.upstream = upstream
        #self.side_b = _side_b
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

        #print(self.lfclient_url,"--------------")
        # create station
        self.station_profile = StationProfile(lfclient_url=self.lfclient_url,   local_realm=super(), debug_=self.debug,     up=False,
                                              dhcp = self._dhcp,                ssid = self.ssid,    ssid_pass = self.password,
                                              security = self.security,         number_template_ = self.number_template,    use_ht160 = use_ht160)#self.new_station_profile()##

        if self.station_profile.use_ht160:
            self.station_profile.mode = 9
        self.station_profile.mode = mode
        if self.ap is not None:
            self.station_profile.set_command_param("add_sta", "ap", self.ap)

        # create VAP
        self.vap_profile = self.new_vap_profile()
        self.vap_profile.vap_name = self.vap_list
        self.vap_profile.ssid = self.ssid
        self.vap_profile.security = self.security
        self.vap_profile.ssid_pass = self.password
        if self.debug:
            print("----- VAP List ----- ----- ----- ----- ----- ----- \n")
            pprint.pprint(self.vap_list)
            print("---- ~VAP List ----- ----- ----- ----- ----- ----- \n")

        # create traffic
        self.cx_profile = self.new_l3_cx_profile()
        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.cx_profile.name_prefix = self.name_prefix
        self.cx_profile.side_a_min_bps = side_a_min_rate
        self.cx_profile.side_a_max_bps = side_a_max_rate
        self.cx_profile.side_b_min_bps = side_b_min_rate
        self.cx_profile.side_b_max_bps = side_b_max_rate

        '''if _db_name != None:
            self.load(_db_name)'''

    def start(self, print_pass=False, print_fail=False):
        print("admin-up....")
        self.station_profile.admin_up() # admin up the stations
        # to-do- check here if upstream port got IP
        temp_stas = self.station_profile.station_names.copy()

        if self.wait_for_ip(temp_stas):
            self._pass("All stations got IPs")
        else:
            self._fail("Stations failed to get IPs")
            self.exit_fail()
        self.cx_profile.start_cx()

    def stop(self):
        self.cx_profile.stop_cx()
        self.station_profile.admin_down()

    def pre_cleanup(self):
        print("clearing...")
        self.cx_profile.cleanup_prefix()
        for sta in self.sta_list:
            self.rm_port(sta, check_exists=True)

    def cleanup(self):
        self.cx_profile.cleanup()
        self.station_profile.cleanup()
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=self.station_profile.station_names,
                                           debug=self.debug)

    def build_vaps(self):
        # Build VAPs
        self.vap_profile.use_security(self.security, self.ssid, passwd=self.password)
        self.vap_profile.set_command_param("set_port", "ip_addr", "192.168.0.1")  ###
        self.vap_profile.set_command_flag("set_port", "ip_address", 1)  ###
        self.vap_profile.set_command_param("set_port", "netmask", "255.255.255.0")  ###
        self.vap_profile.set_command_flag("set_port", "ip_Mask", 1)  ###
        self.vap_profile.set_command_param("set_port", "gateway", "192.168.0.1")  ###
        self.vap_profile.set_command_flag("set_port", "ip_gateway", 1)  ###
        print("Creating VAPs")
        self.vap_profile.create(resource = 1,   radio = self.vap_radio,     channel = 36,       up_ = True,     debug = False,
                                suppress_related_commands_ = True,          use_radius = True,  hs20_enable = False)
        self._pass("PASS: VAP build finished")

    def build(self):
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
                self.station_profile.set_command_param("set_port", "ip_addr", ip)  ###
                self.station_profile.set_command_flag("set_port", "ip_address", 1)  ###
                self.station_profile.set_command_param("set_port", "netmask", "255.255.255.0")  ###
                self.station_profile.set_command_flag("set_port", "ip_Mask", 1)  ###
                self.station_profile.set_command_param("set_port", "gateway", "192.168.0.1")  ###
                self.station_profile.set_command_flag("set_port", "ip_gateway", 1)  ###

                self.station_profile.create(radio=self.radio, sta_names_=[sta_name], debug=self.debug)
                start_ip += 1
        # working...|||
        '''self.station_profile.set_port_data["interest"] = self.station_profile.add_named_flags(self.station_profile.desired_set_port_interest_flags,
                                                              set_port.set_port_interest_flags)
        set_port_r = LFRequest.LFRequest(self.lfclient_url + "/cli-json/set_port", debug_=self.debug)
        #self.station_profile.set_port_data["ip_addr"] = "192.168.200.2"
        set_port_r.addPostData(self.station_profile.set_port_data)
        json_response = set_port_r.jsonPost(self.debug)'''

        '''if self.side_b != None:
            self.cx_profile.create(endp_type="lf_udp", side_a=self.station_profile.station_names, side_b=self.side_b,
                                   sleep_time=0)
        else:'''
        self.cx_profile.create(endp_type="lf_udp", side_a=self.station_profile.station_names, side_b=self.upstream, sleep_time=0)
        self._pass("PASS: Station build finished")

    # To find the channel utilization
    def chn_util(self,ssh_root, ssh_passwd):
        cmd = 'iwpriv wifi1vap0 get_chutil'     # command to get channel utilization
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ssh_root, 22, 'root', ssh_passwd)
            time.sleep(10)
            stdout = ssh.exec_command(cmd)
            stdout = (((stdout[1].readlines())[0].split(':'))[1].split(' '))[0]
            print(stdout, "----- channel utilization")#, "\n", "endp_a_min", self.cx_profile.side_a_min_bps, "\n",
                           # "endp_b_min", self.cx_profile.side_b_min_bps)
            return int(stdout)
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            print("####", e, "####")
            exit(1)
            #return None
        except TimeoutError as e:
            print("####", e, "####")
            exit(1)

    # Rx-bytes of No.of clients is listed
    def throughput(self, util, sta_list):
        bps_rx_a = {}
        bps_rx_b = {}
        pass_fail = []
        print(self.cx_profile.created_cx,"\n#############################\n",self.cx_profile.side_a_min_bps,self.cx_profile.side_b_min_bps)
        for sta in sta_list:
            eid = "Thrp{}-{}".format(sta[4:],int(sta[9:]))#self.name_to_eid(sta)

            if self.cx_profile.side_a_min_bps:
                bps_rx_a[sta] = list((self.json_get("/cx/%s?fields=bps+rx+a" % (eid))).values())[2]['bps rx a']*(10^-6)
                #avg_thrp_a = sum(bps_rx_a.values()) / len(sta_list)

            if self.cx_profile.side_b_min_bps:
                bps_rx_b[sta] = list((self.json_get("/cx/%s?fields=bps+rx+b" % (eid))).values())[2]['bps rx b']*(10^-6)
                #avg_thrp_b = sum(bps_rx_b.values()) / len(sta_list)
        thrp = self.cx_profile.side_a_min_bps*len(sta_list)
        print("bps_rx_a:{}\nbps_rx_b:{}\ndata-rate (100%){}\ndata-rate ({}%)".format(bps_rx_a,bps_rx_b,thrp,100-util,(thrp/100)*(100-util)))
        if self.cx_profile.side_a_min_bps and (thrp/100)*(100-util):

        '''throughput_report.thrp_rept(util = util,       sta_num = len(sta_list),          min = min(rx_bytes.values()),         
                                    max = max(rx_bytes.values()),  avg = avg_thrp,    tbl_title = "Throughput", 
                                    grp_title = "Throughput")
        throughput_report.thrp_rept(util,len(sta_list),
                                    "min = {} | max = {} | avg = {}".format(min(rx_bytes.values()),max(rx_bytes.values()),avg_thrp),
                                    tbl_title = "Throughput",grp_title = "Throughput")
        #, "\navarage rx_bytes",  avg_thrp,"\nmin rx_bytes",min(rx_bytes.values()),"\nmax rx_bytes",max(rx_bytes.values()))
        '''
        '''return {"min":min(bps_rx_a.values()), "max":max(bps_rx_a.values()), "avg":sum(bps_rx_a.values())/len(sta_list)},\
               {"min":min(bps_rx_b.values()), "max":max(bps_rx_b.values()), "avg":sum(bps_rx_b.values()) /len(sta_list)}'''
        return bps_rx_a,bps_rx_b
    def re_run_traff(self, adj_trf_rate, add_sub_rate):
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
        self.cx_profile.create(endp_type="lf_udp", side_a=self.station_profile.station_names, side_b=self.upstream,
                               sleep_time=0)
        self.cx_profile.start_cx()
        print(f"-------side_a_min_bps  {self.cx_profile.side_a_min_bps}\n-------side_b_min_bps  {self.cx_profile.side_b_min_bps}")
        #return self.cx_profile.side_a_min_bps, self.cx_profile.side_b_min_bps

    def check_util(self,real_cli_obj = None, util_list = None, real_cli = None, ssh_root = None, ssh_passwd = None,):
                   #upload = 2000000, download = 2000000):
        bps_rx_a,bps_rx_b = [],[]   #min, max, avg = [], [], []
        sta_create = 1
        #iter = 0
        for util in util_list:
            #iter += 1
            util = int(util)
            if util <= 25:
                self.cx_profile.side_a_min_bps, self.cx_profile.side_b_min_bps = 2500000, 2500000
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
                        real_cli_obj.build()
                    real_cli_obj.start(False, False)
                    time.sleep(60)
                    _bps_rx_a, _bps_rx_b = real_cli_obj.throughput(util,real_cli)
                    bps_rx_a.append(_bps_rx_a)
                    bps_rx_b.append(_bps_rx_b)
                    '''_min,_max,_avg = real_cli_obj.throughput(util,real_cli)
                    min.append(_min)
                    max.append(_max)
                    avg.append(_avg)'''
                    real_cli_obj.stop()
                else:
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
        throughput_report.thrp_rept(util = util_list, sta_num = real_cli,
                                    bps_rx_a = bps_rx_a, bps_rx_b= bps_rx_b,
                                    tbl_title = "Throughput",
                                    grp_title = "Throughput")


def main():
    optional = []
    optional.append({'name': '--mode', 'help': 'Used to force mode of stations'})
    optional.append({'name': '--ap', 'help': 'Used to force a connection to a particular AP'})
    #optional.append({'name': '--upload', 'help': '--a_min bps rate minimum for side_a', 'default': 2500000})
    #optional.append({'name': '--download', 'help': '--b_min bps rate minimum for side_b', 'default': 2500000})
    optional.append({'name': '--test_duration', 'help': '--test_duration sets the duration of the test', 'default': "2m"})
    '''optional.append({'name': '--port_mgr_cols', 'help': 'Columns wished to be monitored from port manager tab',
                     'default': ['ap', 'ip', 'parent dev']})
    optional.append({'name': '--compared_report', 'help': 'report path and file which is wished to be compared with new report',
                    'default': None})
    optional.append({'name': '--monitor_interval', 'help': 'how frequently do you want your monitor function to take measurements; 250ms, 35s, 2h',
                     'default': '2s'})'''
    optional.append({'name':'--num_vaps', 'help':'Number of VAPs to Create', 'default': 1})
    optional.append({'name':'--vap_radio', 'help':'Number of VAPs to Create', 'default': "wiphy3"})
    optional.append({'name':'--util', 'help':'channel utilization','default': "20,40"})
    optional.append({'name':'--num_sta_ntgr', 'help':'number of clients to connect under real AP','default': 10})
    optional.append({'name':'--ssid_ntgr', 'help':'Ssid for real AP', 'default':"channel1"})
    optional.append({'name':'--ip_ntgr','help':"IP of netgear AP", 'default': '192.168.208.22'})
    optional.append({'name':'--ssh_passwd','help':'ssh password', 'default': 'Password@123xzsawq@!'})
    optional.append({'name': '--upload_ntgr', 'help': '--a_min bps rate minimum for side_a of netgear', 'default': 10000000})
    optional.append({'name': '--download_ntgr', 'help': '--b_min bps rate minimum for side_b of netgear', 'default': 10000000})
    optional.append({'name': '--security_ntgr', 'help': '--a_min bps rate minimum for side_a of netgear', 'default': 'open'})
    optional.append({'name': '--passwd_ntgr', 'help': '--b_min bps rate minimum for side_b of netgear', 'default': '[BLANK]'})
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
    --radio wiphy0
    --num_stations 32
    --security {open|wep|wpa|wpa2|wpa3}
    --mode   1
        {"auto"   : "0",    "a"      : "1",     "b"      : "2",   "g"      : "3",       "abg"    : "4",
        "abgn"   : "5",     "bgn"    : "6",     "bg"     : "7",     "abgnAC" : "8",     "anAC"   : "9",
        "an"     : "10",    "bgnAC"  : "11",    "abgnAX" : "12",    "bgnAX"  : "13"}
    --ssid netgear
    --password admin123
    --test_duration 2m (default)
    --monitor_interval_ms 
    --a_min 3000
    --b_min 1000
    --ap "00:0e:8e:78:e1:76"
    --debug
===============================================================================
 ** FURTHER INFORMATION **
    Using the layer3_cols flag:

    Currently the output function does not support inputting the columns in layer3_cols the way they are displayed in the GUI. This quirk is under construction. To output
    certain columns in the GUI in your final report, please match the according GUI column display to it's counterpart to have the columns correctly displayed in
    your report.''', more_optional=optional)


    '''parser.add_argument('--num_sta_ntgr', help='number of clients to connect under real AP', type= int)
    parser.add_argument('--util', help= 'channel utilization', type= str)'''

    args = parser.parse_args()

    #util_list = [int(i) for i in args.util.split(',')]
    util_list = args.util.split(',')

    num_sta = lambda ars: ars if (ars != None) else 2       # if num station is None by deafault it create 2 stations

    # no.of stations name list
    station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=int(num_sta(args.num_stations))-1 , padding_number_=10000, radio=args.radio)
    print(station_list)
    # no.of vap name list
    vap_list = LFUtils.port_name_series(prefix="vap", start_id=0, end_id= int(args.num_vaps) - 1, padding_number=10000, radio=args.vap_radio)
    print(vap_list)
    # traffic data rate for stations under vap
    vap_sta_upload = 2500000
    vap_sta_download = 2500000
    # create stations and run traffic under VAP
    ip_var_test = IPV4VariableTime(host=args.mgr,           port=args.mgr_port,         number_template="0000",
                                   sta_list=station_list,   name_prefix="VT",           upstream="1.1."+vap_list[0],
                                   ssid=args.ssid,          password=args.passwd,       radio=args.radio,
                                   security=args.security,  test_duration=args.test_duration,
                                   use_ht160=False,         side_a_min_rate= vap_sta_upload,
                                   side_b_min_rate=vap_sta_download,
                                   mode=args.mode,          ap=args.ap,                 _debug_on=args.debug,
                                   _vap_list = vap_list[0], _vap_radio = args.vap_radio, _dhcp = False)

    # ip_var_test.stop()
    # time.sleep(30)
    ip_var_test.build_vaps()  # create VAPs
    ip_var_test.pre_cleanup() # clear existing clients
    ip_var_test.build()     # create Stations

    if not ip_var_test.passes():
        print(ip_var_test.get_fail_message())
        ip_var_test.exit_fail()

    try:
        layer3connections = ','.join([[*x.keys()][0] for x in ip_var_test.json_get('endp')['endpoint']])
    except:
        raise ValueError('Try setting the upstream port flag if your device does not have an eth1 port')

    ip_var_test.start(False, False)  # start the traffic and admin-up the sta

    station_list1 = LFUtils.portNameSeries(prefix_="Thsta", start_id_=0, end_id_=int(args.num_sta_ntgr)-1, padding_number_=10000,
                                           radio=args.radio)
    print(station_list1,"station list for netgear AP.....")
    ip_var_test1 = IPV4VariableTime(host=args.mgr,          port=args.mgr_port,         number_template="0000",
                                    sta_list=station_list1, name_prefix="Thrp",         upstream=args.upstream_port,
                                    ssid= args.ssid_ntgr,   password=args.passwd_ntgr,  radio=args.radio,
                                    security=args.security_ntgr,                        test_duration=args.test_duration,
                                    use_ht160=False,        side_a_min_rate=args.upload_ntgr,    side_b_min_rate=args.download_ntgr,
                                    mode=args.mode,         ap=args.ap,             _debug_on=args.debug,   _dhcp = True)

    ip_var_test1.pre_cleanup()  # clean the existing sta and traffics
    # check the channel utilization
    ip_var_test.check_util(real_cli_obj = ip_var_test1, util_list = util_list,
                           real_cli = station_list1,
                           ssh_root = args.ip_ntgr, ssh_passwd = args.ssh_passwd,)
                           #upload = vap_sta_upload, download = vap_sta_download)

    #ip_var_test.stop()
    #ip_var_test1.stop()
    if not ip_var_test.passes():
        print(ip_var_test.get_fail_message())
        ip_var_test.exit_fail()
    time.sleep(5)
    #ip_var_test1.cleanup()
    #ip_var_test.cleanup()
    if ip_var_test.passes():
        ip_var_test.exit_success()


if __name__ == "__main__":
    main()
