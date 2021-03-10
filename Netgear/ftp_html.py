from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np
import os.path
from os import path
import sys
import pdfkit
sys.path.append('/home/lanforge/.local/lib/python3.6/site-packages')
def report_banner(date):
    banner_data = """
                   <!DOCTYPE html>
                    <html lang='en'>
                    <head>
                    <meta charset='UTF-8'>
                    <meta name='viewport' content='width=device-width, initial-scale=1' />
                    <title>LANforge Report</title>                        
                    </head>
                    <title>DFS TEST </title></head>
                    <body>
                    <div class='Section report_banner-1000x205' style='background-image:url("/home/lanforge/LANforgeGUI_5.4.3/images/report_banner-1000x205.jpg");background-repeat:no-repeat;padding:0;margin:0;min-width:1000px; min-height:205px;width:1000px; height:205px;max-width:1000px; max-height:205px;'>                
                    <br>
                    <img align='right' style='padding:25;margin:5;width:200px;' src="/home/lanforge/LANforgeGUI_5.4.3/images/CandelaLogo2-90dpi-200x90-trans.png" border='0' />                
                    <div class='HeaderStyle'>
                    <br>
                    <h1 class='TitleFontPrint' style='color:darkgreen;'>  FTP Test  </h1>
                    <h3 class='TitleFontPrint' style='color:darkgreen;'>""" + str(date) + """</h3>
                    </div>
                    </div>
                    <br><br>
                 """
    return str(banner_data)
def test_objective(objective= "The FTP Test is designed to test the performance of the Netgear Access Point.File Transfer Protocol is a standard network protocol used to transfer files between computers(a client and server) over a TCP/IP network. "):
    test_objective = """
                    <!-- Test Objective -->
                    <h3 align='left'>Objective</h3> 
                    <p align='left' width='900'>""" + str(objective) + """</p>
                    <br>
                    """
    return str(test_objective)
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
                                  """ + str(var) + """
                                </table>
                              </td>
                            </tr>
                        </table>
                        <br>
                        """
    return str(setup_information)
def add_pass_fail_table(result_data):
    var1="<th>40 Clients-2.4GHz</th>"
    var2="<th>40 Clients-5GHz</th>"
    var3=" <th>20+20 Clients-2.4GHz+5GHz</th>"

    for size in ["200000000","500000000","1000000000"]:
        for d in ["Download","Upload"]:
            c=0
            for data in result_data.values():
                if data["band"] == "2.4G" and data["direction"] == d and data["file_size"] == size :
                    c=c+1
                    if data["result"] == "Pass":
                        var1 = var1 + "<td style='background-color:Green'>Pass</td>"
                    elif data["result"] == "Fail":
                        var1 = var1 + "<td style='background-color:Red'>Fail</td>"
            if c==0:
                var1 = var1 + "<td>NA</td>"

    for size in ["200000000","500000000","1000000000"]:
        for d in ["Download","Upload"]:
            c=0
            for data in result_data.values():
                if data["band"] == "5G" and data["direction"] == d and data["file_size"] == size :
                    c=c+1
                    if data["result"] == "Pass":
                        var2 = var2 + "<td style='background-color:Green'>Pass</td>"
                    elif data["result"] == "Fail":
                        var2 = var2 + "<td style='background-color:Red'>Fail</td>"
            if c==0:
                var2 = var2 + "<td>NA</td>"


    for size in ["200000000","500000000","1000000000"]:
        for d in ["Download","Upload"]:
            c=0
            for data in result_data.values():
                if data["band"] == "Both" and data["direction"] == d and data["file_size"] == size :
                    c=c+1
                    if data["result"] == "Pass":
                        var3 = var3 + "<td style='background-color:Green'>Pass</td>"
                    elif data["result"] == "Fail":
                        var3 = var3 + "<td style='background-color:Red'>Fail</td>"
            if c==0:
                var3 = var3 + "<td>NA</td>"




    table_info="""
                <table border="1" width="1000px" cellpadding="2" cellspacing="0">
                     <th style="width:1000px;background-color:grey">PASS/FAIL Results</th>
                    </table>
                    <br>
                    <!-- Table information -->
                    <p align='left' width='900'>This Table will give Pass/Fail Results.</p>
                    <br>
                    <table border="1" width="1000px" cellpadding="2" cellspacing="0">
                     <tr>
                        <th></th>
                        <th colspan="2">Small File (200MB)</th>
                        <th colspan="2">Medium File (500MB)</th>
                        <th colspan="2">Big File (1000MB)</th>
                      </tr>
                      <tr>
                        <th></th>
                        <th>Download</th>
                        <th>Upload</th>
                          <th>Download</th>
                        <th>Upload</th>
                          <th>Download</th>
                        <th>Upload</th>
                      </tr>
                      <tr>
                        """+ var1 +"""
                        
                     </tr>
                      <tr>
                        """+ var2 +"""
                         
                     </tr>
                       <tr>
                        """+ var3 +"""
                         
                     </tr>
                    </table>
                    <br>
    
                """
    return str(table_info)


def input_setup_info_table(input_setup_info=None):
    if input_setup_info is None:
        return None
    else:
        var = ""
        for i in input_setup_info:
            var = var + "<tr><td>" + i + "</td><td colspan='3'>" + str(input_setup_info[i]) + "</td></tr>"

    setup_information = """
                        <!-- Test Setup Information -->
                        <table width='700px' border='1' cellpadding='2' cellspacing='0' style='border-top-color: gray; border-top-style: solid; border-top-width: 1px; border-right-color: gray; border-right-style: solid; border-right-width: 1px; border-bottom-color: gray; border-bottom-style: solid; border-bottom-width: 1px; border-left-color: gray; border-left-style: solid; border-left-width: 1px'>
                            <tr>
                              <th colspan='2'>Input Setup Information</th>
                            </tr>
                            <tr>
                              <td>Information</td>
                              <td>
                                <table width='100%' border='0' cellpadding='2' cellspacing='0' style='border-top-color: gray; border-top-style: solid; border-top-width: 1px; border-right-color: gray; border-right-style: solid; border-right-width: 1px; border-bottom-color: gray; border-bottom-style: solid; border-bottom-width: 1px; border-left-color: gray; border-left-style: solid; border-left-width: 1px'>
                                  """ + str(var) + """
                                </table>
                              </td>
                            </tr>
                        </table>
                        <br>
                        """
    return str(setup_information)

def generate_report(ftp_data=None,
                    date=None,
                    test_setup_info={},
                    input_setup_info = {},
                    graph_path="/home/lanforge/html-reports/FTP-Test"):
    # Need to pass this to test_setup_information()
    input_setup_info = input_setup_info
    test_setup_data = test_setup_info

    reports_root = graph_path + "/" + str(date)
    if path.exists(graph_path):
        os.mkdir(reports_root)
        print("Reports Root is Created")

    else:
        os.mkdir(graph_path)
        os.mkdir(reports_root)
        print("Reports Root is created")
    print("Generating Reports in : ", reports_root)

    html_report = report_banner(date) + \
                  test_setup_information(test_setup_data) + \
                  test_objective() + \
                  add_pass_fail_table(ftp_data) + \
                  input_setup_info_table(input_setup_info)




    # write the html_report into a file in /home/lanforge/html_reports in a directory named FTP-Test and html_report name should be having a timesnap with it
    f = open(reports_root + "/report.html", "a")
    # f = open("report.html", "a")
    f.write(html_report)
    f.close()
    # write logic to generate pdf here
    pdfkit.from_file(reports_root + "/report.html", reports_root + "/report.pdf")


# test blocks from here
if __name__ == '__main__':
    generate_report()