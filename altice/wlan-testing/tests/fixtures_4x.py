import allure
import pytest
import os
import sys

""" Environment Paths """
if "libs" not in sys.path:
    sys.path.append(f'../libs')
for folder in 'py-json', 'py-scripts':
    if folder not in sys.path:
        sys.path.append(f'../lanforge/lanforge-scripts/{folder}')

sys.path.append(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)
sys.path.append(f"../lanforge/lanforge-scripts/py-scripts/tip-cicd-sanity")

sys.path.append(f'../libs')
sys.path.append(f'../libs/lanforge/')
sys.path.append(f'../lanforge/lanforge-scripts')

from LANforge.LFUtils import *


# if 'py-json' not in sys.path:
#     sys.path.append('../py-scripts')
# from controller.controller_4x.controller import AController


class Fixtures_4x:

    def __init__(self, configuration={}, run_lf=False, al_1=False):
        self.lab_info = configuration
        self.run_lf = run_lf
        self.al_1 = al_1
        # print(self.lab_info)
        print("al.1")
        self.controller_obj = ""

    def setup_profiles(self, request, param, run_lf, instantiate_profile, get_configuration, get_markers,
                       testbed, lf_tools, get_all_markers):
        table1 = []
        #     obj = AController(data["CONFIGURATION"]["local-01"]["access_point"][0], pwd="../libs/apnos/", sdk="2.x")

        instantiate_profile_obj = instantiate_profile(get_configuration['access_point'][0],
                                                      pwd="./libs/apnos/",
                                                      sdk="2.x")

        if run_lf:
            return 0

        # print("check params")
        # gives parameter value of setup_params_general
        parameter = dict(param)
        print("parameter", parameter)

        test_cases = {}
        profile_data = {}
        var = ""
        list_key = list(parameter.keys())

        if parameter['mode'] not in ["NAT"]:
            print("Invalid Mode: ", parameter['mode'])
            return test_cases

        profile_data["ssid"] = {}
        lf_dut_data = []

        for i in parameter["ssid_modes"]:
            profile_data["ssid"][i] = []
            for j in range(len(parameter["ssid_modes"][i])):
                data = parameter["ssid_modes"][i][j]
                profile_data["ssid"][i].append(data)
        lf_dut_data = []

        for mode in profile_data['ssid']:
            if mode == "open":
                for j in profile_data["ssid"][mode]:
                    if mode in get_markers.keys() and get_markers[mode]:
                        try:

                            if get_all_markers.__contains__("twog"):
                                lf_dut_data.append(j)
                                instantiate_profile_obj.check_and_set_ssid_sec("2G", profile_data["ssid"][mode][0][
                                    "ssid_name"], mode, profile_data["ssid"][mode][0]["security_key"])
                                j["appliedRadios"] = ["2G"]

                            else:
                                lf_dut_data.append(j)
                                instantiate_profile_obj.check_and_set_ssid_sec("5G", profile_data["ssid"][mode][0][
                                    "ssid_name"], mode, profile_data["ssid"][mode][0]["security_key"])
                                j["appliedRadios"] = ["5G"]

                            j['security'] = 'none'
                            test_cases["open"] = True
                            creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j)

                        except Exception as e:
                            print(e)
                            test_cases["open"] = False
            if mode == "wpa2_personal":
                for j in profile_data["ssid"][mode]:
                    if mode in get_markers.keys() and get_markers[mode]:

                        try:
                            if get_all_markers.__contains__("twog"):
                                lf_dut_data.append(j)
                                print("--------------------------- 110 --------------------------- ")
                                instantiate_profile_obj.check_and_set_ssid_sec("2G", profile_data["ssid"][mode][0][
                                    "ssid_name"], mode ,profile_data["ssid"][mode][0]["security_key"])
                                j["appliedRadios"] = ["2G"]

                            else:
                                lf_dut_data.append(j)
                                print("--------------------------- 116 --------------------------- ")
                                instantiate_profile_obj.check_and_set_ssid_sec("5G", profile_data["ssid"][mode][0][
                                    "ssid_name"], mode, profile_data["ssid"][mode][0]["security_key"])
                                j["appliedRadios"] = ["5G"]


                            j['security'] = 'wpa2'
                            test_cases["wpa2_personal"] = True
                            creates_profile = instantiate_profile_obj.add_ssid(ssid_data=j)

                        except Exception as e:
                            print(e)
                            test_cases["wpa2_personal"] = False

        bssid_list_2g = []
        bssid_list_5g = []
        ssid_data_list = []

        for ap_name in range(len(get_configuration['access_point'])):

            ssid_data = []
            try:
                idx_mapping = {}
                bssid = ""
                for interface in range(len(lf_dut_data)):

                    if get_all_markers.__contains__("twog") and lf_dut_data[interface]['appliedRadios'][0] == '2G':
                        bssid = instantiate_profile_obj.check_bssid_2g()
                        ssid = ["ssid_idx=" + str(0) +
                                " ssid=" + lf_dut_data[interface]['ssid_name'] +
                                " security=" + lf_dut_data[interface]['security'] +
                                " password=" + lf_dut_data[interface]['security_key'] +
                                " bssid=" + str(bssid)
                                ]

                        # if lf_dut_data[interface]['security'] == "psk2":
                        #     lf_dut_data[interface]['security'] = "WPA2"

                        ssid_data.append(ssid)

                    if get_all_markers.__contains__("fiveg") and lf_dut_data[interface]['appliedRadios'][0] == '5G':
                        bssid = instantiate_profile_obj.check_bssid_5g()
                        ssid = ["ssid_idx=" + str(1) +
                                " ssid=" + lf_dut_data[interface]['ssid_name'] +
                                " security=" + lf_dut_data[interface]['security'] +
                                " password=" + lf_dut_data[interface]['security_key'] +
                                " bssid=" + str(bssid)
                                ]
                        # if lf_dut_data[interface]['security'] == "psk2":
                        #     lf_dut_data[interface]['security'] = "WPA2"

                        ssid_data.append(ssid)

            except Exception as e:
                print(e)
                pass

            ssid_data_list.append(ssid_data)
        # ssid_data = [[['ssid_idx=0 ssid=ssid_wpa2_2g security=WPA2 password=something bssid=68:7d:b4:5f:5c:30'],
        #               ['ssid_idx=1 ssid=ssid_wpa2_5g security=WPA2 password=something bssid=68:7d:b4:5f:5c:3e']],
        #              [['ssid_idx=0 ssid=ssid_wpa2_2g security=WPA2 password=something bssid=14:16:9d:53:58:c0'],
        #               ['ssid_idx=1 ssid=ssid_wpa2_5g security=WPA2 password=something bssid=14:16:9d:53:58:ce']]]
        lf_tools.create_non_meh_dut(ssid_data=ssid_data_list)
