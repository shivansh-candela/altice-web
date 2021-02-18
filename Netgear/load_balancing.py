"""
This script particularly checks for load balancing pass/ fail criteria according to rssi threshold
*** under progress ***
cmd - [lanforge@lf0312-7d02 py-scripts]$ python3 load_16.py -i 192.168.200.194 -u root -p Netgear@123xzsawq@! --host localhost --ssid TestAP103 --passwd lanforge  --security wpa2  --radio wiphy3 --rssi2 35 --rssi5l 32 --rssi5h 30

"""

import sys
import os
import argparse
import time
import pexpect
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

class AP_automate:
    def __init__(self, ip, user, pswd):
        self.ip = ip
        self.user = user
        self.pswd = pswd

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


    parser.add_argument('-r2', '--rssi2', type=str, help='Threshold RSSI value for 2.4 ghz')
    parser.add_argument('-r5', '--rssi5l', type=str, help='Threshold RSSI value for 5 ghz low')
    parser.add_argument('-r5h', '--rssi5h', type=str, help='Threshold RSSI value for 5 ghz high')
    args = parser.parse_args()

    num_sta = 1

    sta_id = 0
    station_list = LFUtils.port_name_series(prefix="sta",
                                            start_id=sta_id,
                                            end_id=num_sta - 1,
                                            padding_number=100,
                                            radio=args.radio)
    station = STATION(lfclient_host=args.host, lfclient_port=8080, ssid=args.ssid, paswd=args.passwd,
                  security=args.security, radio=args.radio, sta_list=station_list)
    attenuator = Attenuator()
    ap = AP_automate(args.ip, args.user, args.pswd)

    station.precleanup(station_list)
    station.build()
    station.start(station)
    station.local_realm.wait_for_ip(station_list)
    time.sleep(10)
    channel_values = ["9", "36", "153"]
    rssi = ""
    rssi_threshold = ""
    for channel in channel_values:
        if channel == "9":
            rssi_threshold = args.rssi2
        elif channel == "36":
            rssi_threshold = args.rssi5l
        else:
            rssi_threshold = args.rssi5h
        """print("set channel in ap at ", channel)

        ap.set_channel_in_ap_at_(args.ip, args.user, args.pswd, channel)
        time.sleep(20)"""
        print("set channel in lanforge to ", channel)
        host = "localhost"
        base_url = "http://%s:8080" % host
        resource_id = 1  # typically you're using resource 1 in stand alone realm
        radio = "wiphy3"
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
        print("set attenuation")
        att_values = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950]
        # 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950

        var3 = ""
        for i in att_values:
            print("set attenuation to ", i)
            attenuator.set_att_dbm(i)
            time.sleep(20)
            print("station down")
            station.stop()
            time.sleep(10)
            print("station up")
            station.start(station)
            station.local_realm.wait_for_ip(station_list)
            time.sleep(10)
            print("check if station is up or not")
            var2 = station.json_get("/port/1/1/sta00/?fields=channel")
            var3 = var2['interface']['channel']
            print("wait until channel assigned")
            timeout = time.time() + 60 * 1

            while var3 == "-1":
                var2 = station.json_get("/port/1/1/sta00?fields=channel")
                var3 = var2['interface']['channel']
                time.sleep(1)
                if time.time() > timeout:
                    var2 = station.json_get("/port/1/1/sta00?fields=channel")
                    var3 = var2['interface']['channel']
                    break
            print("channel is at ", var3)
            time.sleep(30)
            if var3 != "-1":
                print("measuring rssi value when client connected")
                ap_logs = ap.check_Rssi_from_ap(args.ip, args.user, args.pswd)

                # print(type(ap_logs))
                N = 1
                res = list(islice(reversed(ap_logs), 0, N))
                res.reverse()
                print(res)

                for r in res:
                    #print(r.split(','))
                    for j in r.split(','):
                        if "rssi" in j:
                            print("yes")
                            #print(j.split(':'))
                            for k in j.split(':'):
                                #print(k)
                                x = k.replace('"', '')
                                print(x)
                                rssi = x
                print("rssi value is ", rssi)
                print("attenuator value at which test stop ", i)
                if rssi > rssi_threshold:
                    data = "PASS"
                    print("PASS")
                    continue
                else:
                    data = "FAIL"
                    print(data)
                    break
            else:
                print("ap stops admitting client")
                print("check in AP for Rssi value")
                print("measuring previous rssi value when client connected")
                ap_logs = ap.check_Rssi_from_ap(args.ip, args.user, args.pswd)

                # print(type(ap_logs))
                N = 1
                res = list(islice(reversed(ap_logs), 0, N))
                res.reverse()
                print(res)

                for i in res:
                    print(i.split(','))
                    for j in i.split(','):
                        if "rssi" in j:
                            print("yes")
                            print(j.split(':'))
                            for k in j.split(':'):
                                # print(k)
                                x = k.replace('"', '')
                                print(x)
                                rssi = x
                print("rssi value is ", rssi)
                print("previous rssi value is ", rssi)
                if rssi >= rssi_threshold:
                    data = "PASS"
                    print(data)
                else:
                    data = "FAIL"
                    print(data)
                    break






if __name__ == '__main__':
    main()