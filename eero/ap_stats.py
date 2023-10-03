"""
>python ap_stats.py  --channel_utilization --memory_utilization --cpu_utilization --temp --interval 1m  --duration 1h
>python ap_stats.py  --channel_utilization --memory_utilization --cpu_utilization --temp --interval 1m  --count 5

"""
import sys
import serial
import paramiko
import argparse
import csv
import os
import datetime
import importlib
import pandas as pd
from collections import Counter

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)
sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
import time


class APSerialAccess():
    def __init__(self, lfclient_host, lfclient_port, baud_rate=115200, serial_port="/dev/ttyUSB0", timeout=1):
        self.host = lfclient_host
        self.port = lfclient_port
        self.baud_rate = baud_rate
        self.serial_port = serial_port
        self.timeout = timeout
        self.serial_access = serial.Serial(port=self.serial_port, baudrate=baud_rate, timeout=self.timeout)
        self.local_realm = realm.Realm(lfclient_host=self.host, lfclient_port=self.port)
        self.serial_access.setDTR(False)
        time.sleep(0.5)
        self.output = ""

    def send_generic_commands(self, command=[], date_time=""):
        self.open_serial_connectio()
        for comm in command:
            self.serial_access.write((comm + '\r\n').encode())
            time.sleep(1)
            # data_list = [0]

            while (self.serial_access.in_waiting > 0):
                data_list = [0]
                self.output += self.serial_access.readall().decode()
                data_list.append(self.output)

            if comm == "iw dev ap_tt0 station dump":
                self.append_to_txt(f"tt0_channel_utilization_{date_time}.txt", data_list=data_list)
            if comm == "iw dev ap_tt1 station dump":
                self.append_to_txt(f"tt1_channel_utilization_{date_time}.txt", data_list=data_list)
            if comm == "iw dev ap_tt2 station dump":
                self.append_to_txt(f"tt2_channel_utilization_{date_time}.txt", data_list=data_list)
            if comm == "free -h":
                self.append_to_txt(f"memory_utilization_{date_time}.txt", data_list=data_list)
            if comm == "mpstat -P ALL":
                self.append_to_txt(f"cpu_utilization_{date_time}.txt", data_list=data_list)
            if comm == "sensors":
                self.append_to_txt(f"temperature_{date_time}.txt", data_list=data_list)

            self.output = ""
        self.close_connection()

    def append_to_csv(self, file_path, data_list):
        if os.path.exists(file_path):
            mode = 'a'  # Append to existing file
        else:
            mode = 'w'  # Create new file
        with open(file_path, mode, newline='') as csvfile:
            writer = csv.writer(csvfile)
            for data in data_list:
                writer.writerow([str(datetime.datetime.now()), data])

    def append_to_txt(self, file_path, data_list):
        with open(file_path, 'a') as txtfile:
            for data in data_list:
                txtfile.write(f"{str(datetime.datetime.now())} {data}\n")

    #Provides a string return while calling this method with command argument
    def get_log(self, command):
        self.output = ''
        self.open_serial_connectio()
        self.serial_access.write((command + '\r\n').encode())
        self.output += self.serial_access.readall().decode()
        # print(self.output)
        while (self.serial_access.in_waiting > 0):
            self.output += self.serial_access.readall().decode()
        self.close_connection()
        return self.output

    def close_connection(self):
        self.serial_access.close()

    def open_serial_connectio(self):
        try:
            self.serial_access.open()
        except Exception as error:
            print(f"Error: {str(error)}")

    def parse_time(self, time_str):
        if time_str.endswith("h"):
            return int(time_str[:-1]) * 60 * 60
        elif time_str.endswith("m"):
            return int(time_str[:-1]) * 60
        elif time_str.endswith("s"):
            return int(time_str[:-1])
        else:
            return int(time_str)

    def create_csv_with_bitrate_summary(self, txt_file_path, csv_file_path):
        # Read data from the text file
        with open(txt_file_path, 'r') as txtfile:
            lines = txtfile.readlines()

        for line in lines:
            print("--------")
            print(line.strip())
        # Initialize lists to store all tx and rx bitrate values
        tx_bitrate = None
        rx_bitrate = None

        # Flag to indicate whether we are currently processing a station entry
        is_station_entry = False

        # Lists to store all tx and rx bitrate values
        all_tx_bitrates = []
        all_rx_bitrates = []

        # Iterate through the lines to find the tx_bitrate and rx_bitrate
        for line in lines:
            if line.startswith("Station"):
                is_station_entry = True
            elif is_station_entry and "tx bitrate:" in line:
                parts = line.split()
                if len(parts) >= 3:
                    tx_bitrate = parts[2]
                    all_tx_bitrates.append(tx_bitrate)
            elif is_station_entry and "rx bitrate:" in line:
                parts = line.split()
                if len(parts) >= 3:
                    rx_bitrate = parts[2]
                    all_rx_bitrates.append(rx_bitrate)
                is_station_entry = False  # Reset the flag when we are done with this station entry

        # Print the extracted values
        print("All tx_bitrates:", all_tx_bitrates)
        print("All rx_bitrates:", all_rx_bitrates)

        # Calculate the most common tx bitrate and rx bitrate
        most_common_tx_bitrate = Counter(all_tx_bitrates).most_common(1)
        most_common_rx_bitrate = Counter(all_rx_bitrates).most_common(1)
        # Print the most common values
        print("Most Common tx_bitrate:", most_common_tx_bitrate[0][0])
        print("Most Common rx_bitrate:", most_common_rx_bitrate[0][0])

        # Create and write to a CSV file
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Most Common tx_bitrate", most_common_tx_bitrate[0][0]])
            writer.writerow(["Most Common rx_bitrate", most_common_rx_bitrate[0][0]])


