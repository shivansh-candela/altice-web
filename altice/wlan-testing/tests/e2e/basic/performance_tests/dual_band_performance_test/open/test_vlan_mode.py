"""
       Dual Band Performance Test : VLAN Mode
       pytest -m "performance and dual_band_test and VLAN"


"""

import os
import allure
import pytest

pytestmark = [pytest.mark.dual_band_test, pytest.mark.vlan, pytest.mark.performance_release]#,
#              pytest.mark.usefixtures("setup_test_run")]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [
            {"ssid_name": "ssid_openp_2g", "appliedRadios": ["2G", "5G"], "security_key": "something"}
            ]},
    "rf": {},
    "radius": False
}


@pytest.mark.dual_band_test
@pytest.mark.wifi5
@pytest.mark.wifi6
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestDualbandPerformanceVLAN(object):
    """
         pytest -m "performance and dual_band_test and vlan and open and twog  and fiveg"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3724", name="WIFI-3724")
    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.fiveg
    def test_client_open_vlan(self, get_vif_state, lf_tools,
                                  create_lanforge_chamberview_dut, lf_test, get_configuration):
        profile_data = setup_params_general["ssid_modes"]["open"]
        ssid_2G = profile_data[0]["ssid_name"]
        ssid_5G = profile_data[0]["ssid_name"]
        dut_name = create_lanforge_chamberview_dut
        mode = "VLAN"
        vlan = 100
        print(lf_tools.dut_idx_mapping)
        dut_5g = ""
        dut_2g = ""
        for i in lf_tools.dut_idx_mapping:
            if lf_tools.dut_idx_mapping[i][3] == "5G":
                dut_5g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_5g)
            if lf_tools.dut_idx_mapping[i][3] == "2G":
                dut_2g = dut_name + ' ' + lf_tools.dut_idx_mapping[i][0] + ' ' + lf_tools.dut_idx_mapping[i][4]
                print(dut_2g)
        if ssid_2G and ssid_5G not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID's NOT AVAILABLE IN VIF STATE")

        dbpt_obj = lf_test.dualbandperformancetest(mode=mode, ssid_2G=ssid_2G, ssid_5G=ssid_5G,
                                                   instance_name="dbp_instance_openp_VLAN_p",
                                                   vlan_id=vlan, dut_5g=dut_5g, dut_2g=dut_2g)
        report_name = dbpt_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
        lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Dual Band Performance Test Open Security Vlan Mode")
        assert True