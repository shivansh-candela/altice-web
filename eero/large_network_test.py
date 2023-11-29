#!/usr/bin/env python3
"""
This script generates the .pcap files and one .csv file based user specified increment order.

Capabilities:
    * The script will support for 2g, 5g, 6g bands.
    * It has the capability for station side sniffing.
    * It will support for multiple resources units.
    * It will generate the pcap's based on the user specified increment order.
    * It will generate the .csv file which will contain the station mac address information base on the user specifed increment order.

Pre-requisites:
    * The LARGE NETWORK TESTBED setup with (200 clients or more)
    * Since the script is dependent on the lanforge-scripts, the script should be place "lanforge-scripts/py-scripts/" path to get the output.


    CLI (Command Line Interface) to run the script:
        python3 large_network_test.py --mgr 192.168.200.240 --scenario 200-clients-long-run
        --twog_radio 1.1.wiphy2 1.1.wiphy3 1.1.wiphy4 1.1.wiphy5
        --fiveg_radio 1.1.wiphy0 1.1.wiphy1 1.3.wiphy0 1.3.wiphy1 1.3.wiphy2 1.3.wiphy3 1.3.wiphy4
        --sixg_radio 1.4.wiphy3 1.4.wiphy4 1.4.wiphy5 1.4.wiphy6 1.4.wiphy7 --twog_channel 1 --fiveg_channel 36 --sixg_channel 37
        --twog_sniff_radio 1.4.wiphy0 --fiveg_sniff_radio 1.4.wiphy1 --sixg_sniff_radio 1.4.wiphy2 --increment 10
        --csv_outfile sta_mac_list.csv --attenuators 1.1.1031 1.1.3104 --attenuator_module_values 0,0,0,0 0,0,0,0

"""
import csv
import datetime
import sys
import os
import importlib
import argparse
import time
import logging

logger = logging.getLogger(__name__)

