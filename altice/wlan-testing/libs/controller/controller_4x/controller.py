import sys

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

import logging
import importlib
import subprocess
import os

import json
import string
import time
import random

import paramiko
import pytest
from scp import SCPClient
import os
import re
sys.path.append(os.path.join(os.path.abspath("../../../lanforge/lanforge-scripts/")))
logger = logging.getLogger(__name__)
# lf_logger_config = importlib.import_module("py-scripts.lf_logger_config")

with open('lab_info.json', 'r') as f:
    data = json.load(f)


class AController:
    def __init__(self, credentials="", pwd=os.getcwd(), sdk="2.x"):
        self.wifi_country_code_2g = None
        self.bssid_country_code_5g = None
        self.bssid_country_5g = None
        self.wifi_country_2g = None
        print(credentials)
        self.expected_radio = None

        self.expected_security_2G = None
        self.expected_channel_2G = None
        self.expected_band_2G = None
        self.expected_ssid_2G = None
        self.expected_security_5G = None
        self.expected_channel_5G = None
        self.expected_band_5G = None
        self.expected_ssid_5G = None

        self.ap_ssid_2G = None
        self.ap_security_2G = None
        self.ap_channel_2G = None
        self.ap_band_2G = None
        
        self.ap_ssid_5G = None
        self.ap_security_5G = None
        self.ap_channel_5G = None
        self.ap_band_5G = None

        self.bssid_detail_2g = None
        self.bssid_detail_5g = None

        self.serial = credentials['serial']
        self.ap_username = credentials['ap_username']
        self.ap_password = credentials['ap_password']
        self.ap_prompt = credentials['ap_prompt']

        print("IN APNOS: libs/apnos/apnos.py")

        self.owrt_args = "--prompt " + self.ap_prompt + " -s serial --log stdout --user " + self.ap_username + " --passwd " + self.ap_password
        self.sdk = sdk
        if sdk == "2.x":
            self.owrt_args = "--prompt " + self.ap_prompt + self.serial + " -s serial --log stdout --user " + self.ap_username + " --passwd " + self.ap_password
        if credentials is None:
            print("No credentials Given")
            exit()
        self.ip = credentials['ip']  # if mode=1, enter jumphost ip else ap ip address
        self.username = credentials['username']  # if mode=1, enter jumphost username else ap username
        self.password = credentials['password']  # if mode=1, enter jumphost password else ap password
        self.port = credentials['port']  # if mode=1, enter jumphost ssh port else ap ssh port
        self.mode = credentials['jumphost']  # 1 for jumphost, 0 for direct ssh

        if 'mode' in credentials:
            self.type = credentials['mode']

        if self.mode:
            self.tty = credentials['jumphost_tty']  # /dev/ttyAP1
            # kill minicom instance
            client = self.ssh_cli_connect()
            cmd = "pgrep 'minicom' -a"
            stdin, stdout, stderr = client.exec_command(cmd)
            a = str(stdout.read()).split("\\n")
            # print("a : ",a)
            for i in a:
                if i.__contains__("minicom usb0"):
                    temp = i.split("minicom")
                    a = temp[0].replace(" ", "")
                    cmd = "kill " + str(a).replace("b'", "")
                    print(cmd)
                    stdin, stdout, stderr = client.exec_command(cmd)
            cmd = '[ -f ~/cicd-git/ ] && echo "True" || echo "False"'
            stdin, stdout, stderr = client.exec_command(cmd)
            output = str(stdout.read())

            if output.__contains__("False"):
                cmd = 'mkdir ~/cicd-git/'
                stdin, stdout, stderr = client.exec_command(cmd)
            cmd = '[ -f ~/cicd-git/openwrt_ctl.py ] && echo "True" || echo "False"'
            stdin, stdout, stderr = client.exec_command(cmd)
            output = str(stdout.read())
            if output.__contains__("False"):
                print("Copying openwrt_ctl serial control Script...")
                with SCPClient(client.get_transport()) as scp:
                    scp.put(pwd + '/openwrt_ctl.py', '~/cicd-git/openwrt_ctl.py')  # Copy my_file.txt to the server
            cmd = '[ -f ~/cicd-git/openwrt_ctl.py ] && echo "True" || echo "False"'
            stdin, stdout, stderr = client.exec_command(cmd)
            var = str(stdout.read())
            client.close()
            if var.__contains__("True"):
                print("APNOS Serial Setup OK")
            else:
                print("APNOS Serial Setup Fail")

        self.setup_cli_connection()

    def setup_cli_connection(self, cmd="cli"):
        output = self.run_generic_cli_command("cli")
        print("output: ", output)
        try:
            if output[0].strip() != "/cli>":
                if output[1].strip() != "/cli>":
                    print("Adding AP in CLI mode")
                    output = self.run_generic_cli_command(cmd="cli")  # To put AP in cli mode
                    print("AP in CLI mode: ", output)
                    # print("AP in CLI mode: ", output)
        except:
            print("AP already in cli mode")
            # output = self.run_generic_cli_command(cmd="cli")  # To put AP in cli mode
            # print("AP already in CLI mode: ", output)

    def run_generic_cli_command(self, cmd=""):
        print("Command: ",cmd)
        try:
            client = self.ssh_cli_connect()
            cmd = cmd
            if cmd=="cli":
                self.owrt_args = "--prompt " + "root@GEN8" + " -s serial --log stdout --user " + self.ap_username + " --passwd " + self.ap_password
            else:
                self.owrt_args = "--prompt " + "/cli" + " -s serial --log stdout --user " + self.ap_username + " --passwd " + self.ap_password
            print("run generic command:",self.owrt_args)
            print("SELF.mode",self.mode)
            if self.mode:
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t /dev/ttyUSB0 --action " \
                      f"cmd --value \"{cmd}\" "
            #./openwrt_ctl.py --prompt /cli -s serial -l stdout -u admin -p DustBunnyRoundup9# -s serial --tty /dev/ttyUSB0 --action cmd --value /cli
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read()
            print("Run Generic Command Output:",output)
            # print(output.decode('utf-8'))
            # status = output.decode('utf-8').splitlines()
            status = re.sub("[^a-zA-Z_/0-9=> :\\^-]+", "", output.decode('utf-8'))
            # print("status: 122",status)
            status = status.split(" ")
            # print("status: 124",status)
            client.close()
        except Exception as e:
            print(e)
            status = " ** Error ** "
        return status

    def run_generic_ap_prompt_command(self, cmd=""):
        print("Command: ",cmd)
        try:
            client = self.ssh_cli_connect()
            cmd = cmd
            self.owrt_args = "--prompt " + "root@GEN8" + " -s serial --log stdout --user " + self.ap_username + " --passwd " + self.ap_password
            print("run generic command:",self.owrt_args)
            print("SELF.mode",self.mode)
            if self.mode:
                cmd = f"cd ~/cicd-git/ && ./openwrt_ctl.py {self.owrt_args} -t /dev/ttyUSB0 --action " \
                      f"cmd --value \"{cmd}\" "
            #./openwrt_ctl.py --prompt /cli -s serial -l stdout -u admin -p DustBunnyRoundup9# -s serial --tty /dev/ttyUSB0 --action cmd --value /cli
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read()
            print("Run Generic AP Prompt Command Output:",output)
            # print(output.decode('utf-8'))
            # status = output.decode('utf-8').splitlines()
            status = re.sub("[^a-zA-Z_/0-9=> :\\^-]+", "", output.decode('utf-8'))
            # print("status: 122",status)
            status = status.split(" ")
            # print("status: 124",status)
            client.close()
        except Exception as e:
            print(e)
            status = " ** Error ** "
        return status

    # Method to connect AP-CLI/ JUMPHOST-CLI
    def ssh_cli_connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("Connecting to jumphost: %s@%s:%s" % (
            self.username, self.ip, self.port))
        client.connect(self.ip, username=self.username, password=self.password,
                       port=self.port, timeout=10, allow_agent=False, banner_timeout=200)
        return client

    
    # To get all the ssid names
    def get_ap_ssid_name(self, radio="2G"):
        if radio == "2G":
            wifi_index = 0
        else:
            wifi_index = 1
        cmd = f"/wireless/basic/show --wifi-index={wifi_index}"

        ssid_details = self.run_generic_cli_command(cmd)
        # print("ssid_details: 145 ", ssid_details)

        for i in range(len(ssid_details)):
            if ssid_details[i] == "":
                continue

            # print("ssid_details[i]: ",ssid_details[i])
            if ssid_details[i].startswith("wifi-ssid"):
                available_ssid_in_ap = ssid_details[i]
                available_ssid_in_ap = available_ssid_in_ap.split("wifi-ssid:")
                print(f"Available SSID in AP: {available_ssid_in_ap[-1]}")

                if radio == "2G":
                    self.ap_ssid_2G = available_ssid_in_ap
                else:
                    self.ap_ssid_5G = available_ssid_in_ap

                return available_ssid_in_ap[-1]
        return None

    # To get security
    def get_ap_security(self, radio="2G"):
        if radio == "2G":
            wifi_index = 0
        else:
            wifi_index = 1
        cmd = f"/wireless/security/show --wifi-index={wifi_index}"

        ssid_sec_details = self.run_generic_cli_command(cmd)

        for i in range(len(ssid_sec_details)):
            if ssid_sec_details[i] == "":
                continue

            if ssid_sec_details[i].startswith("wifi-wl-auth-mode:"):
                available_sec = ssid_sec_details[i]
                available_sec = available_sec.split("wifi-wl-auth-mode:")
                print(f"Available security in AP: {available_sec[-1]}")
                return available_sec[-1]
        return None

    def set_ap_security(self, radio="2G", security=None, password="something"):

        if radio == "2G":
            wifi_index = 0
        else:
            wifi_index = 1
        if security == "open" or security is None:
            print("============Setting Up OPEN Security============")
            cmd = f"/wireless/security/config --wifi-index={wifi_index} --wifi-sec-choose-interface=0 --wifi-wl-auth-mode=None"
        elif security == "wpa2_personal":
            print("=============Setting Up WPA2 Security============")
            cmd = f"/wireless/security/config --wifi-index={wifi_index} --wifi-sec-choose-interface=0 --wifi-wl-auth-mode=WPA2-Personal --wifi-wl-wpa-passphrase={password}"

        command = self.run_generic_cli_command(cmd)
        # print(f"Configure AP security: {command}")
        return command

    def get_ssid_details_2g(self):
        cmd = str(data["AP_CLI"]["wireless_ssid_details_2g"])
        # print("cmd: 143 ", cmd)
        ssid_details = self.run_generic_cli_command(cmd)
        # print("ssid_details: 145 ", ssid_details)

        for i in range(len(ssid_details)):
            if ssid_details[i] == "":
                continue

            # print("ssid_details[i]: ",ssid_details[i])
            if ssid_details[i].startswith("wifi-ssid"):
                available_ssid_in_ap_2g = ssid_details[i]
                available_ssid_in_ap_2g = available_ssid_in_ap_2g.split("wifi-ssid:")
                return available_ssid_in_ap_2g[-1]
        return None

    def get_ssid_details_5g(self):
        cmd = str(data["AP_CLI"]["wireless_ssid_details_5g"])
        ssid_details = self.run_generic_cli_command(cmd)

        for i in range(len(ssid_details)):
            if ssid_details[i] == "":
                continue

            # print("ssid_details[i]: ", ssid_details[i])
            if ssid_details[i].startswith("wifi-ssid"):
                available_ssid_in_ap_5g = ssid_details[i]
                available_ssid_in_ap_5g = available_ssid_in_ap_5g.split("wifi-ssid:")
                return available_ssid_in_ap_5g[-1]
        return None

    def get_all_ssid_details_2g(self):
        cmd = self.run_generic_cli_command(str(data["AP_CLI"]["wireless_ssid_details_2g"]))
        # ssid_details = self.run_generic_cli_command(cmd)
        return cmd

    def get_all_ssid_details_5g(self):
        cmd = str(data["AP_CLI"]["wireless_ssid_details_5g"])
        ssid_details = self.run_generic_cli_command(cmd)
        return ssid_details

    def set_ssid_2g(self):
        cmd = self.run_generic_cli_command(str(data["AP_CLI"]["wireless_ssid_client_connectivity_2g"]))
        # ssid_details = self.run_generic_cli_command(cmd)
        return cmd

    def set_ssid_5g(self):
        cmd = self.run_generic_cli_command(str(data["AP_CLI"]["wireless_ssid_client_connectivity_5g"]))
        # ssid_details = self.run_generic_cli_command(cmd)
        return cmd

    def get_ssid_sec_details_2g(self):
        cmd = str(data["AP_CLI"]["wireless_sec_show_2g"])
        ssid_sec_details = self.run_generic_cli_command(cmd)

        for i in range(len(ssid_sec_details)):
            if ssid_sec_details[i] == "":
                continue

            if ssid_sec_details[i].startswith("wifi-wl-auth-mode:"):
                available_ssid_sec_in_ap_2g = ssid_sec_details[i]
                available_ssid_sec_in_ap_2g = available_ssid_sec_in_ap_2g.split("wifi-wl-auth-mode:")
                return available_ssid_sec_in_ap_2g[-1]
        return None

    def get_ssid_sec_details_5g(self):
        cmd = str(data["AP_CLI"]["wireless_sec_show_5g"])
        ssid_sec_details = self.run_generic_cli_command(cmd)

        for i in range(len(ssid_sec_details)):
            if ssid_sec_details[i] == "":
                continue

            # print("ssid_sec_details[i]: ", ssid_sec_details[i])
            if ssid_sec_details[i].startswith("wifi-wl-auth-mode:"):
                available_ssid_sec_in_ap_5g = ssid_sec_details[i]
                available_ssid_sec_in_ap_5g = available_ssid_sec_in_ap_5g.split("wifi-wl-auth-mode:")
                return available_ssid_sec_in_ap_5g[-1]
        return None

    def get_all_ssid_sec_details_2g(self):
        cmd = self.run_generic_cli_command(str(data["AP_CLI"]["wireless_sec_show_2g"]))
        # ssid_sec_details = self.run_generic_cli_command(cmd)
        return cmd

    def get_all_ssid_sec_details_5g(self):
        cmd = self.run_generic_cli_command(str(data["AP_CLI"]["wireless_sec_show_5g"]))
        # ssid_sec_details = self.run_generic_cli_command(cmd)
        return cmd

    def set_ssid_sec_2g(self, sec=None):
        if sec == "open":
            cmd = self.run_generic_cli_command(str(data["AP_CLI"]["wireless_ssid_open_config_2g"]))
        elif sec == "wpa2_personal":
            cmd = self.run_generic_cli_command(str(data["AP_CLI"]["wireless_ssid_wpa2_personal_config_2g"]))

        # ssid_details = self.run_generic_cli_command(cmd)
        return cmd

    def set_ssid_sec_5g(self, sec=None):
        if sec == "open":
            cmd = self.run_generic_cli_command(str(data["AP_CLI"]["wireless_ssid_open_config_5g"]))
        elif sec == "wpa2_personal":
            cmd = self.run_generic_cli_command(str(data["AP_CLI"]["wireless_ssid_wpa2_personal_config_5g"]))

        # ssid_details = self.run_generic_cli_command(cmd)
        return cmd

    def set_channel_band_2g(self, channel="AUTO", band="20"):
        # print(f"band : {band}, channel : {channel}")
        if band == "20":
            ap_cli_band = 0
            # print(f"band : {band}, channel : {ap_cli_band}")
            cmd = f"/wireless/advance/config --wifi-channel={channel} --wifi-bandwidth={ap_cli_band} --wifi-index=0"
            print(f" ------------------ cmd : {cmd} ------------------")
            # print("cmd: 254: ", cmd)
            cmd = self.run_generic_cli_command(str(cmd))
            return cmd
        elif band == "40":
            ap_cli_band = 1
            cmd = f"/wireless/advance/config --wifi-channel={channel} --wifi-bandwidth={ap_cli_band} --wifi-index=0"
            cmd = self.run_generic_cli_command(str(cmd))
            return cmd
        elif band == "80":
            ap_cli_band = 1
            cmd = f"/wireless/advance/config --wifi-channel={channel} --wifi-bandwidth={ap_cli_band} --wifi-index=0"
            cmd = self.run_generic_cli_command(str(cmd))
        else:
            cmd = None
            return cmd

    def set_channel_band_5g(self, channel="AUTO", band="20"):
        if band == "20":
            ap_cli_band = 0
            cmd = f"/wireless/advance/config --wifi-channel={channel} --wifi-bandwidth={ap_cli_band} --wifi-index=1"
            cmd = self.run_generic_cli_command(str(cmd))
            return cmd
        elif band == "40":
            ap_cli_band = 1
            cmd = f"/wireless/advance/config --wifi-channel={channel} --wifi-bandwidth={ap_cli_band} --wifi-index=1"
            cmd = self.run_generic_cli_command(str(cmd))
            return cmd
        elif band == "80":
            ap_cli_band = 2
            cmd = f"/wireless/advance/config --wifi-channel={channel} --wifi-bandwidth={ap_cli_band} --wifi-index=1"
            cmd = self.run_generic_cli_command(str(cmd))
            return cmd
        elif band == "160":
            ap_cli_band = 3
            cmd = f"/wireless/advance/config --wifi-channel={channel} --wifi-bandwidth={ap_cli_band} --wifi-index=1"
            cmd = self.run_generic_cli_command(str(cmd))
            return cmd
        else:
            cmd = None
            return cmd

    def get_channel_band_2g(self):
        cmd = "/wireless/advance/show --wifi-index=0"
        channel_details_2g = self.run_generic_cli_command(str(cmd))

        for i in range(len(channel_details_2g)):
            if channel_details_2g[i] == "":
                continue

            # print("ssid_sec_details[i]: ", ssid_sec_details[i])
            if channel_details_2g[i].startswith("wifi-channel:"):
                available_channel_2g = channel_details_2g[i]
                available_channel_2g = available_channel_2g.split("wifi-channel:")
                return available_channel_2g[-1]
        return None

    def get_channel_band_5g(self):
        cmd = "/wireless/advance/show --wifi-index=1"
        channel_details_5g = self.run_generic_cli_command(str(cmd))

        for i in range(len(channel_details_5g)):
            if channel_details_5g[i] == "":
                continue

            # print("ssid_sec_details[i]: ", ssid_sec_details[i])
            if channel_details_5g[i].startswith("wifi-channel:"):
                available_channel_5g = channel_details_5g[i]
                available_channel_5g = available_channel_5g.split("wifi-channel:")
                return available_channel_5g[-1]
        return None

    def set_ssid(self, radio="2G", ssid="altice"):
        print("Set SSID")
        if radio == "2G":
            wifi_index = 0;
        else:
            wifi_index = 1;
        command = f"/wireless/basic/config --wifi-index={wifi_index} --wifi-ssid={ssid}"
        print(f"setting ssid : cmd: {command}")
        cmd = self.run_generic_cli_command(command)
        print(f"Result : {cmd}")
        return cmd

    def get_channel_band(self, radio="2G"):
        print("Get Channel")
        if radio == "2G":
            wifi_index = 0
        else:
            wifi_index = 1

        cmd = f"/wireless/advance/show --wifi-index={wifi_index}"
        channel_details = self.run_generic_cli_command(str(cmd))
        print(f"current channel details: {channel_details}")

        for i in range(len(channel_details)):
            if channel_details[i] == "":
                continue

            if channel_details[i].startswith("wifi-channel:"):
                available_channel = channel_details[i]
                available_channel = available_channel.split("wifi-channel:")
                print(f"current ap channel: {available_channel[-1]}")
                return available_channel[-1]
        return None

    def set_channel_band(self, radio="2G", band="20", channel="AUTO"):
        print("Set Channel")
        if radio == "2G":
            wifi_index = 0
            if channel == "11":
                print(
                    "************************************Channel Requested is 11************************************")
                if band == "20":
                    cmd = f"quit"
                    cmd = self.run_generic_cli_command(str(cmd))
                    cmd = f"dmcli eRT setv Device.WiFi.Radio.1.AutoChannelEnable bool 0 ; dmcli eRT setv Device.WiFi.Radio.1.Channel uint {channel} ; dmcli eRT setv Device.WiFi.Radio.2.OperatingChannelBandwidth string 20MHz ; nvram commit ; nvram restart"
                    # print("cmd: 447: ", cmd)
                    cmd = self.run_generic_ap_prompt_command(str(cmd))
                    # print(f" ------------------ after command : {cmd} ------------------")
                    return cmd

                elif band == "40":
                    cmd = f"quit"
                    cmd = self.run_generic_cli_command(str(cmd))
                    cmd = f"dmcli eRT setv Device.WiFi.Radio.1.AutoChannelEnable bool 0 ; dmcli eRT setv Device.WiFi.Radio.1.Channel uint {channel} ; dmcli eRT setv Device.WiFi.Radio.2.OperatingChannelBandwidth string 40MHz ; nvram commit ; nvram restart"
                    # print("cmd: 454: ", cmd)
                    cmd = self.run_generic_ap_prompt_command(str(cmd))
                    # print(f" 455 ------------------ after command : {cmd} ------------------")
                    return cmd
                else:
                    print(
                        "/************************************/ Channel passing failed /************************************/")
                    cmd = None
                    return cmd
            else:
                if band == "20":
                    ap_cli_band = 0
                    print(f"band : {band}, ap_cli_channel : {ap_cli_band}")
                    cmd = f"/wireless/advance/config --wifi-channel={channel} --wifi-bandwidth={ap_cli_band} --wifi-index={wifi_index}"
                    # print("cmd: 447: ", cmd)
                    cmd = self.run_generic_cli_command(str(cmd))
                    # print(f" ------------------ after command : {cmd} ------------------")
                    return cmd
                elif band == "40":
                    ap_cli_band = 1
                    print(f"band : {band}, ap_cli_channel : {ap_cli_band}")
                    cmd = f"/wireless/advance/config --wifi-channel={channel} --wifi-bandwidth={ap_cli_band} --wifi-index={wifi_index}"
                    # print("cmd: 454: ", cmd)
                    cmd = self.run_generic_cli_command(str(cmd))
                    # print(f" 455 ------------------ after command : {cmd} ------------------")
                    return cmd
                elif band == "80":
                    ap_cli_band = 2
                    print(f"band : {band}, ap_cli_channel : {ap_cli_band}")
                    cmd = f"/wireless/advance/config --wifi-channel={channel} --wifi-bandwidth={ap_cli_band} --wifi-index={wifi_index}"
                    # print("cmd: 454: ", cmd)
                    cmd = self.run_generic_cli_command(str(cmd))
                    # print(f" 455 ------------------ after command : {cmd} ------------------")
                    return cmd
                else:
                    print(
                        "/************************************/ Channel passing failed /************************************/")
                    cmd = None
                    return cmd
        else:
            wifi_index = 1
            if channel == "149":
                print(
                    "************************************Channel Requested is 149************************************")
                if band == "20":
                    ap_cli_band = 0
                    print(f"band : {band}, ap_cli_channel : {ap_cli_band}")
                    cmd = f"quit"
                    cmd = self.run_generic_cli_command(str(cmd))
                    cmd = f"dmcli eRT setv Device.WiFi.Radio.2.AutoChannelEnable bool 0 ; dmcli eRT setv Device.WiFi.Radio.2.Channel uint 149 ; dmcli eRT setv Device.WiFi.Radio.2.OperatingChannelBandwidth string 20MHz ; nvram commit ; nvram restart"
                    # print("cmd: 447: ", cmd)
                    cmd = self.run_generic_ap_prompt_command(str(cmd))
                    # print(f" ------------------ after command : {cmd} ------------------")
                    return cmd

                elif band == "40":
                    ap_cli_band = 1
                    print(f"band : {band}, ap_cli_channel : {ap_cli_band}")
                    cmd = f"quit"
                    cmd = self.run_generic_cli_command(str(cmd))
                    cmd = f"dmcli eRT setv Device.WiFi.Radio.2.AutoChannelEnable bool 0 ; dmcli eRT setv Device.WiFi.Radio.2.Channel uint 149 ; dmcli eRT setv Device.WiFi.Radio.2.OperatingChannelBandwidth string 40MHz ; nvram commit ; nvram restart"
                    # print("cmd: 454: ", cmd)
                    cmd = self.run_generic_ap_prompt_command(str(cmd))
                    # print(f" 455 ------------------ after command : {cmd} ------------------")
                    return cmd
                elif band == "80":
                    ap_cli_band = 2
                    print(f"band : {band}, ap_cli_channel : {ap_cli_band}")
                    cmd = f"quit"
                    cmd = self.run_generic_cli_command(str(cmd))
                    cmd = f"dmcli eRT setv Device.WiFi.Radio.2.AutoChannelEnable bool 0 ; dmcli eRT setv Device.WiFi.Radio.2.Channel uint 149 ; dmcli eRT setv Device.WiFi.Radio.2.OperatingChannelBandwidth string 80MHz ; nvram commit ; nvram restart"
                    # print("cmd: 454: ", cmd)
                    cmd = self.run_generic_ap_prompt_command(str(cmd))
                    # print(f" 455 ------------------ after command : {cmd} ------------------")
                    return cmd
                else:
                    print(
                        "/************************************/ Channel passing failed /************************************/")
                    cmd = None
                    return cmd
            else:
                if band == "20":
                    ap_cli_band = 0
                    print(f"band : {band}, ap_cli_channel : {ap_cli_band}")
                    cmd = f"/wireless/advance/config --wifi-channel={channel} --wifi-bandwidth={ap_cli_band} --wifi-index={wifi_index}"
                    # print("cmd: 447: ", cmd)
                    cmd = self.run_generic_cli_command(str(cmd))
                    # print(f" ------------------ after command : {cmd} ------------------")
                    return cmd
                elif band == "40":
                    ap_cli_band = 1
                    print(f"band : {band}, ap_cli_channel : {ap_cli_band}")
                    cmd = f"/wireless/advance/config --wifi-channel={channel} --wifi-bandwidth={ap_cli_band} --wifi-index={wifi_index}"
                    # print("cmd: 454: ", cmd)
                    cmd = self.run_generic_cli_command(str(cmd))
                    # print(f" 455 ------------------ after command : {cmd} ------------------")
                    return cmd
                elif band == "80":
                    ap_cli_band = 2
                    print(f"band : {band}, ap_cli_channel : {ap_cli_band}")
                    cmd = f"/wireless/advance/config --wifi-channel={channel} --wifi-bandwidth={ap_cli_band} --wifi-index={wifi_index}"
                    # print("cmd: 454: ", cmd)
                    cmd = self.run_generic_cli_command(str(cmd))
                    # print(f" 455 ------------------ after command : {cmd} ------------------")
                    return cmd
                else:
                    print(
                        "/************************************/ Channel passing failed /************************************/")
                    cmd = None
                    return cmd


    def check_and_set_ap_channel(self, radio="2G", band="20", channel="AUTO"):
        # print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",self.get_channel_band(radio=radio))
        print("Desired Channel",channel)
        # p=type(self.get_channel_band(radio=radio))
        channel_from_ap = self.get_channel_band(radio=radio)
        channel_from_ap.split("wifi-channel:")
        print("Current Channel",channel_from_ap)
        if channel != channel_from_ap:
            print("Expected channel from AP and Current Channel of AP mismatched"+"\nDesired Channel"+str(channel)+" not equals to Current Channel:"+str(channel_from_ap))
            print("Going to set desired channel in AP")
            self.set_channel_band(radio=str(radio), band=str(band), channel=str(channel))
            if channel==149 or channel==11:
                self.setup_cli_connection(cmd="cli")
                self.get_channel_band(radio=radio)
            else:
                self.get_channel_band(radio=radio)
        # self.get_channel_band(radio=radio)

    def check_and_set_ssid_sec(self, radio="2G", ssid="client_altice", security="open", password="something"):
        self.get_all_ssid_detail(radio=radio)
        print(f"ssid: 481: {ssid}, self.ap_ssid: {self.ap_ssid_5G}")

        if radio == "2G":
            if ssid != self.ap_ssid_2G:
                print("Setting 2g SSID")
                self.set_ssid(radio=radio, ssid=ssid)
            else:
                print("Same named SSID already Exists")
        if radio == "5G":
            if ssid != self.ap_ssid_5G:
                print("Setting 5g SSID")
                self.set_ssid(radio=radio, ssid=ssid)
            else:
                print("Same named SSID already Exists")
        if radio == "2G" or radio == "5G":
            print("Setting SSID SECURITY")
            self.set_ap_security(radio=radio, security=security)


        # sec = self.get_ap_security(radio=radio)
        # if sec == "WPA2-Personal":
        #     ap_security = "wpa2_personal"
        # else:
        #     ap_security = "open"
        # if security != ap_security:
        #     sec_details = self.set_ap_security(radio=radio, security=security, password=password)

        # if ssid != self.get_ap_ssid_name(radio=radio):
        #     ssid_details = self.set_ssid(radio=radio, ssid=ssid)
        # if security != self.get_ap_security(radio=radio):
        #     sec_details = self.set_ap_security(radio=radio, security=security)

    def check_bssid_2g(self):
        return self.bssid_detail_2g

    def check_bssid_5g(self):
        return self.bssid_detail_5g

    def get_all_ssid_detail(self, radio="2G"):
        if radio == "2G":
            wifi_index = 0
        else:
            wifi_index = 1
        cmd = f"/wireless/basic/show --wifi-index={wifi_index}"

        ssid_details = self.run_generic_cli_command(cmd)
        # print("ssid_details: 145 ", ssid_details)

        for i in range(len(ssid_details)):
            if ssid_details[i] == "":
                continue
            elif ssid_details[i].startswith("wifi-ssid"):
                available_ssid_in_ap = ssid_details[i]
                available_ssid_in_ap = available_ssid_in_ap.split("wifi-ssid:")
                print(f"Available SSID in AP: {available_ssid_in_ap[-1]}")
                if radio == "2G":
                    self.ap_ssid_2G = available_ssid_in_ap[-1]
                    print(f"**************** ap_ssid_2g **************** : {self.ap_ssid_2G}")
                else:
                    self.ap_ssid_5G = available_ssid_in_ap[-1]
                    print(f"**************** ap_ssid_5g **************** : {self.ap_ssid_5G}")

            elif ssid_details[i].startswith("BSSID:"):
                available_bssid_in_ap = ssid_details[i]
                available_bssid_in_ap = available_bssid_in_ap.split("BSSID:")
                print(f"Available BSSID in AP {radio}: {available_bssid_in_ap[-1]}")
                if wifi_index == 0:
                    self.bssid_detail_2g = available_bssid_in_ap[-1]
                else:
                    self.bssid_detail_5g = available_bssid_in_ap[-1]

            elif ssid_details[i].startswith("wifi-country:"):
                available_country_in_ap = ssid_details[i]
                available_country_in_ap = available_country_in_ap.split("wifi-country:")
                print(f"wifi-country in AP {radio}: {available_country_in_ap[-1]}")

                if wifi_index == 0:
                    self.wifi_country_2g = available_country_in_ap[-1]
                else:
                    self.bssid_country_5g = available_country_in_ap[-1]

            elif ssid_details[i].startswith("wifi-country-code:"):
                available_country_code_in_ap = ssid_details[i]
                available_country_code_in_ap = available_country_code_in_ap.split("wifi-country-code:")
                print(f"wifi-country code in AP {radio}: {available_country_code_in_ap[-1]}")

                if wifi_index == 0:
                    self.wifi_country_code_2g = available_country_code_in_ap[-1]
                else:
                    self.bssid_country_code_5g = available_country_code_in_ap[-1]

            elif ssid_details[i].startswith("wifi-max-clients:"):
                available_max_clients_in_ap = ssid_details[i]
                available_max_clients_in_ap = available_max_clients_in_ap.split("wifi-country-code:")
                print(f"Max virtual client limit in AP {radio}: {available_max_clients_in_ap[-1]}")

                if wifi_index == 0:
                    self.wifi_country_code_2g = available_max_clients_in_ap[-1]

                else:
                    self.bssid_country_code_5g = available_max_clients_in_ap[-1]
            elif ssid_details[i].startswith("guest-interface:"):
                return
            else:
                pass

        return None

