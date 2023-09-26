import sys
import os
import pandas as pd
import importlib
import copy
import logging
import pandas as pd
import xlsxwriter
import ap_stats
import multiprocessing

logger = logging.getLogger(__name__)

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

if 'py-json' not in sys.path:
    sys.path.append(os.path.join(os.path.abspath('..'), 'py-json'))

import time
import argparse
from LANforge import LFUtils

realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
from lf_report import lf_report
from lf_graph import lf_bar_graph
from lf_graph import lf_bar_graph_horizontal
from datetime import datetime, timedelta
import requests
import json


class throughputheat(Realm):
    def __init__(self,
                 ssid=None,
                 security=None,
                 password=None,
                 name_prefix=None,
                 upstream=None,
                 num_stations=10,
                 host="localhost",
                 port=8080,
                 ap_name="",
                 traffic_type=None,
                 direction="",
                 side_a_min_rate=0, side_a_max_rate=0,
                 side_b_min_rate=56, side_b_max_rate=0,
                 number_template="00000",
                 test_duration="2m",
                 use_ht160=False,
                 _debug_on=False,
                 _exit_on_error=False,
                 _exit_on_fail=False,
                 user_list=[], real_client_list=[], real_client_list1=[], hw_list=[], laptop_list=[], android_list=[],
                 mac_list=[], windows_list=[], linux_list=[],
                 total_resources_list=[], working_resources_list=[], hostname_list=[], username_list=[], eid_list=[],
                 devices_available=[], input_devices_list=[], mac_id1_list=[], mac_id_list=[]):
        super().__init__(lfclient_host=host,
                         lfclient_port=port),
        self.upstream = upstream
        self.host = host
        self.port = port
        self.ssid = ssid
        self.security = security
        self.password = password
        self.num_stations = num_stations
        self.ap_name = ap_name
        self.traffic_type = traffic_type
        self.direction = direction
        self.number_template = number_template
        self.debug = _debug_on
        self.name_prefix = name_prefix
        self.test_duration = test_duration
        self.station_profile = self.new_station_profile()
        self.cx_profile = self.new_l3_cx_profile()
        self.station_profile.lfclient_url = self.lfclient_url
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.password
        self.station_profile.security = self.security
        self.station_profile.number_template_ = self.number_template
        self.station_profile.debug = self.debug
        self.station_profile.use_ht160 = use_ht160
        self.cx_profile.host = self.host
        self.cx_profile.port = self.port
        self.cx_profile.name_prefix = self.name_prefix
        self.cx_profile.side_a_min_bps = side_a_min_rate
        self.cx_profile.side_a_max_bps = side_a_max_rate
        self.cx_profile.side_b_min_bps = side_b_min_rate
        self.cx_profile.side_b_max_bps = side_b_max_rate
        self.hw_list = hw_list
        self.laptop_list = laptop_list
        self.android_list = android_list
        self.mac_list = mac_list
        self.windows_list = windows_list
        self.linux_list = linux_list
        self.total_resources_list = total_resources_list
        self.working_resources_list = working_resources_list
        self.hostname_list = hostname_list
        self.username_list = username_list
        self.eid_list = eid_list
        self.devices_available = devices_available
        self.input_devices_list = input_devices_list
        self.real_client_list = real_client_list
        self.real_client_list1 = real_client_list1
        self.user_list = user_list
        self.mac_id_list = mac_id_list
        self.mac_id1_list = mac_id1_list

    def os_type(self):
        response = self.json_get("/resource/all")
        for key, value in response.items():
            if key == "resources":
                for element in value:
                    for a, b in element.items():
                        self.hw_list.append(b['hw version'])
        for hw_version in self.hw_list:
            if "Win" in hw_version:
                self.windows_list.append(hw_version)
            elif "Linux" in hw_version:
                self.linux_list.append(hw_version)
            elif "Apple" in hw_version:
                self.mac_list.append(hw_version)
            else:
                if hw_version != "":
                    self.android_list.append(hw_version)
        self.laptop_list = self.windows_list + self.linux_list + self.mac_list
        # print("laptop_list :",self.laptop_list)
        # print("android_list :",self.android_list)

    def phantom_check(self):
        port_eid_list, same_eid_list, original_port_list = [], [], []
        response = self.json_get("/resource/all")
        for key, value in response.items():
            if key == "resources":
                for element in value:
                    for a, b in element.items():
                        if b['phantom'] == False:
                            self.working_resources_list.append(b["hw version"])
                            if "Win" in b['hw version']:
                                self.eid_list.append(b['eid'])
                                self.windows_list.append(b['hw version'])
                                self.devices_available.append(b['eid'] + " " + 'Win' + " " + b['hostname'])
                            elif "Linux" in b['hw version']:
                                if ('ct' or 'lf') not in b['hostname']:
                                    self.eid_list.append(b['eid'])
                                    self.linux_list.append(b['hw version'])
                                    self.devices_available.append(b['eid'] + " " + 'Lin' + " " + b['hostname'])
                            elif "Apple" in b['hw version']:
                                self.eid_list.append(b['eid'])
                                self.mac_list.append(b['hw version'])
                                self.devices_available.append(b['eid'] + " " + 'Mac' + " " + b['hostname'])
                            else:
                                self.eid_list.append(b['eid'])
                                self.android_list.append(b['hw version'])
                                self.devices_available.append(b['eid'] + " " + 'android' + " " + b['user'])

        response_port = self.json_get("/port/all")

        mac_id1_list = []
        for interface in response_port['interfaces']:
            for port, port_data in interface.items():
                if not port_data['phantom'] and not port_data['down'] and port_data['parent dev'] == "wiphy0":
                    for id in self.eid_list:
                        if id + '.' in port:
                            original_port_list.append(port)
                            port_eid_list.append(str(self.name_to_eid(port)[0]) + '.' + str(self.name_to_eid(port)[1]))
                            mac_id1_list.append(
                                str(self.name_to_eid(port)[0]) + '.' + str(self.name_to_eid(port)[1]) + ' ' + port_data[
                                    'mac'])

        same_eid_set = set()
        mac_addresses_set = set()

        # Find unique EID values
        for i in range(len(self.eid_list)):
            for j in range(len(port_eid_list)):
                if self.eid_list[i] == port_eid_list[j]:
                    same_eid_set.add(self.eid_list[i])

        # Convert the set of EIDs back to a list
        same_eid_list = [_eid + ' ' for _eid in same_eid_set]
        print("same eid list", same_eid_list)
        print("mac_id list", self.mac_id_list)
        print("self.eid_list:", self.eid_list)
        print("port_eid_list:", port_eid_list)

        same_eid_set = set()

        for i in range(len(self.eid_list)):
            for j in range(len(port_eid_list)):
                if self.eid_list[i] == port_eid_list[j]:
                    same_eid_set.add(self.eid_list[i])

        same_eid_list = [_eid + ' ' for _eid in same_eid_set]
        print("same eid list", same_eid_list)

        # devices_list = input("Enter the desired resources to run the test:")
        devices_list = same_eid_list[0]
        resource_eid_list = devices_list
        resource_eid_list2 = [eid + ' ' for eid in resource_eid_list]
        resource_eid_list1 = [resource + '.' for resource in resource_eid_list]

        for eid in resource_eid_list1:
            for ports_m in original_port_list:
                if eid in ports_m:
                    self.input_devices_list.clear()
                    self.input_devices_list.append(ports_m)
        print("INPUT DEVICES LIST", self.input_devices_list)

        self.real_client_list.clear()
        self.real_client_list1.clear()
        for i in resource_eid_list2:
            for j in range(len(self.devices_available)):
                if i in self.devices_available[j]:
                    self.real_client_list.append(self.devices_available[j])
                    self.real_client_list1.append((self.devices_available[j])[:25])
        print("REAL CLIENT LIST", self.real_client_list)

        self.num_stations = len(self.real_client_list)

        self.mac_id_list.clear()
        for eid in resource_eid_list2:
            for i in mac_id1_list:
                if eid in i:
                    self.mac_id_list.append(i.strip(eid + ' '))
        print("MAC ID LIST", self.mac_id_list)

    def start(self, print_pass=False, print_fail=False):
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

    def stop(self):
        self.cx_profile.stop_cx()
        self.station_profile.admin_down()
        test_end_time = datetime.now().strftime("%b %d %H:%M:%S")
        global endTime
        endTime = test_end_time
        print("Test ended at: ", endTime)
        return endTime

    def pre_cleanup(self):
        # self.cx_profile.cleanup_prefix()
        self.cx_profile.cleanup()

    def cleanup(self):
        self.cx_profile.cleanup()

    def build(self):
        self.create_cx()
        print("cx build finished")

    def create_cx(self):
        direction = ''
        if (int(self.cx_profile.side_b_min_bps)) != 0 and (int(self.cx_profile.side_a_min_bps)) != 0:
            self.direction = "Bi-direction"
            direction = 'Bi-di'
        elif int(self.cx_profile.side_b_min_bps) != 0:
            self.direction = "Download"
            direction = 'DL'
        else:
            if int(self.cx_profile.side_a_min_bps) != 0:
                self.direction = "Upload"
                direction = 'UL'
        print("direction", self.direction)
        traffic_type = (self.traffic_type.strip("lf_")).upper()
        traffic_direction_list, cx_list, traffic_type_list = [], [], []
        for client in range(len(self.real_client_list)):
            traffic_direction_list.append(direction)
            traffic_type_list.append(traffic_type)

        for i in self.real_client_list1:
            for j in traffic_direction_list:
                for k in traffic_type_list:
                    cxs = "%s_%s_%s" % (i, k, j)
                    cx_names = cxs.replace(" ", "")
                    # print(cx_names)
            cx_list.append(cx_names)
        print('cx_list', cx_list)
        count = 0
        for device in range(len(self.input_devices_list)):
            print("Creating connections for endpoint type: %s cx-count: %count " % (
            self.traffic_type, self.cx_profile.get_cx_count()))

            self.cx_profile.create(endp_type=self.traffic_type, side_a=[self.input_devices_list[device]],
                                   side_b=self.upstream,
                                   sleep_time=0, cx_name="%s-%i" % (cx_list[count], len(self.cx_profile.created_cx)))
            count += 1
        print("cross connections created.")

    def monitor(self):
        throughput, upload, download, upload_throughput, download_throughput, connections_upload, connections_download = {}, [], [], [], [], {}, {}
        if (self.test_duration is None) or (int(self.test_duration) <= 1):
            raise ValueError("Monitor test duration should be > 1 second")
        if self.cx_profile.created_cx is None:
            raise ValueError("Monitor needs a list of Layer 3 connections")

        # monitor columns
        start_time = datetime.now()
        test_start_time = datetime.now().strftime("%b %d %H:%M:%S")

        response_port = self.json_get("/port/all")
        print("Monitoring cx and endpoints")
        global startTime
        startTime = test_start_time
        print("Test started at: ", startTime)
        mac_id1_list = []
        for interface in response_port['interfaces']:
            for port, port_data in interface.items():
                if not port_data['phantom'] and not port_data['down'] and port_data['parent dev'] == "wiphy0":
                    for id in self.eid_list:
                        if id + '.' in port:
                            global clientMac
                            clientMac = port_data['mac']
                            ssid = port_data['ssid']
                            global clientTxrate
                            global clientRxrate
                            time.sleep(2)
                            clientTxrate = port_data['tx-rate']
                            clientRxrate = port_data['rx-rate']
                            global clientChannel
                            clientChannel = port_data['channel']
                            global clientSignal
                            clientSignal = port_data['signal']
                            print("mac address of client is:", clientMac)
                            print("channel of client is:", clientChannel)
                            print(" address of client is:", clientSignal)
                            print("tx rate iS :", clientRxrate)
                            print("tx rate is:", clientTxrate)

        end_time = start_time + timedelta(seconds=int(self.test_duration))
        index = -1

        # Initialize connections_upload and connections_download
        connections_upload = dict.fromkeys(list(self.cx_profile.created_cx.keys()), float(0))
        connections_download = dict.fromkeys(list(self.cx_profile.created_cx.keys()), float(0))

        # Initialize upload and download lists with empty lists for each connection
        upload = [[] for _ in range(len(self.cx_profile.created_cx))]
        download = [[] for _ in range(len(self.cx_profile.created_cx))]

        while datetime.now() < end_time:
            index += 1
            response = list(
                self.json_get('/cx/%s?fields=%s' % (
                    ','.join(self.cx_profile.created_cx.keys()), ",".join(['bps rx a', 'bps rx b']))).values())[2:]
            throughput[index] = list(
                map(lambda i: [x for x in i.values()], response))
            time.sleep(1)
        print("throughput", throughput)

        # Calculate upload and download throughput
        for index, key in enumerate(throughput):
            for i in range(len(throughput[key])):
                upload[i].append(throughput[key][i][1])
                download[i].append(throughput[key][i][0])
        print("UPLOAD VALUES ARE SET TO BE!!!", upload)
        print("DOWNLOAD VALUES ARE SET TO BE!!!", download)
        average_download = [sum(inner_list) / len(inner_list) for inner_list in download]
        average_upload = [sum(inner_list) / len(inner_list) for inner_list in upload]

        global avg_dw
        global avg_up
        avg_dw = average_download
        avg_up = average_upload
        print("Average Download Values:", avg_dw)
        print("Average Upload Values:", avg_up)

        # Calculate upload_throughput and download_throughput with division by zero handling
        upload_throughput = [float(f"{(sum(i) / 1000000) / len(i):.2f}") if len(i) > 0 else 0 for i in upload]
        download_throughput = [float(f"{(sum(i) / 1000000) / len(i):.2f}") if len(i) > 0 else 0 for i in download]

        keys = list(connections_upload.keys())
        keys = list(connections_download.keys())

        for i in range(len(download_throughput)):
            connections_download.update({keys[i]: float(f"{(download_throughput[i]):.2f}")})
        for i in range(len(upload_throughput)):
            connections_upload.update({keys[i]: float(f"{(upload_throughput[i]):.2f}")})

        print("upload: ", upload_throughput)
        print("download: ", download_throughput)
        print("connections download", connections_download)
        print("connections", connections_upload)

        return clientChannel, clientMac, clientSignal, clientRxrate, clientTxrate, startTime, avg_dw, avg_up, upload, download, ssid

    def convert_into_df(self, all_data_achieved):
        points = []
        rx_throughput_data = []
        avg_tp_upload = []
        avg_tp_download = []
        tx_rate = []
        rx_rate = []
        rssi = []
        channel = []
        mac = []
        start_time = []
        stop_time = []
        total_upload_data = []
        total_download_data = []

        for data in all_data_achieved:
            point_str = data[0]
            throughput_data = data[1]
            rx_throughput_data.append(data[1][6][0])
            end_time = data[2]
            print("POINT_STR IS:", point_str)
            print("throughput data is:", throughput_data)
            print("end_times is:", end_time)

            mac_str = throughput_data[1]
            rssi_value = throughput_data[2]
            upload_through = throughput_data[7][0]
            download_through = throughput_data[6][0]
            start_timestamp = throughput_data[5]
            tx_values = throughput_data[4]
            rx_values = throughput_data[3]
            total_upload_info = throughput_data[8]
            total_download_info = throughput_data[9]

            points.append(point_str)
            avg_tp_upload.append(upload_through)
            avg_tp_download.append(download_through)
            tx_rate.append(tx_values)
            rx_rate.append(rx_values)
            total_upload_data.append(total_upload_info)
            total_download_data.append(total_download_info)
            rssi.append(rssi_value)
            mac.append(mac_str)
            start_time.append(start_timestamp)
            stop_time.append(end_time)
            channel.append(throughput_data[0])

        data = {
            'Distance': points,
            'Max-throughput upload': avg_tp_upload,
            'Max-Throughput download': avg_tp_download,
            'RSSI': rssi,
            'channel': channel,
            'tx_rate': tx_rate,
            'rx_rate': rx_rate,
            'start-time': start_time,
            'stop-time': stop_time,
        }

        df = pd.DataFrame(data)

        data1 = {
            'client type': ['Android'] * len(all_data_achieved),
            'Client mac': mac,
            'Access Point': ['Eero Jupiter'] * len(all_data_achieved),
            'SSID': ['eero_wifi_2-6G-37'] * len(all_data_achieved),
        }

        df1 = pd.DataFrame(data1)

        data2 = {
            'Distance': points,
            'upload data': total_upload_data,
            'Download data': total_download_data
        }
        df2 = pd.DataFrame(data2)
        with pd.ExcelWriter('eeroHeat.xlsx', engine='xlsxwriter') as writer:
            workbook = writer.book
            worksheet = workbook.add_worksheet('Sheet1')

            # Write headers for both tables
            worksheet.write('A1', 'Table 1: Client Data')
            df1.to_excel(writer, sheet_name='Sheet1', startrow=2, index=False)
            worksheet.write('A7', 'Table 2: My Data')
            df.to_excel(writer, sheet_name='Sheet1', startrow=8, index=False)
            worksheet = writer.book.add_worksheet('Sheet2')
            worksheet.write('A1', 'Table 3:  Data')
            df2.to_excel(writer, sheet_name='Sheet2', startrow=2, index=False)


