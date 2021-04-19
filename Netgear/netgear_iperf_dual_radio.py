#!/usr/bin/env python3

import sys
import pprint
if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

if 'py-json' not in sys.path:
    sys.path.append('../py-json')
from LANforge.lfcli_base import LFCliBase
from LANforge.LFUtils import *
from LANforge import LFUtils
import argparse
import realm
from realm import Realm
import time
from datetime import datetime
import paramiko
from itertools import islice
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import pdfkit
from lf_report import lf_report
from lf_graph import lf_bar_graph


class IperfTest(LFCliBase):
    def __init__(self, host, port, _local_realm, ssid, security, passwd, radio="wiphy0", macvlan_type = "iperf3_serv", sta_type = "iperf3", num_ports=1, macvlan_parent=None,
                 dhcp=False,port_list=[], sta_list=[],sta_list2=[],sta_list3 =[],  tx_rate = "10000", run_time = "60",
                 side_a_speed="0M", side_b_speed="10M", _debug_on=False,_exit_on_error=False,_exit_on_fail=False):
        super().__init__(host, port,_local_realm=realm.Realm(host,port), _debug=_debug_on, _exit_on_fail=_exit_on_fail)
        self.port = port
        self.port_list = []
        self.created_cx = []
        #self.created_cx_cl = []
        self.host = host
        self.sta_list = sta_list
        self.dhcp = dhcp
        self.side_a_speed = side_a_speed
        self.side_b_speed = side_b_speed
        self.radio = radio
        self.security = security
        self.passwd = passwd
        self.ssid = ssid
        #self.created_endp_cl = []
        #self.getbps = []
        self.resulting_endpoints = {}
        self.runtime = run_time
        if macvlan_parent is not None:
            self.macvlan_parent = macvlan_parent
            self.port_list = port_list
        self.mvlan_profile = self.local_realm.new_mvlan_profile()
        self.mvlan_profile.num_macvlans = int(num_ports)
        self.mvlan_profile.desired_macvlans = self.port_list
        self.mvlan_profile.macvlan_parent = self.macvlan_parent
        self.mvlan_profile.dhcp = dhcp
        self.generic_endps_profile = self.local_realm.new_generic_endp_profile()
        self.generic_endps_profile.type = macvlan_type
        self.created_ports = []
        self.mvlan_profile.created_macvlans = self.created_ports
        self.generic_endps_profile.created_cx = self.created_cx
        self.station_profile = self.local_realm.new_station_profile()
        self._local_realm = _local_realm
        self.name_prefix = "generic"
        self.cx_profile = self.local_realm.new_l3_cx_profile()
        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.cx_profile.name_prefix = "L3Test"
        self.cx_profile.side_a_min_bps = side_a_speed
        self.cx_profile.side_a_max_bps = side_a_speed
        self.cx_profile.side_b_min_bps = self.side_b_speed
        self.cx_profile.side_b_max_bps = self.side_b_speed


    def build(self):
        #self.mvlan_profile.cleanup()
        print("Creating MACVLANs")
        self.mvlan_profile.create(admin_down=False, sleep_time=.5, debug=self.debug)
        self._pass("PASS: MACVLAN build finished")

        self.created_ports += self.mvlan_profile.created_macvlans
        self.generic_endps_profile.create(ports=self.mvlan_profile.created_macvlans, sleep_time=.5)
        #self.generic_endps_profile.create(ports=self.created_ports, sleep_time=.5)

    def generic_cleanup(self):
        print("Cleaning up cxs and endpoints")
        for cx_name in self.created_cx_cl:
            req_url = "cli-json/rm_cx"
            data = {
                "test_mgr": "default_tm",
                "cx_name": cx_name
            }
            self.json_post(req_url, data)


        for endp_name in self.created_endp_cl:
            req_url = "cli-json/rm_endp"
            data = {
                "endp_name": endp_name
            }
            self.json_post(req_url, data)
        """if len(self.created_cx) > 0:
            i=0
            for cx_name in self.created_cx:
                self.created_cx.pop(i)
                self.created_endp.pop(i)
                i=i+1"""




    def create_station(self, radio, sta_list, mode):
        self.station_profile.mode = mode
        self.station_profile.use_security(self.security, self.ssid, self.passwd)
        self.station_profile.create(radio=radio, sta_names_=sta_list, debug=self.debug)
        self.station_profile.admin_up()

    def collect_endp_stats(self, endp_map):
        self.bi_uplink = []
        self.bi_downlink = []
        self.avg_bi_dw = 0
        self.avg_bi_up = 0
        for cx_name in endp_map:
            bi_rx_up = self.json_get("/cx/" + cx_name).get(cx_name).get('bps rx a')
            bi_rx_dw = self.json_get("/cx/" + cx_name).get(cx_name).get('bps rx b')
            rx_data_up_mbps = int(bi_rx_up)/1000000
            rx_data_dw_mbps = int(bi_rx_dw) / 1000000
            self.bi_uplink.append(rx_data_up_mbps)
            self.bi_downlink.append(rx_data_dw_mbps)

            self.avg_bi_dw = self.avg_bi_dw +rx_data_dw_mbps
            self.avg_bi_up = self.avg_bi_up + rx_data_up_mbps


    def layer3_creation(self, sta_list):
        self.cx_profile.create(endp_type="lf_udp", side_a="eth1",side_b=sta_list,sleep_time=0)
        self.cx_profile.start_cx()
        time.sleep(int(self.runtime))
        self.collect_endp_stats(self.cx_profile.created_cx.keys())
        self.cx_profile.cleanup()



    def set_flags(self, endp_name, flag_name, val):
        data = {
            "name": endp_name,
            "flag": flag_name,
            "val": val
        }
        self.json_post("cli-json/set_endp_flag", data, debug_=self.debug)

    def cleanup(self, station_list):
        #self.generic_cleanup()
        self.station_profile.cleanup(station_list)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url, port_list=station_list, debug=self.debug)
        time.sleep(1)
    def create_gen_for_client(self, gen_sta_list, run_time, tx_rate, dest,gen_type, suppress_related_commands_=None, valid=None):

        if valid == False:
            self.created_cx_cl = []
            self.created_endp_cl = []
            self.getbps = []
        server_ip = 0
        endp_tpls = []
        for port_name in gen_sta_list:
            port_info = self.local_realm.name_to_eid(port_name)
            if len(port_info) == 2:
                resource = 1
                shelf = port_info[0]
                name = port_info[-1]
            elif len(port_info) == 3:
                resource = port_info[0]
                shelf = port_info[1]
                name = port_info[-1]
            else:
                raise ValueError("Unexpected name for port_name %s" % port_name)
            gen_name_a = "%s-%s" % (self.name_prefix, name)
            gen_name_b = "D_%s-%s" % (self.name_prefix, name)
            endp_tpls.append((shelf, resource, name, gen_name_a, gen_name_b))

        for endp_tpl in endp_tpls:
            shelf = endp_tpl[0]
            resource = endp_tpl[1]
            name = endp_tpl[2]
            gen_name_a = endp_tpl[3]

            data = {
                "alias": gen_name_a,
                "shelf": shelf,
                "resource": resource,
                "port": name,
                "type": "gen_generic"
            }
            if self.debug:
                pprint(data)

            self.json_post("cli-json/add_gen_endp", data, debug_=self.debug)

        self.local_realm.json_post("/cli-json/nc_show_endpoints", {"endpoint": "all"})
        time.sleep(0.5)

        for endp_tpl in endp_tpls:
            gen_name_a = endp_tpl[3]
            gen_name_b = endp_tpl[4]
            self.set_flags(gen_name_a, "ClearPortOnStart", 1)
        time.sleep(0.5)
        for endp_tpl in endp_tpls:
            name = endp_tpl[2]
            gen_name_a = endp_tpl[3]
            if gen_type == "iperf_tx":
                self.cmd = "iperf3 --forceflush --format k --precision 4 -c %s -t %s --tos 0 -b %sK --bind_dev %s -i 1 " \
                           "--pidfile /tmp/lf_helper_iperf3_%s.pid" % (dest[server_ip], run_time, tx_rate, name, gen_name_a)
            elif gen_type == "iperf_rx":
                self.cmd = "iperf3 --forceflush --format k --precision 4 -c %s -t %s -R --tos 0 -b %sK --bind_dev %s -i 1 " \
                           "--pidfile /tmp/lf_helper_iperf3_%s.pid" % (dest[server_ip], run_time, tx_rate, name, gen_name_a)
            data_cmd = {
                "name": gen_name_a,
                "command": self.cmd
            }
            self.json_post("cli-json/set_gen_cmd", data_cmd, debug_=self.debug)
            server_ip = server_ip + 1
        time.sleep(0.5)
        post_data = []
        for endp_tpl in endp_tpls:
            name = endp_tpl[2]
            gen_name_a = endp_tpl[3]
            gen_name_b = endp_tpl[4]
            cx_name = "CX_%s-%s" % (self.name_prefix, name)
            data = {
                "alias": cx_name,
                "test_mgr": "default_tm",
                "tx_endp": gen_name_a,
                "rx_endp": gen_name_b
            }
            post_data.append(data)
            self.created_cx_cl.append(cx_name)
            self.created_endp_cl.append(gen_name_a)
            self.created_endp_cl.append(gen_name_b)
            self.getbps.append(gen_name_a)

        time.sleep(0.5)

        for data in post_data:
            url = "/cli-json/add_cx"
            if self.debug:
                pprint(data)
            self.local_realm.json_post(url, data, debug_=self.debug, suppress_related_commands_=suppress_related_commands_)
            time.sleep(2)
        time.sleep(0.5)
        for data in post_data:
            self.local_realm.json_post("/cli-json/show_cx", {
                "test_mgr": "default_tm",
                "cross_connect": data["alias"]
            })
        time.sleep(0.5)

    def get_rx_data(self):
        count = 0
        self.sta_count = []
        self.downlink = []

        self.avg_dw = 0
        for endps in self.getbps:
            fields = "?fields=bps+rx"
            endp_url = "/generic/%s%s" % (endps, fields)
            endp_json = self.json_get(endp_url)
            get_rxbps_data = (endp_json['endpoint']['bps rx'])
            get_rxbps = get_rxbps_data.split()
            if get_rxbps[1].startswith("K"):
                get_rxbps[0] = float(get_rxbps[0])/10000
            elif get_rxbps[1].startswith("b"):
                get_rxbps[0] = float(get_rxbps[0]) / 1000000
            self.sta_count.append(count)
            self.avg_dw = self.avg_dw+float(get_rxbps[0])
            self.downlink.append(float(get_rxbps[0]))

            count+=1

    def get_tx_data(self):
        self.uplink = []
        self.avg_up = 0
        for endps in self.getbps:
            fields = "?fields=bps+tx"
            endp_url = "/generic/%s%s" % (endps, fields)
            endp_json = self.json_get(endp_url)
            get_txbps_data = (endp_json['endpoint']['bps tx'])
            get_txbps = get_txbps_data.split()
            if get_txbps[1].startswith("K"):
                get_txbps[0] = float(get_txbps[0])/10000
            elif get_txbps[1].startswith("b"):
                get_txbps[0] = float(get_txbps[0]) / 1000000
            self.avg_up = self.avg_up + float(get_txbps[0])
            self.uplink.append(float(get_txbps[0]))


    def generic_cx(self):

        self.generic_endps_profile.start_cx()
        time.sleep(10)
        for cx_name in self.created_cx_cl:
            self.json_post("/cli-json/set_cx_state", {
                "test_mgr": "default_tm",
                "cx_name": cx_name,
                "cx_state": "RUNNING"
            }, debug_=self.debug)
            print(".", end='')
        print("")
        time.sleep(10)
    def macvlan_cleanup(self):
        self.mvlan_profile.cleanup()
        self.generic_endps_profile.cleanup()



