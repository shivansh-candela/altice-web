# import os
# import pytest
# import allure
#
# pytestmark = [pytest.mark.country_code, pytest.mark.nat, pytest.mark.open, pytest.mark.united_states,
#               pytest.mark.bandwidth_20mhz, pytest.mark.al, pytest.mark.tcp, pytest.mark.wifi_capacity,
#               pytest.mark.download, pytest.mark.tcp_download, pytest.mark.wifi_capacity_single_client,
#               pytest.mark.wifi_capacity_wpa2_20mhz_all_channels_single_client_download_1gbps,
#               pytest.mark.throughput_wpa2_20mhz_all_channels_single_client_download_1gbps, pytest.mark.fiveg]
#
# setup_params_general = {
#     "mode": "NAT",
#     "ssid_modes": {
#         "open": [
#             {"ssid_name": "client_connectivity_al", "appliedRadios": ["2G"], "security_key": "something"},
#             {"ssid_name": "client_connectivity_al", "appliedRadios": ["5G"], "security_key": "something"}
#         ]
#     },
#
#     "rf-5G-1": {
#         "5G":
#             {'band': '5G',
#              'country': 'US',
#              "channel-mode": "VHT",
#              'channel-width': 20,
#              "channel": 36}
#     },
#     "rf-5G-2": {
#         "5G":
#             {'band': '5G',
#              'country': 'US',
#              'channel-mode': 'VHT',
#              'channel-width': 20,
#              "channel": 40}
#     },
#     "rf-5G-3": {
#         "5G":
#             {'band': '5G',
#              'country': 'US',
#              'channel-mode': 'VHT',
#              'channel-width': 20,
#              "channel": 44}
#     },
#     "rf-5G-4": {
#         "5G":
#             {'band': '5G',
#              'country': 'US',
#              'channel-mode': 'VHT',
#              'channel-width': 20,
#              "channel": 48}
#     },
#     "rf-5G-5": {
#         "5G":
#             {'band': '5G',
#              'country': 'US',
#              'channel-mode': 'VHT',
#              'channel-width': 20,
#              "channel": 149}
#     },
#     "rf-5G-6": {
#         "5G":
#             {'band': '5G',
#              'country': 'US',
#              'channel-mode': 'VHT',
#              'channel-width': 20,
#              "channel": 153}
#     },
#     "rf-5G-7": {
#         "5G":
#             {'band': '5G',
#              'country': 'US',
#              'channel-mode': 'VHT',
#              'channel-width': 20,
#              "channel": 157}
#     },
#     "rf-5G-8": {
#         "5G":
#             {'band': '5G',
#              'country': 'US',
#              'channel-mode': 'VHT',
#              'channel-width': 20,
#              "channel": 161}
#     },
#     "rf-5G-9": {
#         "5G":
#             {'band': '5G',
#              'country': 'US',
#              'channel-mode': 'VHT',
#              'channel-width': 20,
#              "channel": 165}
#     },
#     "radius": False
# }
#
# #
# @allure.feature("NAT MODE CLIENT CONNECTIVITY")
# @pytest.mark.parametrize(
#     'setup_profiles',
#     [setup_params_general],
#     indirect=True,
#     scope="class"
# )
# @pytest.mark.usefixtures("setup_profiles")
# class TestCountryUS20Mhz5G(object):
#
#     @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
#     @pytest.mark.open
#     @pytest.mark.twentyMhz
#     @pytest.mark.fiveg
#     @pytest.mark.channel36
#     def test_client_nat_wpa2_chn36_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
#                                                  lf_test, update_report,
#                                                  station_names_fiveg, lf_tools,
#                                                  test_cases, testbed, al_1, get_configuration):
#         """
#            pytest -m "country_code and twentyMhz and open and fiveg and channel1"
#         """
#         profile_data = setup_params_general["ssid_modes"]["open"][1]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         security = "open"
#         mode = "NAT"
#         band = "fiveg"
#         vlan = 1
#         channel = setup_params_general['rf-5G-1']['5G']['channel']
#         channel_width = setup_params_general['rf-5G-1']['5G']['channel-width']
#
#         obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
#         obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)
#
#         lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
#         # lf_tools.add_stations(band="ax", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
#         lf_tools.Chamber_View()
#         wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
#                                         download_rate="1Gbps", batch_size="1",
#                                         upload_rate="0", protocol="TCP-IPv4", duration="60000")
#
#         report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
#
#         lf_tools.attach_report_graphs(report_name=report_name)
#         print("Test Completed... Cleaning up Stations")
#         # lf_tools.reset_scenario()
#         assert True
#
#     @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
#     @pytest.mark.open
#     @pytest.mark.twentyMhz
#     @pytest.mark.fiveg
#     @pytest.mark.channel40
#     def test_client_nat_wpa2_chn40_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
#                                                  lf_test, update_report,
#                                                  station_names_fiveg, lf_tools,
#                                                  test_cases, testbed, al_1, get_configuration):
#         """
#            pytest -m "country_code and twentyMhz and open and fiveg and channel2"
#         """
#         profile_data = setup_params_general["ssid_modes"]["open"][1]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         security = "open"
#         mode = "NAT"
#         band = "fiveg"
#         vlan = 1
#         channel = setup_params_general['rf-5G-2']['5G']['channel']
#         channel_width = setup_params_general['rf-5G-2']['5G']['channel-width']
#
#         obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
#         obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)
#
#         lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
#         # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
#         lf_tools.Chamber_View()
#         wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
#                                         download_rate="1Gbps", batch_size="1",
#                                         upload_rate="0", protocol="TCP-IPv4", duration="60000")
#
#         report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
#
#         lf_tools.attach_report_graphs(report_name=report_name)
#         print("Test Completed... Cleaning up Stations")
#         lf_tools.reset_scenario()
#         assert True
#
#     @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
#     @pytest.mark.open
#     @pytest.mark.twentyMhz
#     @pytest.mark.fiveg
#     @pytest.mark.channel44
#     def test_client_nat_wpa2_chn44_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
#                                                  lf_test, update_report,
#                                                  station_names_fiveg, lf_tools,
#                                                  test_cases, testbed, al_1, get_configuration):
#         """
#            pytest -m "country_code and twentyMhz and open and fiveg and channel3"
#         """
#         profile_data = setup_params_general["ssid_modes"]["open"][1]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         security = "open"
#         mode = "NAT"
#         band = "fiveg"
#         vlan = 1
#         channel = setup_params_general['rf-5G-3']['5G']['channel']
#         channel_width = setup_params_general['rf-5G-3']['5G']['channel-width']
#
#         obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
#         obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)
#
#         lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
#         # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
#         lf_tools.Chamber_View()
#         wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
#                                         download_rate="1Gbps", batch_size="1",
#                                         upload_rate="0", protocol="TCP-IPv4", duration="60000")
#
#         report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
#
#         lf_tools.attach_report_graphs(report_name=report_name)
#         print("Test Completed... Cleaning up Stations")
#         lf_tools.reset_scenario()
#         assert True
#
#     @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
#     @pytest.mark.open
#     @pytest.mark.twentyMhz
#     @pytest.mark.fiveg
#     @pytest.mark.channel48
#     def test_client_nat_wpa2_chn48_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
#                                                  lf_test, update_report,
#                                                  station_names_fiveg, lf_tools,
#                                                  test_cases, testbed, al_1, get_configuration):
#         """
#            pytest -m "country_code and twentyMhz and open and fiveg and channel4"
#         """
#         profile_data = setup_params_general["ssid_modes"]["open"][1]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         security = "open"
#         mode = "NAT"
#         band = "fiveg"
#         vlan = 1
#         channel = setup_params_general['rf-5G-4']['5G']['channel']
#         channel_width = setup_params_general['rf-5G-4']['5G']['channel-width']
#
#         obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
#         obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)
#
#         lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
#         # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
#         lf_tools.Chamber_View()
#         wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
#                                         download_rate="1Gbps", batch_size="1",
#                                         upload_rate="0", protocol="TCP-IPv4", duration="60000")
#
#         report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
#
#         lf_tools.attach_report_graphs(report_name=report_name)
#         print("Test Completed... Cleaning up Stations")
#         lf_tools.reset_scenario()
#         assert True
#
#     @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
#     @pytest.mark.open
#     @pytest.mark.twentyMhz
#     @pytest.mark.fiveg
#     @pytest.mark.channel149
#     def test_client_nat_wpa2_chn149_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
#                                                  lf_test, update_report,
#                                                  station_names_fiveg, lf_tools,
#                                                  test_cases, testbed, al_1, get_configuration):
#         """
#            pytest -m "country_code and twentyMhz and open and fiveg and channel5"
#         """
#         profile_data = setup_params_general["ssid_modes"]["open"][1]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         security = "open"
#         mode = "NAT"
#         band = "fiveg"
#         vlan = 1
#         channel = setup_params_general['rf-5G-5']['5G']['channel']
#         channel_width = setup_params_general['rf-5G-5']['5G']['channel-width']
#
#         obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
#         obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)
#
#         lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
#         # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
#         lf_tools.Chamber_View()
#         wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
#                                         download_rate="1Gbps", batch_size="1",
#                                         upload_rate="0", protocol="TCP-IPv4", duration="60000")
#
#         report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
#
#         lf_tools.attach_report_graphs(report_name=report_name)
#         print("Test Completed... Cleaning up Stations")
#         lf_tools.reset_scenario()
#         assert True
#
#     @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
#     @pytest.mark.open
#     @pytest.mark.twentyMhz
#     @pytest.mark.fiveg
#     @pytest.mark.channel153
#     def test_client_nat_wpa2_chn153_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
#                                                  lf_test, update_report,
#                                                  station_names_fiveg, lf_tools,
#                                                  test_cases, testbed, al_1, get_configuration):
#         """
#            pytest -m "country_code and twentyMhz and open and fiveg and channel6"
#         """
#         profile_data = setup_params_general["ssid_modes"]["open"][1]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         security = "open"
#         mode = "NAT"
#         band = "fiveg"
#         vlan = 1
#         channel = setup_params_general['rf-5G-6']['5G']['channel']
#         channel_width = setup_params_general['rf-5G-6']['5G']['channel-width']
#
#         obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
#         obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)
#
#         lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
#         # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
#         lf_tools.Chamber_View()
#         wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
#                                         download_rate="1Gbps", batch_size="1",
#                                         upload_rate="0", protocol="TCP-IPv4", duration="60000")
#
#         report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
#
#         lf_tools.attach_report_graphs(report_name=report_name)
#         print("Test Completed... Cleaning up Stations")
#         lf_tools.reset_scenario()
#         assert True
#
#     @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
#     @pytest.mark.open
#     @pytest.mark.twentyMhz
#     @pytest.mark.fiveg
#     @pytest.mark.channel157
#     def test_client_nat_wpa2_chn157_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
#                                                  lf_test, update_report,
#                                                  station_names_fiveg, lf_tools,
#                                                  test_cases, testbed, al_1, get_configuration):
#         """
#            pytest -m "country_code and twentyMhz and open and fiveg and channel7"
#         """
#         profile_data = setup_params_general["ssid_modes"]["open"][1]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         security = "open"
#         mode = "NAT"
#         band = "fiveg"
#         vlan = 1
#         channel = setup_params_general['rf-5G-7']['5G']['channel']
#         channel_width = setup_params_general['rf-5G-7']['5G']['channel-width']
#
#         obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
#         obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)
#
#         lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
#         # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
#         lf_tools.Chamber_View()
#         wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
#                                         download_rate="1Gbps", batch_size="1",
#                                         upload_rate="0", protocol="TCP-IPv4", duration="60000")
#
#         report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
#
#         lf_tools.attach_report_graphs(report_name=report_name)
#         print("Test Completed... Cleaning up Stations")
#         lf_tools.reset_scenario()
#         assert True
#
#     @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
#     @pytest.mark.open
#     @pytest.mark.twentyMhz
#     @pytest.mark.fiveg
#     @pytest.mark.channel161
#     def test_client_nat_wpa2_chn161_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
#                                                  lf_test, update_report,
#                                                  station_names_fiveg, lf_tools,
#                                                  test_cases, testbed, al_1, get_configuration):
#         """
#            pytest -m "country_code and twentyMhz and open and fiveg and channel8"
#         """
#         profile_data = setup_params_general["ssid_modes"]["open"][1]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         security = "open"
#         mode = "NAT"
#         band = "fiveg"
#         vlan = 1
#         channel = setup_params_general['rf-5G-8']['5G']['channel']
#         channel_width = setup_params_general['rf-5G-8']['5G']['channel-width']
#
#         obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
#         obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)
#
#         lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
#         # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
#         lf_tools.Chamber_View()
#         wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
#                                         download_rate="1Gbps", batch_size="1",
#                                         upload_rate="0", protocol="TCP-IPv4", duration="60000")
#
#         report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
#
#         lf_tools.attach_report_graphs(report_name=report_name)
#         print("Test Completed... Cleaning up Stations")
#         lf_tools.reset_scenario()
#         assert True
#
#     @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
#     @pytest.mark.open
#     @pytest.mark.twentyMhz
#     @pytest.mark.fiveg
#     @pytest.mark.channel165
#     def test_client_nat_wpa2_chn165_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
#                                                  lf_test, update_report,
#                                                  station_names_fiveg, lf_tools,
#                                                  test_cases, testbed, al_1, get_configuration):
#         """
#            pytest -m "country_code and twentyMhz and open and fiveg and channel9"
#         """
#         profile_data = setup_params_general["ssid_modes"]["open"][1]
#         ssid_name = profile_data["ssid_name"]
#         security_key = profile_data["security_key"]
#         security = "open"
#         mode = "NAT"
#         band = "fiveg"
#         vlan = 1
#         channel = setup_params_general['rf-5G-9']['5G']['channel']
#         channel_width = setup_params_general['rf-5G-9']['5G']['channel-width']
#
#         obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
#         obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)
#
#         lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
#         # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
#         lf_tools.Chamber_View()
#         wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
#                                         download_rate="1Gbps", batch_size="1",
#                                         upload_rate="0", protocol="TCP-IPv4", duration="60000")
#
#         report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
#
#         lf_tools.attach_report_graphs(report_name=report_name)
#         print("Test Completed... Cleaning up Stations")
#         lf_tools.reset_scenario()
#         assert True
import os
import pytest
import allure

