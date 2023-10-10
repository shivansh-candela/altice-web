import subprocess
import argparse


class PcapFrameTimeCalculator:
    def __init__(self, pcap_file_path, ap_bssid_list, client_mac, traffic_direction):
        self.pcap_file_path = pcap_file_path
        self.ap_bssid_list = ap_bssid_list
        self.client_mac = client_mac
        self.traffic_direction = traffic_direction

    def get_frame_time(self, display_filter='eapol', lastframe=False):
        try:
            cmd = [
                'tshark',
                '-r', self.pcap_file_path,
                '-Y', display_filter,
                '-T', 'fields',
                '-e', 'frame.time_relative'
            ]
            # print(display_filter,"display_filter--------")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            # print(result)
            output_lines = result.stdout.strip().splitlines()
            if not output_lines:
                print(f"could not find the packets for filter: {display_filter}")
                return None

            if lastframe:
                return float(output_lines[-1])
            else:
                return float(output_lines[0])

        except:
            print("Error running TShark")
            return None

    def calculate_roam_time(self, bssid):
        print(f"Calculating Roamtime to target AP: {bssid}")
        display_filter = f"wlan.fc.type_subtype == 11 and wlan.ra == {bssid}"
        first_frame_time = self.get_frame_time(display_filter=display_filter)
        display_filter = f"wlan_rsna_eapol.keydes.msgnr == 4 and wlan.ra == {bssid}"
        last_frame_time = self.get_frame_time(display_filter=display_filter)
        time_difference = last_frame_time - first_frame_time
        print(f"Roam time to {bssid} in seconds:", time_difference)

    def calculate_qos_time(self, current_bssid, target_bssid):
        print("Calculating Qos missed duration time:")
        print("current bssid: ",current_bssid, ", target bssid: ",target_bssid)

        display_filter1 = f"wlan.fc.type_subtype == 40 and wlan.ra == {current_bssid} and wlan.ta == {self.client_mac} and !(eapol)"
        display_filter2 = f"wlan.fc.type_subtype == 40 and wlan.ra == {target_bssid} and wlan.ta == {self.client_mac} and !(eapol)"

        if self.traffic_direction == 'download':
            display_filter1 = f"wlan.fc.type_subtype == 40 and wlan.ra == {self.client_mac} and wlan.ta == {current_bssid} and !(eapol)"
            display_filter2 = f"wlan.fc.type_subtype == 40 and wlan.ra == {self.client_mac} and wlan.ta == {target_bssid} and !(eapol)"

        # print(f"Fetching the last Qos packet of {current_bssid}, please wait...")
        last_frame_time = self.get_frame_time(display_filter=display_filter1, lastframe=True)
        first_frame_time = self.get_frame_time(display_filter=display_filter2)
        time_difference = first_frame_time - last_frame_time
        print(f"QoS missed duration time between {current_bssid} and {target_bssid} in seconds:", time_difference)


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
    To get the Roam time and QoS missed time from the provided pcap.

EXAMPLE:
        python3 Roamtime_from_pcap.py --pcap_file "testcase2.pcap" --bssid c4:a8:16:02:b4:4a c4:a8:16:02:b3:4a --client_mac 3a:dc:66:ee:50:35
    '''
    )

    parser.add_argument('--pcap_file', '-p', help='Provide the pcap file path', dest="pcap_file", required=True,
                        default=None)
    parser.add_argument('--bssid', '-bssid', nargs='+', help="Provide the list of BSSID's in order", required=True)
    parser.add_argument('--client_mac', '-mac', help="Provide the MAC address of the client", required=True)
    parser.add_argument('--direction', '-direction', help="Traffic direction, upload will be default", default='upload')

    args = parser.parse_args()

    PcapFrameTimeCalculator_obj = PcapFrameTimeCalculator(
        pcap_file_path=args.pcap_file,
        ap_bssid_list=args.bssid,
        client_mac=args.client_mac,
        traffic_direction=args.direction
    )

    for i in range(len(args.bssid) - 1):
        if args.bssid[i + 1]:
            bssid = args.bssid[i + 1]
            PcapFrameTimeCalculator_obj.calculate_roam_time(bssid)
            PcapFrameTimeCalculator_obj.calculate_qos_time(args.bssid[i], bssid)


if __name__ == "__main__":
    main()
