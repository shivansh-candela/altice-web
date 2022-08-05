"""

    Client Connectivity and tcp-udp Traffic Test: nat Mode
    pytest -m "client_connectivity and nat and general"

"""

import allure
import pytest

pytestmark = [pytest.mark.altice_sanity]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [{"ssid_name": "client_connectivity_altice", "appliedRadios": ["2G"], "security_key": "something"},
                 {"ssid_name": "client_connectivity_altice", "appliedRadios": ["5G"],
                  "security_key": "something"}],
        "wpa": [{"ssid_name": "client_connectivity_altice", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "client_connectivity_altice", "appliedRadios": ["5G"],
                 "security_key": "something"}],
        "wpa2_personal": [
            {"ssid_name": "client_connectivity_altice", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "client_connectivity_altice", "appliedRadios": ["5G"],
             "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@pytest.mark.suiteA
@pytest.mark.sanity_ucentral
@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestNATModeConnectivitySuiteA(object):
    """ Client Connectivity SuiteA
        pytest -m "client_connectivity and nat and general and suiteA"
    """

    @pytest.mark.open
    @pytest.mark.twog
    @allure.story('open 2.4 GHZ Band')
    def test_open_ssid_2g(self, instantiate_profile, get_lf_logs,
                          lf_test, update_report,
                          station_names_twog,
                          test_cases, testbed, al_1, get_configuration):
        """Client Connectivity open ssid 2.4G
           pytest -m "client_connectivity and nat and general and open and twog"
        """

        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        ssid_name_2g = obj.get_ssid_details_2g()

        global setup_params_general

        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]

        print("ssid_name_2g: ",ssid_name_2g)
        if ssid_name != ssid_name_2g:
            obj.set_ssid_2g()

        ssid_security_2g = obj.get_ssid_sec_details_2g()
        print("ssid_security_2g: ",ssid_security_2g)
        if ssid_security_2g != "None":
            obj.set_ssid_sec_2g(sec="open")

        security_key = "[BLANK]"
        security = "open"
        mode = "NAT"
        band = "twog"
        vlan = 1

        # dut_name = create_lanforge_chamberview_dut
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)

        assert passes == "PASS", result


    @pytest.mark.open
    @pytest.mark.fiveg
    @allure.story('open 5 GHZ Band')
    def test_open_ssid_5g(self, instantiate_profile, get_lf_logs,
                          lf_test, update_report,
                          station_names_fiveg,
                          test_cases, testbed, al_1, get_configuration):
        """Client Connectivity open ssid 5G
           pytest -m "client_connectivity and nat and general and open and fiveg"
        """

        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        ssid_name_5g = obj.get_ssid_details_5g()

        global setup_params_general

        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]

        print("ssid_name_5g: ",ssid_name_5g)
        if ssid_name != ssid_name_5g:
            obj.ssid_name_5g()

        ssid_security_5g = obj.get_ssid_sec_details_5g()
        print("ssid_security_5g: ",ssid_security_5g)
        if ssid_security_5g != "None":
            obj.set_ssid_sec_5g(sec="open")

        security_key = "[BLANK]"
        security = "open"
        mode = "NAT"
        band = "fiveg"

        vlan = 1

        # dut_name = create_lanforge_chamberview_dut
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.sanity_light
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @allure.story('wpa2_personal 2.4 GHZ Band')
    def test_wpa2_personal_ssid_2g(self, instantiate_profile, get_lf_logs,
                          lf_test, update_report,
                          station_names_twog,
                          test_cases, testbed, al_1, get_configuration):
        """Client Connectivity wpa2_personal ssid 2.4G
           pytest -m "client_connectivity and NAT and general and wpa2_personal and twog"
        """
        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        ssid_name_2g = obj.get_ssid_details_2g()

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "twog"
        vlan = 1

        print("ssid_name_2g: ", ssid_name_2g)
        if ssid_name != ssid_name_2g:
            obj.set_ssid_2g()

        ssid_security_2g = obj.get_ssid_sec_details_2g()
        print("ssid_security_2g: ", ssid_security_2g)

        if ssid_security_2g != "WPA2-Personal":
            obj.set_ssid_sec_2g(sec="wpa2_personal")

        # dut_name = create_lanforge_chamberview_dut
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)

        assert passes == "PASS", result

    @pytest.mark.sanity_light
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @allure.story('wpa2_personal 5 GHZ Band')
    def test_wpa2_personal_ssid_5g(self, instantiate_profile, get_lf_logs,
                          lf_test, update_report,
                          station_names_fiveg,
                          test_cases, testbed, al_1, get_configuration):
        """Client Connectivity wpa2_personal ssid 5G
           pytest -m "client_connectivity and NAT and general and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"

        vlan = 1

        obj = instantiate_profile(get_configuration['access_point'][0], "../libs/apnos/", "2.x")
        ssid_name_5g = obj.get_ssid_details_5g()

        print("ssid_name_2g: ", ssid_name_5g)
        if ssid_name != ssid_name_5g:
            obj.set_ssid_5g()

        ssid_security_5g = obj.get_ssid_sec_details_5g()
        print("ssid_security_5g: ", ssid_security_5g)

        if ssid_security_5g != "WPA2-Personal":
            obj.set_ssid_sec_5g(sec="wpa2_personal")

        # dut_name = create_lanforge_chamberview_dut
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)

        assert passes == "PASS", result