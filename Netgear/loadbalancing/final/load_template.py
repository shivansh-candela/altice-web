
from datetime import datetime

import os.path
from os import path
import sys

print(sys.path)
sys.path.append('/home/lanforge/.local/lib/python3.6/site-packages')
import pdfkit

def report_banner(date):
    banner_data = """
                   <!DOCTYPE html>
                    <html lang='en'>
                    <head>
                    <meta charset='UTF-8'>
                    <meta name='viewport' content='width=device-width, initial-scale=1' />
                    <title>LANforge Report</title>                        

                    </head>

                    <title>LOAD BALANCING TEST</title></head>
                    <body>
                    <div class='Section report_banner-1000x205' style='background-image:url("/home/lanforge/LANforgeGUI_5.4.3/images/report_banner-1000x205.jpg");background-repeat:no-repeat;padding:0;margin:0;min-width:1000px; min-height:205px;width:1000px; height:205px;max-width:1000px; max-height:205px;'>
                    <br>
                    <img align='right' style='padding:25;margin:5;width:200px;' src="/home/lanforge/LANforgeGUI_5.4.3/images/CandelaLogo2-90dpi-200x90-trans.png" border='0' />


                    <div class='HeaderStyle'>
                    <br>
                    <h1 class='TitleFontPrint' style='color:darkgreen;'>  Load Balancing Test  </h1>
                    <h3 class='TitleFontPrint' style='color:darkgreen;'>""" + date + """</h3>
                    </div>
                    </div>

                    <br><br>

                 """
    return str(banner_data)

def test_objective(objective="The LOAD BALANCING Test is designed to test the Performance of the Netgear Access Point.The goal of this test is to make sure that the AP is able to successfully admit or not admit clients based on certain user set thresholds as RSSI Threshold, Channel Utilization Threshold and  Max Client Threshold "):
    test_objective = """
                    <!-- Test Objective -->
                    <h3 align='left'>Objective</h3> 
                    <p align='left' width='900'>""" + str(objective) + """</p>
                    <br>
                    """
    return str(test_objective)

