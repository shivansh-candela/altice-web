"""
This script will create as many client as you want one by one and stops connecting when the maximum client capacity is reached
"""
import sys
import argparse
import time
if 'py-json' not in sys.path:
    sys.path.append('../py-json')
from LANforge import LFUtils
from LANforge import lfcli_base
from LANforge.lfcli_base import LFCliBase
from LANforge.LFUtils import *
import realm
from realm import Realm
class Station(Realm):
    def __init__(self, lfclient_host, lfclient_port, ssid, paswd, security, radio, num_sta, name_prefix="L3", upstream="eth2"):
        self.host = lfclient_host
        self.port = lfclient_port
        self.ssid = ssid
        self.paswd = paswd
        self.security = security
        self.radio = radio
        self.num_sta = num_sta
        self.name_prefix = name_prefix
        self.upstream = upstream
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.station_profile = self.local_realm.new_station_profile()
        self.station_profile.ssid = self.ssid
        self.station_profile.ssid_pass = self.paswd,
        self.station_profile.security = self.security
    def precleanup(self):
        num_sta = 60
        station_list = LFUtils.port_name_series(prefix="sta",
                                                start_id=0,
                                                end_id=num_sta - 1,
                                                padding_number=100,
                                                radio=self.radio)
        self.station_profile.cleanup(station_list)
        LFUtils.wait_until_ports_disappear(base_url=self.local_realm.lfclient_url, port_list=station_list,
                                           debug=self.local_realm.debug)
        time.sleep(1)
    def build(self, sta_name):
        self.station_profile.use_security(self.security, self.ssid, self.paswd)
        self.station_profile.create(radio=self.radio, sta_names_=[sta_name], debug=self.local_realm.debug)
        self.station_profile.admin_up()
        time.sleep(10)
        if self.local_realm.wait_for_ip([sta_name],timeout_sec=60):
            self.local_realm._pass("All stations got IPs", print_=True)
            return 1
        else:
            self.local_realm._fail("Stations failed to get IPs", print_=True)
            print("try again 1st time")
            time.sleep(20)
            print("station down")
            self.local_realm.admin_down(sta_name)
            #self.station_profile.admin_down()
            time.sleep(20)
            print("station up")
            self.station_profile.admin_up()
            time.sleep(20)
            if self.local_realm.wait_for_ip([sta_name], timeout_sec=60):
               self.local_realm._pass("All stations got IPs", print_=True)
               return 1
            else:
                self.local_realm._fail("Stations failed to get IPs", print_=True)
                print("try again 2nd time")
                time.sleep(30)
                print("station down")
                self.local_realm.admin_down(sta_name)
                time.sleep(20)
                print("station up")
                self.station_profile.admin_up()
                time.sleep(20)
                if self.local_realm.wait_for_ip([sta_name], timeout_sec=60):
                   self.local_realm._pass("All stations got IPs", print_=True)
                   return 1
                else:
                    self.local_realm._fail("Stations failed to get IPs", print_=True)
                    print("try again 3rd time")
                    time.sleep(20)
                    print("station down")
                    self.local_realm.admin_down(sta_name)
                    time.sleep(30)
                    print("station up")
                    self.station_profile.admin_up()
                    time.sleep(20)
                    if self.local_realm.wait_for_ip([sta_name],timeout_sec=60):
                       self.local_realm._pass("All stations got IPs", print_=True)
                       return  1
                    else:
                        self.local_realm._fail("Stations failed to get IPs", print_=True)
                        print("try again 4th time")
                        print("wait for ip")
                        if self.local_realm.wait_for_ip([sta_name], timeout_sec=60):
                            self.local_realm._pass("All stations got IPs", print_=True)
                            return 1

                        else:
                           self.local_realm._fail("Stations failed to get IPs", print_=True)
                           return 0
    def start(self, num_sta):
        self.num_sta = num_sta
        station_list = LFUtils.port_name_series(prefix="sta",
                                                start_id=0,
                                                end_id=self.num_sta - 1,
                                                padding_number=100,
                                                radio=self.radio)
        for i in station_list:
            if self.build(i) == 0:
                print("station not created")
                data = "not done"
                break
            else:
                print("station created")
                data = "done"
        return data
    def stop(self):
        # Bring stations down
        self.station_profile.admin_down()
def main():
    parser = argparse.ArgumentParser(description="Client Admission Test Script")
    parser.add_argument('-hst', '--host', type=str, help='host name')
    parser.add_argument('-s', '--ssid', type=str, help='ssid for client')
    parser.add_argument('-pwd', '--passwd', type=str, help='password to connect to ssid')
    parser.add_argument('-sec', '--security', type=str, help='security')
    parser.add_argument('-rad', '--radio', type=str, help='radio at which client will be connected')
    parser.add_argument('-num_sta', '--num_sta', type=int, help='provide number of stations you want to create', default=60)
    # parser.add_argument()
    args = parser.parse_args()
    obj = Station(lfclient_host=args.host, lfclient_port=8080, ssid=args.ssid, paswd=args.passwd,

                     security=args.security, radio=args.radio, num_sta=args.num_sta)
    obj.precleanup()
    obj.start(num_sta=args.num_sta)
if __name__ == '__main__':
    main()
