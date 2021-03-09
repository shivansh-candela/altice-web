""" this report generation template is used for load balancing test """
--> date - 08-March-2021
--> Nikita Yadav
"""
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

def summary_table_description(objective="This table shows you the summary result of load balancing test as PASS or FAIL results"):
    test_objective = """
                    <!-- Test Objective -->
                    <h3 align='left'>Summary Table</h3> 
                    <p align='left' width='900'>""" + str(objective) + """</p>
                    <br>
                    """
    return str(test_objective)

def add_summary_table(summary2, summary5l, summary5h):
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

    summary_html = """
                <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                  <tr>
                    <th colspan='2'>Summary Table </th>
                  </tr>
                  <table width='1000px' border='1' >
                    <tr>
                        <th>

                        </th>
                        <th>
                            RSSI Threshold
                        </th>
                        <th>
                            Channel Utilization Threshold
                        </th>
                        <th>
                            Client Count Threshold
                        </th>

                    </tr>
                      <tr>
                          <td>
                              2.4Ghz Radio
                          </td>""" + str(var) + """</tr>
                      <tr>
                          <td>
                              5Ghz LOW Radio
                          </td>""" + str(var1) + """</tr>
                      <tr>
                          <td>
                              5Ghz HIGH Radio
                          </td>""" + str(var2) + """</tr>
                 </table>
                </table>
                <br><br>
                """
    return str(summary_html)
def channel_utilization_description(objective="The Channel Utilization Test table provides you information regarding "
                                              "set threshold , measured channel utiliszation from the AP "
                                              "which is used to decide the PASS/ FAIL criteria, if the measured utilization "
                                              "is equal or within the range of 5% increase or 5% decrease of the threshold value "
                                              "then it's a PASS criteria else FAIL criteria."):
    description = """
                    <!-- Test Objective -->
                    <h3 align='left'>Channel Utilization</h3> 
                    <p align='left' width='900'>""" + str(objective) + """</p>
                    <br>
                    """
    return str(description)
def channel_utilization_table(ch_threshold , ch_measured):
    '''var = ""
    for i in ch_connect:
        if i == "NO":
            var = var + "<td colspan='1' bgcolor='orange'>NO</td>"
        else:
            var = var + "<td colspan='1' bgcolor='#90EE90'>YES</td>"'''
    var1 = ""
    for i in ch_threshold:
        var1 = var1 + "<td>" + i + "</td>"
    var2 = ""
    for i in ch_measured:
        var2 = var2 + "<td>" + i + "</td>"

    summary_html = """
                    <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                      <tr>
                        <th colspan='2'>Channel Utilization Table</th>
                      </tr>
                      <table width='1000px' border='1' >
                        <tr>
                            <th>

                            </th>
                            <th>
                                2.4 GHZ
                            </th>
                            <th>
                                5GHZ LOW
                            </th>
                            <th>
                                5GHZ HIGH
                            </th>

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
    return str(summary_html)
def Max_client_description(objective="The max client connect Test table provides you information regarding "
                                     "set threshold , measured max client value from the AP  which can be used to "
                                     "decide the PASS/ FAIL criteria, if the measured max client value is equal to threshold "
                                     "value it's a PASS criteria else FAIL criteria."):
    description = """
                    <!-- Test Objective -->
                    <h3 align='left'>Max Client Connect</h3> 
                    <p align='left' width='900'>""" + str(objective) + """</p>
                    <br>
                    """
    return str(description)
def Max_client_table(cl_threshold, cl_measured):
    '''var = ""
    for i in cl_connect:
        if i == "NO":
            var = var + "<td colspan='1' bgcolor='orange'>NO</td>"
        else:
            var = var + "<td colspan='1' bgcolor='#90EE90'>YES</td>"'''
    var1 = ""
    for i in cl_threshold:
        var1 = var1 + "<td>" + i + "</td>"
    var2 = ""
    for i in cl_measured:
        var2 = var2 + "<td>" + i + "</td>"
    summary_html = """
                    <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                      <tr>
                        <th colspan='2'>Max Client Connect Table</th>
                      </tr>
                      <table width='1000px' border='1' >
                        <tr>
                            <th>

                            </th>
                            <th>
                                2.4 GHZ
                            </th>
                            <th>
                                5GHZ LOW
                            </th>
                            <th>
                                5GHZ HIGH
                            </th>

                        </tr>
                          <tr>
                              <td>
                                  Set Threshold Value
                              </td>""" + str(var1) + """ </tr>
                          <tr>
                              <td>
                                  Measured  Value
                              </td>""" + str(var2) + """</tr>
                     </table>
                    </table>
                    <br><br>
                    """
    return str(summary_html)