def add_summary_table(pass_fail_dict = None):
    """pass_fail_dict = {'Client': {'2.4G': 'PASS', '5G_low': 'PASS', '5G_high': 'PASS'},
                      'Utilization': {'2.4G': 'FAIL', '5G_low': 'FAIL', '5G_high': 'FAIL'},
                      'Rssi': {'2.4G': 'FAIL', '5G_low': 'FAIL', '5G_high': 'FAIL'}}"""
    column_head_list = []
    for i in list(pass_fail_dict.keys()):
        if i == "Client":
            column_head_list.append("Client Count Threshold")
        elif i == "Utilization":
            column_head_list.append("Channel Utilization Threshold")
        elif i == "Rssi":
            column_head_list.append("RSSI Threshold")
    var_row = "<th></th>"
    for row in column_head_list:
        var_row = var_row + "<th>" + row + "</th>"

    summary2 = []
    summary5l = []
    summary5h = []
    # print(list(pass_fail_dict["Client"]))
    if "Client" in list(pass_fail_dict.keys()):
        if "2.4G" in list(pass_fail_dict["Client"]):
            summary2.append(pass_fail_dict["Client"]["2.4G"])
        if "5G_low" in list(pass_fail_dict["Client"]):
            summary5l.append(pass_fail_dict["Client"]["5G_low"])
        if "5G_high" in pass_fail_dict["Client"]:
            summary5h.append(pass_fail_dict["Client"]["5G_high"])
    if "Utilization" in list(pass_fail_dict.keys()):
        if "2.4G" in list(pass_fail_dict["Utilization"]):
            summary2.append(pass_fail_dict["Utilization"]["2.4G"])
        if "5G_low" in list(pass_fail_dict["Utilization"]):
            summary5l.append(pass_fail_dict["Utilization"]["5G_low"])
        if "5G_high" in pass_fail_dict["Utilization"]:
            summary5h.append(pass_fail_dict["Utilization"]["5G_high"])
    if "Rssi" in list(pass_fail_dict.keys()):
        if "2.4G" in list(pass_fail_dict["Rssi"]):
            summary2.append(pass_fail_dict["Rssi"]["2.4G"])
        if "5G_low" in list(pass_fail_dict["Rssi"]):
            summary5l.append(pass_fail_dict["Rssi"]["5G_low"])
        if "5G_high" in pass_fail_dict["Rssi"]:
            summary5h.append(pass_fail_dict["Rssi"]["5G_high"])

    #print(summary2)
    #print(summary5l)
    #print(summary5h)

    var = ""
    for i in summary2:
        if i == "FAIL":
            var = var + "<td colspan='1' bgcolor='orange'>FAIL</td>"
        else:
            var = var + "<td colspan='1' bgcolor='#90EE90'>PASS</td>"
    var1 = ""
    for i in summary5l:
        if i == "FAIL":
            var1 = var1 + "<td colspan='1' bgcolor='orange'>FAIL</td>"
        else:
            var1 = var1 + "<td colspan='1' bgcolor='#90EE90'>PASS</td>"
    var2 = ""
    for i in summary5h:
        if i == "FAIL":
            var2 = var2 + "<td colspan='1' bgcolor='orange'>FAIL</td>"
        else:
            var2 = var2 + "<td colspan='1' bgcolor='#90EE90'>PASS</td>"
    val = ""
    if "Client" in list(pass_fail_dict.keys()):
        val = "Client"
    elif "Utilization " in list(pass_fail_dict.keys()):
        val = "Utilization"
    elif "Rssi" in list(pass_fail_dict.keys()):
        val = "Rssi"
    var_col = ""
    for col in list(pass_fail_dict[val]):
        if col == "2.4G":
            var_col = var_col + "<tr><th>" + str(col) + "</th>" + str(var) + "</tr>"
        if col == "5G_low":
            var_col = var_col + "<tr><th>" + str(col) + "</th>" + str(var1) + "</tr>"
        if col == "5G_high":
            var_col = var_col + "<tr><th>" + str(col) + "</th>" + str(var2) + "</tr>"

    summary_html = """
                    <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                    <th style="width:1000px;background-color:grey">SUMMARY TABLE DESCRIPTION</th>
                                </table>
                                <p align='left' width='900'>This Table shows you the summary result of load balancing test as PASS or FAIL criteria.</p>
                      <tr>
                        <th colspan='2'>Summary Table </th>
                      </tr>
                      <table width='1000px' border='1' >
                        <tr> """ + var_row + """
                            """ + var_col + """
                        </tr>

                     </table>
                    </table>
                    <br><br>
                    """
    return str(summary_html)