pytestmark = [pytest.mark.country_code, pytest.mark.nat, pytest.mark.open, pytest.mark.united_states,
              pytest.mark.bandwidth_20mhz, pytest.mark.al, pytest.mark.tcp, pytest.mark.wifi_capacity,
              pytest.mark.download, pytest.mark.tcp_download, pytest.mark.wifi_capacity_single_client,
              pytest.mark.wifi_capacity_open_20mhz_all_channels_single_client_download_1gbps,
              pytest.mark.throughput_open_20mhz_all_channels_single_client_download_1gbps, pytest.mark.fiveg]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [
            {"ssid_name": "client_connectivity_al", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },

    "rf-5G-1": {
        "5G":
            {'band': '5G',
             'country': 'US',
             "channel-mode": "VHT",
             'channel-width': 20,
             "channel": 36}
    },
    "rf-5G-2": {
        "5G":
            {'band': '5G',
             'country': 'US',
             'channel-mode': 'VHT',
             'channel-width': 20,
             "channel": 40}
    },
    "rf-5G-3": {
        "5G":
            {'band': '5G',
             'country': 'US',
             'channel-mode': 'VHT',
             'channel-width': 20,
             "channel": 44}
    },
    "rf-5G-4": {
        "5G":
            {'band': '5G',
             'country': 'US',
             'channel-mode': 'VHT',
             'channel-width': 20,
             "channel": 48}
    },
    "rf-5G-5": {
        "5G":
            {'band': '5G',
             'country': 'US',
             'channel-mode': 'VHT',
             'channel-width': 20,
             "channel": 149}
    },
    # "rf-5G-6": {
    #     "5G":
    #         {'band': '5G',
    #          'country': 'US',
    #          'channel-mode': 'VHT',
    #          'channel-width': 20,
    #          "channel": 153}
    # },
    # "rf-5G-7": {
    #     "5G":
    #         {'band': '5G',
    #          'country': 'US',
    #          'channel-mode': 'VHT',
    #          'channel-width': 20,
    #          "channel": 157}
    # },
    # "rf-5G-8": {
    #     "5G":
    #         {'band': '5G',
    #          'country': 'US',
    #          'channel-mode': 'VHT',
    #          'channel-width': 20,
    #          "channel": 161}
    # },
    # "rf-5G-9": {
    #     "5G":
    #         {'band': '5G',
    #          'country': 'US',
    #          'channel-mode': 'VHT',
    #          'channel-width': 20,
    #          "channel": 165}
    # },
    "radius": False
}


