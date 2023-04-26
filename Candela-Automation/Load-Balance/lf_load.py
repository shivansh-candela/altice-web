import sys
import os
import argparse
import time
import datetime
from datetime import datetime
import logging
import paramiko
from itertools import islice

# sys.path.append('/home/lanforge/.local/lib/python3.6/site-packages')

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)
if 'py-json' not in sys.path:
    sys.path.append('../py-json')

from LANforge.LFUtils import *
from test_client_admission import LoadLayer3
from test_num_client import Station_Connect
from one_station import Station
from load_template import *


class Attenuator:
    def __init__(self):
        pass

    def set_att_dbm(self, attenuator, attenuator_value):
        attenuator_value = str(attenuator_value)
        attenuator = str(attenuator)
        cmd = "./lf_attenmod.pl --action set_atten --atten_serno " + attenuator + " --atten_idx all --atten_val " + attenuator_value
        os.chdir("/home/lanforge/lanforge-scripts")
        os.system(str(cmd))


class AP_Automate:
    def __init__(self, ip, user, pswd, ch_threshold):
        self.ip = ip
        self.user = user
        self.pswd = pswd
        self.ch_threshold = ch_threshold

    def get_ap_model(self, ip, user, pswd):
        self.ip = ip
        self.user = user
        self.pswd = pswd
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(ip, port=22, username=user, password=pswd)
        stdin, stdout, stderr = ssh.exec_command('printmd')
        output = stdout.readlines()
        ssh.close()
        return output

    def set_channel_in_ap_at_(self, ip, user, pswd, channel):
        self.ip = ip
        self.user = user
        self.pswd = pswd
        channel = str(channel)
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # automatically adds the missing host key
        ssh.connect(ip, port=22, username=user, password=pswd)
        if channel == "6":
            command = "conf_set system:wlanSettings:wlanSettingTable:wlan0:channel " + channel
        elif channel == "36":
            command = "conf_set system:wlanSettings:wlanSettingTable:wlan1:channel " + channel
        else:
            command = "conf_set system:wlanSettings:wlanSettingTable:wlan2:channel " + channel
        stdin, stdout, stderr = ssh.exec_command(str(command))
        output = stdout.readlines()
        ssh.close()
        time.sleep(10)

    def set_channel_utilztn2ghz_threashold(self, ip, user, pswd, ch_threshold):
        self.ip = ip
        self.user = user
        self.pswd = pswd
        self.ch_threshold = ch_threshold
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(ip, port=22, username=user, password=pswd)
        command = "conf_set system:wlanSettings:wlanSettingTable:wlan0:channelUtilisationLoadBalanceThreshold " + str(
            ch_threshold)
        stdin, stdout, stderr = ssh.exec_command(str(command))
        output = stdout.readlines()
        ssh.close()

    def set_channel_utilztn5ghz_threashold(self, ip, user, pswd, ch_threshold5):
        self.ip = ip
        self.user = user
        self.pswd = pswd
        self.ch_threshold5 = ch_threshold5
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(ip, port=22, username=user, password=pswd)
        command = "conf_set system:wlanSettings:wlanSettingTable:wlan1:channelUtilisationLoadBalanceThreshold " + str(
            ch_threshold5)
        stdin, stdout, stderr = ssh.exec_command(str(command))
        output = stdout.readlines()
        ssh.close()

    def set_channel_utilztn5ghzh_threashold(self, ip, user, pswd, ch_threshold5h):
        self.ip = ip
        self.user = user
        self.pswd = pswd
        self.ch_threshold5h = ch_threshold5h
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(ip, port=22, username=user, password=pswd)
        command = "conf_set system:wlanSettings:wlanSettingTable:wlan2:channelUtilisationLoadBalanceThreshold " + str(
            ch_threshold5h)
        stdin, stdout, stderr = ssh.exec_command(str(command))
        output = stdout.readlines()
        ssh.close()

    def check_Rssi_from_ap(self, ip, user, pswd):
        self.ip = ip
        self.user = user
        self.pswd = pswd
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(ip, port=22, username=user, password=pswd)
        stdin, stdout, stderr = ssh.exec_command('cat /tmp/log/messages | grep rssi')
        output = stdout.readlines()
        # print('\n'.join(output))
        time.sleep(1)
        return output

    def check_channel_utilization_ap(self, ip, user, pswd, channel):
        self.ip = ip
        self.user = user
        self.pswd = pswd
        self.channel = channel
        if channel == "6":
            command = 'iwpriv wifi0vap0 get_chutil'
        elif channel == "36":
            command = 'iwpriv wifi1vap0 get_chutil'
        else:
            command = 'iwpriv wifi2vap0 get_chutil'
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(ip, port=22, username=user, password=pswd)
        stdin, stdout, stderr = ssh.exec_command(str(command))
        output = stdout.readlines()
        ssh.close()
        return output

    def set_max_client_threshold(self, ip, user, pswd, channel, client, client5, client5h):
        self.ip = ip
        self.user = user
        self.pswd = pswd
        self.channel = channel
        self.client = client
        self.client5 = client5
        self.client5h = client5h
        if channel == "6":
            command = 'conf_set system:wlanSettings:wlanSettingTable:wlan0:maxWirelessClients ' + str(client)
        elif channel == "36":
            command = 'conf_set system:wlanSettings:wlanSettingTable:wlan1:maxWirelessClients ' + str(client5)
        else:
            command = 'conf_set system:wlanSettings:wlanSettingTable:wlan2:maxWirelessClients ' + str(client5h)
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(ip, port=22, username=user, password=pswd)
        stdin, stdout, stderr = ssh.exec_command(str(command))
        output = stdout.readlines()
        ssh.close()
        return output

    def set_rssi_threshold(self, ip, user, pswd, channel, rssi2, rssi5l, rssi5h):
        self.ip = ip
        self.user = user
        self.pswd = pswd
        self.channel = channel
        self.rssi2 = rssi2
        self.rssi5l = rssi5l
        self.rssi5h = rssi5h
        if channel == "6":
            command = 'conf_set system:wlanSettings:wlanSettingTable:wlan0:receiveRSSILoadBalancingThreshold ' + str(
                rssi2)
        elif channel == "36":
            command = 'conf_set system:wlanSettings:wlanSettingTable:wlan1:receiveRSSILoadBalancingThreshold ' + str(
                rssi5l)
        else:
            command = 'conf_set system:wlanSettings:wlanSettingTable:wlan2:receiveRSSILoadBalancingThreshold ' + str(
                rssi5h)
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(ip, port=22, username=user, password=pswd)
        stdin, stdout, stderr = ssh.exec_command(str(command))
        output = stdout.readlines()
        ssh.close()
        return output

    def Max_client_value_from_ap(self, ip, user, pswd, channel):
        self.ip = ip
        self.user = user
        self.pswd = pswd
        self.channel = channel
        if channel == "6":
            command = 'wlanconfig wifi0vap0 list sta'
        elif channel == "36":
            command = 'wlanconfig wifi1vap0 list sta'
        else:
            command = 'wlanconfig wifi2vap0 list sta'
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(ip, port=22, username=user, password=pswd)
        stdin, stdout, stderr = ssh.exec_command(str(command))
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
        time.sleep(10)