def add_utilization_table(information_dict):
    """utilization_dict = {'2.4G': {'set_threshold_value': '90', 'Measured_value': '67'},
                        '5G_low': {'set_threshold_value': '80', 'Measured_value': '69'},
                        '5G_high': {'set_threshold_value': '90', 'Measured_value': '61'}}"""

    ch_threshold = []
    ch_measured = []
    if "2.4G" in list(information_dict['Utilization'].keys()):
        if "set_threshold_value" in information_dict['Utilization']["2.4G"]:
            ch_threshold.append(information_dict['Utilization']["2.4G"]["set_threshold_value"])
        if "Measured_value" in information_dict['Utilization']["2.4G"]:
            ch_measured.append(information_dict['Utilization']["2.4G"]["Measured_value"])
    if "5G_low" in list(information_dict['Utilization'].keys()):
        if "set_threshold_value" in information_dict['Utilization']["5G_low"]:
            ch_threshold.append(information_dict['Utilization']["5G_low"]["set_threshold_value"])
        if "Measured_value" in information_dict['Utilization']["5G_low"]:
            ch_measured.append(information_dict['Utilization']["5G_low"]["Measured_value"])
    if "5G_high" in list(information_dict['Utilization'].keys()):
        if "set_threshold_value" in information_dict['Utilization']["5G_high"]:
            ch_threshold.append(information_dict['Utilization']["5G_high"]["set_threshold_value"])
        if "Measured_value" in information_dict['Utilization']["5G_high"]:
            ch_measured.append(information_dict['Utilization']["5G_high"]["Measured_value"])
    print(ch_threshold)
    print(ch_measured)
    var1 = ""
    for i in ch_threshold:
        var1 = var1 + "<td>" + i + "</td>"
    var2 = ""
    for i in ch_measured:
        var2 = var2 + "<td>" + i + "</td>"

    var_row = "<th></th>"
    for row in information_dict['Utilization'].keys():
        var_row = var_row + "<th>" + row + "</th>"
    html_data = """
                        <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                        <th style="width:1000px;background-color:grey">Channel Utilization TABLE DESCRIPTION</th>
                                </table>
                                <p align='left' width='900'>The Channel Utilization Test table provides you information regarding "
                                              "set threshold , measured channel utiliszation from the AP "
                                              "which is used to decide the PASS/ FAIL criteria, if the measured utilization "
                                              "is equal or within the range of 5% increase or 5% decrease of the threshold value "
                                              "then it's a PASS criteria else FAIL criteria.</p>
                                <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                          <tr>
                            <th colspan='2'>Channel Utilization Table</th>
                          </tr>
                          <table width='1000px' border='1' >
                            <tr>

                                """ + var_row + """

                            </tr>
                              <tr>
                                  <td>
                                      Set Threshold Value
                                  </td>""" + str(var1) + """</tr>
                              <tr>
                                  <td>
                                      Measured Value
                                  </td>""" + str(var2) + """</tr>
                         </table>
                        </table>
                        <br><br>
                        """
    return str(html_data)

def add_client_table(information_dict):
    """client_connect_dict = {'2.4G': {'set_threshold_value': '20', 'Measured_value': '20'},
     '5G_low': {'set_threshold_value': '30', 'Measured_value': '30'},
     '5G_high': {'set_threshold_value': '35', 'Measured_value': '35'}}"""
    ch_threshold = []
    ch_measured = []
    if "2.4G" in list(information_dict['Client'].keys()):
        if "set_threshold_value" in information_dict['Client']["2.4G"]:
            ch_threshold.append(information_dict['Client']["2.4G"]["set_threshold_value"])
        if "Measured_value" in information_dict['Client']["2.4G"]:
            ch_measured.append(information_dict['Client']["2.4G"]["Measured_value"])
    if "5G_low" in list(information_dict['Client'].keys()):
        if "set_threshold_value" in information_dict['Client']["5G_low"]:
            ch_threshold.append(information_dict['Client']["5G_low"]["set_threshold_value"])
        if "Measured_value" in information_dict['Client']["5G_low"]:
            ch_measured.append(information_dict['Client']["5G_low"]["Measured_value"])
    if "5G_high" in list(information_dict['Client'].keys()):
        if "set_threshold_value" in information_dict['Client']["5G_high"]:
            ch_threshold.append(information_dict['Client']["5G_high"]["set_threshold_value"])
        if "Measured_value" in information_dict['Client']["5G_high"]:
            ch_measured.append(information_dict['Client']["5G_high"]["Measured_value"])
    print(ch_threshold)
    print(ch_measured)
    var1 = ""
    for i in ch_threshold:
        var1 = var1 + "<td>" + i + "</td>"
    var2 = ""
    for i in ch_measured:
        var2 = var2 + "<td>" + i + "</td>"

    var_row = "<th></th>"
    for row in information_dict['Client'].keys():
        var_row = var_row + "<th>" + row + "</th>"
    html_data = """
                            <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                            <th style="width:1000px;background-color:grey">Max Client Connect TABLE DESCRIPTION</th>
                                </table>
                                <p align='left' width='900'>TThe max client connect Test table provides you information regarding "
                                     "set threshold , measured max client value from the AP  which can be used to "
                                     "decide the PASS/ FAIL criteria, if the measured max client value is equal to threshold "
                                     "value it's a PASS criteria else FAIL criteria.</p>
                              <tr>
                                <th colspan='2'>Max Client Connect Table</th>
                              </tr>
                              <table width='1000px' border='1' >
                                <tr>

                                    """ + var_row + """

                                </tr>
                                  <tr>
                                      <td>
                                          Set Threshold Value
                                      </td>""" + str(var1) + """</tr>
                                  <tr>
                                      <td>
                                          Measured Value
                                      </td>""" + str(var2) + """</tr>
                             </table>
                            </table>
                            <br><br>
                            """
    return  str(html_data)

