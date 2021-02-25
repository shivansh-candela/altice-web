"""
[lanforge@lf0312-7d02 py-scripts]$ sudo python3 load_test_24.py  -i 192.168.208.196 -u root  -p Password@123xzsawq@! -hst localhost -s loadbalance -pwd [BLANK] -sec open -rad wiphy3 --rssi2 35 --rssi5l 32 --rssi5h 30  --client 22 --client5 30 --client5h 35 --ch_threshold 70 --ch_threshold5 80 --ch_threshold5h 70
"""
import sys
import os
import argparse
import time
import datetime
from datetime import datetime
import logging
import paramiko
from itertools import islice
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
from test_client_admission import LoadLayer3
from test_num_client import Station_Connect
from one_station import Station

class Attenuator:
    def __init__(self):
        pass
    def set_att_dbm(self, attenuator_value):
        attenuator_value = str(attenuator_value)
        cmd = "./lf_attenmod.pl --action set_atten --atten_serno 1030 --atten_idx all --atten_val " + attenuator_value
        os.chdir("/home/lanforge/lanforge-scripts")
        os.system(str(cmd))

class AP_automate:
    def __init__(self, ip, user, pswd, ch_threshold):
        self.ip = ip
        self.user = user
        self.pswd = pswd
        self.ch_threshold = ch_threshold
    def set_channel_in_ap_at_ (self, ip, user, pswd, channel):
        self.ip = ip
        self.user = user
        self.pswd = pswd
        channel = str(channel)
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # automatically adds the missing host key
        ssh.connect(ip, port=22, username=user, password=pswd)
        if channel == "8":
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
        command = "conf_set system:wlanSettings:wlanSettingTable:wlan0:channelUtilisationLoadBalanceThreshold " + str(ch_threshold)
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
        command = "conf_set system:wlanSettings:wlanSettingTable:wlan1:channelUtilisationLoadBalanceThreshold " + str(ch_threshold5)
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
        command = "conf_set system:wlanSettings:wlanSettingTable:wlan2:channelUtilisationLoadBalanceThreshold " + str(ch_threshold5h)
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
        if channel == "8":
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
    def set_max_client_threshold(self, ip, user, pswd,  channel, client , client5, client5h):
        self.ip = ip
        self.user = user
        self.pswd = pswd
        self.channel = channel
        self.client = client
        self.client5 = client5
        self.client5h = client5h
        if channel == "8":
            command = 'conf_set system:wlanSettings:wlanSettingTable:wlan0:maxWirelessClients ' + str(client)
        elif channel == "36":
            command = 'conf_set system:wlanSettings:wlanSettingTable:wlan1:maxWirelessClients ' + str(client5)
        else :
            command = 'conf_set system:wlanSettings:wlanSettingTable:wlan2:maxWirelessClients ' + str(client5h)
        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(ip, port=22, username=user, password=pswd)
        stdin, stdout, stderr = ssh.exec_command(str(command))
        output = stdout.readlines()
        ssh.close()
        return output
    def set_rssi_threshold(self, ip, user, pswd,  channel, rssi2 , rssi5l, rssi5h):
        self.ip = ip
        self.user = user
        self.pswd = pswd
        self.channel = channel
        self.rssi2 = rssi2
        self.rssi5l = rssi5l
        self.rssi5h = rssi5h
        if channel == "8":
            command = 'conf_set system:wlanSettings:wlanSettingTable:wlan0:receiveRSSILoadBalancingThreshold ' + str(rssi2)
        elif channel == "36":
            command = 'conf_set system:wlanSettings:wlanSettingTable:wlan0:receiveRSSILoadBalancingThreshold ' + str(rssi5l)
        else :
            command = 'conf_set system:wlanSettings:wlanSettingTable:wlan0:receiveRSSILoadBalancingThreshold ' + str(rssi5h)
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
        if channel == "8":
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
def main():
    global threshold
    parser = argparse.ArgumentParser(description="Netgear AP Load balancing Test Script")
    parser.add_argument('-i', '--ip', type=str, help='AP ip')
    parser.add_argument('-u', '--user', type=str, help='credentials login/username')
    parser.add_argument('-p', '--pswd', type=str, help='credential password')
    parser.add_argument('-hst', '--host', type=str, help='host name')
    parser.add_argument('-s', '--ssid', type=str, help='ssid for client')
    parser.add_argument('-pwd', '--passwd', type=str, help='password to connect to ssid')
    parser.add_argument('-sec', '--security', type=str, help='security')
    parser.add_argument('-rad', '--radio', type=str, help='radio at which client will be connected')
    parser.add_argument('--upstream', type=str, help="provide upstream name", default="eth1")
    parser.add_argument('-num_sta', '--num_sta', type=int, help='provide number of stations you want to create',default=60)
    parser.add_argument('-ch', '--ch_threshold', type=str, help='Threshold channel value for 2.4 ghz')
    parser.add_argument('-ch5', '--ch_threshold5', type=str, help='Threshold channel value for 5 ghz')
    parser.add_argument('-ch5h', '--ch_threshold5h', type=str, help='Threshold channel value for 5 ghz high')
    parser.add_argument( '--client', type=str, help='Threshold max client  value for 2.4 ghz')
    parser.add_argument( '--client5', type=str, help='Threshold max client value for 5 ghz')
    parser.add_argument('--client5h', type=str, help='Threshold max client value for 5 ghz high')
    parser.add_argument('-r2', '--rssi2', type=str, help='Threshold RSSI value for 2.4 ghz')
    parser.add_argument('-r5', '--rssi5l', type=str, help='Threshold RSSI value for 5 ghz low')
    parser.add_argument('-r5h', '--rssi5h', type=str, help='Threshold RSSI value for 5 ghz high')
    args = parser.parse_args()
    ap = AP_automate(args.ip, args.user, args.pswd, args.ch_threshold)
    obj = LoadLayer3(lfclient_host=args.host, lfclient_port=8080, ssid=args.ssid, paswd=args.passwd, security=args.security, radio=args.radio, upstream=args.upstream, num_sta=args.num_sta)
    test_time = datetime.now()
    test_time = test_time.strftime("%b %d %H:%M:%S")
    print("Test started at ", test_time)
    cmd = "Test started at " + str(test_time)
    logging.warning(str(cmd))
    print("starting load balancing test based on Max number of client client ")
    max_client_pass_fail = []
    max_client_threshold = []
    max_client_connect = []
    max_client_measured = []
    for channel in ["8", "36", "161"]:
        print("set channel in AP at ", channel)
        ap.set_channel_in_ap_at_(args.ip, args.user, args.pswd, channel)
        # fix frequency on lanforge test radio  so that client should not jump to another channel
        print("set channel in lanforge to ", channel)
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
        time.sleep(10)
        client = Station_Connect(lfclient_host=args.host, lfclient_port=8080, ssid=args.ssid, paswd=args.passwd,
                                security=args.security, radio=args.radio, num_sta=args.num_sta)
        print("set max client threshold")
        ap.set_max_client_threshold(args.ip, args.user, args.pswd, channel ,args.client , args.client5, args.client5h)
        if channel == "8":
            max_client_threshold.append(args.client)
        elif channel == "36":
            max_client_threshold.append(args.client5)
        else:
            max_client_threshold.append(args.client5h)
        print("done")
        time.sleep(10)
        print("cleaning up")
        client.precleanup()
        print("client connect started")
        val = client.start(num_sta=args.num_sta)
        if val == "not done":
            print("client unable to connect ")
            connect = "NO"
            max_client_connect.append(connect)
            print("measure max client from AP")
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
            max_client_measured.append(y[3])
            if y[3] <= args.client5:
                test = "PASS"
            else:
                test = "FAIL"
            print(test)
            max_client_pass_fail.append(test)
            time.sleep(10)
        else:
            print("client connected ")
            connect = "YES"
            max_client_connect.append(connect)
            print("measure max client from AP")
            var = ap.Max_client_value_from_ap(args.ip, args.user, args.pswd, channel)
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
            max_client_measured.append(y[3])
            if y[3] <= args.client5:
                test = "PASS"
            else:
                test = "FAIL"
            print(test)
            max_client_pass_fail.append(test)
            time.sleep(10)
    print("list of max client pass/fail criteria ", max_client_pass_fail)
    print("list of max client test threshold value ", max_client_threshold)
    print("list of max client test client connect or not is  ", max_client_connect)
    print("list of max client test measured value from ap is ", max_client_measured)
    print("starting load balancing test for channel utilization")
    channel_client_connect = []
    channel_set_threshold = []
    channel_measured = []
    channel_pass_fail = []
    for channel in ["8", "36", "161"]:
        print("set channel in AP at ", channel)
        ap.set_channel_in_ap_at_(args.ip, args.user, args.pswd, channel)
        # fix frequency on lanforge test radio  so that client should not jump to another channel
        print("set channel in lanforge to ", channel)
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
        time.sleep(10)
        obj = LoadLayer3(lfclient_host=args.host, lfclient_port=8080, ssid=args.ssid, paswd=args.passwd,security=args.security, radio=args.radio, upstream=args.upstream, num_sta=args.num_sta)
        # set channel utilization threshold in AP
        print("set channel utilization threshold in AP")
        if channel == "8":
            ap.set_channel_utilztn2ghz_threashold(args.ip, args.user, args.pswd, args.ch_threshold)
            channel_set_threshold.append(args.ch_threshold)
        elif channel == "36":
            ap.set_channel_utilztn5ghz_threashold(args.ip, args.user, args.pswd, args.ch_threshold5)
            channel_set_threshold.append(args.ch_threshold5)
        else:
            ap.set_channel_utilztn5ghzh_threashold(args.ip, args.user, args.pswd, args.ch_threshold5h)
            channel_set_threshold.append(args.ch_threshold5h)
        print("done")
        time.sleep(10)
        print("cleanup all client and cx on lanforge ")
        obj.precleanup()
        time.sleep(80)
        val = obj.start(num_sta=args.num_sta)
        if channel == "8":
            threshold = args.ch_threshold
        elif channel == "36":
            threshold = args.ch_threshold5
        else:
            threshold = args.ch_threshold5h
        ch_ut = ""
        if val == "not done":
            print("station not associated")
            connect = "NO"
            channel_client_connect.append(connect)
            print("measure channel utilization from AP")
            chutil = ap.check_channel_utilization_ap(args.ip, args.user, args.pswd, channel)
            #print(chutil)
            #print(type(chutil))
            ch= []
            for j in chutil:
                ch.append(j.strip())
            for i in ch[0][22:]:
                ch_ut = ch_ut + i
            print(ch_ut)
            channel_measured.append(ch_ut)
            if ch_ut <= threshold:
                data = "PASS"
                channel_pass_fail.append(data)
                print("load balancing channel utilization test  is ", data)
            else:
                data = "FAIL"
                channel_pass_fail.append(data)
                print("load balancing channel utilization test is ", data)
        else:
            print("client associated")
            print("measure channel utilization from AP")
            chutil = ap.check_channel_utilization_ap(args.ip, args.user, args.pswd, channel)
            print(chutil)
            ch = []
            for j in chutil:
                ch.append(j.strip())
            for i in ch[0][22:]:
                ch_ut = ch_ut + i
            print(ch_ut)
            channel_measured.append(ch_ut)
            if ch_ut <= threshold:
                data = "PASS"
                channel_pass_fail.append(data)
                print("load balancing channel utilization test  is ", data)
            else:
                data = "FAIL"
                channel_pass_fail.append(data)
                print("load balancing channel utilization test is ", data)
        time.sleep(10)
    print("list of channel utilization pass/fail criteria ", channel_pass_fail)
    print("list of channel utilization test threshold value ", channel_set_threshold)
    print("list of channel utilization test client connect or not is  ", channel_client_connect)
    print("list of channel utilization test measured value from ap is ", channel_measured)

    print("\n")
    print("starting load balancing test for RSSI")

    rssi_connect = []
    rssi_set_threshold = []
    rssi_measured = []
    rssi_pass_fail = []
    for channel in ["8", "36", "161"]:
        print("set channel in AP at ", channel)
        ap.set_channel_in_ap_at_(args.ip, args.user, args.pswd, channel)
        # fix frequency on lanforge test radio  so that client should not jump to another channel
        print("set channel in lanforge to ", channel)
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
        time.sleep(10)
        ap.set_rssi_threshold(args.ip, args.user, args.pswd, channel, args.rssi2, args.rssi5l, args.rssi5h)
        time.sleep(10)
        station = Station(lfclient_host=args.host, lfclient_port=8080, ssid=args.ssid, paswd=args.passwd,

                     security=args.security, radio=args.radio, num_sta= 1)
        attenuator = Attenuator()
        station.precleanup()
        station.start(num_sta=1)
        if channel == "8":
            rssi_threshold = args.rssi2
            rssi_set_threshold.append(rssi_threshold)
        elif channel == "36":
            rssi_threshold = args.rssi5l
            rssi_set_threshold.append(rssi_threshold)
        else:
            rssi_threshold = args.rssi5h
            rssi_set_threshold.append(rssi_threshold)
        print("set attenuation")
        att_values = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950]
        # 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950]
        value = ""
        for i in att_values:
            print("set attenuation to ", i)
            attenuator.set_att_dbm(i)
            time.sleep(20)
            print("station down")
            station.stop()
            time.sleep(10)
            print("station up")
            value = station.start(num_sta=1)
            if value == "not done":
                break

        rssi = ""
        if value == "not done":
            connect = "NO"
            rssi_connect.append(connect)
            print("measure rssi value from ap")
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
                            rssi_measured.append(rssi)
            print("rssi value is ", rssi)
            print("attenuator value at which test stop ", i)
            if rssi >= rssi_threshold:
                data = "PASS"
                rssi_pass_fail.append(data)
                print(data)
            else:
                data = "FAIL"
                rssi_pass_fail.append(data)
                print(data)
        else:
            connect = "YES"
            rssi_connect.append(connect)
            print("measure rssi value from ap")
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
                            rssi_measured.append(rssi)
            print("rssi value is ", rssi)
            print("attenuator value at which test stop ", i)
            if rssi >= rssi_threshold:
                data = "PASS"
                rssi_pass_fail.append(data)
                print(data)
            else:
                data = "FAIL"
                rssi_pass_fail.append(data)
                print(data)
        time.sleep(10)
    print("Test Finished")
    test_end = datetime.now()
    test_end = test_end.strftime("%b %d %H:%M:%S")
    print("Test ended at ", test_end)
    s1 = test_time
    s2 = test_end  # for example
    FMT = '%b %d %H:%M:%S'
    test_duration = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
    print("total test duration ", test_duration)
    print("list of rssi  pass/fail criteria ", rssi_pass_fail)
    print("list of rssi test threshold value ", rssi_set_threshold)
    print("list of rssi test client connect or not is  ", rssi_connect)
    print("list of rssi test measured value from ap is ", rssi_measured)
if __name__ == '__main__':
    main()