clientChannel = 0
all_data_achieved = []
avg_dw = 0
distance_from_ap_is = 0
avg_up = 0
clientMac = 0
startTime = 0
endTime = 0
clientTxrate = 0
clientRxraTE = 0
clientSignal = 0


class CanbeeRobotController:
    def __init__(self, base_url):
        self.base_url = base_url

    def post_data_to_canbee(self, data_to_send):
        try:
            json_data = json.dumps(data_to_send)
            headers = {'Content-Type': 'application/json'}
            response = requests.post(self.base_url + '/inputs', data=json_data, headers=headers)
            if response.status_code == 200:
                print('POST request was successful!')
                print('Response:', response.text)
                return True
            else:
                print('POST request failed with status code:', response.status_code)
                print('Response:', response.text)
                return False
        except Exception as e:
            print('An error occurred:', str(e))
            return False

    def get_data_from_canbee(self):
        try:
            response = requests.get(self.base_url + '/logs')
            if response.status_code == 200:
                print('GET request was successful!')
                print('Response:', response.text)
                data = json.loads(response.text)
                bot_status = data.get("bot_status")
                return bot_status
            else:
                print('GET request failed with status code:', response.status_code)
                print('Response:', response.text)
        except Exception as e:
            print('An error occurred:', str(e))

    # class.function()

    def get_distance_from_canbee(self):
        try:
            response = requests.get(self.base_url + '/readNfc')
            if response.status_code == 200:
                print('GET request 2 was successful!')
                print('Response:', response.text)
                data_acheived = json.loads(response.text)

                # Access the "Coordinate" value
                coordinate = data_acheived.get("NFC_tag", {}).get("Coordinate")
                return coordinate


            else:
                print('GET request 2 failed with status code:', response.status_code)
                print('Response:', response.text)
                return -1
        except Exception as e:
            print('An error occurred:', str(e))
            return