def main():
    global threshold
    parser = argparse.ArgumentParser(description="Netgear AP Load balancing Test Script")
    parser.add_argument('-i', '--ip', type=str, help='AP ip')
    parser.add_argument('-u', '--user', type=str, help='credentials login/username')
    parser.add_argument('-p', '--pswd', type=str, help='credential password')
    parser.add_argument('-hst', '--host', type=str, help='host name')
    parser.add_argument('-s', '--ssid', type=str, help='ssid for client')
    parser.add_argument('-pwd', '--password', type=str, help='password to connect to ssid', default="[BLANK]")
    parser.add_argument('-sec', '--security', type=str, help='security Ex. wpa | wpa2 | wpa3', default="open")
    parser.add_argument('-rad', '--radio', type=str, help='radio at which client will be connected', default="wiphy3")
    parser.add_argument('--upstream', type=str, help="provide upstream name", default="eth1")
    parser.add_argument('-num_sta', '--num_sta', type=int, help='provide number of stations you want to create',
                        default=60)
    parser.add_argument('-ch', '--ch_threshold', type=str, help='Threshold channel value for 2.4 ghz')
    parser.add_argument('-ch5', '--ch_threshold5', type=str, help='Threshold channel value for 5 ghz')
    parser.add_argument('-ch5h', '--ch_threshold5h', type=str, help='Threshold channel value for 5 ghz high')
    parser.add_argument('--client', type=str, help='Threshold max client  value for 2.4 ghz')
    parser.add_argument('--client5', type=str, help='Threshold max client value for 5 ghz')
    parser.add_argument('--client5h', type=str, help='Threshold max client value for 5 ghz high')
    parser.add_argument('-r2', '--rssi2', type=str, help='Threshold RSSI value for 2.4 ghz')
    parser.add_argument('-r5', '--rssi5l', type=str, help='Threshold RSSI value for 5 ghz low')
    parser.add_argument('-r5h', '--rssi5h', type=str, help='Threshold RSSI value for 5 ghz high')
    parser.add_argument('--test', nargs="+", type=str, help='select type of test you want to perform, Eg. Client, Utilization, Rssi',
                        default=['Client', 'Utilization', 'Rssi'])
    parser.add_argument('--bands', nargs="+", type=str,
                        help='select type of bands you want to perform the test on like 2.4G/5G_low/5G_high, Eg 2.4G 5G_low',
                        default=['2.4G', '5G_low', '5G_high'])
    parser.add_argument('--add_attenuator', type=str, help="add the attenuator serial number on which performing the test eg 2222")

    args = parser.parse_args()
    date1 = str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
    main_path = "/home/lanforge/html-reports/Loadbalancelog"
    report_root = "/home/lanforge/html-reports/Loadbalancelog" + "/" + str(date1)
    new_path = report_root + "/test.log"
    # print(report_r
    if path.exists(main_path):
        os.mkdir(report_root)
        print("Reports Root is Created")

    else:
        os.mkdir(main_path)
        os.mkdir(report_root)
        print("Reports Root is created")
    logging.basicConfig(filename=new_path, filemode='a',
                        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    ap = AP_Automate(args.ip, args.user, args.pswd, args.ch_threshold)
    obj = LoadLayer3(lfclient_host=args.host, lfclient_port=8080, ssid=args.ssid, paswd=args.passwd,
                     security=args.security, radio=args.radio, upstream=args.upstream, num_sta=args.num_sta)
    test_time = datetime.now()
    test_time = test_time.strftime("%b %d %H:%M:%S")
    print("Test started at ", test_time)
    cmd = "Test started at " + str(test_time)
    logging.warning(str(cmd))
    max_client_pass_fail = []
    max_client_threshold = []
    max_client_measured = []
    channel_set_threshold = []
    channel_measured = []
    channel_pass_fail = []
    rssi_set_threshold = []
    rssi_measured = []
    rssi_pass_fail = []
    global compare
    channel_list = None
    if args.bands == ['2.4G', '5G_low', '5G_high']:
        channel_list = ["6", "36", "161"]
    elif args.bands == ['2.4G']:
        channel_list = ["6"]
        # print(channel_list)
    elif args.bands == ['5G_low']:
        channel_list = ["36"]
        # print(channel_list)
    elif args.bands == ['5G_high']:
        channel_list = ["161"]
    elif args.bands == ["2.4G", "5G_low"]:
        channel_list = ["6", "36"]
    elif args.bands == ["2.4G", "5G_high"]:
        channel_list = ["6", "161"]
    elif args.bands == ["5G_low", "5G_high"]:
        channel_list = ["36", "161"]

    # defining dictionary for different data
    pass_fail_dict = dict.fromkeys(args.test)
    for i in pass_fail_dict:
        pass_fail_dict[i] = dict.fromkeys(args.bands)
    print(pass_fail_dict)
    client_connect_dict = dict.fromkeys(args.bands)
    lst = ["set_threshold_value", "Measured_value"]
    for i in client_connect_dict:
        client_connect_dict[i] = dict.fromkeys(lst)
    print(client_connect_dict)
    utilization_dict = dict.fromkeys(args.bands)
    for i in utilization_dict:
        utilization_dict[i] = dict.fromkeys(lst)
    print(utilization_dict)
    rssi_dict = dict.fromkeys(args.bands)
    for i in rssi_dict:
        rssi_dict[i] = dict.fromkeys(lst)
    print(rssi_dict)

    for test in args.test:
        if test == "Client":
            print("starting load balancing test based on Max number of client client ")
            logging.warning('starting load balancing test based on Max number of client client')

            for channel in channel_list:
                print("set channel in AP at ", channel)
                cmd = "set channel in AP at " + channel
                logging.warning(str(cmd))
                ap.set_channel_in_ap_at_(args.ip, args.user, args.pswd, channel)
                # fix frequency on lanforge test radio  so that client should not jump to another channel
                print("set channel in lanforge to ", channel)
                cmd1 = "set channel in lanforge to " + channel
                logging.warning(str(cmd1))
                host = "localhost"
                base_url = "http://%s:8080" % host
                resource_id = 1  # typically you're using resource 1 in stand alone realm
                radio = args.radio
                lf_r = LFRequest.LFRequest(base_url + "/cli-json/set_wifi_radio")
                lf_r.addPostData({
                    "shelf": 1,
                    "resource": resource_id,
                    "radio": radio,
                    "mode": 8,
                    "channel": channel,
                })
                lf_r.jsonPost()
                print("done")
                logging.warning('done')
                time.sleep(10)
                client = Station_Connect(lfclient_host=args.host, lfclient_port=8080, ssid=args.ssid, paswd=args.passwd,
                                         security=args.security, radio=args.radio, num_sta=args.num_sta)
                print("set max client threshold")
                logging.warning('set max client threshold')
                ap.set_max_client_threshold(args.ip, args.user, args.pswd, channel, args.client, args.client5,
                                            args.client5h)
                if channel == "6":
                    client_threshold = args.client
                    max_client_threshold.append(args.client)
                elif channel == "36":
                    client_threshold = args.client5
                    max_client_threshold.append(args.client5)
                else:
                    client_threshold = args.client5h
                    max_client_threshold.append(args.client5h)
                print("done")
                logging.warning('done')
                time.sleep(10)
                print("cleaning up")
                logging.warning('cleaning up')
                client.precleanup()
                print("client connect started")
                logging.warning('client connect started')
                val = client.start(num_sta=args.num_sta)
                if val == "not done":
                    print("client unable to connect ")
                    logging.warning('client unable to connect')
                    connect = "NO"
                    # max_client_connect.append(connect)
                    print("measure max client from AP")
                    logging.warning('measure max client from AP')
                    time.sleep(60)
                    var = ap.Max_client_value_from_ap(args.ip, args.user, args.pswd, channel)
                    # print(var)

                    N = 11
                    res = list(islice(reversed(var), 0, N))
                    res.reverse()
                    # print(res)

                    b = []
                    for i in res:
                        b.append(i.strip())
                    x = []
                    x.append(b[0])
                    y = []
                    for i in x:
                        # print(i.split(' '))
                        for j in i.split(' '):
                            y.append(j)
                    print("y[3]", y[3])
                    print("y[4]", y[4])
                    if y[3] == "":
                        compare = y[4]
                        # print("hoi", y[4])
                    else:
                        compare = y[3]
                    # print("reached",compare)

                    max_client_measured.append(compare)
                    print("max client", client_threshold)
                    cmd = "max client" + client_threshold
                    logging.warning(str(cmd))
                    print(type(client_threshold))
                    print("compare", compare)
                    print(type(compare))

                    if compare == client_threshold:
                        test = "PASS"
                    else:
                        test = "FAIL"
                    print(test)
                    logging.warning(str(test))
                    max_client_pass_fail.append(test)
                    time.sleep(10)
                else:
                    print("client connected ")
                    logging.warning('client connected ')
                    connect = "YES"
                    # max_client_connect.append(connect)
                    print("measure max client from AP")
                    logging.warning('measure max client from AP')
                    time.sleep(60)
                    var = ap.Max_client_value_from_ap(args.ip, args.user, args.pswd, channel)
                    # print(var)
                    N = 11
                    res = list(islice(reversed(var), 0, N))
                    res.reverse()
                    b = []
                    for i in res:
                        b.append(i.strip())
                    x = []
                    x.append(b[0])
                    y = []

                    for i in x:
                        # print(i.split(' '))
                        for j in i.split(' '):
                            y.append(j)
                    print(y[3])
                    print(y[4])
                    if y[3] == "":
                        compare = y[4]
                    else:
                        compare = y[3]
                    max_client_measured.append(compare)
                    print("max client", client_threshold)
                    print(type(client_threshold))
                    print("compare", compare)
                    print(type(compare))

                    if compare == client_threshold:
                        test = "PASS"
                    else:
                        test = "FAIL"
                    print(test)
                    logging.warning(str(test))
                    max_client_pass_fail.append(test)
                    time.sleep(10)

            if args.bands == ['2.4G', '5G_low', '5G_high']:
                pass_fail_dict['Client']['2.4G'] = max_client_pass_fail[0]
                pass_fail_dict['Client']['5G_low'] = max_client_pass_fail[1]
                pass_fail_dict['Client']['5G_high'] = max_client_pass_fail[2]
                client_connect_dict['2.4G']['set_threshold_value'] = max_client_threshold[0]
                client_connect_dict['5G_low']['set_threshold_value'] = max_client_threshold[1]
                client_connect_dict['5G_high']['set_threshold_value'] = max_client_threshold[2]
                client_connect_dict['2.4G']['Measured_value'] = max_client_measured[0]
                client_connect_dict['5G_low']['Measured_value'] = max_client_measured[1]
                client_connect_dict['5G_high']['Measured_value'] = max_client_measured[2]
            elif args.bands == ['2.4G']:
                pass_fail_dict['Client']['2.4G'] = max_client_pass_fail[0]
                client_connect_dict['2.4G']['set_threshold_value'] = max_client_threshold[0]
                client_connect_dict['2.4G']['Measured_value'] = max_client_measured[0]
            elif args.bands == ['5G_low']:
                pass_fail_dict['Client']['5G_low'] = max_client_pass_fail[0]
                client_connect_dict['5G_low']['set_threshold_value'] = max_client_threshold[0]
                client_connect_dict['5G_low']['Measured_value'] = max_client_measured[0]
            elif args.bands == ['5G_high']:
                pass_fail_dict['Client']['5G_high'] = max_client_pass_fail[0]
                client_connect_dict['5G_high']['set_threshold_value'] = max_client_threshold[0]
                client_connect_dict['5G_high']['Measured_value'] = max_client_measured[0]
            elif args.bands == ["2.4G", "5G_low"]:
                pass_fail_dict['Client']['2.4G'] = max_client_pass_fail[0]
                pass_fail_dict['Client']['5G_low'] = max_client_pass_fail[1]
                client_connect_dict['2.4G']['set_threshold_value'] = max_client_threshold[0]
                client_connect_dict['5G_low']['set_threshold_value'] = max_client_threshold[1]
                client_connect_dict['2.4G']['Measured_value'] = max_client_measured[0]
                client_connect_dict['5G_low']['Measured_value'] = max_client_measured[1]
            elif args.bands == ["2.4G", "5G_high"]:
                pass_fail_dict['Client']['2.4G'] = max_client_pass_fail[0]
                pass_fail_dict['Client']['5G_high'] = max_client_pass_fail[1]
                client_connect_dict['2.4G']['set_threshold_value'] = max_client_threshold[0]
                client_connect_dict['5G_high']['set_threshold_value'] = max_client_threshold[1]
                client_connect_dict['2.4G']['Measured_value'] = max_client_measured[0]
                client_connect_dict['5G_high']['Measured_value'] = max_client_measured[1]
            elif args.bands == ["5G_low", "5G_high"]:
                pass_fail_dict['Client']['5G_low'] = max_client_pass_fail[0]
                pass_fail_dict['Client']['5G_high'] = max_client_pass_fail[1]
                client_connect_dict['5G_low']['set_threshold_value'] = max_client_threshold[0]
                client_connect_dict['5G_high']['set_threshold_value'] = max_client_threshold[1]
                client_connect_dict['5G_low']['Measured_value'] = max_client_measured[0]
                client_connect_dict['5G_high']['Measured_value'] = max_client_measured[1]
            print("list of max client pass/fail criteria ", max_client_pass_fail)
            cmd = "list of max client pass/fail criteria " + str(max_client_pass_fail)
            logging.warning(str(cmd))
            print("list of max client test threshold value ", max_client_threshold)
            cmd1 = "list of max client test threshold value " + str(max_client_threshold)
            logging.warning(str(cmd1))
            # print("list of max client test client connect or not is  ", max_client_connect)
            print("list of max client test measured value from ap is ", max_client_measured)
            cmd2 = "list of max client test measured value from ap is " + str(max_client_measured)
            logging.warning(str(cmd2))
            print("pass_fail_dict", pass_fail_dict)
            cmd3 = "pass fail dictionary value for max client test is " + str(pass_fail_dict)
            logging.warning(str(cmd3))
            print("client_connect_dict", client_connect_dict)
            cmd4 = "max client info dictionary is " + str(client_connect_dict)
            logging.warning(cmd4)


        elif test == "Utilization":
            print("starting load balancing test for channel utilization")
            logging.warning('starting load balancing test for channel utilization')
            # channel_client_connect = []
            for channel in channel_list:
                print("set channel in AP at ", channel)
                cmd = "set channel in AP at " + channel
                logging.warning(str(cmd))
                ap.set_channel_in_ap_at_(args.ip, args.user, args.pswd, channel)
                # fix frequency on lanforge test radio  so that client should not jump to another channel
                print("set channel in lanforge to ", channel)
                cmd1 = "set channel in lanforge to " + channel
                logging.warning(str(cmd1))
                host = "localhost"
                base_url = "http://%s:8080" % host
                resource_id = 1  # typically you're using resource 1 in stand alone realm
                radio = args.radio
                lf_r = LFRequest.LFRequest(base_url + "/cli-json/set_wifi_radio")
                lf_r.addPostData({
                    "shelf": 1,
                    "resource": resource_id,
                    "radio": radio,
                    "mode": 8,
                    "channel": channel,
                })
                lf_r.jsonPost()
                print("done")
                logging.warning('done')
                time.sleep(10)
                obj = LoadLayer3(lfclient_host=args.host, lfclient_port=8080, ssid=args.ssid, paswd=args.passwd,
                                 security=args.security, radio=args.radio, upstream=args.upstream, num_sta=args.num_sta)
                # set channel utilization threshold in AP
                print("set channel utilization threshold in AP")
                logging.warning('set channel utilization threshold in AP')
                if channel == "6":
                    ap.set_channel_utilztn2ghz_threashold(args.ip, args.user, args.pswd, args.ch_threshold)
                    channel_set_threshold.append(args.ch_threshold)
                elif channel == "36":
                    ap.set_channel_utilztn5ghz_threashold(args.ip, args.user, args.pswd, args.ch_threshold5)
                    channel_set_threshold.append(args.ch_threshold5)
                else:
                    ap.set_channel_utilztn5ghzh_threashold(args.ip, args.user, args.pswd, args.ch_threshold5h)
                    channel_set_threshold.append(args.ch_threshold5h)
                print("done")
                logging.warning('done')
                time.sleep(10)
                print("cleanup all client and cx on lanforge ")
                logging.warning('cleanup all client and cx on lanforge ')
                obj.precleanup()
                time.sleep(80)
                val = obj.start(num_sta=args.num_sta)
                if channel == "6":
                    threshold = args.ch_threshold
                elif channel == "36":
                    threshold = args.ch_threshold5
                else:
                    threshold = args.ch_threshold5h

                if val == "not done":
                    print("station not associated")
                    logging.warning('station not associated')
                    connect = "NO"
                    # channel_client_connect.append(connect)
                    print("measure channel utilization from AP")
                    logging.warning('measure channel utilization from AP')
                    chutil = ap.check_channel_utilization_ap(args.ip, args.user, args.pswd, channel)
                    # print(chutil)
                    # print(type(chutil))
                    ch = []
                    ch_ut = ""
                    for j in chutil:
                        ch.append(j.strip())
                    for i in ch[0][22:]:
                        ch_ut = ch_ut + i
                    print(ch_ut)
                    channel_measured.append(ch_ut)
                    if ch_ut == str(int(threshold) - 5) or ch_ut == str(int(threshold) - 4) \
                            or ch_ut == str(int(threshold) - 3) or ch_ut == str(int(threshold) - 2) \
                            or ch_ut == str(int(threshold) - 1) or ch_ut == threshold \
                            or ch_ut == str(int(threshold) + 1) or ch_ut == str(int(threshold) + 2) \
                            or ch_ut == str(int(threshold) + 2) or ch_ut == str(int(threshold) + 3) \
                            or ch_ut == str(int(threshold) + 4) or ch_ut == str(int(threshold) + 5):
                        data = "PASS"
                        channel_pass_fail.append(data)
                        logging.warning(str(data))
                        print("load balancing channel utilization test  is ", data)
                    else:
                        data = "FAIL"
                        channel_pass_fail.append(data)
                        logging.warning(str(data))
                        print("load balancing channel utilization test is ", data)
                else:
                    ch_ut = ""
                    print("client associated")
                    logging.warning('client associated')
                    print("measure channel utilization from AP")
                    logging.warning('measure channel utilization from AP')
                    chutil = ap.check_channel_utilization_ap(args.ip, args.user, args.pswd, channel)
                    print(chutil)
                    ch = []
                    for j in chutil:
                        ch.append(j.strip())
                    for i in ch[0][22:]:
                        ch_ut = ch_ut + i
                    print(ch_ut)
                    channel_measured.append(ch_ut)
                    if ch_ut == str(int(threshold) - 5) or ch_ut == str(int(threshold) - 4) \
                            or ch_ut == str(int(threshold) - 3) or ch_ut == str(int(threshold) - 2) \
                            or ch_ut == str(int(threshold) - 1) or ch_ut == threshold \
                            or ch_ut == str(int(threshold) + 1) or ch_ut == str(int(threshold) + 2) \
                            or ch_ut == str(int(threshold) + 2) or ch_ut == str(int(threshold) + 3) \
                            or ch_ut == str(int(threshold) + 4) or ch_ut == str(int(threshold) + 5):
                        data = "PASS"
                        channel_pass_fail.append(data)
                        logging.warning(str(data))
                        print("load balancing channel utilization test  is ", data)
                    else:
                        data = "FAIL"
                        channel_pass_fail.append(data)
                        logging.warning(str(data))
                        print("load balancing channel utilization test is ", data)
                time.sleep(10)

            if args.bands == ['2.4G', '5G_low', '5G_high']:
                pass_fail_dict['Utilization']['2.4G'] = channel_pass_fail[0]
                pass_fail_dict['Utilization']['5G_low'] = channel_pass_fail[1]
                pass_fail_dict['Utilization']['5G_high'] = channel_pass_fail[2]
                utilization_dict['2.4G']['set_threshold_value'] = channel_set_threshold[0]
                utilization_dict['5G_low']['set_threshold_value'] = channel_set_threshold[1]
                utilization_dict['5G_high']['set_threshold_value'] = channel_set_threshold[2]
                utilization_dict['2.4G']['Measured_value'] = channel_measured[0]
                utilization_dict['5G_low']['Measured_value'] = channel_measured[1]
                utilization_dict['5G_high']['Measured_value'] = channel_measured[2]
            elif args.bands == ['2.4G']:
                pass_fail_dict['Utilization']['2.4G'] = channel_pass_fail[0]
                utilization_dict['2.4G']['set_threshold_value'] = channel_set_threshold[0]
                utilization_dict['2.4G']['Measured_value'] = channel_measured[0]
            elif args.bands == ['5G_low']:
                pass_fail_dict['Utilization']['5G_low'] = channel_pass_fail[0]
                utilization_dict['5G_low']['set_threshold_value'] = channel_set_threshold[0]
                utilization_dict['5G_low']['Measured_value'] = channel_measured[0]
            elif args.bands == ['5G_high']:
                pass_fail_dict['Utilization']['5G_high'] = channel_pass_fail[0]
                utilization_dict['5G_high']['set_threshold_value'] = channel_set_threshold[0]
                utilization_dict['5G_high']['Measured_value'] = channel_measured[0]
            elif args.bands == ["2.4G", "5G_low"]:
                pass_fail_dict['Utilization']['2.4G'] = channel_pass_fail[0]
                pass_fail_dict['Utilization']['5G_low'] = channel_pass_fail[1]
                utilization_dict['2.4G']['set_threshold_value'] = channel_set_threshold[0]
                utilization_dict['5G_low']['set_threshold_value'] = channel_set_threshold[1]
                utilization_dict['2.4G']['Measured_value'] = channel_measured[0]
                utilization_dict['5G_low']['Measured_value'] = channel_measured[1]
            elif args.bands == ["2.4G", "5G_high"]:
                pass_fail_dict['Utilization']['2.4G'] = channel_pass_fail[0]
                pass_fail_dict['Utilization']['5G_high'] = channel_pass_fail[1]
                utilization_dict['2.4G']['set_threshold_value'] = channel_set_threshold[0]
                utilization_dict['5G_high']['set_threshold_value'] = channel_set_threshold[1]
                utilization_dict['2.4G']['Measured_value'] = channel_measured[0]
                utilization_dict['5G_high']['Measured_value'] = channel_measured[1]
            elif args.bands == ["5G_low", "5G_high"]:
                pass_fail_dict['Utilization']['5G_low'] = channel_pass_fail[0]
                pass_fail_dict['Utilization']['5G_high'] = channel_pass_fail[1]
                utilization_dict['5G_low']['set_threshold_value'] = channel_set_threshold[0]
                utilization_dict['5G_high']['set_threshold_value'] = channel_set_threshold[1]
                utilization_dict['5G_low']['Measured_value'] = channel_measured[0]
                utilization_dict['5G_high']['Measured_value'] = channel_measured[1]
            print("list of channel utilization pass/fail criteria ", channel_pass_fail)
            cmd = "list of channel utilization pass/fail criteria " + str(channel_pass_fail)
            logging.warning(str(cmd))
            print("list of channel utilization test threshold value ", channel_set_threshold)
            cmd1 = "list of channel utilization test threshold value " + str(channel_set_threshold)
            logging.warning(str(cmd1))
            # print("list of channel utilization test client connect or not is  ", channel_client_connect)
            print("list of channel utilization test measured value from ap is ", channel_measured)
            cmd2 = "list of channel utilization test measured value from ap is " + str(channel_measured)
            logging.warning(str(cmd2))
            print("pass_fail_dict", pass_fail_dict)
            cmd3 = "pass fail dictionary value for max client test is " + str(pass_fail_dict)
            logging.warning(str(cmd3))
            print("utilization_dict", utilization_dict)
            cmd4 = "channel utilization info dictionary is " + str(utilization_dict)
            logging.warning(cmd4)
        elif test == "Rssi":
            print("starting load balancing test for RSSI")
            logging.warning('starting load balancing test for RSSI')
            rssi = ""
            rssi_threshold = ""
            for channel in channel_list:
                if channel == "6":
                    rssi_threshold = args.rssi2
                    rssi_set_threshold.append(rssi_threshold)
                elif channel == "36":
                    rssi_threshold = args.rssi5l
                    rssi_set_threshold.append(rssi_threshold)
                else:
                    rssi_threshold = args.rssi5h
                    rssi_set_threshold.append(rssi_threshold)
                print("set channel in AP at ", channel)
                cmd = "set channel in AP at " + channel
                logging.warning(str(cmd))
                ap.set_channel_in_ap_at_(args.ip, args.user, args.pswd, channel)
                # fix frequency on lanforge test radio  so that client should not jump to another channel
                print("set channel in lanforge to ", channel)
                cmd2 = "set channel in lanforge to " + channel
                logging.warning(str(cmd2))
                host = "localhost"
                base_url = "http://%s:8080" % host
                resource_id = 1  # typically you're using resource 1 in stand alone realm
                radio = args.radio
                lf_r = LFRequest.LFRequest(base_url + "/cli-json/set_wifi_radio")
                lf_r.addPostData({
                    "shelf": 1,
                    "resource": resource_id,
                    "radio": radio,
                    "mode": 8,
                    "channel": channel,
                })
                lf_r.jsonPost()
                print("done")
                logging.warning('done')
                time.sleep(10)
                ap.set_rssi_threshold(args.ip, args.user, args.pswd, channel, args.rssi2, args.rssi5l, args.rssi5h)
                time.sleep(10)
                station = Station(lfclient_host=args.host, lfclient_port=8080, ssid=args.ssid, paswd=args.passwd,
                                  security=args.security, radio=args.radio, num_sta=1)
                attenuator = Attenuator()
                station.precleanup()
                station.start(num_sta=1)

                print("set attenuation")
                logging.warning('set attenuation')
                att_values = [0, 50, 150, 250, 350, 450, 550, 650, 750, 850, 950]
                # [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950]

                value = ""
                for i in att_values:
                    print("set attenuation to ", i)
                    cmd = "set attenuation to " + str(i)
                    logging.warning(str(cmd))
                    attenuator.set_att_dbm(attenuator=args.add_attenuator, attenuator_value=i)
                    time.sleep(20)
                    print("station down")
                    logging.warning('station down')
                    station.stop()
                    time.sleep(10)
                    print("station up")
                    logging.warning('station up')
                    value = station.start(num_sta=1)
                    if value == "not done":
                        break

                if value == "not done":
                    connect = "NO"
                    # rssi_connect.append(connect)
                    print("measure rssi value from ap")
                    logging.warning('measure rssi value from ap')
                    ap_logs = ap.check_Rssi_from_ap(args.ip, args.user, args.pswd)
                    N = 1
                    res = list(islice(reversed(ap_logs), 0, N))
                    res.reverse()
                    print(res)

                    for r in res:
                        # print(r.split(','))
                        for j in r.split(','):
                            if "rssi" in j:
                                print("yes")
                                # print(j.split(':'))
                                for k in j.split(':'):
                                    # print(k)
                                    x = k.replace('"', '')
                                    print(x)
                                    rssi = x

                    print("rssi value is ", rssi)
                    cmd = "rssi value is " + rssi
                    logging.warning(str(cmd))
                    rssi_measured.append(rssi)
                    print("attenuator value at which test stop ", i)
                    cmd1 = "attenuator value at which test stop " + str(i)
                    if rssi == str(int(rssi_threshold) - 1) or rssi == rssi_threshold or rssi == str(
                            int(rssi_threshold) + 1):
                        data = "PASS"
                        logging.warning(str(data))
                        rssi_pass_fail.append(data)
                        print(data)
                    else:
                        data = "FAIL"
                        logging.warning(str(data))
                        rssi_pass_fail.append(data)
                        print(data)
                else:
                    connect = "YES"
                    # rssi_connect.append(connect)
                    print("measure rssi value from ap")
                    logging.warning('measure rssi value from ap')
                    ap_logs = ap.check_Rssi_from_ap(args.ip, args.user, args.pswd)
                    N = 1
                    res = list(islice(reversed(ap_logs), 0, N))
                    res.reverse()
                    print(res)

                    for r in res:
                        # print(r.split(','))
                        for j in r.split(','):
                            if "rssi" in j:
                                print("yes")
                                # print(j.split(':'))
                                for k in j.split(':'):
                                    # print(k)
                                    x = k.replace('"', '')
                                    print(x)
                                    rssi = x

                    print("rssi value is ", rssi)
                    rssi_measured.append(rssi)
                    print("attenuator value at which test stop ", i)
                    if rssi == str(int(rssi_threshold) - 1) or rssi == rssi_threshold or rssi == str(
                            int(rssi_threshold) + 1):
                        data = "PASS"
                        logging.warning(str(data))
                        rssi_pass_fail.append(data)
                        print(data)
                    else:
                        data = "FAIL"
                        logging.warning(str(data))
                        rssi_pass_fail.append(data)
                        print(data)
                time.sleep(10)
            if args.bands == ['2.4G', '5G_low', '5G_high']:
                pass_fail_dict['Rssi']['2.4G'] = rssi_pass_fail[0]
                pass_fail_dict['Rssi']['5G_low'] = rssi_pass_fail[1]
                pass_fail_dict['Rssi']['5G_high'] = rssi_pass_fail[2]
                rssi_dict['2.4G']['set_threshold_value'] = rssi_set_threshold[0]
                rssi_dict['5G_low']['set_threshold_value'] = rssi_set_threshold[1]
                rssi_dict['5G_high']['set_threshold_value'] = rssi_set_threshold[2]
                rssi_dict['2.4G']['Measured_value'] = rssi_measured[0]
                rssi_dict['5G_low']['Measured_value'] = rssi_measured[1]
                rssi_dict['5G_high']['Measured_value'] = rssi_measured[2]
            elif args.bands == ['2.4G']:
                pass_fail_dict['Rssi']['2.4G'] = rssi_pass_fail[0]
                rssi_dict['2.4G']['set_threshold_value'] = rssi_set_threshold[0]
                rssi_dict['2.4G']['Measured_value'] = rssi_measured[0]
            elif args.bands == ['5G_low']:
                pass_fail_dict['Rssi']['5G_low'] = rssi_pass_fail[0]
                rssi_dict['5G_low']['set_threshold_value'] = rssi_set_threshold[0]
                rssi_dict['5G_low']['Measured_value'] = rssi_measured[0]
            elif args.bands == ['5G_high']:
                pass_fail_dict['Rssi']['5G_high'] = rssi_pass_fail[0]
                rssi_dict['5G_high']['set_threshold_value'] = rssi_set_threshold[0]
                rssi_dict['5G_high']['Measured_value'] = rssi_measured[0]
            elif args.bands == ["2.4G", "5G_low"]:
                pass_fail_dict['Rssi']['2.4G'] = rssi_pass_fail[0]
                pass_fail_dict['Rssi']['5G_low'] = rssi_pass_fail[1]
                rssi_dict['2.4G']['set_threshold_value'] = rssi_set_threshold[0]
                rssi_dict['5G_low']['set_threshold_value'] = rssi_set_threshold[1]
                rssi_dict['2.4G']['Measured_value'] = rssi_measured[0]
                rssi_dict['5G_low']['Measured_value'] = rssi_measured[1]
            elif args.bands == ["2.4G", "5G_high"]:
                pass_fail_dict['Rssi']['2.4G'] = rssi_pass_fail[0]
                pass_fail_dict['Rssi']['5G_high'] = rssi_pass_fail[1]
                rssi_dict['2.4G']['set_threshold_value'] = rssi_set_threshold[0]
                rssi_dict['5G_high']['set_threshold_value'] = rssi_set_threshold[1]
                rssi_dict['2.4G']['Measured_value'] = rssi_measured[0]
                rssi_dict['5G_high']['Measured_value'] = rssi_measured[1]
            elif args.bands == ["5G_low", "5G_high"]:
                pass_fail_dict['Rssi']['5G_low'] = rssi_pass_fail[0]
                pass_fail_dict['Rssi']['5G_high'] = rssi_pass_fail[1]
                rssi_dict['5G_low']['set_threshold_value'] = rssi_set_threshold[0]
                rssi_dict['5G_high']['set_threshold_value'] = rssi_set_threshold[1]
                rssi_dict['5G_low']['Measured_value'] = rssi_measured[0]
                rssi_dict['5G_high']['Measured_value'] = rssi_measured[1]
            print("list of rssi  pass/fail criteria ", rssi_pass_fail)
            cmd = "list of rssi  pass/fail criteria " + str(rssi_pass_fail)
            logging.warning(str(cmd))
            print("list of rssi test threshold value ", rssi_set_threshold)
            cmd1 = "list of rssi test threshold value " + str(rssi_set_threshold)
            logging.warning(str(cmd1))
            # print("list of rssi test client connect or not is  ", rssi_connect)
            print("list of rssi test measured value from ap is ", rssi_measured)
            cmd2 = "list of rssi test measured value from ap is " + str(rssi_measured)
            logging.warning(str(cmd2))
            print("pass_fail_dict", pass_fail_dict)
            cmd3 = "pass fail dictionary value for max client test is " + str(pass_fail_dict)
            logging.warning(str(cmd3))
            print("rssi_dict", rssi_dict)
            cmd4 = " Rssi info dictionary is " + str(rssi_dict)
            logging.warning(cmd4)
    print("final", pass_fail_dict)
    print("final max client dictionary ", client_connect_dict)
    print("final channel dictionary ", utilization_dict)
    print("final rssi dictionary ", rssi_dict)
    print("Test Finished")
    """rssi_dict = {'2.4G': {'set_threshold_value': '18', 'Measured_value': '41'}}
    client_connect_dict = {'2.4G': {'set_threshold_value': '20', 'Measured_value': '20'}}
    utilization_dict = {'2.4G': {'set_threshold_value': '90', 'Measured_value': '67'}}"""

    information_dict = dict.fromkeys(args.test)

    for test in args.test:
        print(test)
        if test == "Client":
            information_dict['Client'] = client_connect_dict
            # print(information_dict)
        elif test == "Utilization":
            information_dict['Utilization'] = utilization_dict
        elif test == "Rssi":
            information_dict['Rssi'] = rssi_dict
    print("hi", information_dict)

    test = args.test

    logging.warning('Test Finished')
    test_end = datetime.now()
    test_end = test_end.strftime("%b %d %H:%M:%S")
    print("Test ended at ", test_end)
    cmd = "Test ended at " + test_end
    logging.warning(str(cmd))
    s1 = test_time
    s2 = test_end  # for example
    FMT = '%b %d %H:%M:%S'
    test_duration = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
    print("total test duration ", test_duration)
    print(type(test_duration))
    test_duration = str(test_duration)
    print(type(test_duration))
    cmd1 = "total test duration " + str(test_duration)
    logging.warning(str(cmd1))
    date = str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
    model = ap.get_ap_model(args.ip, args.user, args.pswd)
    model_name = model[0][12:]
    test_setup_info = {
        "AP Name": model_name,
        "SSID": args.ssid,
        "Test Duration": test_duration
    }
    input_setup_info = {}

    generate_report(date,
                    test_setup_info,
                    pass_fail_dict,
                    information_dict,
                    test,
                    report_path="/home/lanforge/html-reports/Loadbalancing")


if __name__ == '__main__':
    main()