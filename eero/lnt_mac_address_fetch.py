#!/usr/bin/env python3
"""
This script will fetch the mac address for the stations from the lanforge.

Capabilities:
    * The script will give the .csv file output in the output report directory.
    * The .csv file will contain the mac address for all existing stations in respective lanforge system.

Pre-requisites:
    * Any lanforge system with already existing stations.
    * Since the script is dependent on the lanforge-scripts, the script should be place "lanforge-scripts/py-scripts/" path to get the output.

    CLI (Command Line Interface) to run the script:
        python3 large_network_test.py --mgr 192.168.200.240 --scenario 200-clients-long-run
        --twog_radio 1.1.wiphy2 1.1.wiphy3 1.1.wiphy4 1.1.wiphy5
        --fiveg_radio 1.1.wiphy0 1.1.wiphy1 1.3.wiphy0 1.3.wiphy1 1.3.wiphy2 1.3.wiphy3 1.3.wiphy4
        --sixg_radio 1.4.wiphy3 1.4.wiphy4 1.4.wiphy5 1.4.wiphy6 1.4.wiphy7 --twog_channel 1 --fiveg_channel 36 --sixg_channel 37
        --twog_sniff_radio 1.4.wiphy0 --fiveg_sniff_radio 1.4.wiphy1 --sixg_sniff_radio 1.4.wiphy2 --increment 10
        --csv_outfile sta_mac_list.csv --attenuators 1.1.1031 1.1.3104 --attenuator_module_values 0,0,0,0 0,0,0,0

"""
import sys
import os
import csv
import datetime
import importlib
import argparse
import logging

logger = logging.getLogger(__name__)

if sys.version_info[0] != 3:
    print("This script requires Python Version-3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm


class LNT_MAC_FETCHING(Realm):
    def __init__(self,
                 lf_host="localhost",
                 lf_port=8080):
        super().__init__(lfclient_host=lf_host,
                         lfclient_port=lf_port)
        self.directory = None
        self.lf_host = lf_host
        self.lf_port = lf_port

    # building the output folder, where the output .csv file will be saved
    def building_output_directory(self, directory_name="LNT_STA_MAC_LIST"):
        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S_")  # %Y-%m-%d-%H-h-%m-m-%S-s
        if directory_name:
            self.directory = os.path.join(now + str(directory_name))
            print("Name of the Report Folder: {}".format(self.directory))
        try:
            if not os.path.exists(self.directory):
                os.mkdir(self.directory)
        except Exception as e:
            print("ERROR : The report path is existed but unable to find. Exception raised : {}\n".format(e))
        return self.directory

    # querying the port-mgr tab for mac address & writing them in a .csv file
    def station_mac_listing_to_csv(self):
        resp = self.json_get(f"/port/?fields=mac,port")
        filtered_data = []
        for item in resp['interfaces']:
            for port, data in item.items():
                if "sta" in port or "wlan" in port:
                    filtered_data.append({'Port-ID': data['port'], 'Port': port, 'MAC': data['mac']})
        # print(filtered_data)
        sorted_filtered_data = sorted(filtered_data, key=lambda x: x['Port-ID'])
        # print(sorted_filtered_data)

        csv_file_path = f"./{self.directory}/sta_mac_list.csv"

        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = ['Port-ID', 'Port', 'MAC']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()  # Writing Header
            for row in sorted_filtered_data:
                writer.writerow(row)
        print(f'Data has been written to {csv_file_path}')


def main():
    parser = argparse.ArgumentParser(prog='large_network_test.py',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog='''
                                     lnt_mac_address_fetch.py''',
                                     description=''' 
    CLI: python3 lnt_mac_address_fetch.py --mgr 192.168.200.240
                                     ''')
    required = parser.add_argument_group('Required arguments to run large_network_test.py')
    # optional = parser.add_argument_group('Optional arguments to run large_network_test.py')

    required.add_argument('--mgr', help='hostname for where LANforge GUI is running',
                          default='192.168.200.161')
    required.add_argument('--mgr_port', help='port LANforge GUI HTTP service is running on',
                          default=8080)

    args = parser.parse_args()

    LNT_obj = LNT_MAC_FETCHING(lf_host=args.mgr, lf_port=args.mgr_port)
    LNT_obj.building_output_directory()
    LNT_obj.station_mac_listing_to_csv()


if __name__ == "__main__":
    main()