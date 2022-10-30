import os
import pytest
import allure
import time

pytestmark = [pytest.mark.country_code, pytest.mark.nat, pytest.mark.wpa2, pytest.mark.united_states,
              pytest.mark.bandwidth_80mhz, pytest.mark.al, pytest.mark.tcp, pytest.mark.wifi_capacity_test,
              pytest.mark.download, pytest.mark.tcp_download, pytest.mark.wifi_capacity_single_client,
              pytest.mark.wifi_capacity_wpa2_80mhz_all_channels_single_client_download_1gbps,
              pytest.mark.throughput_wpa2_80mhz_all_channels_single_client_download_1gbps, pytest.mark.fiveg]

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
             'channel-width': 80,
             "channel": 36}
    },
    "rf-5G-2": {
        "5G":
            {'band': '5G',
             'country': 'US',
             'channel-mode': 'VHT',
             'channel-width': 80,
             "channel": 40}
    },
    "rf-5G-3": {
        "5G":
            {'band': '5G',
             'country': 'US',
             'channel-mode': 'VHT',
             'channel-width': 80,
             "channel": 44}
    },
    "rf-5G-4": {
        "5G":
            {'band': '5G',
             'country': 'US',
             'channel-mode': 'VHT',
             'channel-width': 80,
             "channel": 48}
    },
    "rf-5G-5": {
        "5G":
            {'band': '5G',
             'country': 'US',
             'channel-mode': 'VHT',
             'channel-width': 80,
             "channel": 149}
    },
    "radius": False,
    "expected-throughput": 780.65
}