if sys.version_info[0] != 3:
    print("This script requires Python Version-3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))
realm = importlib.import_module("py-json.realm")
Realm = realm.Realm
cv_test_manager = importlib.import_module("py-json.cv_test_manager")
cv_test_reports = importlib.import_module("py-json.cv_test_reports")
lf_report = cv_test_reports.lanforge_reports
lf_report_pdf = importlib.import_module("py-scripts.lf_report")

attenuator = importlib.import_module("py-scripts.attenuator_serial")
modify = importlib.import_module("py-scripts.lf_atten_mod_test")
sniff_radio = importlib.import_module("py-scripts.lf_sniff_radio")
lf_modify_radio = importlib.import_module("py-scripts.lf_modify_radio")
lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")
set_wifi_radio = importlib.import_module("py-json.LANforge.set_wifi_radio")
set_radio_mode = set_wifi_radio.set_radio_mode

logger = logging.getLogger(__name__)


class Large_Network_Test(Realm):
    def __init__(self,
                 lf_host="192.168.200.161",
                 lf_port=8080,
                 twog_radio=None,
                 fiveg_radio=None,
                 sixg_radio=None,
                 twog_channel=None,
                 fiveg_channel=None,
                 sixg_channel=None,
                 increment=None,
                 csv_outfile="station_mac's_csv.csv",
                 twog_sniff_radio=None,
                 fiveg_sniff_radio=None,
                 sixg_sniff_radio=None,
                 debug_on_=True,
                 ):
        super().__init__(lfclient_host=lf_host,
                         lfclient_port=lf_port)
        self.radio_list = None
        self.channel_list = None
        self.pcap_obj = None
        self.pcap_obj_ = None
        self.pcap_name = None
        self.pcap_name_ = None
        self.lf_host = lf_host
        self.lf_port = lf_port
        self.debug = debug_on_
        self.increment = increment

        self.csv_outfile = csv_outfile
        self.twog_radio = twog_radio
        self.fiveg_radio = fiveg_radio
        self.sixg_radio = sixg_radio

        self.twog_channel = twog_channel
        self.fiveg_channel = fiveg_channel
        self.sixg_channel = sixg_channel

        self.twon_sniff_radio = twog_sniff_radio
        self.fivn_sniff__radio = fiveg_sniff_radio
        self.sixn_sniff_radio = sixg_sniff_radio
        self.cv_test = cv_test_manager.cv_test(lfclient_host=self.lf_host,
                                               lfclient_port=self.lf_port)
        self.report = lf_report_pdf.lf_report(_path='', _results_dir_name="Large_Client_Test",
                                              _output_html=f"large_client_test.html",
                                              _output_pdf=f"lanrge_client_test.pdf")
        self.report_path = self.report.get_path_date_time()

    def load_apply_scenario(self, scenario):  # Loading the existing scenario
        self.cv_test.sync_cv()  # chamber-view sync
        time.sleep(2)
        logger.info(f"Loading Given '{scenario}' scenario...")
        self.cv_test.apply_cv_scenario(scenario)  # Apply scenario
        self.cv_test.show_text_blob(None, None, False)  # Show changes on GUI
        self.cv_test.apply_cv_scenario(scenario)  # Apply scenario
        self.cv_test.build_cv_scenario()  # build scenario
        time.sleep(20)  # waiting for 20 sec to build the existing scenario

    def attenuator_serial(self):  # Fetching the attenuator serial numbers
        obj = attenuator.AttenuatorSerial(lfclient_host=self.lf_host, lfclient_port=self.lf_port)
        val = obj.show()
        return val

    def attenuator_modify(self, serno, idx, val):  # To modify the attenuators
        atten_obj = modify.CreateAttenuator(self.lf_host, self.lf_port, serno, idx, val)
        atten_obj.build()

    def setting_attenuator(self, serial_num,
                           attenuator_mod_values=None):  # Setting attenuation with specified module values
        if attenuator_mod_values:
            if len(serial_num) == len(attenuator_mod_values):
                for serial_number, module_val in zip(serial_num, attenuator_mod_values):
                    logger.info(f"Attenuator Serial Number: {serial_number}")
                    for index, value in enumerate(module_val):
                        logger.info(f"idx = {str(index)}")
                        logger.info(f"val = {value}")
                        self.attenuator_modify(serno=serial_number, idx=str(index), val=value)
            else:
                logger.info("Please specify attenuator module values for each attenuator.")
                exit(0)
        else:  # Default attenuation for all modules is '0' unless specified with 'attenuation_module_values' for attenuators.
            for serial_number in serial_num:
                self.attenuator_modify(serno=serial_number, idx="all", val=0)

    # starting sniffing on radio
    def start_sniffer(self, radio_channel=None, radio=None, test_name="sniff_radio", monitor_name="monitor",
                      duration=60):
        self.pcap_name = test_name + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")).replace(':',
                                                                                                        '-') + ".pcap"
        self.pcap_obj = sniff_radio.SniffRadio(lfclient_host=self.lf_host, lfclient_port=self.lf_port, radio=radio,
                                               channel=radio_channel, monitor_name=monitor_name, channel_bw="20")
        self.pcap_obj.setup(0, 0, 0)
        time.sleep(5)
        self.pcap_obj.monitor.admin_up()
        time.sleep(5)
        logger.info("Starting Sniffer")
        self.pcap_obj.monitor.start_sniff(capname=self.pcap_name, duration_sec=duration)

    def stop_sniffer(self):  # stopping sniffing on radio
        logger.info("Stopping The Sniffer...")
        directory_name = os.path.join(self.report_path, "Pcap's")
        try:
            if not (os.path.exists(directory_name) and os.path.isdir(directory_name)):
                os.makedirs(directory_name)
        except Exception as x:
            logger.info(str(x))
        self.pcap_obj.monitor.admin_down()
        self.pcap_obj.cleanup()
        lf_report.pull_reports(hostname=self.lf_host, port=22, username="lanforge",
                               password="lanforge", report_location="/home/lanforge/" + self.pcap_name,
                               report_dir=f"{self.report_path}/Pcap's/")
        return self.pcap_name

    # starting station side sniffing
    def start_station_side_sniffer(self, station_name=None, duration=60):  # station_name=1.1.sta0001
        sta_name = ""
        if "." in station_name:
            sta_name = station_name.split(".")
        self.pcap_name_ = sta_name[2] + "_" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")).replace(':',
                                                                                                                 '-') + ".pcap"
        self.pcap_obj_ = sniff_radio.SniffRadio(lfclient_host=self.lf_host, lfclient_port=self.lf_port, channel_bw="20")
        self.pcap_obj_.monitor.monitor_name = sta_name[2]
        self.pcap_obj_.monitor.resource = sta_name[1]
        logger.info("Starting Station Side Sniffer...")
        self.pcap_obj_.monitor.start_sniff(capname=self.pcap_name_, duration_sec=duration)

    def stop_station_sniffer(self):  # stopping station side sniffing
        logger.info("Stopping The Station Side Sniffer...")
        directory_name = os.path.join(self.report_path, "Pcap's")
        try:
            if not (os.path.exists(directory_name) and os.path.isdir(directory_name)):
                os.makedirs(directory_name)
        except Exception as x:
            logger.info(str(x))
        lf_report.pull_reports(hostname="192.168.200.175", port=22, username="lanforge", password="lanforge",
                               report_location="/home/lanforge/" + self.pcap_name_,
                               report_dir=f"{self.report_path}/Pcap's/")
        return self.pcap_name_

    def station_list(self, radio_name):  # Fetching the existing station list on specified radio
        sta_list = []
        radio_split = []
        if '.' in radio_name:
            radio_split = radio_name.split(".")
        logger.info(f"Resource:{radio_split[0]}.{radio_split[1]}.")
        response = self.json_get("/port/list?fields=port+type,parent+dev,port")
        if (response is None) or ("interfaces" not in response):
            logger.critical("station_list: incomplete response:")
        # iterating the response
        for x in range(len(response['interfaces'])):
            for k, v in response['interfaces'][x].items():
                if v['parent dev'] == radio_split[2] and v['port type'] == "WIFI-STA":
                    if (radio_split[0] + "." + radio_split[1] + ".") in v['port'] or (
                            radio_split[0] + ".0" + radio_split[1] + ".") in v['port']:
                        sta_list.append(list(response['interfaces'][x].keys())[0])
        logger.info(f"Available Stations List on Radio {radio_name} : \n{sta_list}")
        del response
        return sta_list

    def get_sta_mac(self, sta_list):  # Fetching the Mac address on specified sta_list: ['1.1.sta00501', '1.1.sta00502']
        sta_mac_dict = {}
        for station in sta_list:
            sta_split = station.split(".")
            time.sleep(2)  # waiting for few seconds until loading the scenario
            response = self.json_get(f"/port/{sta_split[0]}/{sta_split[1]}/{sta_split[2]}?fields=mac")
            if (response is None) or ("interface" not in response):
                logger.critical(f"station_mac_list: incomplete response: {response}")
            else:
                for item in response['interface'].values():
                    sta_mac_dict[station] = item
        logger.info(f"Station's Mac Address: {sta_mac_dict}")
        return sta_mac_dict

    def modify_radio(self, radio):  # Setting the flags for specified radio (1.2.wiphy0)
        shelf, resource, radio_name, *nil = self.name_to_eid(eid=radio)
        modify_radio_ = lf_modify_radio.lf_modify_radio(lf_mgr=self.lf_host)
        modify_radio_.set_wifi_radio(_shelf=shelf, _resource=resource, _radio=radio_name,
                                     _flags_value=184614912)

    def station_mac_listing_to_csv(self, sta_mac_dict):
        # Opening CSV file in append mode and write the dictionaries (station with mac address) with one row space
        with open(f'./{self.report_path}/{self.csv_outfile}', 'a', newline='') as csvfile:
            fieldnames = ['Station Names', 'MAC Address']  # Define the column names for the CSV file
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for key, value in sta_mac_dict.items():
                writer.writerow({'Station Names': key, 'MAC Address': value})
            writer.writerow({})  # Adding an empty row

    def setup(self, radio_list, channel_list, sniffer_radio=None, station_sniff=False, band="5g"):
        radio_based_stations = []
        for radio in radio_list:
            # getting station list base on radios
            radio_based_stations += self.station_list(radio_name=radio)
        logger.info(f"Final All Available Stations : \n{radio_based_stations}")

        station_increment_separation = [radio_based_stations[i:i + self.increment] for i in
                                        range(0, len(radio_based_stations), self.increment)]
        logger.info(f"Increment Division For Final Available Stations List: \n{station_increment_separation}")

        # Modifying the radio
        logger.info(f"Setting channel & flags for sniffing radio: {sniffer_radio}")
        self.modify_radio(radio=sniffer_radio)

        # main logic
        for station_list in station_increment_separation:
            # start sniffer on radio
            logger.info(f"Creating Monitor Interface/Sniffer on Radio ({sniffer_radio}).")
            self.start_sniffer(radio_channel=channel_list[0], radio=sniffer_radio.split(".")[2],
                               test_name=f"test_{str(len(station_list))}_{band}_",
                               monitor_name=f"monitor_{band}", duration=60)
            # station admin-up
            for sta in station_list:
                if station_sniff:
                    self.admin_up(port_eid=sta)
                    logger.info(f"Starting Sniffer on Station ({sta}).")
                    time.sleep(1)
                    self.start_station_side_sniffer(station_name=sta, duration=60)
                    self.wait_for_ip(station_list=[sta], timeout_sec=-1)
                    sta_side_pcap_file_name = self.stop_station_sniffer()
                    file_name = f"./{self.report_path}/Pcap's/" + str(sta_side_pcap_file_name)
                    logger.info(
                        f"Attaching the Station Side Pcap File({sta_side_pcap_file_name}) to Report Folder: {file_name}")
                else:
                    self.admin_up(port_eid=sta)
            # wait until station got ip
            if self.wait_for_ip(station_list=station_list, timeout_sec=-1):
                logger.info(f"PASS-IP: All {station_list} stations got IPs.")
            else:
                logger.info(f"FAILED-IP: May be some some stations {station_list} not got the IP...")
            logger.info("Stop Sniffer")
            file_name_ = self.stop_sniffer()
            file_name = f"./{self.report_path}/Pcap's/" + str(file_name_)
            logger.info(f"Attaching the 'Pcap File'({file_name_}) to Report Folder: {file_name}")
            # getting mac addresses for stations
            sta_mac_dict = self.get_sta_mac(sta_list=station_list)
            logger.info(f"Station Mac Address {sta_mac_dict}")
            # appending the station's mac address in a csv file
            self.station_mac_listing_to_csv(sta_mac_dict=sta_mac_dict)