def main():

    parser = LFCliBase.create_bare_argparse(
        prog='create_macvlan.py',
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''Run Iperf Test.''',

        description='''\
         python netgear_Iperf_test.py --mgr 192.168.200.28 --mgr_port 8080 --macvlan_parent eth1 --num_ports 5 --radio wiphy1 --ssid Captive --passwd [Blank] --security open 

''')
    parser.add_argument('--ssid', help='SSID for stations to associate to')
    parser.add_argument('--passwd', help='Number of stations to create', default=0)
    parser.add_argument('--security', help='security type to use for ssid { wep | wpa | wpa2 | wpa3 | open }')
    parser.add_argument('--radio', help='radio EID, e.g: 1.wiphy2')
    parser.add_argument('--macvlan_parent', help='specifies parent port for macvlan creation', default=None)
    parser.add_argument('--num_ports', help='number of ports to create', default=1)
    parser.add_argument('--tx_rate', help='Enter the tx rate in Kbps eg. 10Mbps=10000k', default=10000)
    parser.add_argument('--time', help='Enter the run time in sec', default=60)
    parser.add_argument('--side_a_min_speed', help='--speed you want to monitor traffic with (max is 10G)',
                        default="0M")
    parser.add_argument('--side_b_min_speed', help='--speed you want to monitor traffic with (max is 10G)',
                        default="10M")

    args = parser.parse_args()
    time_stamp1 = datetime.now()
    port_list = []
    station_list_rad0 = []
    station_list_rad1 = []
    station_list_both = []
    max_min_value = []
    all_avg_value = []

    num_ports = int(args.num_ports)

    port_list = LFUtils.port_name_series(prefix=args.macvlan_parent + "#", start_id=0,
                                         end_id=num_ports - 1, padding_number=100000,
                                         radio=args.radio)

    def station_list(rad,start,end):
        sta_list = LFUtils.port_name_series(prefix="sta" + "#", start_id=start,
                                                     end_id=end, padding_number=100000,
                                                     radio=rad)
        return sta_list

    station_list_rad0 = station_list("wiphy0", 0, int(num_ports/2)-1)
    station_list_rad1 = station_list("wiphy1", int(num_ports/2), num_ports-1)
    station_list_both = station_list("wiphy0", 0, num_ports-1)


    ip_test = IperfTest(args.mgr, args.mgr_port, ssid=args.ssid,_local_realm = None,
                        passwd=args.passwd,
                        security=args.security,  port_list=port_list,sta_list=station_list_rad0, sta_list2=station_list_rad1,
                        sta_list3 =station_list_both, side_a_speed=args.side_a_min_speed, side_b_speed=args.side_b_min_speed,_debug_on=args.debug, macvlan_parent=args.macvlan_parent,
                        dhcp=True, num_ports=args.num_ports, tx_rate = args.tx_rate, run_time = args.time)

    ip_test.build()

    num_macvlan = 0
    target_ip_rad0 = []
    target_ip_rad1 = []
    target_ip_both = []

    # store all macvlan ip address for particular client
    while True:
        if(num_macvlan < int(num_ports/2)):
            macvlan_ip_list = ip_test.json_get("/port/1/1/eth1#%s?field=ip"% (num_macvlan))
            get_ip = (macvlan_ip_list['interface']['ip'])
            target_ip_rad0.append(get_ip)
        else:
            if(num_macvlan < num_ports):
                macvlan_ip_list = ip_test.json_get("/port/1/1/eth1#%s?field=ip" % (num_macvlan))
                get_ip = (macvlan_ip_list['interface']['ip'])
                target_ip_rad1.append(get_ip)
            else:
                break
        target_ip_both.append(get_ip)
        num_macvlan = num_macvlan + 1

    test_setup = pd.DataFrame({
        'Device Under Test': [""],
        'SSID': [args.ssid],
        "IP": ["192.168.208.18"],
        "user": ["admin"],
        "Number of Stations": ["40"],
    })

    date = str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]

    report = lf_report()
    report.set_title("Iperf-3 Test")
    report.set_date(date)
    report.build_banner()
    report.set_obj_html("Objective",
                        "Verify that number of clients connected on different/same radio can meet the intended throughput while running the traffic")
    report.build_objective()
    report.set_table_title("Test Setup Information")
    report.build_table_title()
    report.set_dataframe(test_setup)
    report.build_table()

    # method to run all scenario test
    def run_scenarios(radio_frq, radio1,radio2, mode):

        ip_test.cleanup(station_list_both)
        ip_test.cleanup(station_list_rad0)
        ip_test.cleanup(station_list_rad1)
        if radio2 is not None:
            # create stations for dual radio
            ip_test.create_station("wiphy0", station_list_rad0, "6")
            time.sleep(10)
            ip_test.create_station("wiphy1", station_list_rad1, "10")
            time.sleep(10)
            print("Starting Downlink Test")
            # create Generic station on transmit side for uploading
            ip_test.create_gen_for_client(station_list_rad0, args.time, args.tx_rate, target_ip_rad0,"iperf_tx", valid = False)
            time.sleep(10)
            ip_test.create_gen_for_client(station_list_rad1, args.time, args.tx_rate, target_ip_rad1,"iperf_tx", valid = True)
        else:
            # create stations for single radio
            ip_test.create_station(radio1, station_list_both, mode)
            time.sleep(10)
            print("Starting Downlink Test")
            # create Generic station on transmit side for uploading
            ip_test.create_gen_for_client(station_list_both, args.time, args.tx_rate, target_ip_both, "iperf_tx", valid = False)
        time.sleep(10)
        # run generic test
        ip_test.generic_cx()
        time.sleep(int(args.time))
        print("Finish Downlink Test")
        # store all uplink data
        ip_test.get_tx_data()
        time.sleep(2)
        print("Starting Uplink Test")
        # stop and clean generic client
        ip_test.generic_endps_profile.stop_cx()
        ip_test.generic_cleanup()
        time.sleep(2)
        if radio2 is not None:
            # create Generic station on rx side for downloading (single radio)
            ip_test.create_gen_for_client(station_list_rad0, args.time, args.tx_rate, target_ip_rad0, "iperf_rx", valid = False)
            time.sleep(10)
            ip_test.create_gen_for_client(station_list_rad1, args.time, args.tx_rate, target_ip_rad1, "iperf_rx", valid = True)
        else:
            # create Generic station on rx side for downloading (dual radio)
            ip_test.create_gen_for_client(station_list_both, args.time, args.tx_rate, target_ip_both, "iperf_rx", valid = False)
        time.sleep(10)
        # run generc test
        ip_test.generic_cx()
        time.sleep(int(args.time))
        print("Finish Uplink Test")
        # store all downlink data
        ip_test.get_rx_data()
        time.sleep(2)
        print("Starting Bi-Directional Test")
        # create and run layer 3 to store all data for uplink and downlink
        ip_test.layer3_creation(station_list_both)
        print("Finish Bi-Directional Test")
        # save the data
        dw = ip_test.downlink
        up = ip_test.uplink
        # save data in list to calculate avg throughput
        all_avg_value.append(ip_test.avg_dw/int(num_ports))
        all_avg_value.append(ip_test.avg_up/int(num_ports))
        all_avg_value.append(ip_test.avg_bi_dw/int(num_ports))
        all_avg_value.append(ip_test.avg_bi_up/int(num_ports))
        # save data in list to calculate min and max throughput
        max_min_value.append(min(dw))
        max_min_value.append(min(up))
        max_min_value.append(min(ip_test.bi_downlink))
        max_min_value.append(min(ip_test.bi_uplink))
        max_min_value.append(max(dw))
        max_min_value.append(max(up))
        max_min_value.append(max(ip_test.bi_downlink))
        max_min_value.append(max(ip_test.bi_uplink))

        report.set_obj_html("Download-Single Radio (%s GHz)" % (radio_frq),
                            "The scenerio gives the result of downlink test for %s clients connected on %s GHz" % (num_ports, radio_frq))
        report.build_objective()
        x_axis = ip_test.sta_count
        graph = lf_bar_graph(_data_set=[dw],
                             _xaxis_name="stations",
                             _yaxis_name="Throughput (Mbps)",
                             _xaxis_categories=x_axis,
                             _graph_image_name="downlink_radio_dw_%sGHz" % (radio_frq),
                             _label=["downlink"],
                             _color=[None],
                             _color_edge='red')

        graph_png = graph.build_bar_graph()
        print("graph name {}".format(graph_png))
        report.set_graph_image(graph_png)
        report.build_graph()
        report.set_obj_html("Upload-Single Radio (%s GHz)"% (radio_frq),
                            "The scenerio gives the result of Uplink test for %s clients connected on %s GHz" % (
                                num_ports, radio_frq))
        report.build_objective()
        graph = lf_bar_graph(_data_set=[up],
                             _xaxis_name="stations",
                             _yaxis_name="Throughput (Mbps)",
                             _xaxis_categories=x_axis,
                             _graph_image_name="uplink_radio_up_%sGHz" % (radio_frq),
                             _label=["uplink"],
                             _color=['lightcoral'],
                             _color_edge='red')

        graph_png = graph.build_bar_graph()
        print("graph name {}".format(graph_png))
        report.set_graph_image(graph_png)
        report.build_graph()

        report.set_obj_html("L3-BiDirectional-Single Radio(%s GHz)" % (radio_frq),
                            "The scenerio gives the result of BiDirectional test for %s clients connected on %s GHz" % (num_ports,
                                                                                                                       radio_frq))
        report.build_objective()
        graph = lf_bar_graph(_data_set=[ip_test.bi_downlink, ip_test.bi_uplink],
                             _xaxis_name="stations",
                             _yaxis_name="Throughput (Mbps)",
                             _xaxis_categories=x_axis,
                             _graph_image_name="Bi-Radio_%sGHz" % (radio_frq),
                             _label=["downlink", "uplink"],
                             _color=['palegreen', 'seagreen'],
                             _color_edge='red')

        graph_png = graph.build_bar_graph()
        print("graph name {}".format(graph_png))
        report.set_graph_image(graph_png)
        report.build_graph()

    print("*******************************************Start test for single radio (2.4 GHz)*****************************************")
    run_scenarios("2.4", "wiphy0", None,  "6")
    print("*************************************************Finish test for single radio (2.4 GHz)**************************************************")




    station_list_both = station_list("wiphy0", 0, num_ports - 1)
    station_list_rad0 = station_list("wiphy0", 0, int(num_ports / 2) - 1)
    station_list_rad1 = station_list("wiphy1", int(num_ports / 2), num_ports - 1)

    ip_test = IperfTest(args.mgr, args.mgr_port, ssid=args.ssid, _local_realm=None,
                        passwd=args.passwd,
                        security=args.security, port_list=port_list, sta_list=station_list_rad0,
                        sta_list2=station_list_rad1,
                        sta_list3=station_list_both, side_a_speed=args.side_a_min_speed, side_b_speed=args.side_b_min_speed,_debug_on=args.debug, macvlan_parent=args.macvlan_parent,
                        dhcp=True, num_ports=args.num_ports, tx_rate=args.tx_rate, run_time=args.time)
    print("************************Start test for single radio (5 GHz)********************************************")
    run_scenarios("5", "wiphy1", None, "10")
    print("************************************Finish test for single radio (5 GHz)********************************************")

    station_list_both = station_list("wiphy0", 0, num_ports - 1)
    station_list_rad0 = station_list("wiphy0", 0, int(num_ports / 2) - 1)
    station_list_rad1 = station_list("wiphy1", int(num_ports / 2), num_ports - 1)

    ip_test = IperfTest(args.mgr, args.mgr_port, ssid=args.ssid, _local_realm=None,
                        passwd=args.passwd,
                        security=args.security, port_list=port_list, sta_list=station_list_rad0,
                        sta_list2=station_list_rad1,
                        sta_list3=station_list_both, side_a_speed=args.side_a_min_speed,
                        side_b_speed=args.side_b_min_speed, _debug_on=args.debug, macvlan_parent=args.macvlan_parent,
                        dhcp=True, num_ports=args.num_ports, tx_rate=args.tx_rate, run_time=args.time)

    # This scenerio is for dual radio uploading and downloading


    print("*****************************Start test for single radio (2.4 + 5GHz)******************************************************")
    run_scenarios("both", "wiphy0", "wiphy1", "10")
    print("******************************************Finish test for single radio (2.4 + 5GHz)**************************************************")


    Actual_throughput = int(args.tx_rate)/1000
    time_stamp2 = datetime.now()
    test_duration = str(time_stamp2 - time_stamp1)[:-7]

    summary_data = pd.DataFrame({
        'Sr No.' : ["1","2","3","4","5","6","7","8","9"],
        'Test Scenario': ["Iperf3-download-Single radio","Iperf3-Upload-Single radio","L3-BiDirectional-Single radio",
                                    "Iperf3-download-Single radio","Iperf3-Upload-Single radio","L3-BiDirectional-Single radio",
                                    "Iperf3-download-dual radio","Iperf3-Upload-dual radio","L3-BiDirectional-dual radio"],
        'Radio' : ["2.4 GHz", "2.4 GHz", "2.4 GHz", "5 GHz", "5 GHz", "5 GHz", "2.4 Ghz +5 GHz", "2.4 Ghz +5 GHz", "2.4 Ghz +5 GHz"],
        'Traffic' : ["Downlink", "Uplink", "Downlink,Uplink", "Downlink", "Uplink", "Downlink,Uplink", "Downlink", "Uplink", "Downlink,Uplink"],
        'No. of Client': ["%s(2.4 GHz)" % (num_ports),"%s(2.4 GHz)" % (num_ports),"%s(2.4 GHz)" % (num_ports),
                         "%s(5 GHz)" % (num_ports),"%s(5 GHz)" % (num_ports),"%s(5 GHz)" % (num_ports),
                         "%s(2.4 GHz)+%s(5 GHz)" % (int(num_ports)/2,int(num_ports)/2),"%s(2.4 GHz)+%s(5 GHz)" % (int(num_ports)/2,int(num_ports)/2),
                         "%s(2.4 GHz)+%s(5 GHz)" % (int(num_ports) / 2, int(num_ports) / 2)],
        "Intended Throughput/Client": ["%s Mbps" % (Actual_throughput),"%s Mbps" % (Actual_throughput),"%s Mbps,%s Mbps" % (Actual_throughput,Actual_throughput),
                                "%s Mbps" % (Actual_throughput),
                                "%s Mbps" % (Actual_throughput),"%s Mbps,%s Mbps" % (Actual_throughput,Actual_throughput), "%s Mbps" % (Actual_throughput),
                                "%s Mbps" % (Actual_throughput),"%s Mbps,%s Mbps" % (Actual_throughput,Actual_throughput)],
        "Aggregate Throughput(Min)/Client": [str(round(float(max_min_value[0]),2)),str(round(float(max_min_value[1]),2)),"%s,%s" % (round(float(max_min_value[2]),2),round(float(max_min_value[3]),2)),
                                    str(round(float(max_min_value[8]),2)),str(round(float(max_min_value[9]),2)), "%s,%s" % (round(float(max_min_value[10]),2),round(float(max_min_value[11]),2)),
                                             str(round(float(max_min_value[16]),2)),
                                    str(round(float(max_min_value[17]),2)),"%s,%s" % (round(float(max_min_value[18]),2),round(float(max_min_value[19]),2))],
        "Aggregate Throughput(Max)/Client": [str(round(float(max_min_value[4]),2)), str(round(float(max_min_value[5]),2)), "%s,%s" % (round(float(max_min_value[6]),2),round(float(max_min_value[7]),2)),
                                    str(round(float(max_min_value[12]),2)), str(round(float(max_min_value[13]),2)), "%s,%s" % ((round(float(max_min_value[14]),2)),(round(float(max_min_value[15]),2))),
                                             str(round(float(max_min_value[20]),2)),
                                    str(round(float(max_min_value[21]),2)), "%s,%s" % (round(float(max_min_value[22]),2),round(float(max_min_value[23]),2))],
        "Overall Thrughput": [str(round(float(all_avg_value[0]),2)), str(round(float(all_avg_value[1]),2)),"%s,%s" % ((round(float(all_avg_value[2]),2)),(round(float(all_avg_value[3]),2))),
                              str(round(float(all_avg_value[4]),2)),str(round(float(all_avg_value[5]),2)),"%s,%s" % (str(round(float(all_avg_value[6]),2)),str(round(float(all_avg_value[7]),2))),
                                    str(round(float(all_avg_value[8]),2)), str(round(float(all_avg_value[9]),2)), "%s,%s" % ((round(float(all_avg_value[10]),2)),(round(float(all_avg_value[11]),2)))],
        "Aggregate Throughput(Avg)": [str(round(float(all_avg_value[0])/num_ports,2)), str(round(float(all_avg_value[1])/num_ports,2)),
                                      "%s,%s" % ((round(float(all_avg_value[2])/num_ports,2)),(round(float(all_avg_value[3])/num_ports,2))),
                                      str(round(float(all_avg_value[4])/num_ports,2)),str(round(float(all_avg_value[5])/num_ports,2)),
                                      "%s,%s" % ((round(float(all_avg_value[6])/num_ports,2)),(round(float(all_avg_value[7])/num_ports,2))),
                                      str(round(float(all_avg_value[8])/num_ports,2)),str(round(float(all_avg_value[9])/num_ports,2)),
                                    "%s,%s" % ((round(float(all_avg_value[10])/num_ports,2)),(round(float(all_avg_value[11])/num_ports,2)))]})
    report.set_obj_html("",
                        "Total Test Duration : %s" % (str(test_duration)))
    report.build_objective()
    report.set_table_title("Summary Table")
    report.build_table_title()
    report.set_dataframe(summary_data)
    report.build_table()
    html_file = report.write_html()
    print("returned file ")
    print(html_file)
    report.write_pdf()


if __name__ == "__main__":
    main()
