import pyshark
import argparse
import os
import pandas as pd
from datetime import datetime
import subprocess




parser = argparse.ArgumentParser(
        prog='connectiontimes_Wireshark.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='',
        description='''\
    """

------------------------------------------------------------------------------------------------------------------------
EXAMPLE1: For 2G or 5G which needs decryption of pcap
        python3 connectiontimes_Wireshark.py --pcap_file 121.pcap  --client_mac 00:0a:52:ed:58:d0 00:0a:52:34:85:d0 00:0a:52:66:4e:d0 00:0a:52:ad:a4:d0 00:0a:52:71:44:d0 00:0a:52:b3:54:d0 00:0a:52:36:c1:d0 00:0a:52:41:ae:d0 00:0a:52:04:d7:d0 00:0a:52:d9:99:d0 00:0a:52:51:aa:d0  
        --output_csv check  --decrypt_phrase 1234567890:eero_wifi_1-5G-36 
------------------------------------------------------------------------------------------------------------------------

EXAMPLE2:  For 6g
        python3 connectiontimes_Wireshark.py --pcap_file 121.pcap  --client_mac 00:0a:52:ed:58:d0 00:0a:52:34:85:d0 00:0a:52:66:4e:d0 00:0a:52:ad:a4:d0 00:0a:52:71:44:d0 00:0a:52:b3:54:d0 00:0a:52:36:c1:d0 00:0a:52:41:ae:d0 00:0a:52:04:d7:d0 00:0a:52:d9:99:d0 00:0a:52:51:aa:d0  
        --output_csv check_1 --six_g
------------------------------------------------------------------------------------------------------------------------

    '''
    )

parser.add_argument('--pcap_file', '-p', help='Provide the pcap file path', dest="pcap_file", required=True,
                    default=None)
parser.add_argument('--client_mac_list', '-mac', nargs='+', help="Provide the MAC address of the client", required=True)
parser.add_argument('--six_g', '-six_GHz', action='store_true', help="mention the argument if providing a 6GHz pcap")
parser.add_argument('--output_csv', '-output_csv_name',
                        help="provide the csv name in which the csv should be created ", default='Roamtime_csv')
parser.add_argument('--decrypt_phrase', '-decrypt_keys',help="Provide the Decryption phrase to decrypt the pcap in the format of <wpa_key>:<ssid>")

