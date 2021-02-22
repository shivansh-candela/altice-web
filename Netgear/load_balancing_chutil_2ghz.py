"""
This script particularly checks for load balancing pass/ fail criteria according to channel utilization threshold
*** under progress ***
cmd - sudo python3 load_test_21.py  -i 192.168.208.201 -u root  -p Netgear@123xzsawq@! -hst localhost -s Nikita -pwd [BLANK] -sec open -rad wiphy0 -ch 70

"""

import sys
import os
import argparse
import time

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
from load_21 import LoadLayer3




class STATION(LFCliBase):
    def __init__(self, lfclient_host, lfclient_port, ssid, paswd, security, radio, sta_list=None):
        super().__init__(lfclient_host, lfclient_port)
        self.host = lfclient_host
        self.port = lfclient_port
        self.ssid = ssid
        self.paswd = paswd
        self.security = security
        self.radio = radio
        self.sta_list = sta_list

        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.paswd,
        self.station_profile.security = self.security

    def precleanup(self, sta_list):
        self.station_profile.cleanup(sta_list)
        LFUtils.wait_until_ports_disappear(base_url=self.lfclient_url,
                                           port_list=sta_list,
                                           debug=self.debug)
        time.sleep(1)

    def build(self):
        self.station_profile.use_security(self.security, self.ssid, self.paswd)
        self.station_profile.create(radio=self.radio, sta_names_=self.sta_list, debug=self.debug)

    def start(self, sta_list):
        self.station_profile.admin_up()

    def stop(self):
        # Bring stations down
        self.station_profile.admin_down()

class Attenuator:
    def __init__(self):
        pass

    def set_att_dbm(self, attenuator_value):
        attenuator_value = str(attenuator_value)
        cmd = "./lf_attenmod.pl --action set_atten --atten_serno 1030 --atten_idx all --atten_val " + attenuator_value
        os.chdir("/home/lanforge/lanforge-scripts")
        os.system(str(cmd))


    def start(self):
        data = ""
        num_sta = 1
        station_list = LFUtils.port_name_series(prefix="sta",
                                                start_id=0,
                                                end_id=num_sta - 1,
                                                padding_number=100,
                                                radio=self.radio)

        for i in station_list:
            if self.build(i) == 0:
                print("station not created")
                print("AP stops admitting client ")
                print("measure the channel utilization from AP")
                data = "done"

            else:
                print("station created")
                data = "not done"
        return data

    def stop(self):
        # Bring stations down
        self.station_profile.admin_down()
        self.cx_profile.stop_cx()

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

    def set_channel_utilztn5ghz_threashold(self, ip, user, pswd, ch_threshold):
        self.ip = ip
        self.user = user
        self.pswd = pswd
        self.ch_threshold = ch_threshold

        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(ip, port=22, username=user, password=pswd)
        command = "conf_set system:wlanSettings:wlanSettingTable:wlan1:channelUtilisationLoadBalanceThreshold " + str(ch_threshold)
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
    def channel_utilization_ap_for_2ghz(self, ip, user, pswd):
        self.ip = ip
        self.user = user
        self.pswd = pswd

        ssh = paramiko.SSHClient()  # creating shh client object we use this object to connect to router
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # automatically adds the missing host key
        ssh.connect(ip, port=22, username=user, password=pswd)
        stdin, stdout, stderr = ssh.exec_command('iwpriv wifi0vap0 get_chutil')
        output = stdout.readlines()

        time.sleep(1)
        return output


def main():
    parser = argparse.ArgumentParser(description="Netgear AP DFS Test Script")
    parser.add_argument('-i', '--ip', type=str, help='AP ip')
    parser.add_argument('-u', '--user', type=str, help='credentials login/username')
    parser.add_argument('-p', '--pswd', type=str, help='credential password')
    parser.add_argument('-hst', '--host', type=str, help='host name')
    parser.add_argument('-s', '--ssid', type=str, help='ssid for client')
    parser.add_argument('-pwd', '--passwd', type=str, help='password to connect to ssid')
    parser.add_argument('-sec', '--security', type=str, help='security')
    parser.add_argument('-rad', '--radio', type=str, help='radio at which client will be connected')
    parser.add_argument('--upstream', type=str, help="provide upstream name", default="eth2")


    parser.add_argument('-r2', '--rssi2', type=str, help='Threshold RSSI value for 2.4 ghz')
    parser.add_argument('-r5', '--rssi5l', type=str, help='Threshold RSSI value for 5 ghz low')
    parser.add_argument('-r5h', '--rssi5h', type=str, help='Threshold RSSI value for 5 ghz high')
    parser.add_argument('-ch', '--ch_threshold', type=str, help='Threshold channel value for 2.4 ghz')
    parser.add_argument('-ch5', '--ch_threshold5', type=str, help='Threshold channel value for 5 ghz')
    args = parser.parse_args()
    ap = AP_automate(args.ip, args.user, args.pswd, args.ch_threshold)
    obj = LoadLayer3(lfclient_host=args.host, lfclient_port=8080, ssid=args.ssid, paswd=args.passwd, security=args.security, radio=args.radio, upstream=args.upstream)


    for channel in ["8"]:
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
        # set channel utilization threshold in AP
        print("set channel utilization threshold in AP")
        ap.set_channel_utilztn2ghz_threashold(args.ip, args.user, args.pswd, args.ch_threshold)
        print("done")
        time.sleep(10)
        print("cleanup all client and cx on lanforge ")
        obj.precleanup()
        time.sleep(5)
        val = obj.start()
        ch_ut = ""
        if val == "done":
            print("measure channel utilization from AP")
            chutil = ap.channel_utilization_ap_for_2ghz(args.ip, args.user, args.pswd)
            print(chutil)
            ch= []
            for j in chutil:
                ch.append(j.strip())
            for i in ch[0][22:]:
                ch_ut = ch_ut + i
            print(ch_ut)
            if ch_ut > args.ch_threshold:
                data = "FAIL"
                print("load balancing channel utilization test for 2.4Ghz is ", data)
            else:
                data = "PASS"
                print("load balancing channel utilization test for 2.4Ghz is ", data)
        else:
            print("need to see")
            print("measure channel utilization from AP")
            chutil = ap.channel_utilization_ap_for_2ghz(args.ip, args.user, args.pswd)
            print(chutil)
            ch = []
            for j in chutil:
                ch.append(j.strip())
            for i in ch[0][22:]:
                ch_ut = ch_ut + i
            print(ch_ut)
            if ch_ut > args.ch_threshold:
                data = "FAIL"
                print("load balancing channel utilization test for 2.4Ghz is ", data)
            else:
                data = "PASS"
                print("load balancing channel utilization test for 2.4Ghz is ", data)

if __name__ == '__main__':
    main()