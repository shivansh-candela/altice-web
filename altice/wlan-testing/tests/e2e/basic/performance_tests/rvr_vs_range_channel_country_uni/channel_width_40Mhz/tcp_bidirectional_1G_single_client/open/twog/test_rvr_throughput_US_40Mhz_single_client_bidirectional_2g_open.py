import os
import pytest
import allure
import time

pytestmark = [pytest.mark.country_code, pytest.mark.nat, pytest.mark.open, pytest.mark.united_states,
              pytest.mark.bandwidth_40mhz, pytest.mark.al, pytest.mark.tcp, pytest.mark.rate_vs_range,
              pytest.mark.bidirectional, pytest.mark.tcp_bidirectional,
              pytest.mark.rate_vs_range_open_40mhz_all_channels_single_client_bidirectional_1gbps,
              pytest.mark.rate_vs_range_throughput_open_40mhz_all_channels_single_client_bidirectional_1gbps, pytest.mark.twog, pytest.mark.tcp]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [
            {"ssid_name": "client_connectivity_al", "appliedRadios": ["5G"], "security_key":["BLANK"]}
        ]
    },

    "rf-2G-1": {
        "2G":
            {'band': '2G',
             'country': 'US',
             "channel-mode": "VHT",
             'channel-width': 40,
             "channel": 1}
    },
    "rf-2G-2": {
        "2G":
            {'band': '2G',
             'country': 'US',
             'channel-mode': 'VHT',
             'channel-width': 40,
             "channel": 6}
    },
    "rf-2G-3": {
        "2G":
            {'band': '2G',
             'country': 'US',
             'channel-mode': 'VHT',
             'channel-width': 40,
             "channel": 11}
    },
    "radius": False,
    "expected-throughput":{"0":200,"20":200,"40":200,"60":200,"80":200,"100":200,"120":200,"140":200,"160":200,
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
class TestCountryUS40Mhz2G(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.open
    @pytest.mark.fourtyMhz
    @pytest.mark.twog
    @pytest.mark.channel_1
    @pytest.mark.tcp_bidirectional
    def test_client_open_ch1_40Mhz_US_2g_tcp_bidirectional(self, instantiate_profile, get_lf_logs,
                                                                  lf_test, update_report,
                                                                  station_names_twog, lf_tools,
                                                                  test_cases, testbed, al_1, get_configuration,
                                                                  create_lanforge_chamberview_dut, get_attenuators):
        """
           pytest -m "country_code and twentyMhz and open and twog and channel149"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "open"
        mode = "NAT"
        band = "twog"
        vlan = 1
        channel = setup_params_general['rf-2G-1']['2G']['channel']
        channel_width = setup_params_general['rf-2G-1']['2G']['channel-width']
        pass_value=setup_params_general["expected-throughput"]
        print("PASSS VALLUES",pass_value)
        atn=pass_value.keys()
        atn = list(pass_value.keys())
        attenuations=list(''.join(l + ',' * (n % 1 == 0) for n, l in enumerate(atn)))
        attenuations1= attenuations[:len(attenuations) - 1]
        main_attenuations = ' '.join([str(elem) for elem in attenuations1])
        main_attenuations2=main_attenuations.replace(" ","")
        batch_size = 1
        lf_tools.reset_scenario()
        connected_attenuators, selected_attenuators = get_attenuators
        print(f"connected_attenuators : {connected_attenuators}")
        print(f"selected_attenuators : {selected_attenuators}")
        listToStr= ' '.join([str(elem) for elem in selected_attenuators])
        attenuator="1.1."+listToStr
        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        obj.check_and_set_ap_channel(radio="2G", band=channel_width, channel=channel)
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)
        # print("sta", station)
        # lf_tools.Chamber_View()
        val = [['modes: 802.11bgn-AX'], ['pkts: MTU'], ['directions: DUT Transmit;DUT Receive'], ['traffic_types:TCP'],
               ['bandw_options: AUTO'], ['spatial_streams: AUTO'], [f'attenuator: {attenuator}'],
               [f'attenuations: {main_attenuations2}'], ['chamber: 0'], ['tt_deg: 0']]

        if station:
            # print("TEstcase channel", channel)
            rvr_o = lf_test.ratevsrange(station_name=station_names_twog, mode=mode, download_rate="100%",upload_rate="100%",
                                        duration='60000',
                                        instance_name="RVR_Channel_1_40_Mhz_Tcp_Twog_Mode",
                                        vlan_id=vlan, dut_name=lf_tools.dut_name, raw_lines=val, ssid_channel=channel)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            obj.get_channel_band(radio="2G")                #to recheck the AP configuration
            print("report name ", report_name)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries", entries)
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Rate vs Range Test")
            print("Test Completed... Cleaning up Stations")
            # lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            kpi = "kpi.csv"
            # pass_value = {"0": 100, "2": 95, "4": 90, "6": 100, "8": 95, "10": 90}
            # atn = [0, 2, 4, 6, 8, 10]
            # pass_value = {"1": 100, "2": 95, "3": 90, "4": 90, "5": 90, "6": 90, "7": 90, "8": 90, "9": 90, "10": 90,
            #               "11": 90, "12": 90, "13": 90, "14": 90, "15": 90, "16": 90, "17": 90, "18": 90, "19": 90,
            #               "20": 90, "21": 90, "22": 90, "23": 90, "24": 90, "25": 90, "26": 90, "27": 90, "28": 90,
            #               "29": 90, "30": 90}
            # atn = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50,
            #        52, 54, 56, 58, 60, 62, 64, 66, 68, 70]
            if kpi in entries:
                kpi_val = lf_tools.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
                print("KPI VALUE", kpi_val)
                if str(kpi_val) == "empty":
                    print("Throughput value from kpi.csv is empty, Test failed")
                    allure.attach(name="CSV Data", body="Throughput value from kpi.csv is empty, Test failed")
                    assert False, "Throughput value from kpi.csv is empty, Test failed"
                else:
                    allure.attach(name="CSV Data", body="Throughput value : " + str(kpi_val))
                    start, thrpt_val, pass_fail = 0, {}, []
                    for i in pass_value:
                        count = 0
                        direction = "DUT-TX"
                        for j in range(start, len(kpi_val), len(atn)):
                            thrpt_val[f"{atn[start]}--{direction}"] = kpi_val[j][0]
                            if kpi_val[j][0] == None:
                                print("KPI value is missing")
                            else:
                                if kpi_val[j][0] >= pass_value[i]:
                                    pass_fail.append("PASS")
                                else:
                                    pass_fail.append("FAIL")
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
                        "test-download": "1Gbps",
                        "test-upload": "1Gbps",
                        "test-batch-size": "1",
                        "test-upload-rate": "1",
                        "test-protocol": "TCP-IPV4",
                        "test-duration": "60 Sec",
                        "expected-throughput": pass_value,
                        "throughput-value": thrpt_val

                    }
                    if "FAIL" in pass_fail:
                        pdf = lf_tools.create_rvr_dynamic_pdf(report_name, get_configuration, result)
                        print("Test failed due to lesser value")
                        if os.path.exists(pdf):
                            result["result"] = "FAIL"
                            allure.attach.file(source=pdf,
                                               name="Rate_Vs_Range_1GBPS_bidirectional_Throughput_TCP_40Mhz_open_2g_Test",
                                               attachment_type="PDF")
                        allure.attach(name="FAILED:Throughput Results:", body=str(
                            "Actual throughput:"))
                        assert False, "Test failed due to lesser value"
                    else:
                        result["result"] = "PASS"
                        pdf = lf_tools.create_rvr_dynamic_pdf(report_name, get_configuration, result)
                        print("Test passed successfully")
                        if os.path.exists(pdf):
                            allure.attach.file(source=pdf,
                                               name="Rate_Vs_Range_1GBPS_bidirectional_Throughput_TCP_40Mhz_open_2g_Test",
                                               attachment_type="PDF")
                        allure.attach(name="FAILED:Throughput Results:", body=str(
                            "Actual throughput:"))
                        assert True
            else:
                print("csv file does not exist, Test failed")
                allure.attach(name="CSV Data", body="csv file does not exist")
                assert False, "csv file does not exist"
        else:
            print("Test failed due to no station ip")
            assert False, "Test failed due to no station ip"

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.open
    @pytest.mark.fourtyMhz
    @pytest.mark.twog
    @pytest.mark.channel_6
    @pytest.mark.tcp_bidirectional
    def test_client_open_ch6_40Mhz_US_2g_tcp_bidirectional(self, instantiate_profile, get_lf_logs,
                                                                  lf_test, update_report,
                                                                  station_names_twog, lf_tools,
                                                                  test_cases, testbed, al_1, get_configuration,create_lanforge_chamberview_dut, get_attenuators):
        """
           pytest -m "country_code and twentyMhz and open and twog and channel149"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "open"
        mode = "NAT"
        band = "twog"
        vlan = 1
        channel = setup_params_general['rf-2G-2']['2G']['channel']
        channel_width = setup_params_general['rf-2G-2']['2G']['channel-width']
        pass_value = setup_params_general["expected-throughput"]
        print("PASSS VALLUES", pass_value)
        atn = pass_value.keys()
        atn = list(pass_value.keys())
        attenuations = list(''.join(l + ',' * (n % 1 == 0) for n, l in enumerate(atn)))
        attenuations1 = attenuations[:len(attenuations) - 1]
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
        obj.check_and_set_ap_channel(radio="2G", band=channel_width, channel=channel)
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)
        # print("sta", station)
        # lf_tools.Chamber_View()
        val = [['modes: 802.11bgn-AX'], ['pkts: MTU'], ['directions: DUT Transmit;DUT Receive'], ['traffic_types:TCP'],
               ['bandw_options: AUTO'], ['spatial_streams: AUTO'], [f'attenuator: {attenuator}'],
               [f'attenuations: {main_attenuations2}'], ['chamber: 0'], ['tt_deg: 0']]

        if station:
            rvr_o = lf_test.ratevsrange(station_name=station_names_twog, mode=mode, download_rate="100%",upload_rate="100%",
                                        duration='60000',
                                        instance_name="RVR_Channel_6_40_Mhz_Tcp_Twog_Mode",
                                        vlan_id=vlan, dut_name=lf_tools.dut_name, raw_lines=val, ssid_channel=channel)
            report_name = rvr_o.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            print("report name ", report_name)
            entries = os.listdir("../reports/" + report_name + '/')
            print("entries", entries)
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Rate vs Range Test")
            print("Test Completed... Cleaning up Stations")
            # lf_test.Client_disconnect(clear_all_sta=True, clean_l3_traffic=True)
            kpi = "kpi.csv"
            # pass_value = {"1": 100, "2": 95, "3": 90, "4": 90, "5": 90, "6": 90, "7": 90, "8": 90, "9": 90, "10": 90,
            #               "11": 90, "12": 90, "13": 90, "14": 90, "15": 90, "16": 90, "17": 90, "18": 90, "19": 90,
            #               "20": 90, "21": 90, "22": 90, "23": 90, "24": 90, "25": 90, "26": 90, "27": 90, "28": 90,
            #               "29": 90, "30": 90}
            # atn = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50,
            #        52, 54, 56, 58, 60, 62, 64, 66, 68, 70]
            if kpi in entries:
                kpi_val = lf_tools.read_kpi_file(column_name=["numeric-score"], dir_name=report_name)
                print(kpi_val)
                if str(kpi_val) == "empty":
                    print("Throughput value from kpi.csv is empty, Test failed")
                    allure.attach(name="CSV Data", body="Throughput value from kpi.csv is empty, Test failed")
                    assert False, "Throughput value from kpi.csv is empty, Test failed"
                else:
                    allure.attach(name="CSV Data", body="Throughput value : " + str(kpi_val))
                    start, thrpt_val, pass_fail = 0, {}, []
                    for i in pass_value:
                        # count = 0
                        direction = "DUT-TX"
                        for j in range(start, len(kpi_val), len(atn)):
                            thrpt_val[f"{atn[start]}--{direction}"] = kpi_val[j][0]
                            if kpi_val[j][0] >= pass_value[i]:
                                pass_fail.append("PASS")
                            else:
                                pass_fail.append("FAIL")
                            # count += 1
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
                        "test-download": "1Gbps",
                        "test-upload": "1Gbps",
                        "test-batch-size": "1",
                        "test-upload-rate": "1",
                        "test-protocol": "TCP-IPV4",
                        "test-duration": "60 Sec",
                        "expected-throughput": pass_value,
                        "throughput-value": thrpt_val

                    }
                    if "FAIL" in pass_fail:
                        pdf = lf_tools.create_rvr_dynamic_pdf(report_name, get_configuration, result)
                        print("Test failed due to lesser value")
                        if os.path.exists(pdf):
                            result["result"] = "FAIL"
                            allure.attach.file(source=pdf,
                                               name="Rate_Vs_Range_1GBPS_bidirectional_Throughput_TCP_40Mhz_open_2g_Test",
                                               attachment_type="PDF")
                        allure.attach(name="FAILED:Throughput Results:", body=str(
                            "Actual throughput:"))
                        assert False, "Test failed due to lesser value"
                    else:
                        result["result"] = "PASS"
                        pdf = lf_tools.create_rvr_dynamic_pdf(report_name, get_configuration, result)
                        print("Test passed successfully")
                        if os.path.exists(pdf):
                            allure.attach.file(source=pdf,
                                               name="Rate_Vs_Range_1GBPS_bidirectional_Throughput_TCP_40Mhz_open_2g_Test",
                                               attachment_type="PDF")
                        allure.attach(name="FAILED:Throughput Results:", body=str(
                            "Actual throughput:"))
                        assert True
            else:
                print("csv file does not exist, Test failed")
                allure.attach(name="CSV Data", body="csv file does not exist")
                assert False, "csv file does not exist"
        else:
            print("Test failed due to no station ip")
            assert False, "Test failed due to no station ip"

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2546", name="WIFI-6938")
    @pytest.mark.open
    @pytest.mark.fourtyMhz
    @pytest.mark.twog
    @pytest.mark.channel_11
    @pytest.mark.tcp_bidirectional
    
    def test_client_open_ch11_40Mhz_US_2g_tcp_bidirectional(self, instantiate_profile, get_lf_logs,
                                                            lf_test, update_report,
                                                            station_names_twog, lf_tools,
                                                            test_cases, testbed, al_1, get_configuration,
                                                            create_lanforge_chamberview_dut, get_attenuators):
        """
           pytest -m "country_code and twentyMhz and open and twog and channel149"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "open"
        mode = "NAT"
        band = "twog"
        vlan = 1
        channel = setup_params_general['rf-2G-3']['2G']['channel']
        channel_width = setup_params_general['rf-2G-3']['2G']['channel-width']
        pass_value = setup_params_general["expected-throughput"]
        print("PASSS VALLUES", pass_value)
        atn = pass_value.keys()
        atn = list(pass_value.keys())
        attenuations = list(''.join(l + ',' * (n % 1 == 0) for n, l in enumerate(atn)))
        attenuations1 = attenuations[:len(attenuations) - 1]
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
        obj.check_and_set_ap_channel(radio="2G", band=channel_width, channel=channel)
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)
        val = [['modes: 802.11bgn-AX'], ['pkts: MTU'], ['directions: DUT Transmit;DUT Receive'], ['traffic_types:TCP'],
               ['bandw_options: AUTO'], ['spatial_streams: AUTO'], [f'attenuator: {attenuator}'],
               [f'attenuations: {main_attenuations2}'], ['chamber: 0'], ['tt_deg: 0']]

        if station:
            rvr_o = lf_test.ratevsrange(station_name=station_names_twog, mode=mode, download_rate="100%",upload_rate="100%",
                                        duration='60000',
                                        instance_name="RVR_Channel_11_40_Mhz_Tcp_Twog_Mode",
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
                print(kpi_val)
                if str(kpi_val) == "empty":
                    print("Throughput value from kpi.csv is empty, Test failed")
                    allure.attach(name="CSV Data", body="Throughput value from kpi.csv is empty, Test failed")
                    assert False, "Throughput value from kpi.csv is empty, Test failed"
                else:
                    allure.attach(name="CSV Data", body="Throughput value : " + str(kpi_val))
                    start, thrpt_val, pass_fail = 0, {}, []
                    for i in pass_value:
                        # count = 0
                        direction = "DUT-TX"
                        for j in range(start, len(kpi_val), len(atn)):
                            thrpt_val[f"{atn[start]}--{direction}"] = kpi_val[j][0]
                            if kpi_val[j][0] >= pass_value[i]:
                                pass_fail.append("PASS")
                            else:
                                pass_fail.append("FAIL")
                            # count += 1
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
                        "test-download": "1Gbps",
                        "test-upload": "1Gbps",
                        "test-batch-size": "1",
                        "test-upload-rate": "1",
                        "test-protocol": "TCP-IPV4",
                        "test-duration": "60 Sec",
                        "expected-throughput": pass_value,
                        "throughput-value": thrpt_val

                    }
                    if "FAIL" in pass_fail:
                        pdf = lf_tools.create_rvr_dynamic_pdf(report_name, get_configuration, result)
                        print("Test failed due to lesser value")
                        if os.path.exists(pdf):
                            result["result"] = "FAIL"
                            allure.attach.file(source=pdf,
                                               name="Rate_Vs_Range_1GBPS_bidirectional_Throughput_TCP_40Mhz_open_2g_Test",
                                               attachment_type="PDF")
                        allure.attach(name="FAILED:Throughput Results:", body=str(
                            "Actual throughput:"))
                        assert False, "Test failed due to lesser value"
                    else:
                        result["result"] = "PASS"
                        pdf = lf_tools.create_rvr_dynamic_pdf(report_name, get_configuration, result)
                        print("Test passed successfully")
                        if os.path.exists(pdf):
                            allure.attach.file(source=pdf,
                                               name="Rate_Vs_Range_1GBPS_bidirectional_Throughput_TCP_40Mhz_open_2g_Test",
                                               attachment_type="PDF")
                        allure.attach(name="FAILED:Throughput Results:", body=str(
                            "Actual throughput:"))
                        assert True
            else:
                print("csv file does not exist, Test failed")
                allure.attach(name="CSV Data", body="csv file does not exist")
                assert False, "csv file does not exist"
        else:
            print("Test failed due to no station ip")
            assert False, "Test failed due to no station ip"