def rssi_description(objective="The RSSI Test table provides you information regarding "
                               "set threshold , measured rssi  value from the AP which can "
                               "be used to decide the PASS/ FAIL criteria, "
                               "if the measured rssi value is within the range of 1dbm increase or 1dbm decrease of the threshold value"
                               "or is equal to threshold value it's a PASS criteria else FAIL criteria."):
    description = """
                    <!-- Test Objective -->
                    <h3 align='left'> RSSI </h3> 
                    <p align='left' width='900'>""" + str(objective) + """</p>
                    <br>
                    """
    return str(description)
def RSSI_table(rssi_set_threshold, rssi_measured):
    '''var = ""
    for i in rssi_connect:
        if i == "NO":
            var = var + "<td colspan='1' bgcolor='orange'>NO</td>"
        else:
            var = var + "<td colspan='1' bgcolor='#90EE90'>YES</td>"'''
    var1 = ""
    for i in rssi_set_threshold:
        var1 = var1 + "<td>" + i + "</td>"
    var2 = ""
    for i in rssi_measured:
        var2 = var2 + "<td>" + i + "</td>"
    summary_html = """
                    <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                      <tr>
                        <th colspan='2'> RSSI Table</th>
                      </tr>
                      <table width='1000px' border='1' >
                        <tr>
                            <th>

                            </th>
                            <th>
                                2.4 GHZ
                            </th>
                            <th>
                                5GHZ LOW
                            </th>
                            <th>
                                5GHZ HIGH
                            </th>

                        </tr>
                          <tr>
                              <td>
                                  Set Threshold Value
                              </td>""" + str(var1) + """</tr>
                          <tr>
                              <td>
                                  Measured  Value
                              </td>""" + str(var2) + """</tr>
                     </table>
                    </table>
                    <br><br>
                    """
    return str(summary_html)



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

def generate_report(date=None,
                    test_setup_info={} ,
                    summary_table2ghz= [] ,
                    summary_table5ghz=[],
                    summary_table5ghzh=[],
                    channel_set_threshold=[],
                    channel_measured=[],
                    max_client_threshold=[],
                    max_client_measured=[] ,
                    rssi_set_threshold=[],
                    rssi_measured=[],
                    report_path="/home/lanforge/html-reports/Loadbalancing"):
    test_setup_data = test_setup_info
    summary2 = summary_table2ghz
    summary5l = summary_table5ghz
    summary5h = summary_table5ghzh
    #ch_connect = channel_client_connect
    ch_threshold = channel_set_threshold
    ch_measured = channel_measured
    #cl_connect = max_client_connect
    cl_threshold = max_client_threshold
    cl_measured = max_client_measured
    #rssi_connect = rssi_connect
    rssi_set_threshold = rssi_set_threshold
    rssi_measured = rssi_measured
    reports_root = report_path + "/" + str(date)
    if path.exists(report_path):
        os.mkdir(reports_root)
        print("Reports Root is Created")

    else:
        os.mkdir(report_path)
        os.mkdir(reports_root)
        print("Reports Root is created")
    print("Generating Reports in : ", reports_root)

    html_report = report_banner(date) + \
                  test_setup_information(test_setup_data) + \
                  test_objective() + \
                  summary_table_description() + \
                  add_summary_table(summary2, summary5l, summary5h) + \
                  channel_utilization_description() + \
                  channel_utilization_table(ch_threshold, ch_measured) + \
                  Max_client_description() + \
                  Max_client_table(cl_threshold, cl_measured) + \
                  rssi_description() + \
                  RSSI_table(rssi_set_threshold, rssi_measured)


    f = open(reports_root + "/load_report.html", "a")

    f.write(html_report)
    f.close()
    # write logic to generate pdf here
    pdfkit.from_file(reports_root + "/load_report.html", reports_root + "/load_report.pdf")


# test blocks from here
if __name__ == '__main__':
    generate_report()




