import json
import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)
if "libs" not in sys.path:
    sys.path.append(f'../libs')

from controller.controller_1x.controller import ProfileUtility
from controller.controller_2x.controller import UProfileUtility
from controller.controller_3x.controller import CController
from controller.controller_4x.controller import AController
import time
from lanforge.lf_tools import ChamberView
import pytest
import allure


@pytest.fixture(scope="session")
def instantiate_profile(request):
    if request.config.getoption("1.x"):
        yield ProfileUtility
    elif request.config.getoption("cc.1"):
        yield CController
    elif request.config.getoption("al.1"):
        yield AController
    else:
        yield UProfileUtility


@pytest.fixture(scope="session")
def create_lanforge_chamberview(lf_tools):
    scenario_object, scenario_name = lf_tools.Chamber_View()
    return scenario_name


@pytest.fixture(scope="session")
def create_lanforge_chamberview_dut(lf_tools, run_lf):
    if not run_lf:
        dut_object, dut_name = lf_tools.Create_Dut()
        return dut_name
    return ""


@pytest.fixture(scope="class")
def setup_profiles(request, setup_controller, testbed, get_equipment_ref, fixtures_ver, reset_scenario_lf,
                   instantiate_profile, get_markers, create_lanforge_chamberview_dut, lf_tools, run_lf,
                   get_security_flags, get_configuration, radius_info, get_apnos, radius_accounting_info, cc_1, al_1, get_all_markers):
    param = dict(request.param)

    # VLAN Setup
    if request.param["mode"] == "VLAN":

        vlan_list = list()
        refactored_vlan_list = list()
        ssid_modes = request.param["ssid_modes"].keys()
        for mode in ssid_modes:
            for ssid in range(len(request.param["ssid_modes"][mode])):
                if "vlan" in request.param["ssid_modes"][mode][ssid]:
                    vlan_list.append(request.param["ssid_modes"][mode][ssid]["vlan"])
                else:
                    pass
        if vlan_list:
            [refactored_vlan_list.append(x) for x in vlan_list if x not in refactored_vlan_list]
            vlan_list = refactored_vlan_list
            for i in range(len(vlan_list)):
                if vlan_list[i] > 4095 or vlan_list[i] < 1:
                    vlan_list.pop(i)
    if request.param["mode"] == "VLAN":
        lf_tools.reset_scenario()
        lf_tools.add_vlan(vlan_ids=vlan_list)

    # call this, if 1.x
    print("fixture version ", fixtures_ver)
    if cc_1:
        return_var = fixtures_ver.setup_profiles(request, param, run_lf, instantiate_profile, get_configuration, get_markers, lf_tools)
    elif al_1:
        return_var = fixtures_ver.setup_profiles(request, param, run_lf, instantiate_profile, get_configuration,
                                                 get_markers, testbed, lf_tools, get_all_markers)
    else:
        return_var = fixtures_ver.setup_profiles(request, param, setup_controller, testbed, get_equipment_ref,
                                             instantiate_profile,
                                             get_markers, create_lanforge_chamberview_dut, lf_tools,
                                             get_security_flags, get_configuration, radius_info, get_apnos,
                                             radius_accounting_info, run_lf=run_lf)

    yield return_var


@pytest.fixture(scope="session")
def station_names_twog(request, get_configuration):
    station_names = []
    for i in range(0, int(request.config.getini("num_stations"))):
        station_names.append(get_configuration["traffic_generator"]["details"]["2.4G-Station-Name"] + "0" + str(i))
    yield station_names


@pytest.fixture(scope="session")
def station_names_fiveg(request, get_configuration):
    station_names = []
    for i in range(0, int(request.config.getini("num_stations"))):
        station_names.append(get_configuration["traffic_generator"]["details"]["5G-Station-Name"] + "0" + str(i))
    yield station_names


@pytest.fixture(scope="session")
def station_names_ax(request, get_configuration):
    station_names = []
    for i in range(0, int(request.config.getini("num_stations"))):
        station_names.append(get_configuration["traffic_generator"]["details"]["AX-Station-Name"] + "0" + str(i))
    yield station_names


@pytest.fixture(scope="session")
def num_stations(request):
    num_sta = int(request.config.getini("num_stations"))
    yield num_sta


@pytest.fixture(scope="class")
def get_vif_state(get_apnos, get_configuration, request, lf_tools, run_lf):
    if request.config.getoption("1.x"):
        ap_ssh = get_apnos(get_configuration['access_point'][0], pwd="../libs/apnos/", sdk="1.x")
        vif_state = list(ap_ssh.get_vif_state_ssids())
        vif_state.sort()
        yield vif_state
    else:
        yield lf_tools.ssid_list


@pytest.fixture(scope="session")
def dfs_start(fixtures_ver, get_apnos, get_configuration):
    dfs_start = fixtures_ver.dfs(get_apnos, get_configuration)
    yield dfs_start


@pytest.fixture(scope="class")
def get_vlan_list(get_apnos, get_configuration):
    ap_ssh = get_apnos(get_configuration['access_point'][0], pwd="../libs/apnos/")
    vlan_list = list(ap_ssh.get_vlan())
    vlan_list.sort()
    yield vlan_list


@pytest.fixture(scope="session")
def reset_scenario_lf(request, lf_tools, run_lf):
    if not run_lf:
        lf_tools.reset_scenario()
        def teardown_session():
            lf_tools.reset_scenario()

        request.addfinalizer(teardown_session)
    yield ""
