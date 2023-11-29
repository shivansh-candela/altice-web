'''

The script is used to get the Authentication time ,Re-association time ,4-way handshake time,Roam time and QoS missed time from the provided pcap.

Capabilities:
    It calculates the respective times and gives an output in a CSV    


Pre-requisites:
    This script requires TShark to be installed..
    Note: When you install Wireshark, the tshark typically comes bundled with it as part of the Wireshark package 
    if not, you can consider manually installing tshark separately.
    

example CLI:
        python3 Roamtime_from_pcap.py --pcap_file "testcase2.pcap" --bssid c4:a8:16:02:b4:4a c4:a8:16:02:b3:4a --client_mac 3a:dc:66:ee:50:35

'''

import subprocess
import argparse
from datetime import datetime
import pandas as pd


class PcapFrameTimeCalculator:
    def __init__(self, pcap_file_path, ap_bssid_list, client_mac, traffic_direction, output_csv_name):
        self.pcap_file_path = pcap_file_path
        self.ap_bssid_list = ap_bssid_list
        self.client_mac = client_mac
        self.traffic_direction = traffic_direction
        self.output_csv = output_csv_name

    def get_frame_time(self, display_filter='eapol', lastframe=False):
        try:
            cmd = [
                'tshark',
                '-r', self.pcap_file_path,
                '-Y', display_filter,
                '-T', 'fields',
                '-e', 'frame.time'
            ]
            # print(display_filter,"display_filter--------")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            # print(result)
            output_lines = result.stdout.strip().splitlines()
            # print(output_lines[-1].split(",")[1].split(" ")[-2])
            # print(type(output_lines[0]))
            if not output_lines:
                print(f"could not find the packets for filter: {display_filter}")
                return None

            if lastframe:
                # return output_lines[-1]
                for elem in output_lines[-1].split(",")[1].split(" "):
                    if ':' in elem:
                        return elem[:-3]
            else:
                # print(output_lines[0].split(",")[1].split(" "),"output_lines---------------")
                for elem in output_lines[0].split(",")[1].split(" "):
                    if ':' in elem:
                        return elem[:-3]

        except Exception as e:
            print("Error running TShark", e)
            return None

    def calculate_roam_time(self, current_bssid, target_bssid):
        print(f"Calculating Roamtime from current Ap-{current_bssid} to target Ap-{target_bssid}:")
        display_filter = f"wlan.fc.type_subtype == 11 and wlan.ra == {target_bssid}"
        first_frame_time = self.get_frame_time(display_filter=display_filter)
        display_filter = f"wlan_rsna_eapol.keydes.msgnr == 4 and wlan.ra == {target_bssid}"
        last_frame_time = self.get_frame_time(display_filter=display_filter)
        # print(last_frame_time,first_frame_time)
        time_difference = datetime.strptime(last_frame_time, "%H:%M:%S.%f") - datetime.strptime(first_frame_time,
                                                                                                "%H:%M:%S.%f")
        # time_difference = last_frame_time - first_frame_time
        print(f"Roam time from current Ap-{current_bssid} to target Ap-{current_bssid} in seconds:", round(time_difference.total_seconds(), 3), end="\n\n")
        self.roam_auth_first_frame = first_frame_time
        self.roam_eapol_last_frame = last_frame_time
        self.roam_time = round(time_difference.total_seconds(), 3)

    def calculate_auth_time(self, bssid):
        print(f"Calculating Authentication time to target Ap: {bssid}")
        display_filter = f"wlan.fc.type_subtype == 11 and wlan.ra == {bssid} and wlan.ta == {self.client_mac}"
        first_frame_time = self.get_frame_time(display_filter=display_filter)
        display_filter = f"wlan.fc.type_subtype == 11 and wlan.ra == {self.client_mac} and wlan.ta == {bssid}"
        last_frame_time = self.get_frame_time(display_filter=display_filter)
        # time_difference = last_frame_time - first_frame_time
        time_difference = datetime.strptime(last_frame_time, "%H:%M:%S.%f") - datetime.strptime(first_frame_time,
                                                                                                "%H:%M:%S.%f")
        print(f"Authentication time to target Ap: {bssid} in seconds:", round(time_difference.total_seconds(), 3),
              end="\n\n")
        self.auth_first_frame = first_frame_time
        self.auth_last_frame = last_frame_time
        self.auth_time = round(time_difference.total_seconds(), 3)

    def calculate_reassociation_time(self, bssid):
        print(f"Calculating Re-association time to target Ap: {bssid}")
        display_filter = f"wlan.fc.type_subtype == 2 and wlan.ra == {bssid} and wlan.ta == {self.client_mac}"
        first_frame_time = self.get_frame_time(display_filter=display_filter)
        display_filter = f"wlan.fc.type_subtype == 3 and wlan.ra == {self.client_mac} and wlan.ta == {bssid}"
        last_frame_time = self.get_frame_time(display_filter=display_filter)
        # time_difference = last_frame_time - first_frame_time
        time_difference = datetime.strptime(last_frame_time, "%H:%M:%S.%f") - datetime.strptime(first_frame_time,
                                                                                                "%H:%M:%S.%f")
        print(f"Re-association time to target Ap: {bssid} in seconds:", round(time_difference.total_seconds(), 3),
              end="\n\n")
        self.reassoc_first_frame = first_frame_time
        self.reassoc_last_frame = last_frame_time
        self.reassoc_time = round(time_difference.total_seconds(), 3)

    def calculate_handshake_time(self, bssid):
        print(f"Calculating 4-way Handshake time to target Ap: {bssid}")
        display_filter = f"wlan_rsna_eapol.keydes.msgnr == 1 and wlan.ta == {bssid} and wlan.ra == {self.client_mac}"
        first_frame_time = self.get_frame_time(display_filter=display_filter)
        display_filter = f"wlan_rsna_eapol.keydes.msgnr == 4 and wlan.ra == {bssid} and wlan.ta == {self.client_mac}"
        last_frame_time = self.get_frame_time(display_filter=display_filter)
        # time_difference = last_frame_time - first_frame_time
        time_difference = datetime.strptime(last_frame_time, "%H:%M:%S.%f") - datetime.strptime(first_frame_time,
                                                                                                "%H:%M:%S.%f")
        print(f"4-way Handshake time to target Ap: {bssid} in seconds:", round(time_difference.total_seconds(), 3),
              end="\n\n")
        self.eapol_first_frame = first_frame_time
        self.eapol_last_frame = last_frame_time

        self.four_way_time = round(time_difference.total_seconds(), 3)

    def calculate_qos_time(self, current_bssid, target_bssid):
        print("Calculating Qos missed duration time:")
        print("current bssid: ", current_bssid, ", target bssid: ", target_bssid)

        display_filter1 = f"wlan.fc.type_subtype == 40 and wlan.ra == {current_bssid} and wlan.ta == {self.client_mac} and !(eapol)"
        display_filter2 = f"wlan.fc.type_subtype == 40 and wlan.ra == {target_bssid} and wlan.ta == {self.client_mac} and !(eapol)"

        if self.traffic_direction == 'download':
            display_filter1 = f"wlan.fc.type_subtype == 40 and wlan.ra == {self.client_mac} and wlan.ta == {current_bssid} and !(eapol)"
            display_filter2 = f"wlan.fc.type_subtype == 40 and wlan.ra == {self.client_mac} and wlan.ta == {target_bssid} and !(eapol)"

        # print(f"Fetching the last Qos packet of {current_bssid}, please wait...")
        last_frame_time = self.get_frame_time(display_filter=display_filter1, lastframe=True)
        first_frame_time = self.get_frame_time(display_filter=display_filter2)
        # time_difference = first_frame_time - last_frame_time
        time_difference = datetime.strptime(first_frame_time, "%H:%M:%S.%f") - datetime.strptime(last_frame_time,
                                                                                                 "%H:%M:%S.%f")
        print(f"QoS missed duration time between {current_bssid} and {target_bssid} in seconds:",
              round(time_difference.total_seconds(), 3))
        self.qos_missed_time = round(time_difference.total_seconds(), 3)
        self.qos_first_frame = first_frame_time
        self.qos_last_frame = last_frame_time

    def generate_csv(self, count):
        # print(datetime.strptime(self.auth_last_frame, "%H:%M:%S.%f"),"-------")
        # print(self.auth_last_frame,"-----")
        data = {
            'Parameter': ['Roamtime', 'Auth request time', 'Auth response time', 'Authentication Time',
                          'Re-assoc request time', 'Re-assoc response time', 'Re-association Time', 'eapol-1/4',
                          'eapol-4/4', '4-Way Handshake Time',
                          'last Qos pack to Ap1', 'first Qos pack to Ap2', 'Qos Missed Duration'],
            'Timestamp': [f"{self.roam_auth_first_frame} - {self.roam_eapol_last_frame}",f"-{self.auth_first_frame}-",f"-{self.auth_last_frame}-",
                          '',f"-{self.reassoc_first_frame}-",f"-{self.reassoc_last_frame}-" ,'',f"-{self.eapol_first_frame}-",f"-{self.eapol_last_frame}-", '', f"-{self.qos_last_frame}-",f"-{self.qos_first_frame}-" ,''],
            'Duration in seconds': [self.roam_time, '', '', self.auth_time, '', '', self.reassoc_time, '', '',
                                    self.four_way_time, '', '', self.qos_missed_time]}

        df = pd.DataFrame(data)
        datetime.strptime(self.qos_first_frame, "%H:%M:%S.%f")
        if (count == 1):
            df.to_csv(f'{self.output_csv}_.csv', index=False)
        else:
            df.to_csv(f'{self.output_csv}_2.csv', index=False)

