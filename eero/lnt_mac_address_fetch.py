#!/usr/bin/env python3

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

    def station_mac_listing_to_csv(self):
        resp = self.json_get(f"/port/?fields=mac")
        filtered_data = []
        for item in resp['interfaces']:
            for port, data in item.items():
                if "sta" in port or "wlan" in port:
                    filtered_data.append({'Port': port, 'MAC': data['mac']})
        print(filtered_data)

        csv_file_path = f"./{self.directory}/sta_mac_list.csv"

        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = ['Port', 'MAC']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()  # Writing Header
            for row in filtered_data:
                writer.writerow(row)
        print(f'Data has been written to {csv_file_path}')


def main():
    parser = argparse.ArgumentParser(prog='large_network_test.py',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog='''
                                     large_network_test.py''',
                                     description=''' 
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