def add_rssi_table(information_dict):
    """rssi_dict = {'2.4G': {'set_threshold_value': '18', 'Measured_value': '41'},
                 '5G_low': {'set_threshold_value': '10', 'Measured_value': '39'},
                 '5G_high': {'set_threshold_value': '10', 'Measured_value': '40'}}"""
    ch_threshold = []
    ch_measured = []
    if "2.4G" in list(information_dict['Rssi'].keys()):
        if "set_threshold_value" in information_dict['Rssi']["2.4G"]:
            ch_threshold.append(information_dict['Rssi']["2.4G"]["set_threshold_value"])
        if "Measured_value" in information_dict['Rssi']["2.4G"]:
            ch_measured.append(information_dict['Rssi']["2.4G"]["Measured_value"])
    if "5G_low" in list(information_dict['Rssi'].keys()):
        if "set_threshold_value" in information_dict['Rssi']["5G_low"]:
            ch_threshold.append(information_dict['Rssi']["5G_low"]["set_threshold_value"])
        if "Measured_value" in information_dict['Rssi']["5G_low"]:
            ch_measured.append(information_dict['Rssi']["5G_low"]["Measured_value"])
    if "5G_high" in list(information_dict['Rssi'].keys()):
        if "set_threshold_value" in information_dict['Rssi']["5G_high"]:
            ch_threshold.append(information_dict['Rssi']["5G_high"]["set_threshold_value"])
        if "Measured_value" in information_dict['Rssi']["5G_high"]:
            ch_measured.append(information_dict['Rssi']["5G_high"]["Measured_value"])
    print(ch_threshold)
    print(ch_measured)
    var1 = ""
    for i in ch_threshold:
        var1 = var1 + "<td>" + i + "</td>"
    var2 = ""
    for i in ch_measured:
        var2 = var2 + "<td>" + i + "</td>"

    var_row = "<th></th>"
    for row in information_dict['Rssi'].keys():
        var_row = var_row + "<th>" + row + "</th>"
    html_data = """
                                <table border="1" width="1000px" cellpadding="2" cellspacing="0">
                                <th style="width:1000px;background-color:grey">RSSI TABLE DESCRIPTION</th>
                                </table>
                                <p align='left' width='900'>The RSSI Test table provides you information regarding set threshold , measured rssi value from the AP which can be
                                        used to decide the PASS/ FAIL criteria, if the measured rssi value is within the range of 1dbm increase or 1dbm decrease
                                        of the threshold valueor is equal to threshold value it's a PASS criteria else FAIL criteria.</p>
                                <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                            <tr>
                                <th colspan='2'>RSSI TABLE </th>
                            </tr>
                                  <table width='1000px' border='1' >
                                    <tr>

                                        """ + var_row + """

                                    </tr>
                                      <tr>
                                          <td>
                                              Set Threshold Value
                                          </td>""" + str(var1) + """</tr>
                                      <tr>
                                          <td>
                                              Measured Value
                                          </td>""" + str(var2) + """</tr>
                                 </table>
                                </table>
                                <br><br>
                                """
    return str(html_data)