def main():
    parser = argparse.ArgumentParser(prog='large_network_test.py',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog='''
                                     large_network_test.py''',
                                     description=''' 
    CLI: 
         # To run the on only 2G
            python3 large_network_test.py --mgr 192.168.200.161 --scenario eero-script --twog_radio 1.1.phy0 --twog_channel 1 
            --twog_sniff_radio 1.1.phy1 --increment 2 --csv_outfile sta_mac_list.csv --attenuators 1.1.1031 1.1.3104 --attenuator_module_values 0,0,0,0 0,0,0,0
    
         # To run the on only 5G
            python3 large_network_test.py --mgr 192.168.200.161 --scenario eero-script --fiveg_radio 1.1.phy1 --fiveg_channel 36 
            --fiveg_sniff_radio 1.1.phy0 --increment 2 --csv_outfile sta_mac_list.csv --attenuators 1.1.1031 1.1.3104 --attenuator_module_values 0,0,0,0 0,0,0,0
    
        # To run the on only 5G
            python3 large_network_test.py --mgr 192.168.200.161 --scenario eero-script --sixg_radio 1.1.phy1 --sixg_channel 37 
            --sixg_sniff_radio 1.1.phy0 --increment 2 --csv_outfile sta_mac_list.csv --attenuators 1.1.1031 1.1.3104 --attenuator_module_values 0,0,0,0 0,0,0,0
    
        # To run on multiple bands (2g,5g,6g)
            python3 large_network_test.py --mgr 192.168.200.240 --scenario 200-clients-long-run 
               --twog_radio 1.1.wiphy2 1.1.wiphy3 1.1.wiphy4 1.1.wiphy5 
               --fiveg_radio 1.1.wiphy0 1.1.wiphy1 1.3.wiphy0 1.3.wiphy1 1.3.wiphy2 1.3.wiphy3 1.3.wiphy4 
               --sixg_radio 1.4.wiphy3 1.4.wiphy4 1.4.wiphy5 1.4.wiphy6 1.4.wiphy7 
               --twog_channel 1 
               --fiveg_channel 36 
               --sixg_channel 37 
               --twog_sniff_radio 1.4.wiphy0 
               --fiveg_sniff_radio 1.4.wiphy1 
               --sixg_sniff_radio 1.4.wiphy2 
               --increment 10 
               --csv_outfile sta_mac_list.csv 
               --attenuators 1.1.1031 1.1.3104 
               --attenuator_module_values 0,0,0,0 0,0,0,0
    
                                            or
    
            python3 large_network_test.py --mgr 192.168.200.240 --scenario 200-clients-long-run --twog_radio 1.1.wiphy2 1.1.wiphy3 1.1.wiphy4 1.1.wiphy5 
            --fiveg_radio 1.1.wiphy0 1.1.wiphy1 1.3.wiphy0 1.3.wiphy1 1.3.wiphy2 1.3.wiphy3 1.3.wiphy4 
            --sixg_radio 1.4.wiphy3 1.4.wiphy4 1.4.wiphy5 1.4.wiphy6 1.4.wiphy7 --twog_channel 1 --fiveg_channel 36 --sixg_channel 37 
            --twog_sniff_radio 1.4.wiphy0 --fiveg_sniff_radio 1.4.wiphy1 --sixg_sniff_radio 1.4.wiphy2 --increment 10 
            --csv_outfile sta_mac_list.csv --attenuators 1.1.1031 1.1.3104 --attenuator_module_values 0,0,0,0 0,0,0,0
''')
    required = parser.add_argument_group('Required arguments to run large_network_test.py')
    optional = parser.add_argument_group('Optional arguments to run large_network_test.py')

    required.add_argument('--mgr', help='hostname for where LANforge GUI is running',
                          default='192.168.200.161')
    required.add_argument('--mgr_port', help='port LANforge GUI HTTP service is running on',
                          default=8080)
    required.add_argument("--scenario", type=str, help="Name of the scenario that we want to load and apply")
    optional.add_argument('--csv_outfile', type=str, help='--outfile: give the filename with path',
                          default="sta_mac_list.csv")

    optional.add_argument('--twog_radio', help='2g_radios: Radio to sniff', nargs="+")
    optional.add_argument('--fiveg_radio', help='5g_radios: Radio to sniff', nargs="+")
    optional.add_argument('--sixg_radio', help='6g_radios: Radio to sniff', nargs="+")

    optional.add_argument('--twog_sniff_radio', help='2g_radios: Radio to sniff')
    optional.add_argument('--fiveg_sniff_radio', help='5g_radios: Radio to sniff')
    optional.add_argument('--sixg_sniff_radio', help='6g_radios: Radio to sniff')

    optional.add_argument('--twog_channel',
                          help="--channel Set channel on selected Radio, the channel [52, 56 ...]channel will get converted to the control frequency. Must enter Channel",
                          nargs="+", default='1')
    optional.add_argument('--fiveg_channel',
                          help="--channel Set channel on selected Radio, the channel [52, 56 ...]channel will get converted to the control frequency. Must enter Channel",
                          nargs="+", default='36')
    optional.add_argument('--sixg_channel',
                          help="--channel Set channel on selected Radio, the channel [52, 56 ...]channel will get converted to the control frequency. Must enter Channel",
                          nargs="+", default='37')

    optional.add_argument('--increment', type=int, help='Specify the increment number')
    optional.add_argument('--attenuators',
                          help='Use theis flag to define attenuation names. eg: --attenuators 1.1.87 1.1.88', nargs="+")
    optional.add_argument('--attenuator_module_values',
                          help='Specify Attenuator module values in (ddb) for each given attenuator using --attenuators (4 module values for each attenuator)'
                               'eg: --attenuator_module_values 100,200,300,0 450,450,550,550', nargs="+")
    # logging configuration
    optional.add_argument("--lf_logger_config_json",
                          help="--lf_logger_config_json <json file> , json configuration of logger")

    args = parser.parse_args()

    # set up logger
    logger_config = lf_logger_config.lf_logger_config()
    if args.lf_logger_config_json:
        logger_config.lf_logger_config_json = args.lf_logger_config_json
        logger_config.load_lf_logger_config()

    module_values = []
    if len(args.attenuators) == len(args.attenuator_module_values):
        if args.attenuator_module_values:
            try:
                module_values = [list(map(int, atte_mod_values.split(','))) for atte_mod_values in
                                 args.attenuator_module_values]
                logger.info(f"Attenuation Module Value: {module_values}")
                for item in module_values:
                    if len(item) != 4:
                        raise argparse.ArgumentTypeError(
                            "'--attenuator_module_values' input must contain exactly 4 module values.")
            except ValueError:
                raise argparse.ArgumentTypeError("Invalid Input: Module values must be numeric.")
    else:
        raise argparse.ArgumentTypeError(
            "Invalid Input: Please check the given '--attenuator_module_values' values match for given attenuators.")

    obj = Large_Network_Test(lf_host=args.mgr,
                             lf_port=args.mgr_port,
                             twog_radio=args.twog_radio,
                             fiveg_radio=args.fiveg_radio,
                             sixg_radio=args.sixg_radio,
                             csv_outfile=args.csv_outfile,
                             twog_sniff_radio=args.twog_sniff_radio,
                             fiveg_sniff_radio=args.fiveg_sniff_radio,
                             sixg_sniff_radio=args.sixg_sniff_radio,
                             twog_channel=args.twog_channel,
                             fiveg_channel=args.fiveg_channel,
                             sixg_channel=args.sixg_channel,
                             increment=args.increment
                             )
    obj.load_apply_scenario(scenario=args.scenario)

    attenuator_serial_list = []
    if not args.attenuators and not args.attenuator_module_values:
        ser_no = obj.attenuator_serial()
        for attenuator_ in ser_no:
            attenuator_serial_list.append(attenuator_[0])
    else:
        for attenuator_ in args.attenuators:
            attenuator_serial_list.append(attenuator_.split(".")[2])
    logger.info(f"Attenuator List: {attenuator_serial_list}")
    obj.setting_attenuator(serial_num=attenuator_serial_list, attenuator_mod_values=module_values)
    if args.fiveg_radio and args.fiveg_channel:
        obj.setup(radio_list=args.fiveg_radio, channel_list=args.fiveg_channel, sniffer_radio=args.fiveg_sniff_radio,
                  station_sniff=True, band="5g")
    if args.twog_radio and args.twog_channel:
        obj.setup(radio_list=args.twog_radio, channel_list=args.twog_channel, sniffer_radio=args.twog_sniff_radio,
                  station_sniff=False, band="2g")
    if args.sixg_radio and args.sixg_channel:
        obj.setup(radio_list=args.sixg_radio, channel_list=args.sixg_channel, sniffer_radio=args.sixg_sniff_radio,
                  station_sniff=True, band="6g")


if __name__ == "__main__":
    main()