@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestCountryUS20Mhz5G(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.open
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel36
    def test_client_nat_open_chn36_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
                                                 lf_test, update_report,
                                                 station_names_fiveg, lf_tools,
                                                 test_cases, testbed, al_1, get_configuration):
        """
           pytest -m "country_code and twentyMhz and open and fiveg and channel36"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "open"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general['rf-5G-1']['5G']['channel']
        channel_width = setup_params_general['rf-5G-1']['5G']['channel-width']

        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)

        lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1",
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        # lf_tools.reset_scenario()
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.open
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel40
    def test_client_nat_open_chn40_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
                                                 lf_test, update_report,
                                                 station_names_fiveg, lf_tools,
                                                 test_cases, testbed, al_1, get_configuration):
        """
           pytest -m "country_code and twentyMhz and open and fiveg and channel40"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "open"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general['rf-5G-2']['5G']['channel']
        channel_width = setup_params_general['rf-5G-2']['5G']['channel-width']

        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)

        lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1",
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        lf_tools.reset_scenario()
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.open
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel44
    def test_client_nat_open_chn44_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
                                                 lf_test, update_report,
                                                 station_names_fiveg, lf_tools,
                                                 test_cases, testbed, al_1, get_configuration):
        """
           pytest -m "country_code and twentyMhz and open and fiveg and channel44"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "open"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general['rf-5G-3']['5G']['channel']
        channel_width = setup_params_general['rf-5G-3']['5G']['channel-width']

        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)

        lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1",
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        lf_tools.reset_scenario()
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.open
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel48
    def test_client_nat_open_chn48_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
                                                 lf_test, update_report,
                                                 station_names_fiveg, lf_tools,
                                                 test_cases, testbed, al_1, get_configuration):
        """
           pytest -m "country_code and twentyMhz and open and fiveg and channel48"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "open"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general['rf-5G-4']['5G']['channel']
        channel_width = setup_params_general['rf-5G-4']['5G']['channel-width']

        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)

        lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1",
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        lf_tools.reset_scenario()
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.open
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel149
    def test_client_nat_open_chn149_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
                                                 lf_test, update_report,
                                                 station_names_fiveg, lf_tools,
                                                 test_cases, testbed, al_1, get_configuration):
        """
           pytest -m "country_code and twentyMhz and open and fiveg and channel149"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "open"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general['rf-5G-5']['5G']['channel']
        channel_width = setup_params_general['rf-5G-5']['5G']['channel-width']

        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)

        lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1",
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        lf_tools.reset_scenario()
        assert True

    # @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    # @pytest.mark.open
    # @pytest.mark.twentyMhz
    # @pytest.mark.fiveg
    # @pytest.mark.channel153
    # def test_client_nat_open_chn153_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
    #                                              lf_test, update_report,
    #                                              station_names_fiveg, lf_tools,
    #                                              test_cases, testbed, al_1, get_configuration):
    #     """
    #        pytest -m "country_code and twentyMhz and open and fiveg and channel6"
    #     """
    #     profile_data = setup_params_general["ssid_modes"]["open"][0]
    #     ssid_name = profile_data["ssid_name"]
    #     security_key = profile_data["security_key"]
    #     security = "open"
    #     mode = "NAT"
    #     band = "fiveg"
    #     vlan = 1
    #     channel = setup_params_general['rf-5G-6']['5G']['channel']
    #     channel_width = setup_params_general['rf-5G-6']['5G']['channel-width']
    #
    #     obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
    #     obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)
    #
    #     lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
    #     # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
    #     lf_tools.Chamber_View()
    #     wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
    #                                     download_rate="1Gbps", batch_size="1",
    #                                     upload_rate="0", protocol="TCP-IPv4", duration="60000")
    #
    #     report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
    #
    #     lf_tools.attach_report_graphs(report_name=report_name)
    #     print("Test Completed... Cleaning up Stations")
    #     lf_tools.reset_scenario()
    #     assert True
    #
    # @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    # @pytest.mark.open
    # @pytest.mark.twentyMhz
    # @pytest.mark.fiveg
    # @pytest.mark.channel157
    # def test_client_nat_open_chn157_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
    #                                              lf_test, update_report,
    #                                              station_names_fiveg, lf_tools,
    #                                              test_cases, testbed, al_1, get_configuration):
    #     """
    #        pytest -m "country_code and twentyMhz and open and fiveg and channel7"
    #     """
    #     profile_data = setup_params_general["ssid_modes"]["open"][0]
    #     ssid_name = profile_data["ssid_name"]
    #     security_key = profile_data["security_key"]
    #     security = "open"
    #     mode = "NAT"
    #     band = "fiveg"
    #     vlan = 1
    #     channel = setup_params_general['rf-5G-7']['5G']['channel']
    #     channel_width = setup_params_general['rf-5G-7']['5G']['channel-width']
    #
    #     obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
    #     obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)
    #
    #     lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
    #     # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
    #     lf_tools.Chamber_View()
    #     wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
    #                                     download_rate="1Gbps", batch_size="1",
    #                                     upload_rate="0", protocol="TCP-IPv4", duration="60000")
    #
    #     report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
    #
    #     lf_tools.attach_report_graphs(report_name=report_name)
    #     print("Test Completed... Cleaning up Stations")
    #     lf_tools.reset_scenario()
    #     assert True
    #
    # @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    # @pytest.mark.open
    # @pytest.mark.twentyMhz
    # @pytest.mark.fiveg
    # @pytest.mark.channel161
    # def test_client_nat_open_chn161_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
    #                                              lf_test, update_report,
    #                                              station_names_fiveg, lf_tools,
    #                                              test_cases, testbed, al_1, get_configuration):
    #     """
    #        pytest -m "country_code and twentyMhz and open and fiveg and channel8"
    #     """
    #     profile_data = setup_params_general["ssid_modes"]["open"][0]
    #     ssid_name = profile_data["ssid_name"]
    #     security_key = profile_data["security_key"]
    #     security = "open"
    #     mode = "NAT"
    #     band = "fiveg"
    #     vlan = 1
    #     channel = setup_params_general['rf-5G-8']['5G']['channel']
    #     channel_width = setup_params_general['rf-5G-8']['5G']['channel-width']
    #
    #     obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
    #     obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)
    #
    #     lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
    #     # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
    #     lf_tools.Chamber_View()
    #     wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
    #                                     download_rate="1Gbps", batch_size="1",
    #                                     upload_rate="0", protocol="TCP-IPv4", duration="60000")
    #
    #     report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
    #
    #     lf_tools.attach_report_graphs(report_name=report_name)
    #     print("Test Completed... Cleaning up Stations")
    #     lf_tools.reset_scenario()
    #     assert True
    #
    # @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    # @pytest.mark.open
    # @pytest.mark.twentyMhz
    # @pytest.mark.fiveg
    # @pytest.mark.channel165
    # def test_client_nat_open_chn165_20Mhz_US_5g(self, instantiate_profile, get_lf_logs,
    #                                              lf_test, update_report,
    #                                              station_names_fiveg, lf_tools,
    #                                              test_cases, testbed, al_1, get_configuration):
    #     """
    #        pytest -m "country_code and twentyMhz and open and fiveg and channel9"
    #     """
    #     profile_data = setup_params_general["ssid_modes"]["open"][0]
    #     ssid_name = profile_data["ssid_name"]
    #     security_key = profile_data["security_key"]
    #     security = "open"
    #     mode = "NAT"
    #     band = "fiveg"
    #     vlan = 1
    #     channel = setup_params_general['rf-5G-9']['5G']['channel']
    #     channel_width = setup_params_general['rf-5G-9']['5G']['channel-width']
    #
    #     obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
    #     obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)
    #
    #     lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
    #     # lf_tools.add_stations(band="ax", num_stations="max", dut=lf_tools.dut_name, ssid_name=ssid_name)
    #     lf_tools.Chamber_View()
    #     wct_obj = lf_test.wifi_capacity(instance_name="test_client_open_NAT_tcp_dl", mode=mode, vlan_id=vlan,
    #                                     download_rate="1Gbps", batch_size="1",
    #                                     upload_rate="0", protocol="TCP-IPv4", duration="60000")
    #
    #     report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
    #
    #     lf_tools.attach_report_graphs(report_name=report_name)
    #     print("Test Completed... Cleaning up Stations")
    #     lf_tools.reset_scenario()
    #     assert True
