import os
import pytest
import allure

pytestmark = [pytest.mark.country_code, pytest.mark.nat, pytest.mark.wpa2, pytest.mark.united_states,
              pytest.mark.bandwidth_20mhz, pytest.mark.al, pytest.mark.tcp, pytest.mark.wifi_capacity,
              pytest.mark.download, pytest.mark.tcp_download, pytest.mark.wifi_capacity_single_client,
              pytest.mark.wifi_capacity_wpa2_20mhz_all_channels_single_client_download_1gbps,
              pytest.mark.throughput_wpa2_20mhz_all_channels_single_client_download_1gbps]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "client_connectivity", "appliedRadios": ["2G"], "security_key": "something"},
        ]
    },

    "rf-2G-1": {
        "2G":
            {'band': '2G',
             'country': 'US',
             "channel-mode": "VHT",
             'channel-width': 20,
             "channel": 1}
    },
    # "rf-2G-2": {
    #     "2G":
    #         {'band': '2G',
    #          'country': 'US',
    #          'channel-mode': 'VHT',
    #          'channel-width': 20,
    #          "channel": 2}
    # },
    # "rf-2G-3": {
    #     "2G":
    #         {'band': '2G',
    #          'country': 'US',
    #          'channel-mode': 'VHT',
    #          'channel-width': 20,
    #          "channel": 3}
    # },
    # "rf-2G-4": {
    #     "2G":
    #         {'band': '2G',
    #          'country': 'US',
    #          'channel-mode': 'VHT',
    #          'channel-width': 20,
    #          "channel": 4}
    # },
    # "rf-2G-5": {
    #     "2G":
    #         {'band': '2G',
    #          'country': 'US',
    #          'channel-mode': 'VHT',
    #          'channel-width': 20,
    #          "channel": 5}
    # },
    "rf-2G-6": {
        "2G":
            {'band': '2G',
             'country': 'US',
             'channel-mode': 'VHT',
             'channel-width': 20,
             "channel": 6}
    },
    # "rf-2G-7": {
    #     "2G":
    #         {'band': '2G',
    #          'country': 'US',
    #          'channel-mode': 'VHT',
    #          'channel-width': 20,
    #          "channel": 7}
    # },
    # "rf-2G-8": {
    #     "2G":
    #         {'band': '2G',
    #          'country': 'US',
    #          'channel-mode': 'VHT',
    #          'channel-width': 20,
    #          "channel": 8}
    # },
    # "rf-2G-9": {
    #     "2G":
    #         {'band': '2G',
    #          'country': 'US',
    #          'channel-mode': 'VHT',
    #          'channel-width': 20,
    #          "channel": 9}
    # },
    # "rf-2G-10": {
    #     "2G":
    #         {'band': '2G',
    #          'country': 'US',
    #          'channel-mode': 'VHT',
    #          'channel-width': 20,
    #          "channel": 10}
    # },
    "rf-2G-11": {
        "2G":
            {'band': '2G',
             'country': 'US',
             'channel-mode': 'VHT',
             'channel-width': 20,
             "channel": 11}
    },
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
class TestCountryUS20Mhz2g(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.twog
    @pytest.mark.channel1
    def test_client_nat_wpa2_chn1_20Mhz_US_2g(self, instantiate_profile, get_lf_logs,
                                                 lf_test, update_report,
                                                 station_names_twog, lf_tools,
                                                 test_cases, testbed, al_1, get_configuration):
        """
           pytest -m "country_code and twentyMhz and wpa2 and twog and channel1"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "twog"
        vlan = 1
        channel = setup_params_general['rf-2G-1']['2G']['channel']
        channel_width = setup_params_general['rf-2G-1']['2G']['channel-width']

        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        obj.check_and_set_ap_channel(radio="2G", band=channel_width, channel=channel)

        lf_tools.add_stations(band="2G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
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
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.twog
    @pytest.mark.channel6
    def test_client_nat_wpa2_chn6_20Mhz_US_2g(self, instantiate_profile, get_lf_logs,
                                                 lf_test, update_report,
                                                 station_names_twog, lf_tools,
                                                 test_cases, testbed, al_1, get_configuration):
        """
           pytest -m "country_code and twentyMhz and wpa2 and twog and channel6"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "twog"
        vlan = 1
        channel = setup_params_general['rf-2G-6']['2G']['channel']
        channel_width = setup_params_general['rf-2G-6']['2G']['channel-width']

        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        obj.check_and_set_ap_channel(radio="2G", band=channel_width, channel=channel)

        lf_tools.add_stations(band="2G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
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
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.twog
    @pytest.mark.channel11
    def test_client_nat_wpa2_chn11_20Mhz_US_2g(self, instantiate_profile, get_lf_logs,
                                                  lf_test, update_report,
                                                  station_names_twog, lf_tools,
                                                  test_cases, testbed, al_1, get_configuration):
        """
           pytest -m "country_code and twentyMhz and wpa2 and twog and channel11"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "twog"
        vlan = 1
        channel = setup_params_general['rf-2G-11']['2G']['channel']
        channel_width = setup_params_general['rf-2G-11']['2G']['channel-width']

        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        obj.check_and_set_ap_channel(radio="2G", band=channel_width, channel=channel)

        lf_tools.add_stations(band="2G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
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
    # @pytest.mark.wpa2_personal
    # @pytest.mark.twentyMhz
    # @pytest.mark.twog
    # @pytest.mark.channel2
    # def test_client_nat_wpa2_chn2_20Mhz_US_2g(self, instantiate_profile, get_lf_logs,
    #                                              lf_test, update_report,
    #                                              station_names_twog, lf_tools,
    #                                              test_cases, testbed, al_1, get_configuration):
    #     """
    #        pytest -m "country_code and twentyMhz and wpa2 and twog and channel2"
    #     """
    #     profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
    #     ssid_name = profile_data["ssid_name"]
    #     security_key = profile_data["security_key"]
    #     security = "wpa2"
    #     mode = "NAT"
    #     band = "twog"
    #     vlan = 1
    #     channel = setup_params_general['rf-2G-2']['2G']['channel']
    #     channel_width = setup_params_general['rf-2G-2']['2G']['channel-width']
    #
    #     obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
    #     obj.check_and_set_ap_channel(radio="2G", band=channel_width, channel=channel)
    #
    #     lf_tools.add_stations(band="2G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
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
    # @pytest.mark.wpa2_personal
    # @pytest.mark.twentyMhz
    # @pytest.mark.twog
    # @pytest.mark.channel3
    # def test_client_nat_wpa2_chn3_20Mhz_US_2g(self, instantiate_profile, get_lf_logs,
    #                                              lf_test, update_report,
    #                                              station_names_twog, lf_tools,
    #                                              test_cases, testbed, al_1, get_configuration):
    #     """
    #        pytest -m "country_code and twentyMhz and wpa2 and twog and channel3"
    #     """
    #     profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
    #     ssid_name = profile_data["ssid_name"]
    #     security_key = profile_data["security_key"]
    #     security = "wpa2"
    #     mode = "NAT"
    #     band = "twog"
    #     vlan = 1
    #     channel = setup_params_general['rf-2G-3']['2G']['channel']
    #     channel_width = setup_params_general['rf-2G-3']['2G']['channel-width']
    #
    #     obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
    #     obj.check_and_set_ap_channel(radio="2G", band=channel_width, channel=channel)
    #
    #     lf_tools.add_stations(band="2G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
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
    # @pytest.mark.wpa2_personal
    # @pytest.mark.twentyMhz
    # @pytest.mark.twog
    # @pytest.mark.channel4
    # def test_client_nat_wpa2_chn4_20Mhz_US_2g(self, instantiate_profile, get_lf_logs,
    #                                              lf_test, update_report,
    #                                              station_names_twog, lf_tools,
    #                                              test_cases, testbed, al_1, get_configuration):
    #     """
    #        pytest -m "country_code and twentyMhz and wpa2 and twog and channel4"
    #     """
    #     profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
    #     ssid_name = profile_data["ssid_name"]
    #     security_key = profile_data["security_key"]
    #     security = "wpa2"
    #     mode = "NAT"
    #     band = "twog"
    #     vlan = 1
    #     channel = setup_params_general['rf-2G-4']['2G']['channel']
    #     channel_width = setup_params_general['rf-2G-4']['2G']['channel-width']
    #
    #     obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
    #     obj.check_and_set_ap_channel(radio="2G", band=channel_width, channel=channel)
    #
    #     lf_tools.add_stations(band="2G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
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
    # @pytest.mark.wpa2_personal
    # @pytest.mark.twentyMhz
    # @pytest.mark.twog
    # @pytest.mark.channel5
    # def test_client_nat_wpa2_chn5_20Mhz_US_2g(self, instantiate_profile, get_lf_logs,
    #                                              lf_test, update_report,
    #                                              station_names_twog, lf_tools,
    #                                              test_cases, testbed, al_1, get_configuration):
    #     """
    #        pytest -m "country_code and twentyMhz and wpa2 and twog and channel5"
    #     """
    #     profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
    #     ssid_name = profile_data["ssid_name"]
    #     security_key = profile_data["security_key"]
    #     security = "wpa2"
    #     mode = "NAT"
    #     band = "twog"
    #     vlan = 1
    #     channel = setup_params_general['rf-2G-5']['2G']['channel']
    #     channel_width = setup_params_general['rf-2G-5']['2G']['channel-width']
    #
    #     obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
    #     obj.check_and_set_ap_channel(radio="2G", band=channel_width, channel=channel)
    #
    #     lf_tools.add_stations(band="2G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
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
    # @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    # @pytest.mark.wpa2_personal
    # @pytest.mark.twentyMhz
    # @pytest.mark.twog
    # @pytest.mark.channel7
    # def test_client_nat_wpa2_chn7_20Mhz_US_2g(self, instantiate_profile, get_lf_logs,
    #                                              lf_test, update_report,
    #                                              station_names_twog, lf_tools,
    #                                              test_cases, testbed, al_1, get_configuration):
    #     """
    #        pytest -m "country_code and twentyMhz and wpa2 and twog and channel7"
    #     """
    #     profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
    #     ssid_name = profile_data["ssid_name"]
    #     security_key = profile_data["security_key"]
    #     security = "wpa2"
    #     mode = "NAT"
    #     band = "twog"
    #     vlan = 1
    #     channel = setup_params_general['rf-2G-7']['2G']['channel']
    #     channel_width = setup_params_general['rf-2G-7']['2G']['channel-width']
    #
    #     obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
    #     obj.check_and_set_ap_channel(radio="2G", band=channel_width, channel=channel)
    #
    #     lf_tools.add_stations(band="2G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
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
    # @pytest.mark.wpa2_personal
    # @pytest.mark.twentyMhz
    # @pytest.mark.twog
    # @pytest.mark.channel8
    # def test_client_nat_wpa2_chn8_20Mhz_US_2g(self, instantiate_profile, get_lf_logs,
    #                                              lf_test, update_report,
    #                                              station_names_twog, lf_tools,
    #                                              test_cases, testbed, al_1, get_configuration):
    #     """
    #        pytest -m "country_code and twentyMhz and wpa2 and twog and channel8"
    #     """
    #     profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
    #     ssid_name = profile_data["ssid_name"]
    #     security_key = profile_data["security_key"]
    #     security = "wpa2"
    #     mode = "NAT"
    #     band = "twog"
    #     vlan = 1
    #     channel = setup_params_general['rf-2G-8']['2G']['channel']
    #     channel_width = setup_params_general['rf-2G-8']['2G']['channel-width']
    #
    #     obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
    #     obj.check_and_set_ap_channel(radio="2G", band=channel_width, channel=channel)
    #
    #     lf_tools.add_stations(band="2G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
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
    # @pytest.mark.wpa2_personal
    # @pytest.mark.twentyMhz
    # @pytest.mark.twog
    # @pytest.mark.channel9
    # def test_client_nat_wpa2_chn9_20Mhz_US_2g(self, instantiate_profile, get_lf_logs,
    #                                              lf_test, update_report,
    #                                              station_names_twog, lf_tools,
    #                                              test_cases, testbed, al_1, get_configuration):
    #     """
    #        pytest -m "country_code and twentyMhz and wpa2 and twog and channel9"
    #     """
    #     profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
    #     ssid_name = profile_data["ssid_name"]
    #     security_key = profile_data["security_key"]
    #     security = "wpa2"
    #     mode = "NAT"
    #     band = "twog"
    #     vlan = 1
    #     channel = setup_params_general['rf-2G-9']['2G']['channel']
    #     channel_width = setup_params_general['rf-2G-9']['2G']['channel-width']
    #
    #     obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
    #     obj.check_and_set_ap_channel(radio="2G", band=channel_width, channel=channel)
    #
    #     lf_tools.add_stations(band="2G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
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
    # @pytest.mark.wpa2_personal
    # @pytest.mark.twentyMhz
    # @pytest.mark.twog
    # @pytest.mark.channel10
    # def test_client_nat_wpa2_chn10_20Mhz_US_2g(self, instantiate_profile, get_lf_logs,
    #                                               lf_test, update_report,
    #                                               station_names_twog, lf_tools,
    #                                               test_cases, testbed, al_1, get_configuration):
    #     """
    #        pytest -m "country_code and twentyMhz and wpa2 and twog and channel10"
    #     """
    #     profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
    #     ssid_name = profile_data["ssid_name"]
    #     security_key = profile_data["security_key"]
    #     security = "wpa2"
    #     mode = "NAT"
    #     band = "twog"
    #     vlan = 1
    #     channel = setup_params_general['rf-2G-10']['2G']['channel']
    #     channel_width = setup_params_general['rf-2G-10']['2G']['channel-width']
    #
    #     obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
    #     obj.check_and_set_ap_channel(radio="2G", band=channel_width, channel=channel)
    #
    #     lf_tools.add_stations(band="2G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
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
