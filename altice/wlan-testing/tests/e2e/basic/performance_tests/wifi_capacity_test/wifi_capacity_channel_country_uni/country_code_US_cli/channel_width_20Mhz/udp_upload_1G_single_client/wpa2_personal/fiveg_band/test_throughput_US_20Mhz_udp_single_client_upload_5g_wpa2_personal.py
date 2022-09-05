import os
import pytest
import allure

pytestmark = [pytest.mark.country_code, pytest.mark.nat, pytest.mark.wpa2, pytest.mark.united_states,
              pytest.mark.bandwidth_20mhz, pytest.mark.al, pytest.mark.udp, pytest.mark.wifi_capacity,
              pytest.mark.upload, pytest.mark.udp_upload, pytest.mark.wifi_capacity_single_client,
              pytest.mark.wifi_capacity_wpa2_20mhz_all_channels_single_client_upload_1gbps,
              pytest.mark.throughput_wpa2_20mhz_all_channels_single_client_upload_1gbps, pytest.mark.fiveg,pytest.mark.udp]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
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
    "radius": False,
    "expected-throughput": 170
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
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel36
    @pytest.mark.upload
    def test_client_nat_wpa2_chn36_20Mhz_US_5g_udp_upload(self, instantiate_profile, get_lf_logs,
                                                 lf_test, update_report,
                                                 station_names_fiveg, lf_tools,
                                                 test_cases, testbed, al_1, get_configuration):
        """
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel36"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general['rf-5G-1']['5G']['channel']
        channel_width = setup_params_general['rf-5G-1']['5G']['channel-width']
        expected_throughput = setup_params_general["expected-throughput"]
        batch_size = 1


        lf_tools.reset_scenario()

        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)

        lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()

        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_NAT_udp_ul_5g", mode=mode, vlan_id=vlan,
                                        upload_rate="1Gbps", batch_size="1",
                                        download_rate="0", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        lf_tools.attach_report_kpi(report_name=report_name)

        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=str(batch_size))
        print(csv_val)
        print(f"Upload Traffic Throughput: {csv_val['Up']['UL Mbps - 1 STA']}")
        actual_throughput = csv_val['Up']['UL Mbps - 1 STA']

        result = {

            "result": None,
            "ssid-name": ssid_name,
            "security": security,
            "security-key": security_key,
            "band": band,
            "channel": channel,
            "description" : "WiFi capacity test",
            "test-download" : "0",
            "test-batch-size" : "1",
            "test-upload-rate" : "1Gbps",
            "test-protocol" : "UDP-IPV4",
            "test-duration" : "60 Sec",
            "expected-throughput": f" > {expected_throughput}",
            "actual-throughput": actual_throughput
        }

        if expected_throughput < float(actual_throughput):
            result["result"] = "PASS"
            pdf = lf_tools.create_dynamic_pdf(report_name, get_configuration, result)
            print(f"pdf: {pdf}")
            if os.path.exists(pdf):
                allure.attach.file(source=pdf,
                                   name="WiFi_Capacity_1GBPS_Upload_Throughput_WPA2_UDP_5g_Test", attachment_type="PDF")
            assert True
        else:
            result["result"] = "FAIL"
            pdf = lf_tools.create_dynamic_pdf(report_name, get_configuration, result)
            print(f"pdf: {pdf}")
            if os.path.exists(pdf):
                allure.attach.file(source=pdf,
                                   name="WiFi_Capacity_1GBPS_Upload_Throughput_WPA2_UDP_5g_Test", attachment_type="PDF")
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.twentyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel40
    @pytest.mark.upload
    def test_client_nat_wpa2_chn40_20Mhz_US_5g_udp_upload(self, instantiate_profile, get_lf_logs,
                                                 lf_test, update_report,
                                                 station_names_fiveg, lf_tools,
                                                 test_cases, testbed, al_1, get_configuration):
        """
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel40"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general['rf-5G-2']['5G']['channel']
        channel_width = setup_params_general['rf-5G-2']['5G']['channel-width']
        expected_throughput = setup_params_general["expected-throughput"]
        batch_size = 1


        lf_tools.reset_scenario()

        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)

        lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()

        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_NAT_udp_ul_5g", mode=mode, vlan_id=vlan,
                                        upload_rate="1Gbps", batch_size="1",
                                        download_rate="0", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        lf_tools.attach_report_kpi(report_name=report_name)

        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=str(batch_size))
        print(csv_val)
        print(f"Upload Traffic Throughput: {csv_val['Up']['UL Mbps - 1 STA']}")
        actual_throughput = csv_val['Up']['UL Mbps - 1 STA']

        result = {

            "result": None,
            "ssid-name": ssid_name,
            "security": security,
            "security-key": security_key,
            "band": band,
            "channel": channel,
            "description" : "WiFi capacity test",
            "test-download" : "0",
            "test-batch-size" : "1",
            "test-upload-rate" : "1Gbps",
            "test-protocol" : "UDP-IPV4",
            "test-duration" : "60 Sec",
            "expected-throughput": f" > {expected_throughput}",
            "actual-throughput": actual_throughput
        }

        if expected_throughput < float(actual_throughput):
            result["result"] = "PASS"
            pdf = lf_tools.create_dynamic_pdf(report_name, get_configuration, result)
            print(f"pdf: {pdf}")
            if os.path.exists(pdf):
                allure.attach.file(source=pdf,
                                   name="WiFi_Capacity_1GBPS_Upload_Throughput_WPA2_UDP_5g_Test", attachment_type="PDF")
            assert True
        else:
            result["result"] = "FAIL"
            pdf = lf_tools.create_dynamic_pdf(report_name, get_configuration, result)
            print(f"pdf: {pdf}")
            if os.path.exists(pdf):
                allure.attach.file(source=pdf,
                                   name="WiFi_Capacity_1GBPS_Upload_Throughput_WPA2_UDP_5g_Test", attachment_type="PDF")
            assert False