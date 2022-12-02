import os
import pytest
import allure
import time

pytestmark = [pytest.mark.country_code, pytest.mark.nat, pytest.mark.wpa2, pytest.mark.united_states,
              pytest.mark.bandwidth_40mhz, pytest.mark.al, pytest.mark.tcp, pytest.mark.rate_vs_range,
              pytest.mark.upload, pytest.mark.tcp_upload,
              pytest.mark.rate_vs_range_wpa2_40mhz_all_channels_single_client_upload_1gbps,
              pytest.mark.rate_vs_range_throughput_wpa2_40mhz_all_channels_single_client_upload_1gbps, pytest.mark.fiveg, pytest.mark.tcp]

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
             'channel-width': 40,
             "channel": 36}
    },
    "rf-5G-2": {
        "5G":
            {'band': '5G',
             'country': 'US',
             'channel-mode': 'VHT',
             'channel-width': 40,
             "channel": 40}
    },
    "rf-5G-3": {
        "5G":
            {'band': '5G',
             'country': 'US',
             'channel-mode': 'VHT',
             'channel-width': 40,
             "channel": 44}
    },
    "rf-5G-4": {
        "5G":
            {'band': '5G',
             'country': 'US',
             'channel-mode': 'VHT',
             'channel-width': 40,
             "channel": 48}
    },
    "rf-5G-5": {
        "5G":
            {'band': '5G',
             'country': 'US',
             'channel-mode': 'VHT',
             'channel-width': 40,
             "channel": 149}
    },
    "radius": False,
    "expected-throughput": {"0":200,"20":200,"40":200,"60":200,"80":200,"100":200,"120":200,"140":200,"160":200,
                            "180":200,"200":200,"220":200,"240":200,"260":200,"280":200,"300":200}
}