args = parser.parse_args()
transmitter_addresses_list =args.client_mac_list
print(transmitter_addresses_list)
# Replace 'your_capture.pcap' with the path to your PCAP file
pcap_file = args.pcap_file
# pcap_file = '30_2.pcap'
probe_assoc_time_list = []
authrequest_assoc_time_list = []
authresponse_assoc_time_list = []
four_way_handshake_time_list = []
dhcp_time_list = []
mac_list = []
# Define the transmitter addresses as a list
# transmitter_addresses = ['00:0a:52:b6:a1:dd', '9c:57:bc:ca:95:a3', '00:0a:52:ce:62:dd' ]
all_data = pd.DataFrame()
for i,transmitter_address in enumerate(transmitter_addresses_list):
    probetime = 0
    Assoctime = 0
    firstmessage = 0
    fourthmessage = 0
    authenticationresponse = 0
    authenticationrequest = 0
    first__dhcp_frame_timestamp = None
    last_frame_timestamp = None
    time_differences_list =[]
    mac_list.append(transmitter_address)

    # Create the display filters using the variable
    display_filter1 = f'(wlan.fc.type_subtype==5) && (wlan.da == {transmitter_address})'
    display_filter2 = f'(wlan.fc.type_subtype==1) && (wlan.da == {transmitter_address})'
    display_filter3 = f'(wlan_rsna_eapol.keydes.msgnr == 1 ) && (wlan.ra == {transmitter_address})'
    display_filter4 = f'(wlan_rsna_eapol.keydes.msgnr == 4 ) && (wlan.ta == {transmitter_address})'
    display_filter5 = f'(wlan.fc.type_subtype==11) && (wlan.ta == {transmitter_address})'
    display_filter6 = f'(wlan.fc.type_subtype==11) && (wlan.da == {transmitter_address})'
    display_filter7 = 'dhcp'


    # print(display_filter7,"---------")




    # Open the PCAP file and apply the display filters
    capture1 = pyshark.FileCapture(pcap_file, display_filter=display_filter1)
    capture2 = pyshark.FileCapture(pcap_file, display_filter=display_filter2)
    capture3 = pyshark.FileCapture(pcap_file, display_filter=display_filter3)
    capture4 = pyshark.FileCapture(pcap_file, display_filter=display_filter4)
    capture5 = pyshark.FileCapture(pcap_file, display_filter=display_filter5)
    capture6 = pyshark.FileCapture(pcap_file, display_filter=display_filter6)
    capture7 = pyshark.FileCapture(pcap_file, display_filter=display_filter7)




    # Iterate through the packets in each capture and print the timestamps
    print(f"Transmitter Address: {transmitter_address}")
    for packet in capture1:
        probetime = packet.sniff_time
        print("Probe Response Timestamp:", packet.sniff_time)

    for packet in capture2:
        Assoctime = packet.sniff_time
        print("Assoc Response Timestamp:", packet.sniff_time)

    for packet in capture3:
        firstmessage = packet.sniff_time
        print(packet.sniff_time)
    for packet in capture4:
        fourthmessage = packet.sniff_time
        print(packet.sniff_time)
    for packet in capture5:
        authenticationrequest = packet.sniff_time
        print(packet.sniff_time)

    for packet in capture6:
        authenticationresponse = packet.sniff_time
        print(packet.sniff_time)
    # print(capture7,"-------------------")
    if args.six_g:
        first_frame = True
        for packet in capture7:
            # print("-------------------")
            if first_frame:
                first__dhcp_frame_timestamp = str(packet.sniff_time).split(" ")[-1]
                first_frame = False

            last_frame_timestamp = str(packet.sniff_time).split(" ")[-1]

    else:
        if args.decrypt_phrase is None:
            print("please provide the decryption phrase ")
        # args.decrypt_phrase = "1234567890:eero_wifi_1-5G-36"
        # decryption = "uat:80211_keys:\"wpa-pwd\",\" 1234567890:eero_wifi_1-5G-36\""
        decryption = f'uat:80211_keys:"wpa-pwd"," {args.decrypt_phrase}"'
        command = [
            'tshark',
            '-r', pcap_file,
            '-o', 'wlan.enable_decryption:TRUE',
            '-o',  decryption,
            '-Y', f'dhcp.option.dhcp == 1 && wlan.addr == {transmitter_address}',
            '-T', 'fields',
            '-e', 'frame.time'
        ]
        result = ""
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
        except:
            print("could not decrypt the pcap.")
        output_lines = result.stdout.strip().splitlines()
        if output_lines:
            for elem in output_lines[0].split(",")[1].split(" "):
                if ':' in elem:
                    first__dhcp_frame_timestamp = elem[:-3]
                    print(f"first Dhcp timestamp for {transmitter_address}:", first__dhcp_frame_timestamp)

        command = [
            'tshark',
            '-r', pcap_file,
            '-o', 'wlan.enable_decryption:TRUE',
            '-o', decryption,
            '-Y', f'dhcp.option.dhcp == 5 && wlan.addr ==  {transmitter_address}',
            '-T', 'fields',
            '-e', 'frame.time'
        ]
        result1 = ""
        try:
            result1 = subprocess.run(command, capture_output=True, text=True, check=True)
        except:
            print("could not decrypt the pcap.")

        # print(result)
        output_lines1 = result1.stdout.strip().splitlines()
        if output_lines1:
            for elem in output_lines1[-1].split(",")[1].split(" "):
                if ':' in elem:
                    last_frame_timestamp = elem[:-3]
                    print(f"last Dhcp timestamp for {last_frame_timestamp}:", first__dhcp_frame_timestamp)

    if probetime and Assoctime:
        time_difference = Assoctime - probetime
        print(f"Time Difference between Assoc and Probe for {transmitter_address}: {time_difference}")
        # time_differences_list.append(time_difference)
        probe_assoc_time_list.append(str(time_difference).split(":")[-1])
    else:
        print("No matching Probe and Assoc responses found.")
        probe_assoc_time_list.append("-")

    if authenticationrequest and Assoctime:
        time_difference = Assoctime - authenticationrequest
        print(f"Time Difference between authreq and Probe for {transmitter_address}: {time_difference}")
        authrequest_assoc_time_list.append(str(time_difference).split(":")[-1])


    else:
        print("No matching authreq and Assoc responses found.")
        authrequest_assoc_time_list.append("-")


    if authenticationresponse and Assoctime:
        time_difference = Assoctime - authenticationresponse
        print(f"Time Difference between authres and Probe for {transmitter_address}: {time_difference}")
        authresponse_assoc_time_list.append(str(time_difference).split(":")[-1])

    else:
        print("No matching authres and authres responses found.")
        authresponse_assoc_time_list.append("-")


    if firstmessage and fourthmessage:
        time_difference = fourthmessage - firstmessage
        print(f"Time interval for 4 way handshake {transmitter_address}: {time_difference}")
        four_way_handshake_time_list.append(str(time_difference).split(":")[-1])

    else:
        print("No eapol found")
        four_way_handshake_time_list.append("-")


    if first__dhcp_frame_timestamp and last_frame_timestamp:
        time_difference = datetime.strptime(last_frame_timestamp, "%H:%M:%S.%f") - datetime.strptime(first__dhcp_frame_timestamp,
                                                                                                 "%H:%M:%S.%f")
        # time_difference = last_frame_timestamp - first__dhcp_frame_timestamp
        print(f"Time interval for DHCP {transmitter_address}: {time_difference}")
        dhcp_time_list.append(str(time_difference).split(":")[-1])

    else:
        print("could not fetch dhcp time")
        dhcp_time_list.append("-")


    # print(datetime.strptime(self.auth_last_frame, "%H:%M:%S.%f"),"-------")
    capture1.close()
    capture2.close()
    capture3.close()
    capture4.close()
    capture5.close()
    capture6.close()
    capture7.close()
    # print(four_way_handshake_time_list,"-----")

data = {
    'Sl.no.': [str(i+1)+" " for i in range(len(four_way_handshake_time_list))],
    'Client MAC':mac_list,
    'probe request to assoc response (sec)': probe_assoc_time_list,
    'authentication request to assoc response (sec)': authrequest_assoc_time_list,
    'authentication response to assoc response (sec)':authresponse_assoc_time_list,
    '4-Way handshake Time (sec)':four_way_handshake_time_list,
    'Dhcp time (sec)':dhcp_time_list
}
df = pd.DataFrame(data)
# datetime.strptime(self.qos_first_frame, "%H:%M:%S.%f")
# if (count == 1):
all_data = all_data._append(df, ignore_index=True)
all_data.to_csv(f'{args.output_csv}.csv', index=False)


