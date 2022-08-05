"""

    Client Connectivity and tcp-udp Traffic Test: Bridge Mode
    pytest -m "client_connectivity and bridge and general"

"""

import allure
import pytest

pytestmark = [pytest.mark.client_connectivity,  pytest.mark.cli]

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


@allure.suite(suite_name="Altice Sanity LF")
@allure.sub_suite(sub_suite_name="Nat Mode Client Connectivity : Suite-A")
@pytest.mark.suiteA
@pytest.mark.sudo
@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles_generic',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles_generic")
class TestBridgeModeConnectivitySuiteA(object):
    """ Client Connectivity SuiteA
        pytest -m "client_connectivity and bridge and general and suiteA"
    """

    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.altice_2g
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2809", name="JIRA LINK")
    def test_open_ssid_2g(self, lf_test, station_names_twog, set_ap_channel_and_band, get_ap_channel_generic):
        """Client Connectivity open ssid 2.4G
           pytest -m "client_connectivity and bridge and general and open and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "NAT"
        band = "twog"
        channel = get_ap_channel_generic[0]["2G"]
        print("ssid channel:- ", channel)
        vlan = 1
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result

    @pytest.mark.open
    @pytest.mark.fiveg
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2801", name="JIRA LINK")
    def test_open_ssid_5g(self, lf_test, station_names_fiveg, get_ap_channel_generic):
        """Client Connectivity open ssid 5G
           pytest -m "client_connectivity and bridge and general and open and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "NAT"
        band = "fiveg"
        channel = get_ap_channel_generic[0]["5G"]
        print("ssid channel:- ", channel)
        vlan = 1
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan, ssid_channel=channel)

        assert passes == "PASS", result