@allure.feature("RATE VS RANGE")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestCountryUS40Mhz5G(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.fourtyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel_36
    @pytest.mark.tcp_upload
    def test_client_wpa2_ch36_40Mhz_US_5g_tcp_upload(self, instantiate_profile, get_lf_logs,
                                                                  lf_test, update_report,
                                                                  station_names_fiveg, lf_tools,
                                                                  test_cases, testbed, al_1, get_configuration,
                                                                  create_lanforge_chamberview_dut, get_attenuators):
        """
           pytest -m "country_code and fourtyMhz and wpa2 and fiveg and channel149"
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
        pass_value=setup_params_general["expected-throughput"]
        atn=list(pass_value.keys())
        attenuations=list(''.join(l + ',' * (n % 1 == 0) for n, l in enumerate(atn)))
        attenuations1= attenuations[:len(attenuations) - 1]
        main_attenuations = ' '.join([str(elem) for elem in attenuations1])
        main_attenuations2=main_attenuations.replace(" ","")
        batch_size = 1
        lf_tools.reset_scenario()
        connected_attenuators, selected_attenuators = get_attenuators
        listToStr= ' '.join([str(elem) for elem in selected_attenuators])
        attenuator="1.1."+listToStr
        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        val = [['modes: Auto'], ['pkts: MTU'], ['directions: DUT Receive'], ['traffic_types:TCP'],
               ['bandw_options: AUTO'], ['spatial_streams: AUTO'], [f'attenuator: {attenuator}'],
               [f'attenuations: {main_attenuations2}'], ['chamber: 0'], ['tt_deg: 0']]

        if station:
            rvr_o = lf_test.ratevsrange(station_name=station_names_fiveg, mode=mode, download_rate="100%",
                                        duration='60000',
                                        instance_name="RVR_Channel_36_40_Mhz_Tcp_Fiveg_Mode",
                                        vlan_id=vlan, dut_name=lf_tools.dut_name, raw_lines=val, ssid_channel=channel)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            obj.get_channel_band(radio="5G")                #to recheck the AP configuration
            print("report name ", report_name)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries", entries)
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Rate vs Range Test")
            print("Test Completed... Cleaning up Stations")
            # lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            kpi = "kpi.csv"
            if kpi in entries:
                kpi_val = lf_tools.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
                print("KPI VALUE", kpi_val)
                if str(kpi_val) == "empty":
                    print("Throughput value from kpi.csv is empty, Test failed")
                    allure.attach(name="CSV Data", body="Throughput value from kpi.csv is empty, Test failed")
                    assert False, "Throughput value from kpi.csv is empty, Test failed"
                else:
                    allure.attach(name="CSV Data", body="Throughput value : " + str(kpi_val))
                    start, thrpt_val, pass_fail, passed_throughput, failed_throughput = 0, {}, [], [], []
                    for i in pass_value:
                        count = 0
                        direction = "DUT-RX"
                        for j in range(start, len(kpi_val), len(atn)):
                            thrpt_val[f"{atn[start]}--{direction}"] = kpi_val[j][0]
                            if kpi_val[j][0] == None:
                                print("KPI value is missing")
                            else:
                                print("PF VALUE THPT", thrpt_val[f"{atn[start]}--{direction}"])
                                print("PF VALUE THPT KPI", kpi_val[j][0])
                                if kpi_val[j][0] >= pass_value[i]:
                                    pass_fail.append("PASS")
                                    thpt = thrpt_val[f"{atn[start]}--{direction}"] = kpi_val[j][0]
                                    t = str(thpt) + "is more than " + str(pass_value[i])
                                    passed_throughput.append(str(t))
                                else:
                                    pass_fail.append("FAIL")
                                    thpt = thrpt_val[f"{atn[start]}--{direction}"] = kpi_val[j][0]
                                    t = str(thpt) + "is less than " + str(pass_value[i])
                                    failed_throughput.append(str(t))
                                count += 1
                                direction = "DUT-RX"
                            start += 1
                    print(pass_fail, "\nThroughput value-->", thrpt_val)
                    result = {
                        "result": None,
                        "ssid-name": ssid_name,
                        "security": security,
                        "security-key": security_key,
                        "band": band,
                        "channel": channel,
                        "description": "RvR capacity test",
                        "test-download": "0",
                        "test-upload": "1Gbps",
                        "test-batch-size": "1",
                        "test-upload-rate": "1",
                        "test-protocol": "UDP-IPV4",
                        "test-duration": "60 Sec",
                        "expected-throughput": pass_value,
                        "throughput-value": thrpt_val

                    }
                    if len(failed_throughput) >= 1:
                        print("LENGTH of Failed", len(failed_throughput))
                        pdf = lf_tools.create_rvr_dynamic_pdf(report_name, get_configuration, result)
                        print("Test failed due to lesser value")
                        if os.path.exists(pdf):
                            result["result"] = "FAIL"
                            allure.attach.file(source=pdf,
                                               name="Rate_Vs_Range_1GBPS_Upload_Throughput_UDP_Test",
                                               attachment_type="PDF")
                        allure.attach(name="FAILED:Throughput Results: ", body=str(
                            "Failed Throughputs are: " + str(failed_throughput)) + "Passed Throughputs: " + str(
                            passed_throughput))
                        assert False, "Test failed due to lesser value"
                    else:
                        print("LENGTH of Passed", len(passed_throughput))
                        result["result"] = "PASS"
                        pdf = lf_tools.create_rvr_dynamic_pdf(report_name, get_configuration, result)
                        print("Test passed successfully")
                        if os.path.exists(pdf):
                            allure.attach.file(source=pdf,
                                               name="Rate_Vs_Range_1GBPS_Upoad_Throughput_UDP_Test",
                                               attachment_type="PDF")
                        allure.attach(name="Passed:Throughput Results:",
                                      body=str("Passed Throughputs are :" + str(passed_throughput)))
                        assert True
            else:
                print("csv file does not exist, Test failed")
                allure.attach(name="CSV Data", body="csv file does not exist")
                assert False, "csv file does not exist"
        else:
            print("Test failed due to no station ip")
            assert False, "Test failed due to no station ip"

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.wpa2_personal
    @pytest.mark.fourtyMhz
    @pytest.mark.fiveg
    @pytest.mark.channel_149
    @pytest.mark.tcp_upload
    @pytest.mark.sg1234
    def test_client_wpa2_ch149_40Mhz_US_5g_tcp_upload(self, instantiate_profile, get_lf_logs,
                                                                  lf_test, update_report,
                                                                  station_names_fiveg, lf_tools,
                                                                  test_cases, testbed, al_1, get_configuration,create_lanforge_chamberview_dut,get_attenuators):
        """
           pytest -m "country_code and fourtyMhz and wpa2 and fiveg and channel149"
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
        pass_value = setup_params_general["expected-throughput"]
        print("PASSS VALLUES", pass_value)
        atn = pass_value.keys()
        atn=list(pass_value.keys())
        attenuations = list(''.join(l + ',' * (n % 1 == 0) for n, l in enumerate(atn)))
        attenuations1 = attenuations[:len(attenuations) - 2]
        main_attenuations = ' '.join([str(elem) for elem in attenuations1])
        main_attenuations2 = main_attenuations.replace(" ", "")
        batch_size = 1
        lf_tools.reset_scenario()
        connected_attenuators, selected_attenuators = get_attenuators
        print(f"connected_attenuators : {connected_attenuators}")
        print(f"selected_attenuators : {selected_attenuators}")
        listToStr = ' '.join([str(elem) for elem in selected_attenuators])
        attenuator = "1.1." + listToStr
        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        obj.check_and_set_ap_channel(radio="5G", band=channel_width, channel=channel)
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)
        # print("sta", station)
        # lf_tools.Chamber_View()
        val = [['modes: Auto'], ['pkts: MTU'], ['directions: DUT Receive'], ['traffic_types:TCP'],
               ['bandw_options: AUTO'], ['spatial_streams: AUTO'], [f'attenuator: {attenuator}'],
               [f'attenuations: {main_attenuations2}'], ['chamber: 0'], ['tt_deg: 0']]

        if station:
            rvr_o = lf_test.ratevsrange(station_name=station_names_fiveg, mode=mode, download_rate="100%",
                                        duration='60000',
                                        instance_name="RVR_Channel_149_40_Mhz_Tcp_Fiveg_Mode",
                                        vlan_id=vlan, dut_name=lf_tools.dut_name, raw_lines=val, ssid_channel=channel)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            print("report name ", report_name)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries", entries)
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Rate vs Range Test")
            print("Test Completed... Cleaning up Stations")
            # lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            kpi = "kpi.csv"
            if kpi in entries:
                kpi_val = lf_tools.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
                print("KPI VALUE", kpi_val)
                if str(kpi_val) == "empty":
                    print("Throughput value from kpi.csv is empty, Test failed")
                    allure.attach(name="CSV Data", body="Throughput value from kpi.csv is empty, Test failed")
                    assert False, "Throughput value from kpi.csv is empty, Test failed"
                else:
                    allure.attach(name="CSV Data", body="Throughput value : " + str(kpi_val))
                    start, thrpt_val, pass_fail, passed_throughput, failed_throughput = 0, {}, [], [], []
                    for i in pass_value:
                        count = 0
                        direction = "DUT-RX"
                        for j in range(start, len(kpi_val), len(atn)):
                            thrpt_val[f"{atn[start]}--{direction}"] = kpi_val[j][0]
                            if kpi_val[j][0] == None:
                                print("KPI value is missing")
                            else:
                                print("PF VALUE THPT", thrpt_val[f"{atn[start]}--{direction}"])
                                print("PF VALUE THPT KPI", kpi_val[j][0])
                                if kpi_val[j][0] >= pass_value[i]:
                                    pass_fail.append("PASS")
                                    thpt = thrpt_val[f"{atn[start]}--{direction}"] = kpi_val[j][0]
                                    t = str(thpt) + "is more than " + str(pass_value[i])
                                    passed_throughput.append(str(t))
                                else:
                                    pass_fail.append("FAIL")
                                    thpt = thrpt_val[f"{atn[start]}--{direction}"] = kpi_val[j][0]
                                    t = str(thpt) + "is less than " + str(pass_value[i])
                                    failed_throughput.append(str(t))
                                count += 1
                                direction = "DUT-RX"
                            start += 1
                    print(pass_fail, "\nThroughput value-->", thrpt_val)
                    result = {
                        "result": None,
                        "ssid-name": ssid_name,
                        "security": security,
                        "security-key": security_key,
                        "band": band,
                        "channel": channel,
                        "description": "RvR capacity test",
                        "test-download": "0",
                        "test-upload": "1Gbps",
                        "test-batch-size": "1",
                        "test-upload-rate": "1",
                        "test-protocol": "UDP-IPV4",
                        "test-duration": "60 Sec",
                        "expected-throughput": pass_value,
                        "throughput-value": thrpt_val

                    }
                    if len(failed_throughput) >= 1:
                        print("LENGTH of Failed", len(failed_throughput))
                        pdf = lf_tools.create_rvr_dynamic_pdf(report_name, get_configuration, result)
                        print("Test failed due to lesser value")
                        if os.path.exists(pdf):
                            result["result"] = "FAIL"
                            allure.attach.file(source=pdf,
                                               name="Rate_Vs_Range_1GBPS_Upload_Throughput_UDP_Test",
                                               attachment_type="PDF")
                        allure.attach(name="FAILED:Throughput Results: ", body=str(
                            "Failed Throughputs are: " + str(failed_throughput)) + "Passed Throughputs: " + str(
                            passed_throughput))
                        assert False, "Test failed due to lesser value"
                    else:
                        print("LENGTH of Passed", len(passed_throughput))
                        result["result"] = "PASS"
                        pdf = lf_tools.create_rvr_dynamic_pdf(report_name, get_configuration, result)
                        print("Test passed successfully")
                        if os.path.exists(pdf):
                            allure.attach.file(source=pdf,
                                               name="Rate_Vs_Range_1GBPS_Upoad_Throughput_UDP_Test",
                                               attachment_type="PDF")
                        allure.attach(name="Passed:Throughput Results:",
                                      body=str("Passed Throughputs are :" + str(passed_throughput)))
                        assert True
            else:
                print("csv file does not exist, Test failed")
                allure.attach(name="CSV Data", body="csv file does not exist")
                assert False, "csv file does not exist"
        else:
            print("Test failed due to no station ip")
            assert False, "Test failed due to no station ip"