def main():
    parser = argparse.ArgumentParser(
        prog='ap_stats.py',
        formatter_class=argparse.RawTextHelpFormatter,
        description='''
        >python ap_stats.py  --channel_utilization --memory_utilization --cpu_utilization --temp --interval 1m  --duration 1h
        : Use this if you want this script to run for 1 hour with 1 min. interval.

        >python ap_stats.py  --channel_utilization --memory_utilization --cpu_utilization --temp --interval 1m  --count 5
        : Use this if you want this script to run 5 times with 1 min. interval.
        ''')

    # This argument will need inputs
    parser.add_argument('--mgr', help='hostname for where LANforge GUI is running', default='localhost')
    parser.add_argument('--mgr_port', help='port LANforge GUI HTTP service is running on', default=8080)
    parser.add_argument('--serial_port', help='Which port AP is connected to ',
                        default='/dev/ttyUSB0')

    # This arguments will work as flags
    parser.add_argument('--channel_utilization', "--chu", "-chu",
                        help='--channel_utilization: This provides channel utilization value',
                        action='store_true')
    parser.add_argument('--memory_utilization', "--mu", "-mu",
                        help='--memory_utilization: This provides memory utilization value',
                        action='store_true')
    parser.add_argument('--cpu_utilization', "--cpu", "-cpu",
                        help='--cpu_utilization: This provides CPU utilization value',
                        action='store_true')
    parser.add_argument('--temp', "--t", "-t",
                        help='--temp: This provides Temp value',
                        action='store_true')

    # This arguments are mandatory
    parser.add_argument("--interval", "-i", "--i",
                        required=True,
                        help="Interval in the format 'h' for hours, 'm' for minutes, or 's' for seconds. ex. 10m",
                        default="1m")

    parser.add_argument("--duration", "-d", "--d",
                        help="Total test duration, Duration in the format 'h' for hours, 'm' for minutes, or 's' for seconds. ex. 1h")

    parser.add_argument("--count", "--c", "-c",
                        help="This can be used instead of duration, This tells script to take how many readings of interval difference"
                             "ex. if count is 2 then 2 values will be captured with user provided time interval",
                        default=1,
                        type=int)

    args = parser.parse_args()

    use_duration = False
    use_count = False

    get_ap_access = APSerialAccess(lfclient_host=args.mgr, lfclient_port=args.mgr_port)
    end_time = 0

    if args.duration is not None:
        use_duration = True
        duration = get_ap_access.parse_time(args.duration)
        end_time = time.time() + duration

    else:
        use_count = True

    current_datetime = datetime.datetime.now()
    date_time = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
    interval = get_ap_access.parse_time(args.interval)

    # print(f"Test Start Time: {time.strftime('%H:%M:%S',time.gmtime(time.time()))}\nInterval : {interval}\nTotal Duration: {duration}\nTest End Time in HH:MM:SS: {datetime.timedelta(seconds=end_time)}")
    count = args.count

    def functions():
        if args.channel_utilization:
            get_ap_access.send_generic_commands(
                command=["iw dev ap_tt0 survey dump", "iw dev ap_tt1 survey dump", "iw dev ap_tt2 survey dump"],
                date_time=date_time)

        if args.memory_utilization:
            get_ap_access.send_generic_commands(command=["free -h"], date_time=date_time)

        if args.cpu_utilization:
            get_ap_access.send_generic_commands(command=["mpstat -P ALL"], date_time=date_time)

        if args.temp:
            get_ap_access.send_generic_commands(command=["sensors"], date_time=date_time)
        if args.channel_utilization or args.memory_utilization or args.cpu_utilization or args.temp:
            txt_file_path = f'tt0_channel_utilization_{date_time}.txt'  # Change this to the appropriate file
            csv_file_path = f'bitrate_summary_{date_time}.csv'  # Change this to the desired Excel file name
            get_ap_access.create_csv_with_bitrate_summary(txt_file_path, csv_file_path)

    while (use_duration or use_count):
        if time.time() < end_time:
            functions()
            if (end_time - time.time() < interval):
                break
            print(f"Time left: {end_time - time.time()} Sec")

        elif count >= 1:
            functions()
            count -= 1
            print(f"Count left: {count}")
            if count < 1:
                break

        print(f"Sleeping for {interval} Seconds")
        time.sleep(interval)



if __name__ == '__main__':
    main()