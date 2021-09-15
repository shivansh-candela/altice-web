#!/usr/bin/env python3

"""
NAME: rvr_test.py

PURPOSE: rvr_test.py will measure the performance of stations over a certain distance of the DUT. Distance is emulated
        using programmable attenuators and throughput test is run at each distance/RSSI step.

EXAMPLE:
python3 rvr_test.py --mgr 192.168.200.21 --mgr_port 8080 -u eth1 --num_stations 1
--radio wiphy1 --ssid TestAP5-71 --password lanforge --security wpa2 --mode 11 --a_min 1000000 --b_min 1000000 --traffic_type lf_udp

python3 rvr_test.py --num_stations 1 --radio wiphy1 --ssid ct523c-vap --password ct523c-vap --security wpa2 --mode 11 --a_min 1000000 --b_min 1000000 --traffic_type lf_udp


Use './rvr_test.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
"""

import sys
import os
import pandas as pd

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

if 'py-json' not in sys.path:
    sys.path.append(os.path.join(os.path.abspath('..'), 'py-json'))

import argparse
from LANforge import LFUtils
from realm import Realm
from lf_report import lf_report
from lf_graph import lf_bar_graph
import time
from datetime import datetime, timedelta


class RvR(Realm):
    def __init__(self, ssid=None, security=None, password="", create_sta=True, name_prefix=None, upstream=None,
                 host="localhost", port=8080,
                 mode=0, ap_model="", traffic_type="lf_tcp,lf_udp", traffic_direction="bidirectional",
                 side_a_min_rate=0, side_a_max_rate=0,
                 sta_list=None, side_b_min_rate=56, side_b_max_rate=0, number_template="00000", test_duration="2m",
                 num_stations=10,
                 serial_number='2222', indices="all", atten_val="0", traffic=500, radio="wiphy0",
                 _debug_on=False, _exit_on_error=False, _exit_on_fail=False):
        super().__init__(lfclient_host=host,
                         lfclient_port=port),
        self.upstream = upstream
        self.host = host
        self.port = port
        self.ssid = ssid
        self.security = security
        self.password = password
        self.radio = radio
        self.num_stations = num_stations
        self.station_names = sta_list
        self.create_sta = create_sta
        self.mode = mode
        self.ap_model = ap_model
        self.traffic_type = traffic_type.split(",")
        self.traffic_direction = traffic_direction
        self.traffic = traffic
        self.number_template = number_template
        self.debug = _debug_on
        self.name_prefix = name_prefix
        self.test_duration = test_duration
        self.station_profile = self.new_station_profile()
        self.station_profile.lfclient_url = self.lfclient_url
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.password
        self.station_profile.security = self.security
        self.station_profile.number_template_ = self.number_template
        self.station_profile.debug = self.debug
        self.station_profile.mode = mode
        self.cx_profile = self.new_l3_cx_profile()
        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.cx_profile.name_prefix = self.name_prefix
        self.cx_profile.side_a_min_bps = side_a_min_rate // self.num_stations
        self.cx_profile.side_a_max_bps = side_a_max_rate
        self.cx_profile.side_b_min_bps = side_b_min_rate // self.num_stations
        self.cx_profile.side_b_max_bps = side_b_max_rate
        self.attenuator_profile = self.new_attenuator_profile()
        self.serial_number = serial_number
        self.indices = indices.split(",")
        self.atten_values = atten_val

    def initialize_attenuator(self):
        self.attenuator_profile.atten_serno = self.serial_number
        self.attenuator_profile.atten_idx = "all"
        self.attenuator_profile.atten_val = '0'
        self.attenuator_profile.mode = None
        self.attenuator_profile.pulse_width_us5 = None
        self.attenuator_profile.pulse_interval_ms = None,
        self.attenuator_profile.pulse_count = None,
        self.attenuator_profile.pulse_time_ms = None
        self.attenuator_profile.create()
        # self.attenuator_profile.show()

    def set_attenuation(self, value):
        self.attenuator_profile.atten_serno = self.serial_number
        self.attenuator_profile.atten_idx = "all"
        self.attenuator_profile.atten_val = str(int(value) * 10)
        self.attenuator_profile.create()
        # self.attenuator_profile.show()

    def start_l3(self):
        if len(self.cx_profile.created_cx) > 0:
            for cx in self.cx_profile.created_cx.keys():
                req_url = "cli-json/set_cx_report_timer"
                data = {
                    "test_mgr": "all",
                    "cx_name": cx,
                    "milliseconds": 1000
                }
                self.json_post(req_url, data)
        self.cx_profile.start_cx()
        print("Monitoring CX's & Endpoints")

    def stop_l3(self):
        self.cx_profile.stop_cx()
        # self.station_profile.admin_down()

    def reset_l3(self):
        if len(self.cx_profile.created_cx) > 0:
            clear_endp = "cli-json/clear_endp_counters"
            data = {
                "endp_name": "all"
            }
            self.json_post(clear_endp, data)
            clear_cx = "cli-json/clear_cx_counters"
            data = {
                "cx_name": "all"
            }
            self.json_post(clear_cx, data)

    def pre_cleanup(self):
        self.cx_profile.cleanup_prefix()
        if self.create_sta:
            for sta in self.station_names:
                self.rm_port(sta, check_exists=True)

    def cleanup(self):
        self.cx_profile.cleanup()
        if self.create_sta:
            self.station_profile.cleanup()
            LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                               port_list=self.station_profile.station_names,
                                               debug=self.debug)

    def start_stations(self):
        self.station_profile.admin_up()
        # check here if upstream port got IP
        temp_stations = self.station_profile.station_names.copy()
        if self.wait_for_ip(temp_stations):
            self._pass("All stations got IPs")
        else:
            self._fail("Stations failed to get IPs")
            self.exit_fail()
        self._pass("PASS: Station build finished")

    def build(self):
        throughput_dbm = {}
        if len(self.traffic_type) == 2:
            throughput_dbm = {f"{self.traffic_type[0]}": {}, f"{self.traffic_type[1]}": {}}
        elif len(self.traffic_type) == 1:
            throughput_dbm = {f"{self.traffic_type[0]}": {}}
        upload, download = [], []
        self.station_profile.set_number_template(self.number_template)
        self.station_profile.use_security(security_type=self.station_profile.security,
                                          ssid=self.station_profile.ssid,
                                          passwd=self.station_profile.ssid_pass)
        print("Creating stations")
        self.station_profile.set_command_flag("add_sta", "create_admin_down", 1)
        self.station_profile.set_command_param("set_port", "report_timer", 1500)
        self.station_profile.set_command_flag("set_port", "rpt_timer", 1)
        self.station_profile.create(radio=self.radio, sta_names_=self.station_names, debug=self.debug)
        self.start_stations()
        for traffic in self.traffic_type:
            self.cx_profile.create(endp_type=traffic, side_a=self.station_profile.station_names,
                                   side_b=self.upstream,
                                   sleep_time=0)
            self.initialize_attenuator()
            for val in self.atten_values:
                throughput = {'upload': [], 'download': []}
                self.set_attenuation(value=val)
                self.start_l3()
                upload, download = self.monitor()
                # self.stop_l3()
                self.reset_l3()
                throughput['upload'] = upload
                throughput['download'] = download
                throughput_dbm[''.join(traffic)][f"{val} dB"] = throughput
            self.cx_profile.cleanup()
        print(throughput_dbm)
        return throughput_dbm

    def monitor(self):
        throughput, upload, download = {}, [], []
        if (self.test_duration is None) or (int(self.test_duration) <= 1):
            raise ValueError("Monitor test duration should be > 1 second")
        if self.cx_profile.created_cx is None:
            raise ValueError("Monitor needs a list of Layer 3 connections")
        # monitor columns
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=int(self.test_duration))
        index = -1
        connections = dict.fromkeys(list(self.cx_profile.created_cx.keys()), float(0))
        [(upload.append([]), download.append([])) for i in range(len(self.cx_profile.created_cx))]
        while datetime.now() < end_time:
            index += 1
            response = list(
                self.json_get('/cx/%s?fields=%s' % (
                    ','.join(self.cx_profile.created_cx.keys()), ",".join(['bps rx a', 'bps rx b']))).values())[2:]
            throughput[index] = list(
                map(lambda i: [x for x in i.values()], response))
            time.sleep(1)
        # # rx_rate list is calculated
        # print("Total rx values are %s", throughput)
        for index, key in enumerate(throughput):
            for i in range(len(throughput[key])):
                upload[i].append(throughput[key][i][0])
                download[i].append(throughput[key][i][1])
        print("Upload values", upload)
        print("Download Values", download)
        upload_throughput = [float(f"{(sum(i) / 1000000) / len(i): .2f}") for i in upload]
        download_throughput = [float(f"{(sum(i) / 1000000) / len(i): .2f}") for i in download]
        print("upload: ", upload_throughput)
        print("download: ", download_throughput)
        return upload_throughput, download_throughput

    def set_report_data(self, data):
        res = {}
        if data is not None:
            res = data
        else:
            print("No Data found to generate report!")
            exit(1)
        if self.traffic_type is not None:
            if self.traffic_direction == 'upload':
                for traffic in self.traffic_type:
                    for key in res[traffic]:
                        if 'download' in res[traffic][key]:
                            res[traffic][key].pop('download')
            elif self.traffic_direction == 'download':
                for traffic in self.traffic_type:
                    for key in res[traffic]:
                        if 'download' in res[traffic][key]:
                            res[traffic][key].pop('upload')
            table_df = {}
            num_stations = []
            mode = []
            graph_df = {}
            if len(self.traffic_type) == 2:
                graph_df = {f"{self.traffic_type[0]}": {}, f"{self.traffic_type[1]}": {}}
            elif len(self.traffic_type) == 1:
                graph_df = {f"{self.traffic_type[0]}": {}}
            # for case in self.traffic_type:
            #     throughput_df = []
            #     for key in res[case]:
            #         table_df.update({"No of Stations": []})
            #         table_df.update({"Mode": []})
            #         table_df.update({"Throughput for traffic {}".format(key): []})
            #     graph_df.update({case: [throughput_df]})
            # print(throughput)
            # table_df.update({"No of Stations": num_stations})
            # table_df.update({"Mode": mode})
            for traffic in self.traffic_type:
                if self.traffic_direction == 'upload':
                    graph_df[traffic].update({"upload throughput": [float(f"{sum(res[traffic][i]['upload']):.2f}") for i in res[traffic]]})
                elif self.traffic_direction == 'download':
                    graph_df[traffic].update({"download throughput": [float(f"{sum(res[traffic][i]['download']):.2f}") for i in res[traffic]]})
                elif self.traffic_direction == 'bidirectional':
                    graph_df[traffic].update({"upload throughput": [float(f"{sum(res[traffic][i]['upload']):.2f}") for i in res[traffic]]})
                    graph_df[traffic].update({"download throughput": [float(f"{sum(res[traffic][i]['download']):.2f}") for i in res[traffic]]})
            # res.update({"throughput_table_df": table_df})
            res.update({"graph_df": graph_df})
        return res

    def generate_report(self, data, test_setup_info, input_setup_info):
        res = self.set_report_data(data)
        report = lf_report(_output_pdf="rvr_test.pdf", _output_html="rvr_test.html")
        report_path = report.get_path()
        report_path_date_time = report.get_path_date_time()
        print("path: {}".format(report_path))
        print("path_date_time: {}".format(report_path_date_time))
        report.set_title("Rate vs Range")
        report.build_banner()
        # objective title and description
        report.set_obj_html(_obj_title="Objective",
                            _obj="Through this test we can measure the performance of stations over a certain distance "
                                 "of the DUT, Distance is emulated using programmable attenuators and throughput test is"
                                 "run at each distance/RSSI step")
        report.build_objective()
        report.test_setup_table(test_setup_data=test_setup_info, value="Device Under Test")
        # report.set_table_title(
        #     "Overall download Throughput for different attenuation")
        # report.build_table_title()
        # df_throughput = pd.DataFrame(res["throughput_table_df"])
        # report.set_table_dataframe(df_throughput)
        # report.build_table()
        print(res)
        for key in res["graph_df"]:
            for direction in res["graph_df"][key]:
                report.set_obj_html(
                    _obj_title=f"Overall {direction} for {len(self.station_names)} clients using {key} traffic.",
                    _obj=f"The below graph represents overall {direction} for different attenuation (RSSI) ")
                report.build_objective()
                graph = lf_bar_graph(_data_set=[res["graph_df"][key][direction]],
                                     _xaxis_name="Attenuation",
                                     _yaxis_name="Throughput(in Mbps)",
                                     _xaxis_categories=[str(key) for key in res[key].keys()],
                                     _graph_image_name=f"rvr_{key}_{direction}",
                                     _label=[str(direction).split()[0] if direction == 'upload throughput' else str(direction).split()[0]],
                                     _color=['olivedrab' if direction == 'upload throughput' else 'orangered'],
                                     _color_edge='grey',
                                     _xaxis_step=1,
                                     _graph_title="Overall throughput vs attenuation",
                                     _title_size=16,
                                     _bar_width=0.15,
                                     _figsize=(18, 6),
                                     _legend_loc="best",
                                     _legend_box=(1.0, 1.0),
                                     _dpi=96,
                                     _show_bar_value=True,
                                     _enable_csv=True)
                graph_png = graph.build_bar_graph()

                print("graph name {}".format(graph_png))

                report.set_graph_image(graph_png)
                # need to move the graph image to the results directory
                report.move_graph_image()
                report.set_csv_filename(graph_png)
                report.move_csv_file()
                report.build_graph()
        report.test_setup_table(test_setup_data=input_setup_info, value="Information")
        report.build_custom()
        report.build_footer()
        report.write_html()
        report.write_pdf()


