import sys
import os
import argparse
import time
import numpy as np
import re
import pandas as pd
import matplotlib.pyplot as plt

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

if 'py-json' not in sys.path:
    sys.path.append('../py-json')
import LANforge
from LANforge import LFUtils
from LANforge import lfcli_base
from LANforge.lfcli_base import LFCliBase
from LANforge.LFUtils import *
import realm
from realm import Realm
from pytz import timezone
import pytz
import datetime
import pdfkit
from lf_report import lf_report
from lf_graph import lf_stacked_graph, lf_horizontal_stacked_graph, lf_bar_graph, lf_scatter_graph


# from operator import itemgetter


class STATION(LFCliBase):
    def __init__(self, lfclient_host, lfclient_port, ssid, paswd, security, sta_list=None, sta_list2=None, mode=0,
                 use_ht160=False):
        super().__init__(lfclient_host, lfclient_port)
        self.host = lfclient_host
        self.port = lfclient_port
        self.ssid = ssid
        self.paswd = paswd
        self.security = security
        self.mode = mode
        self.sta_list = sta_list
        self.sta_list2 = sta_list2
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.paswd,
        self.station_profile.security = self.security
        self.station_profile.use_ht160 = use_ht160
        if self.station_profile.use_ht160:
            self.station_profile.mode = 9
    # clean station before create
    def precleanup(self, sta_list):
        self.station_profile.cleanup(sta_list)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                           port_list=sta_list,
                                           debug=self.debug)
        time.sleep(1)

    def build(self, ip, sta_list, radio, mode):
        # create station
        self.station_profile.mode = mode
        self.station_profile.use_security(self.security, self.ssid, self.paswd)
        self.station_profile.create(radio=radio, sta_names_=sta_list, debug=self.debug)
        # cli command to run perl file through lanforge gui
        for sta_name in sta_list:
            each_sta_name = sta_name.split(".")

            data = {
                "shelf": 1,
                "resource": 1,
                "port": each_sta_name[2],
                "req_flush": 1,
                "post_ifup_script": "'./portal-bot.pl --user [BLANK] --bot bp_net.pm --ap_url http://%s:3001/wifidog/ --login_action portal/2 --logout_url portal/2 --pass [BLANK] --start_url http://www.msftconnecttest.com/redirect --login_form login/1'" % (
                    ip)}
            self.json_post("cli-json/set_wifi_extra2", data)

    def start(self):
        # station up
        self.station_profile.admin_up()

    def stop(self):
        # Bring stations down
        self.station_profile.admin_down()

    def cleanup(self):
        # clean all stations
        self.station_profile.cleanup()