duration = []


def main():
    # throughputheat(host='192.168.200.161').convert_into_df(all_data_achieved=[[6, ['11', '0c:60:46:d7:b6:5a', '-57', '72 Mbps', '72 Mbps', 'Aug 23 13:15:43', [102.66666666666667], [214.66666666666666]], 'Aug 23 13:15:53'], [12, ['11', '0c:60:46:d7:b6:5a', '-58', '72 Mbps', '72 Mbps', 'Aug 23 13:16:14', [402.4], [401.4]], 'Aug 23 13:16:24']])
    # exit()
    distances = [6, 12]
    # distances = [6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66]
    parser = argparse.ArgumentParser(
        prog='throughput_QOS.py',
        formatter_class=argparse.RawTextHelpFormatter,
    )

    required = parser.add_argument_group('Required arguments to run lf_interop_qos.py')
    optional = parser.add_argument_group('Optional arguments to run lf_interop_qos.py')
    required.add_argument('--mgr',
                          '--lfmgr',
                          default='localhost',
                          help='hostname for where LANforge GUI is running')
    required.add_argument('--mgr_port',
                          '--port',
                          default=8080,
                          help='port LANforge GUI HTTP service is running on')
    required.add_argument('--upstream_port',
                          '-u',
                          default='eth1',
                          help='non-station port that generates traffic: <resource>.<port>, e.g: 1.eth1')
    required.add_argument('--security',
                          default="open",
                          help='WiFi Security protocol: < open | wep | wpa | wpa2 | wpa3 >')
    required.add_argument('--ssid',
                          help='WiFi SSID for script objects to associate to')
    required.add_argument('--passwd',
                          '--password',
                          '--key',
                          default="[BLANK]",
                          help='WiFi passphrase/password/key')
    required.add_argument('--traffic_type', help='Select the Traffic Type [lf_udp, lf_tcp]', required=True)
    required.add_argument('--upload', help='--upload traffic load per connection (upload rate)')
    required.add_argument('--download', help='--download traffic load per connection (download rate)')
    required.add_argument('--test_duration', help='--test_duration sets the duration of the test', default="2m")
    required.add_argument('--ap_name', help="AP Model Name", default="Test-AP")
    optional.add_argument('-d',
                          '--debug',
                          action="store_true",
                          help='Enable debugging')
    required.add_argument('--roboip', type=str, help='IP address for Canbee Controller')
    required.add_argument('--roboport', type=int, help='Port number for Canbee Controller')
    required.add_argument('--speed', type=int, help='Speed value for Canbee Controller')
    parser.add_argument('--channel_utilization', "--chu", "-chu",
                        help='--channel_utilization: This provides channel utilization value',
                        action='store_true')
    parser.add_argument('--memory_utilization', "--mu", "-mu",
                        help='--memory_utilization: This provides memory utilization value',
                        action='store_true')
    parser.add_argument('--cpu_utilization', "--cpu", "-cpu",
                        help='--cpu_utilization: This provides CPU utilization value',
                        action='store_true')
    parser.add_argument('--temp', "--t", "-t",
                        help='--temp: This provides Temp value',
                        action='store_true')
    # This arguments are mandatory
    parser.add_argument("--interval", "-i", "--i",
                        required=True,
                        help="Interval in the format 'h' for hours, 'm' for minutes, or 's' for seconds. ex. 10m",
                        default="1m")

    parser.add_argument("--duration", "-dur", "--dur",
                        help="Total test duration, Duration in the format 'h' for hours, 'm' for minutes, or 's' for seconds. ex. 1h")

    parser.add_argument("--count", "--c", "-c",
                        help="This can be used instead of duration, This tells script to take how many readings of interval difference"
                             "ex. if count is 2 then 2 values will be captured with user provided time interval",
                        default=1,
                        type=int)

    args = parser.parse_args()
    print("--------------------------------------------")
    print(args)
    print("--------------------------------------------")

    test_results = {'test_results': []}

    loads = {}
    station_list = []
    data = {}

    if args.download and args.upload:
        loads = {'upload': str(args.upload).split(","), 'download': str(args.download).split(",")}

    elif args.download:
        loads = {'upload': [], 'download': str(args.download).split(",")}
        for i in range(len(args.download)):
            loads['upload'].append(0)
    else:
        if args.upload:
            loads = {'upload': str(args.upload).split(","), 'download': []}
            for i in range(len(args.upload)):
                loads['download'].append(0)
    print(loads)
    if args.test_duration.endswith('s') or args.test_duration.endswith('S'):
        args.test_duration = int(args.test_duration[0:-1])
        duration = args.test_duration
        print("args are:>>>>>>", duration)
    elif args.test_duration.endswith('m') or args.test_duration.endswith('M'):
        args.test_duration = int(args.test_duration[0:-1]) * 60
    elif args.test_duration.endswith('h') or args.test_duration.endswith('H'):
        args.test_duration = int(args.test_duration[0:-1]) * 60 * 60
    elif args.test_duration.endswith(''):
        args.test_duration = int(args.test_duration)

    roboip = args.roboip
    roboport = args.roboport

    # Combine ip and port to create the base_url
    base_url = f'http://{roboip}:{roboport}'
    speed = args.speed

    canbee_controller = CanbeeRobotController(base_url)

    data_to_send = {
        "halt": "Skip",
        "mode": "Auto",
        "speed": speed
    }

    for index in range(len(loads["download"])):
        print("INDEX IS:", index)
        throughput_qos = throughputheat(host=args.mgr,
                                        port=args.mgr_port,
                                        number_template="0000",
                                        ap_name=args.ap_name,
                                        upstream=args.upstream_port,
                                        ssid=args.ssid,
                                        password=args.passwd,
                                        security=args.security,
                                        test_duration=args.test_duration,
                                        use_ht160=False,
                                        side_a_min_rate=int(loads['upload'][index]),
                                        side_b_min_rate=int(loads['download'][index]),
                                        traffic_type=args.traffic_type,
                                        _debug_on=args.debug)

    #---------------------- AP stats script code---------------------------------------------
    ap_stats_obj = ap_stats.APSerialAccess(lfclient_host=args.mgr, lfclient_port=args.mgr_port, serial_port="/dev/ttyUSB1")
    # ap_stats_obj
    count = args.count
    current_datetime = datetime.now()
    date_time = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
    def functions():
        if args.channel_utilization:
            ap_stats_obj.send_generic_commands(
                command=["iw dev ap_tt0 station dump", "iw dev ap_tt1 station dump", "iw dev ap_tt2 station dump"],
                date_time=date_time)

        if args.memory_utilization:
            ap_stats_obj.send_generic_commands(command=["free -h"], date_time=date_time)

        if args.cpu_utilization:
            ap_stats_obj.send_generic_commands(command=["mpstat -P ALL"], date_time=date_time)

        if args.temp:
            ap_stats_obj.send_generic_commands(command=["sensors"], date_time=date_time)

        if args.channel_utilization or args.memory_utilization or args.cpu_utilization or args.temp:
            txt_file_path = f'tt2_channel_utilization_{date_time}.txt'  # Change this to the appropriate file
            csv_file_path = f'bitrate_summary_{date_time}.csv'  # Change this to the desired Excel file name
            ap_stats_obj.create_csv_with_bitrate_summary(txt_file_path, csv_file_path)


    while distances:

        posted_successfully = canbee_controller.post_data_to_canbee(data_to_send)
        while posted_successfully != True:
            print("Reattempting to instruct the robot to move ahead after 3 sec")
            time.sleep(3)
            posted_successfully = canbee_controller.post_data_to_canbee(data_to_send)
            time.sleep(1)
        robot_message = canbee_controller.get_data_from_canbee()
        while robot_message != "Stopped":
            print("reading robot message after 3 sec")
            robot_message = canbee_controller.get_data_from_canbee()
            time.sleep(3)
        print("state was Stopped. soo executing the get_distance_from_canbee function")
        distance_from_ap = canbee_controller.get_distance_from_canbee()
        while distance_from_ap == -1:
            print("Retrying to get distance after 3 sec")
            time.sleep(3)
            distance_from_ap = canbee_controller.get_distance_from_canbee()
        print(distances, distance_from_ap)
        # i = input("are you ready with log")
        def ap_log():
            use_duration = False
            use_count = False
            end_time = 0
            if args.duration is not None:
                use_duration = True
                duration = ap_stats_obj.parse_time(args.duration)
                end_time = time.time() + duration

            else:
                use_count = True
            interval = ap_stats_obj.parse_time(args.interval)

            count = args.count
            while (use_duration or use_count): # Ap stats code
                if time.time() < end_time:
                    functions()
                    if (end_time - time.time() < interval):
                        break
                    print(f"Time left: {end_time - time.time()} Sec")

                elif count >= 1:
                    functions()
                    count -= 1
                    print(f"Count left: {count}")
                    if count < 1:
                        break

                print(f"Sleeping for {interval} Seconds")
                time.sleep(interval) # ap stats code
        process2 = multiprocessing.Process(target=ap_log())

        # ap_statistics = ap_stats.APSerialAccess()
        def client_log():
            for i in distances:  # Iterate through the list
                if i == distance_from_ap:  # Check if i matches the coordinate
                    distances.remove(i)
                    throughput_qos.pre_cleanup()
                    throughput_qos.os_type()
                    throughput_qos.phantom_check()
                    throughput_qos.build()
                    throughput_qos.start(False, False)
                    time.sleep(10)
                    # data_acheived= throughput_qos.monitor()
                    # print("final data is:>>><<<<<",data_acheived)
                    # stop_time_only = throughput_qos.stop()
                    # print("stop time is:", stop_time_only)
                    # all_data_achieved.append((data_achieved, stop_time_only))

                    data_achieved = throughput_qos.monitor()
                    process2.start()
                    data_achieved_as_list = list(data_achieved)
                    print("final data is:>>><<<<<", data_achieved_as_list)
                    stop_time_only = throughput_qos.stop()
                    print("stop time is:", stop_time_only)
                    all_data_achieved.append([distance_from_ap, data_achieved_as_list, stop_time_only])

                    throughput_qos.cleanup()

                    # throughput_qos.convert_into_df(all_data_achieved)
                    time.sleep(5)
                    # test_results['test_results'].append(throughput_qos.evaluate_qos(connections_download,connections_upload))
                    # data.update(test_results)
                    print("test ended")
                    print("DATA1:", all_data_achieved)

        process1 = multiprocessing.Process(target=client_log())

        # Start both processes
        process1.start()


        # Wait for the specified duration
        time.sleep(args.test_duration)

        # Terminate both processes after the specified duration
        process1.terminate()
        process2.terminate()
    throughput_qos.convert_into_df(all_data_achieved)


if __name__ == "__main__":
    main()