@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestCountryUS80Mhz5G(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel_36
    @pytest.mark.tcp_download
    def test_client_nat_wpa2_chn36_80Mhz_US_5g_tcp_download(self, instantiate_profile, get_lf_logs,
                                                 lf_test, update_report,
                                                 station_names_fiveg, lf_tools,
                                                 test_cases, testbed, al_1, get_configuration, get_attenuators):
        """
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel_36"
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
        connected_attenuators, selected_attenuators = get_attenuators
        print(f"connected_attenuators : {connected_attenuators}")
        print(f"selected_attenuators : {selected_attenuators}")

        attenuation_value = 0
        connected_attenuators = list(set(connected_attenuators) - set(selected_attenuators))

        if selected_attenuators:  # selected attenuators list is Empty
            for selected_atten in range(len(selected_attenuators)):
                print(f"This is available in selected : selected_attens : {selected_atten}")
                for i in range(4):
                    lf_test.attenuator_modify(int(selected_attenuators[selected_atten]), i, attenuation_value)
                    time.sleep(0.5)

        for connected_atten in range(len(connected_attenuators)):
            print(f"This is available in connected : connected_atten : {connected_atten}")
            for i in range(4):
                lf_test.attenuator_modify(int(connected_attenuators[connected_atten]), i, 0)
                time.sleep(0.5)

        # for connected_atten in range(len(connected_attenuators)):
        #     for selected_atten in range(len(selected_attenuators)):
        #         if connected_atten in selected_attenuators:
        #             print(f"This is available in selected : connected_atten : {connected_atten}")
        #             for i in range(4):
        #                 lf_test.attenuator_modify(int(connected_attenuators[connected_atten]), i, attenuation_value)
        #                 time.sleep(0.5)
        #         else:
        #             print(f"This is not available in selected : connected_atten : {connected_atten}")
        #             for i in range(4):
        #                 lf_test.attenuator_modify(int(connected_attenuators[connected_atten]), i, 0)
        #                 time.sleep(0.5)

        # Start//To set attenuation
        # attenuator_serial = lf_test.attenuator_serial()
        # print(f"attenuator_serial : {attenuator_serial}")
        # connected_attenuators = get_configuration['traffic_generator']['details']['attenuation_connected_serial']
        # attenuator_serial1 = (attenuator_serial[0].split("."))[-1]
        # print(f"attenuator_serial1 : {attenuator_serial1}")

        # End//Attenuation is set

        # Start//To Do: This code looks important for ip not getting issue might need to test later
        # for i in range(3):
        #     sta.append(station_name + str(i))
        # print(sta)
        # lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 1)
        # sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
        #                                             radio=radio_name, station_name=sta)
        # if not sta_ip:
        #     print("test failed due to no station ip")
        #     assert False
        # END//To Do: This code looks important for ip not getting issue might need to test later

        lf_tools.reset_scenario()

        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)

        lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()

        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_NAT_tcp_dl_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1",
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        lf_tools.attach_report_kpi(report_name=report_name)

        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=str(batch_size))
        print(csv_val)
        print(f"Download Traffic Throughput: {csv_val['Down']['DL Mbps - 1 STA']}")
        actual_throughput = csv_val['Down']['DL Mbps - 1 STA']

        result = {

            "result": None,
            "ssid-name": ssid_name,
            "security": security,
            "security-key": security_key,
            "band": band,
            "channel": channel,
            "description" : "WiFi capacity test",
            "test-download" : "1Gbps",
            "test-batch-size" : "1",
            "test-upload-rate" : "0",
            "test-protocol" : "TCP-IPV4",
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
                                   name="WiFi_Capacity_1GBPS_Download_Throughput_TCP_5g_Test", attachment_type="PDF")
            allure.attach(name="PASSED:Throughput Results:", body=str(
                "Actual throughput:" + str(float(actual_throughput)) + " is greater than Expected Throughput:" + str(
                    expected_throughput)))
            lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            assert True
        else:
            result["result"] = "FAIL"
            pdf = lf_tools.create_dynamic_pdf(report_name, get_configuration, result)
            print(f"pdf: {pdf}")
            if os.path.exists(pdf):
                allure.attach.file(source=pdf,
                                   name="WiFi_Capacity_1GBPS_Download_Throughput_TCP_5g_Test", attachment_type="PDF")
            allure.attach(name="FAILED:Throughput Results:", body=str(
                "Actual throughput:" + str(float(actual_throughput)) + " is lesser than Expected Throughput:" + str(
                    expected_throughput)))
            lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            assert False


    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.eightyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel_149
    @pytest.mark.tcp_download
    def test_client_nat_wpa2_chn149_80Mhz_US_5g_tcp_download(self, instantiate_profile, get_lf_logs,
                                                 lf_test, update_report,
                                                 station_names_fiveg, lf_tools,
                                                 test_cases, testbed, al_1, get_configuration, get_attenuators):
        """
           pytest -m "country_code and twentyMhz and wpa2 and fiveg and channel_149"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        channel = setup_params_general['rf-5G-5']['5G']['channel']
        channel_width = setup_params_general['rf-5G-5']['5G']['channel-width']
        expected_throughput = setup_params_general["expected-throughput"]
        batch_size = 1


        lf_tools.reset_scenario()
        connected_attenuators, selected_attenuators = get_attenuators
        print(f"connected_attenuators : {connected_attenuators}")
        print(f"selected_attenuators : {selected_attenuators}")

        attenuation_value = 0
        connected_attenuators = list(set(connected_attenuators) - set(selected_attenuators))

        if selected_attenuators:  # selected attenuators list is Empty
            for selected_atten in range(len(selected_attenuators)):
                print(f"This is available in selected : selected_attens : {selected_atten}")
                for i in range(4):
                    lf_test.attenuator_modify(int(selected_attenuators[selected_atten]), i, attenuation_value)
                    time.sleep(0.5)

        for connected_atten in range(len(connected_attenuators)):
            print(f"This is available in connected : connected_atten : {connected_atten}")
            for i in range(4):
                lf_test.attenuator_modify(int(connected_attenuators[connected_atten]), i, 0)
                time.sleep(0.5)

        # for connected_atten in range(len(connected_attenuators)):
        #     for selected_atten in range(len(selected_attenuators)):
        #         if connected_atten in selected_attenuators:
        #             print(f"This is available in selected : connected_atten : {connected_atten}")
        #             for i in range(4):
        #                 lf_test.attenuator_modify(int(connected_attenuators[connected_atten]), i, attenuation_value)
        #                 time.sleep(0.5)
        #         else:
        #             print(f"This is not available in selected : connected_atten : {connected_atten}")
        #             for i in range(4):
        #                 lf_test.attenuator_modify(int(connected_attenuators[connected_atten]), i, 0)
        #                 time.sleep(0.5)

        # Start//To set attenuation
        # attenuator_serial = lf_test.attenuator_serial()
        # print(f"attenuator_serial : {attenuator_serial}")
        # connected_attenuators = get_configuration['traffic_generator']['details']['attenuation_connected_serial']
        # attenuator_serial1 = (attenuator_serial[0].split("."))[-1]
        # print(f"attenuator_serial1 : {attenuator_serial1}")

        # End//Attenuation is set

        # Start//To Do: This code looks important for ip not getting issue might need to test later
        # for i in range(3):
        #     sta.append(station_name + str(i))
        # print(sta)
        # lf_tools.set_radio_antenna("cli-json/set_wifi_radio", shelf, resource, values[2], 1)
        # sta_ip = lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"],
        #                                             radio=radio_name, station_name=sta)
        # if not sta_ip:
        #     print("test failed due to no station ip")
        #     assert False
        # END//To Do: This code looks important for ip not getting issue might need to test later

        lf_tools.reset_scenario()

        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)

        lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        # lf_tools.add_stations(band="ax", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()

        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_NAT_tcp_dl_5g", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1",
                                        upload_rate="0", protocol="TCP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        lf_tools.attach_report_kpi(report_name=report_name)

        csv_val = lf_tools.read_csv_individual_station_throughput(dir_name=report_name, option=None,
                                                                  individual_station_throughput=False, kpi_csv=True,
                                                                  file_name="/kpi.csv", batch_size=str(batch_size))
        print(csv_val)
        print(f"Download Traffic Throughput: {csv_val['Down']['DL Mbps - 1 STA']}")
        actual_throughput = csv_val['Down']['DL Mbps - 1 STA']

        result = {

            "result": None,
            "ssid-name": ssid_name,
            "security": security,
            "security-key": security_key,
            "band": band,
            "channel": channel,
            "description" : "WiFi capacity test",
            "test-download" : "1Gbps",
            "test-batch-size" : "1",
            "test-upload-rate" : "0",
            "test-protocol" : "TCP-IPV4",
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
                                   name="WiFi_Capacity_1GBPS_Download_Throughput_TCP_5g_Test", attachment_type="PDF")
            allure.attach(name="PASSED:Throughput Results:", body=str(
                "Actual throughput:" + str(float(actual_throughput)) + " is greater than Expected Throughput:" + str(
                    expected_throughput)))
            lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            assert True
        else:
            result["result"] = "FAIL"
            pdf = lf_tools.create_dynamic_pdf(report_name, get_configuration, result)
            print(f"pdf: {pdf}")
            if os.path.exists(pdf):
                allure.attach.file(source=pdf,
                                   name="WiFi_Capacity_1GBPS_Download_Throughput_TCP_5g_Test", attachment_type="PDF")
            allure.attach(name="FAILED:Throughput Results:", body=str(
                "Actual throughput:" + str(float(actual_throughput)) + " is lesser than Expected Throughput:" + str(
                    expected_throughput)))
            lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            assert False