def main():
    # set PST Time
    pst = pytz.timezone('America/Los_Angeles')
    start_time = datetime.datetime.now(pst)
    date = str(start_time).split(",")[0].replace(" ", "-").split(".")[0]
    time_stamp1 = datetime.datetime.now()
    parser = LFCliBase.create_bare_argparse(
        prog='clickthru_captive_portal.py',
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''Run Click Through Captive Portal Test.''',
        description='''\
    This is the Click through Captive Portal script.....
    Some examples are
    1. Run all scenarios(2.4 GHz, 5 GHz, 2.4 + 5 GHz) : python3 clickthru_captive_portal.py -mgr 192.168.200.12 -ssid portal -pwd [Blank] -sec open --radio1 wiphy0 --radio2 wiphy1 -num_port 40 --mode1 6 --mode2 10 --ip 192.168.215.49 --all_test 1 
    2. Run two scenario(2.4 GHz, 5 GHz) : python3 clickthru_captive_portal.py -mgr 192.168.200.12 -ssid portal -pwd [Blank] -sec open --radio1 wiphy0 --radio2 wiphy1 -num_port 40 --mode1 6 --mode2 1 --ip 192.168.215.49 --test_2G 1 --test_5G 1 
    3. Run one scenario only(2.4 + 5 GHz) : python3 clickthru_captive_portal.py -mgr 192.168.200.12 -ssid portal -pwd [Blank] -sec open --radio1 wiphy0 --radio2 wiphy1 -num_port 40 --mode1 6 --mode2 10 --ip 192.168.215.49 --test_both 1
    
    ''')
    parser.add_argument('-mgr', '--host', type=str, help='host name')
    parser.add_argument('-ssid', '--ssid', type=str, help='ssid for client')
    parser.add_argument('-pwd', '--passwd', type=str, help='password to connect to ssid')
    parser.add_argument('-sec', '--security', type=str, help='security')
    parser.add_argument('-radio1', '--radio1', type=str, help='radio at which client will be connected on 2.4/5 GHz')
    parser.add_argument('-radio2', '--radio2', type=str, help='radio at which client will be connected on 2.4/5 GHz')
    parser.add_argument('-num_port', '--num_port', type=str, help='number of client')
    parser.add_argument("--mode1", type=str, help="Used to force mode of stations.(enter 6 for 2.4GHz and 10 for 5GHz)")
    parser.add_argument("--mode2", type=str, help="Used to force mode of stations.(enter 6 for 2.4GHz and 10 for 5GHz)")
    parser.add_argument("--ip", type=str,
                        help="ip address of AP")
    parser.add_argument('--user', help='--Enter the username', default="admin")
    parser.add_argument('--all_test', help='--run all scenario', default=None)
    parser.add_argument('--test_2G', help='--run 2.4 GHz scenario', default=None)
    parser.add_argument('--test_5G', help='--run 5 GHz scenario', default=None)
    parser.add_argument('--test_both', help='--run 2+5 GHz scenario', default=None)
    args = parser.parse_args()

    # give setup table information
    test_setup = pd.DataFrame({
        'Device Under Test': [""],
        'SSID': [args.ssid],
        "IP": [args.ip],
        "user": [args.user],
        "Number of Stations": [args.num_port],
    })
    report = lf_report()
    # write objective in report
    report.set_title("Click Through CP Test")
    report.set_date(date)
    report.build_banner()
    report.set_obj_html("Objective",
                        "The Objective of CP Test is to verify Active Captive Portal Detection, Active Portal Tab, Incative Portal"
                        ", Error Page.")
    report.build_objective()

    report.set_obj_html("",
                        "\"CP page redirection failure\" = Verify that all the clients redirected to Splash page successfully when trying to access an http page simultaneously from all clients.")
    report.build_objective()
    report.set_obj_html("",
                        "\"CP page redirection time\" = Verify that all the clients redirected to Splash page successfully within the expected time when accessed simultaneously.")
    report.build_objective()
    report.set_obj_html("",
                        "\"Auth success\" = Verify that all the clients got Success Splash page after authentication.")
    report.build_objective()

    report.set_obj_html("",
                        "\"Auto redirection to webpage\" = Verify that Clients gets redirected to configured redirection webpage after successful authentication.")
    report.build_objective()
    report.set_obj_html("",
                        "\"Session retain\" = Verify that CP session retains for all clients when client disconnect and connect back"
                        "during the active session.")
    report.build_objective()
    report.set_table_title("Test Setup Information")
    report.build_table_title()
    report.set_table_dataframe(test_setup)
    report.build_table()
    # function to run test
    def run_test(freq, radio, mode):
        if (args.num_port is not None):
            num_sta = int(args.num_port)
        else:
            num_sta = 2
        station = STATION(lfclient_host=args.host, lfclient_port=8080, ssid=args.ssid, paswd=args.passwd,
                          security=args.security, sta_list=None, sta_list2=None, mode=mode)
        total_station = []

        # Take data from Event log from lanforge Gui
        # capture last event log id
        def get_last_event_id():
            old_event_logs = station.json_get("/events/")
            if old_event_logs is not None:
                count_old_logs = old_event_logs['events']
                log_len = len(count_old_logs)
                find_last_id = count_old_logs[log_len - 1]
                for key, value in find_last_id.items():
                    return int(key) + 1
            else:
                return int(0)

        get_id = get_last_event_id()
        print("Start Test.....")
        if radio is not None:
            # station create for single radio (either 2.4 or 5 GHz)
            sta_id = 0
            station_list = LFUtils.port_name_series(prefix="sta",
                                                    start_id=sta_id,
                                                    end_id=num_sta - 1,
                                                    padding_number=100,
                                                    radio=radio)
            station = STATION(lfclient_host=args.host, lfclient_port=8080, ssid=args.ssid, paswd=args.passwd,
                              security=args.security, sta_list=station_list, sta_list2=None, mode=mode)
            station.precleanup(station_list)
            station.build(args.ip, station_list, radio, mode)
            station.start()
            station.local_realm.wait_for_ip(station_list)
            time.sleep(60)

        else:
            # station create for both radio at time (2.4 GHz and 5 GHz)
            station_list1 = LFUtils.port_name_series(prefix="sta",
                                                     start_id=0,
                                                     end_id=int(num_sta / 2) - 1,
                                                     padding_number=100,
                                                     radio=args.radio1)
            station_list2 = LFUtils.port_name_series(prefix="sta",
                                                     start_id=int(num_sta / 2),
                                                     end_id=num_sta - 1,
                                                     padding_number=100,
                                                     radio=args.radio2)
            station = STATION(lfclient_host=args.host, lfclient_port=8080, ssid=args.ssid, paswd=args.passwd,
                              security=args.security, sta_list=station_list1, sta_list2=station_list2,
                              mode=mode)
            station.precleanup(station_list1)
            station.precleanup(station_list2)
            station.build(args.ip, station_list1, args.radio1, args.mode1)
            station.build(args.ip, station_list2, args.radio2, args.mode2)
            station.start()
            station.local_realm.wait_for_ip(station_list1)
            station.local_realm.wait_for_ip(station_list2)
            time.sleep(60)

        sta_get_ip = dict()
        portal_logs = dict()
        portal_logs_fail = dict()
        auth_sucess = []
        auth_fail = []
        redirect_pass = []
        redirect_fail = []
        session_retain_pass = []
        session_retain_fail = []
        # store all the event log from last id
        print("**************Starting ID in event log is \"%s\" for radio %s GHz*******************" % (get_id, freq))
        while True:
            all_logs = station.json_get("/events/%s" % get_id)
            get_id = get_id + 1
            if all_logs is None:
                break
            else:
                get_events = all_logs['event']
                # print(get_events)
                # This will give login success station name
                if get_events["event"] == 'IFUP-OK':
                    dt_obj = datetime.datetime.strptime(get_events['time-stamp'], "%Y-%m-%d %H:%M:%S.%f")
                    portal_logs[get_events["name"]] = dt_obj.timestamp()
                # This will give login fail station name
                if get_events["event"] == 'IFUP-FAIL':
                    dt_obj1 = datetime.datetime.strptime(get_events['time-stamp'], "%Y-%m-%d %H:%M:%S.%f")
                    portal_logs_fail[get_events["name"]] = dt_obj1.timestamp()
                # give station name and timimg when station get ip address
                if get_events["event"] == 'IPv4-Set':
                    dt_obj2 = datetime.datetime.strptime(get_events['time-stamp'], "%Y-%m-%d %H:%M:%S.%f")
                    sta_get_ip[get_events["name"]] = dt_obj2.timestamp()
                # give station name which is able/unable to get successful splash page
                if "portal login:" in get_events['event description']:
                    if "OK portal login:" in get_events['event description']:
                        auth_sucess.append(get_events["name"])
                    if "Failed portal login:" in get_events['event description']:
                        auth_fail.append(get_events["name"])
                # This gives the pass/fail station name who is able/unable to load webpage after login successfully
                if "auto redirection webpage" in get_events['event description']:
                    if "OK" in get_events['event description']:
                        redirect_pass.append(get_events["name"])
                    if "FAIL" in get_events['event description']:
                        redirect_fail.append(get_events["name"])
        if radio is not None:
            # after login CP page, station get dowm amd up again to check session retain
            get_id = get_last_event_id()
            # station down
            station.stop()
            time.sleep(5)
            # station up
            station.start()
            station.local_realm.wait_for_ip(station_list)
            time.sleep(60)
            station.cleanup()
        else:
            # after login CP page, station get dowm amd up again to check session retain
            get_id = get_last_event_id()
            # station down
            station.stop()
            time.sleep(5)
            # station up
            station.start()
            station.local_realm.wait_for_ip(station_list1)
            station.local_realm.wait_for_ip(station_list2)
            time.sleep(60)
            station.cleanup()
        while True:
            all_logs = station.json_get("/events/%s" % (get_id))
            get_id = get_id + 1
            if all_logs is None:
                break
            else:
                get_events = all_logs['event']
                # print(get_events)
                # get station names which get success/fail for session retain test
                if "session retain" in get_events['event description']:
                    if "success" in get_events['event description']:
                        session_retain_pass.append(get_events["name"])
                    if "Fail" in get_events['event description']:
                        session_retain_fail.append(get_events["name"])
        login_time = dict()
        login_fail_time = dict()
        # calculate redirection time for station which is successfully login
        # find redirection time here
        for key, value in portal_logs.items():
            for key1, value1 in sta_get_ip.items():
                if key == key1:
                    sta_name = int(key1[-2:])
                    # take timestamp difference betweem get ip address to splash page
                    login_time[sta_name] = abs(value - value1)
        # calculate redirection time for station which is Fail
        for key, value in portal_logs_fail.items():
            for key1, value1 in sta_get_ip.items():
                if key == key1:
                    sta_name = int(key1[-2:])
                    # take timestamp difference betweem get ip address to failed
                    login_fail_time[sta_name] = abs(value - value1)

        login_time_ms = []
        login_label_value = []
        for num in range(0, int(args.num_port)):
            for key, value in login_time.items():
                if num == key:
                    login_time_ms.append(value)
                    login_label_value.append(0)
                    break
            for key, value in login_fail_time.items():
                if num == key:
                    login_time_ms.append(value)
                    login_label_value.append(1)
                    break

        login_station = []
        no_login_station = []
        redirect_sta = []
        no_redirect = []
        session_retain_pass_int = []
        session_retain_fail_int = []
        for sta in auth_sucess:
            station_in_number = int(sta[-2:])
            login_station.append(station_in_number)
        for sta in auth_fail:
            station_in_number = int(sta[-2:])
            no_login_station.append(station_in_number)
        for sta in redirect_pass:
            station_in_number = int(sta[-2:])
            redirect_sta.append(station_in_number)
        for sta in redirect_fail:
            station_in_number = int(sta[-2:])
            no_redirect.append(station_in_number)
        for sta in session_retain_pass:
            station_in_number = int(sta[-2:])
            session_retain_pass_int.append(station_in_number)
        for sta in session_retain_fail:
            station_in_number = int(sta[-2:])
            session_retain_fail_int.append(station_in_number)

        auto_redirect_pass = []
        auto_redirect_fail = []
        sess_retain = []

        all_client = list(range(0, num_sta))
        pass_count = 0
        fail_count = 0
        sess_retain_cnt = 0
        sess_retain_fail_cnt = 0
        redirect_pass_count = 0
        redirect_fail_count = 0
        auth_result = []
        redirect_result = []
        login_success = []
        login_fail = []
        for sta in all_client:
            if sta in login_station:
                pass_count = pass_count + 1
                auth_result.append("Pass")
                login_success.append(1)
                if sta in session_retain_pass_int:
                    sess_retain_cnt = sess_retain_cnt + 1
                    sess_retain.append("Pass")
                else:
                    sess_retain.append("Fail")
                if sta in session_retain_fail_int:
                    sess_retain_fail_cnt = sess_retain_fail_cnt + 1
            else:
                auth_result.append("Fail")
                login_success.append(0)
                sess_retain.append("Fail")
                sess_retain_fail_cnt = sess_retain_fail_cnt + 1

            if sta in no_login_station:
                fail_count = fail_count + 1
                login_fail.append(1)
            else:
                login_fail.append(0)
            if sta in redirect_sta:
                redirect_pass_count = redirect_pass_count + 1
                redirect_result.append("Pass")
            else:
                redirect_result.append("Fail")
            if sta in no_redirect:
                redirect_fail_count = redirect_fail_count + 1
        # redirection time graph
        x_axis = [start_time + datetime.timedelta(minutes=i) for i in range(len(login_time_ms))]
        report.set_graph_title("Run CP Test on radio %s GHz" % freq)
        report.build_graph_title()
        report.set_obj_html("",
                            "The scenario gives the result of clients which is connected on %s GHz radio." % freq)
        report.build_objective()

        report.set_obj_html("CP Page Redirection Time",
                            "This graph shows the redirection time of all pass and fail clients.The time is  "
                            "calculated from the client get ip address to login successful/Failure page.")
        report.build_objective()
        graph = lf_scatter_graph(_x_data_set=x_axis, _y_data_set=[login_time_ms], _values=login_label_value,
                                 _xaxis_name="Date", _yaxis_name="Time (sec)",
                                 _graph_image_name="page_redirection_time_%s" % freq, _color=['deeppink', 'cyan'],
                                 _label=["Login OK Time", "Login Fail Time"])
        graph_png = graph.build_scatter_graph()

        print("graph name {}".format(graph_png))

        report.set_graph_image(graph_png)
        report.move_graph_image()
        report.build_graph()
        report.set_obj_html("All Pass/Fail Result",
                            "This graph shows the high level overview of all client results in percentage.")
        report.build_objective()
        pass_count = round((pass_count / int(args.num_port)) * 100, 2)
        fail_count = round((fail_count / int(args.num_port)) * 100, 2)
        redirect_pass_count = round((redirect_pass_count / int(args.num_port)) * 100, 2)
        redirect_fail_count = round((redirect_fail_count / int(args.num_port)) * 100, 2)
        sess_retain_cnt = round((sess_retain_cnt / int(args.num_port)) * 100, 2)
        sess_retain_fail_cnt = round((sess_retain_fail_cnt / int(args.num_port)) * 100, 2)
        # high level overviw of all pass/fail results
        graph = lf_horizontal_stacked_graph(_seg=3,
                                            _yaxis_set=('Auth-Success', 'Auto-Redirection', 'Session-Retain'),
                                            _xaxis_set1=[pass_count, redirect_pass_count, sess_retain_cnt],
                                            _xaxis_set2=[fail_count, redirect_fail_count, sess_retain_fail_cnt],
                                            _unit="%",
                                            _xaxis_name="Stations",
                                            _label=['Success', 'Fail'],
                                            _graph_image_name="pass_fail_result_%s" % freq,
                                            _color=["g", "r"],
                                            _figsize=(10, 4),
                                            _disable_xaxis=True)

        graph_png = graph.build_horizontal_stacked_graph()

        print("graph name {}".format(graph_png))

        report.set_graph_image(graph_png)
        report.move_graph_image()
        report.build_graph()
        dataset = [login_success, login_fail]
        x_axis_values = list(range(0, int(args.num_port) - 1))
        # graph which gives station name with auth pass/fail result
        report.set_obj_html("Auth Success/Fail Result",
                            "This graph shows which client is able/unable to get splash page after authentication.")
        report.build_objective()
        graph = lf_bar_graph(_data_set=dataset,
                             _xaxis_name="stations",
                             _yaxis_name="Login Pass/Fail",
                             _xaxis_categories=x_axis_values,
                             _graph_image_name="auth_result_%s" % freq,
                             _label=["Pass", "Fail"],
                             _color=['springgreen', 'crimson'],
                             _color_edge='white')

        graph_png = graph.build_bar_graph()

        print("graph name {}".format(graph_png))

        report.set_graph_image(graph_png)
        # need to move the graph image to the results
        report.move_graph_image()

        report.build_graph()
        for sta in all_client:
            total_station.append("station-%s" % (sta))

        # Generate Summary Table
        report.set_obj_html("Summary Table",
                            "This summary table gives the detail information of each station..")
        report.build_objective()
        try:
            dataframe2 = pd.DataFrame({
                'Station Name': total_station,
                'Redirection Time (sec)': login_time_ms,
                'Auth Success': auth_result,
                'Auto-Redirection': redirect_result,
                'Session-Retain': sess_retain
            })
            report.set_table_dataframe(dataframe2)
            report.build_table()
        except ValueError:
            print("Error : not getting event log properly")

    if (args.all_test is not None) or (args.all_test is None and args.test_2G is None and args.test_5G is None and
                                       args.test_both is None):
        print("**********************Start test on 2.4 GHz************************")
        run_test("2.4", args.radio1, args.mode1)
        print("**********************Finish test on 2.4 GHz************************")
        print("**********************Start test on 5 GHz************************")
        run_test("5", args.radio2, args.mode2)
        print("**********************Finish test on 5 GHz************************")
        print("**********************Start test on 2.4 + 5 GHz************************")
        run_test("2.4&5", None, None)
        print("**********************Finish test on 2.4 + 5 GHz************************")
    else:
        if args.test_2G is not None:
            print("**********************Start test on 2.4 GHz************************")
            run_test("2.4", args.radio1, args.mode1)
            print("**********************Finish test on 2.4 GHz************************")
        if args.test_5G is not None:
            print("**********************Start test on 5 GHz************************")
            run_test("5", args.radio2, args.mode2)
            print("**********************Finish test on 5 GHz************************")
        if args.test_both is not None:
            print("**********************Start test on 2.4 + 5 GHz************************")
            run_test("2.4&5", None, None)
            print("**********************Finish test on 2.4 + 5 GHz************************")
    time_stamp2 = datetime.datetime.now()
    test_duration = str(time_stamp2 - time_stamp1)[:-7]
    report.set_obj_html("",
                        "Total Test Duration : %s" % (str(test_duration)))
    report.build_objective()
    html_file = report.write_html()
    print("returned file ")
    print(html_file)
    report.write_pdf()


if __name__ == '__main__':
    main()