def main():
    parser = argparse.ArgumentParser(
        prog='Roamtime_from_pcap.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='',
        description='''\
    """
------------
SETUP:
This script requires TShark to be installed and available in your system's PATH.
    Note: When you install Wireshark, the tshark typically comes bundled with it as part of the Wireshark package 
    if not, you can consider manually installing tshark separately.

PURPOSE:
    To get the Authentication time ,Re-association time ,4-way handshake time,Roam time and QoS missed time from the provided pcap.

EXAMPLE:
        python3 Roamtime_from_pcap.py --pcap_file "testcase2.pcap" --bssid c4:a8:16:02:b4:4a c4:a8:16:02:b3:4a --client_mac 3a:dc:66:ee:50:35
    '''
    )

    parser.add_argument('--pcap_file', '-p', help='Provide the pcap file path', dest="pcap_file", required=True,
                        default=None)
    parser.add_argument('--bssid', '-bssid', nargs='+', help="Provide the list of BSSID's in order", required=True)
    parser.add_argument('--client_mac', '-mac', help="Provide the MAC address of the client", required=True)
    parser.add_argument('--direction', '-direction', help="Traffic direction, upload will be default", default='upload')
    parser.add_argument('--output_csv', '-output_csv_name',
                        help="provide the csv name in which the csv should be created ", default='Roamtime_csv')

    args = parser.parse_args()

    PcapFrameTimeCalculator_obj = PcapFrameTimeCalculator(
        pcap_file_path=args.pcap_file,
        ap_bssid_list=args.bssid,
        client_mac=args.client_mac,
        traffic_direction=args.direction,
        output_csv_name=args.output_csv
    )

    for i in range(len(args.bssid) - 1):
        if args.bssid[i + 1]:
            bssid = args.bssid[i + 1]
            PcapFrameTimeCalculator_obj.calculate_auth_time(bssid)
            PcapFrameTimeCalculator_obj.calculate_reassociation_time(bssid)
            PcapFrameTimeCalculator_obj.calculate_handshake_time(bssid)
            PcapFrameTimeCalculator_obj.calculate_roam_time(args.bssid[i],bssid)
            PcapFrameTimeCalculator_obj.calculate_qos_time(args.bssid[i], bssid)

            PcapFrameTimeCalculator_obj.generate_csv(i + 1)


if __name__ == "__main__":
    main()