def test_setup_information(test_setup_data=None):
    if test_setup_data is None:
        return None
    else:
        var = ""
        for i in test_setup_data:
            var = var + "<tr><td>" + i + "</td><td colspan='3'>" + str(test_setup_data[i]) + "</td></tr>"

    setup_information = """
                        <!-- Test Setup Information -->
                        <table width='700px' border='1' cellpadding='2' cellspacing='0' style='border-top-color: gray; border-top-style: solid; border-top-width: 1px; border-right-color: gray; border-right-style: solid; border-right-width: 1px; border-bottom-color: gray; border-bottom-style: solid; border-bottom-width: 1px; border-left-color: gray; border-left-style: solid; border-left-width: 1px'>
                            <tr>
                              <th colspan='2'>Test Setup Information</th>
                            </tr>
                            <tr>
                              <td>Device Under Test</td>
                              <td>
                                <table width='100%' border='0' cellpadding='2' cellspacing='0' style='border-top-color: gray; border-top-style: solid; border-top-width: 1px; border-right-color: gray; border-right-style: solid; border-right-width: 1px; border-bottom-color: gray; border-bottom-style: solid; border-bottom-width: 1px; border-left-color: gray; border-left-style: solid; border-left-width: 1px'>
                                  """ + var + """
                                </table>
                              </td>
                            </tr>
                        </table>

                        <br>
                        """
    return str(setup_information)

def generate_report(date = None,
                    test_setup_info = None,
                    pass_fail_dict= None,
                    information_dict = None,
                    test= None,
                    report_path="/home/lanforge/html-reports/Loadbalancing",
                    ):
    test_setup_data = test_setup_info

    reports_root = report_path + "/" + str(date)
    if path.exists(report_path):
        os.mkdir(reports_root)
        print("Reports Root is Created")

    else:
        os.mkdir(report_path)
        os.mkdir(reports_root)
        print("Reports Root is created")
    print("Generating Reports in : ", reports_root)

    if test == ["Client"]:
        html_report = report_banner(date) + \
                  test_setup_information(test_setup_data) + \
                  test_objective() + \
                  add_summary_table(pass_fail_dict) + \
                  add_client_table(information_dict)
    elif test == ['Utilization']:
        html_report = report_banner(date) + \
                      test_setup_information(test_setup_data) + \
                      test_objective() + \
                      add_summary_table(pass_fail_dict) + \
                      add_utilization_table(information_dict)
    elif test == ["Rssi"]:
        html_report = report_banner(date) + \
                      test_setup_information(test_setup_data) + \
                      test_objective() + \
                      add_summary_table(pass_fail_dict) + \
                      add_rssi_table(information_dict)
    elif test == ['Client','Utilization']:
        html_report = report_banner(date) + \
                      test_setup_information(test_setup_data) + \
                      test_objective() + \
                      add_summary_table(pass_fail_dict) + \
                      add_client_table(information_dict) + \
                      add_utilization_table(information_dict)
    elif test == ['Client', 'Rssi']:
        html_report = report_banner(date) + \
                      test_setup_information(test_setup_data) + \
                      test_objective() + \
                      add_summary_table(pass_fail_dict) + \
                      add_client_table(information_dict) + \
                      add_rssi_table(information_dict)
    elif test == ['Utilization', 'Rssi']:
        html_report = report_banner(date) + \
                      test_setup_information(test_setup_data) + \
                      test_objective() + \
                      add_summary_table(pass_fail_dict) + \
                      add_utilization_table(information_dict) + \
                      add_rssi_table(information_dict)

    f = open(reports_root + "/load_report.html", "a")

    f.write(html_report)
    f.close()
    # write logic to generate pdf here
    pdfkit.from_file(reports_root + "/load_report.html", reports_root + "/load_report.pdf")


# test blocks from here
if __name__ == '__main__':
    generate_report()