if __name__ == '__main__':
    obj = AController(data["CONFIGURATION"]["local-01"]["access_point"][0], pwd="../../apnos", sdk="2.x")
    obj.setup_cli_connection()
    print(obj.get_ssid_sec_details_2g())
    print(obj.get_ssid_sec_details_5g())
    print(obj.get_ssid_details_2g())
    print(obj.get_ssid_details_5g())


# if __name__ == '__main__':
# controller = {
#     "url": "https://172.16.0.2",
#     "ip": "localhost",
#     "username": "admin",
#     "password": "Cisco123",
#     "ssh_port": "8888",
#     "series": "9800",
#     "prompt": "WLC2",
#     "band": ["5g"],
#     "scheme": "ssh"
# }
# access_point = [
#     {
#         "ap_name": "AP687D.B45C.1D1C",
#         "chamber": "C1",
#         "model": "cisco9136i",
#         "mode": "wifi6",
#         "serial": "FOC25322JQP",
#         "tag_policy": "RM204-TB2-AP1",
#         "policy_profile": "default-policy-profile",
#         "ssid": {
#             "2g-ssid": "candela2ghz",
#             "5g-ssid": "open-wlan",
#             "6g-ssid": "candela6ghz",
#             "2g-password": "hello123",
#             "5g-password": "[BLANK]",
#             "6g-password": "hello123",
#             "2g-encryption": "WPA2",
#             "5g-encryption": "open",
#             "6g-encryption": "WPA3",
#             "2g-bssid": "68:7d:b4:5f:5c:31 ",
#             "5g-bssid": "68:7d:b4:5f:5c:3c",
#             "6g-bssid": "68:7d:b4:5f:5c:38"
#         },
#
#         "ip": "192.168.100.109",
#         "username": "lanforge",
#         "password": "lanforge",
#         "port": 22,
#         "jumphost_tty": "/dev/ttyAP1",
#         "version": "17.7.1.11"
#     }]
# obj = AController(data["CONFIGURATION"]["local-01"]["access_point"][0], pwd="../libs/apnos/", sdk="2.x")
# obj.setup_cli_connection()
# print(obj.get_ssid_sec_details_2g())
# print(obj.get_ssid_sec_details_5g())
# print(obj.get_ssid_details_2g())
# print(obj.get_ssid_details_5g())
# x = obj.get_all_ssids_from_controller()
# print(x)
# obj.no_logging_console()
# obj.line_console()
# obj.delete_wlan()
# obj.no_logging_console()
# obj.get_ssids()
# obj.delete_wlan()
# obj.create_wlan_open()
# obj.get_ssids()
# obj.get_number_of_wlan_present()

# if __name__ == '__main__':
#     logger_config = lf_logger_config.lf_logger_config()
#     series = importlib.import_module("cc_module_9800_3504")
#     cc = series.create_controller_series_object(
#             scheme="ssh",
#             dest="localhost",
#             user="admin",
#             passwd="xyz",
#             prompt="WLC2",
#             series="9800",
#             ap="AP2C57.4152.385C",
#             port="8888",
#             band="5g",
#             timeout="10")
#     cc.show_ap_config_slots()
#     cc.show_wlan_summary()
#