def main():
    parser = argparse.ArgumentParser(description='''\
    rvr_test.py:
    --------------------
    Generic command layout:
    =====================================================================
    sudo python3 rvr_test.py --mgr localhost --mgr_port 8080 --upstream eth1 --num_stations 40 
    --security WPA2 --ssid NETGEAR73-5G --password fancylotus986 --radio wiphy3 --atten_serno 2222 --atten_idx all
    --atten_val 10 --test_duration 1m --ap_model WAX610 --traffic 100''', allow_abbrev=False)
    optional = parser.add_argument_group('optional arguments')
    required = parser.add_argument_group('required arguments')
    optional.add_argument('--mgr', help='hostname for where LANforge GUI is running', default='localhost')
    optional.add_argument('--mgr_port', help='port LANforge GUI HTTP service is running on', default=8080)
    optional.add_argument('--upstream', help='non-station port that generates traffic: <resource>.<port>, '
                                             'e.g: 1.eth1', default='eth1')
    optional.add_argument('--mode', help='Used to force mode of stations', default="0")
    required.add_argument('--radio', help='radio to use for creating clients', default="wiphy0")
    required.add_argument('--ssid', help="ssid for client association with Access Point", required=True)
    required.add_argument('--security', help="security type of ssid", required=True)
    required.add_argument('--password', help="password of ssid", required=True)
    required.add_argument('--traffic_type', help='provide the traffic Type lf_udp, lf_tcp', default='lf_tcp')
    optional.add_argument('--traffic_direction', help='Traffic direction i.e upload or download or bidirectional',
                          default="bidirectional")
    required.add_argument('--traffic', help='traffic to be created for each client in layer 3', required=True)
    required.add_argument('--test_duration', help='test_duration sets the duration of the test', required=True)
    optional.add_argument('--create_sta', help='Used to force a connection to a particular AP', default=True)
    optional.add_argument('--sta_names',
                          help='Used to force a connection to a particular AP, create_sta should be False',
                          default="sta0000")
    optional.add_argument('--ap_model', help="AP Model Name", default="Test-AP")
    required.add_argument('--num_stations', help='number of stations to create', required=True)
    optional.add_argument('-as', '--atten_serno', help='Serial number for requested Attenuator', default='2222')
    optional.add_argument('-ai', '--atten_idx',
                          help='Attenuator index eg. For module 1 = 0,module 2 = 1 --> --atten_idx 0,1',
                          default='all')
    optional.add_argument('-av', '--atten_val',
                          help='Requested attenuation in 1/10ths of dB (ddB) ex:--> --atten_val 0, 10', default='0')
    optional.add_argument('--debug', help="to enable debug", default=False)
    args = parser.parse_args()
    test_start_time = datetime.now().strftime("%b %d %H:%M:%S")
    print("Test started at ", test_start_time)
    print(parser.parse_args())
    if args.test_duration.endswith('s') or args.test_duration.endswith('S'):
        args.test_duration = int(args.test_duration[0:-1])
    elif args.test_duration.endswith('m') or args.test_duration.endswith('M'):
        args.test_duration = int(args.test_duration[0:-1]) * 60
    elif args.test_duration.endswith('h') or args.test_duration.endswith('H'):
        args.test_duration = int(args.test_duration[0:-1]) * 60 * 60
    elif args.test_duration.endswith(''):
        args.test_duration = int(args.test_duration)

    if args.atten_val:
        if args.atten_val.split(',')[0] != '0':
            temp = ['0']
            temp.extend(args.atten_val.split(','))
            args.atten_val = temp
        else:
            args.atten_val = args.atten_val.split(',')
    side_a, side_b = 25, 25
    if args.traffic_direction == "upload":
        side_a = 0
        side_b = int(args.traffic) * 1000000
    elif args.traffic_direction == "download":
        side_a = int(args.traffic) * 1000000
        side_b = 0
    elif args.traffic_direction == "bidirectional":
        side_a = int(args.traffic) * 1000000
        side_b = int(args.traffic) * 1000000

    if args.create_sta:
        station_list = LFUtils.portNameSeries(prefix_="sta", start_id_=0, end_id_=int(args.num_stations) - 1,
                                              padding_number_=10000,
                                              radio=args.radio)
    else:
        station_list = args.sta_names.split(",")

    rvr_obj = RvR(host=args.mgr,
                  port=args.mgr_port,
                  number_template="0000",
                  sta_list=station_list,
                  create_sta=args.create_sta,
                  num_stations=int(args.num_stations),
                  name_prefix="RvR-",
                  upstream=args.upstream,
                  radio=args.radio,
                  ssid=args.ssid,
                  password=args.password,
                  security=args.security,
                  test_duration=args.test_duration,
                  traffic=args.traffic,
                  side_a_min_rate=side_a,
                  side_b_min_rate=side_b,
                  mode=args.mode,
                  ap_model=args.ap_model,
                  serial_number=args.atten_serno,
                  indices=args.atten_idx,
                  atten_val=args.atten_val,
                  traffic_type=args.traffic_type,
                  traffic_direction=args.traffic_direction,
                  _debug_on=args.debug)

    rvr_obj.pre_cleanup()
    data = rvr_obj.build()
    rvr_obj.cleanup()

    test_end_time = datetime.now().strftime("%b %d %H:%M:%S")
    print("Test ended at: ", test_end_time)

    test_setup_info = {
        "AP Model": rvr_obj.ap_model,
        "Number of Stations": rvr_obj.num_stations,
        "SSID": rvr_obj.ssid,
        "Intended traffic": f"{rvr_obj.traffic} Mbps",
        "Test Duration": datetime.strptime(test_end_time, "%b %d %H:%M:%S") - datetime.strptime(
            test_start_time, "%b %d %H:%M:%S")
    }

    input_setup_info = {
        "contact": "support@candelatech.com"
    }
    rvr_obj.generate_report(data=data, test_setup_info=test_setup_info, input_setup_info=input_setup_info)


if __name__ == "__main__":
    main()

