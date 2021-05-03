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
                    <title>FTP Test </title></head>
                    <body>
                    <div class='Section report_banner-1000x205' style='background-image:url("/home/lanforge/LANforgeGUI_5.4.3/images/report_banner-1000x205.jpg");background-repeat:no-repeat;padding:0;margin:0;min-width:1000px; min-height:205px;width:1000px; height:205px;max-width:1000px; max-height:205px;'>                
                    <br>
                    <img align='right' style='padding:25;margin:5;width:200px;' src="/home/lanforge/LANforgeGUI_5.4.3/images/CandelaLogo2-90dpi-200x90-trans.png" border='0' />                
                    <div class='HeaderStyle'>
                    <br>
                    <h1 class='TitleFontPrint' style='color:darkgreen;'>  Webpage Download Test </h1>
                    <h3 class='TitleFontPrint' style='color:darkgreen;'>""" + str(date) + """</h3>
                    </div>
                    </div>
                    <br><br>
                 """
    return str(banner_data)

def test_objective(
        objective='The Webpage Download Test is designed to test the performance of the Netgear Access Point.The goal check whether the webpage loading'
                  'time meets the expectation when clients connected on single radio as well as dual radio'):
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
                                  """ + var + """
                                </table>
                              </td>
                            </tr>
                        </table>

                        <br>
                        """
    return str(setup_information)

def graph_html(graph_path="", graph_name=""):
    graph_html_obj = """
    <h3>""" + graph_name + """</h3> 
      <img align='center' style='padding:15;margin:5;width:1000px;' src=""" + graph_path + """ border='1' />
    <br><br>
    """
    return str(graph_html_obj)
def bar_plot(ax, data, colors=None, total_width=0.8, single_width=1, legend=True):
    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Iterate over all data
    for i, (name, values) in enumerate(data.items()):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys(), bbox_to_anchor=(1.1,1.05), loc='upper right')
    ax.set_ylabel('Time in seconds')
    ax.set_xlabel("Stations")
    x_data =[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
    idx = np.asarray([i for i in range(len(x_data))])
    ax.set_xticks(idx)
    ax.set_xticklabels(x_data)



def generate_graph(result_data, graph_path):
    download_time = dict.fromkeys(result_data.keys())
    for i in download_time:
        try:
            download_time[i] = result_data[i]['dl_time']
        except:
            download_time[i] = []
    print(download_time)
    lst = []
    lst1 = []
    lst2 = []
    dwnld_time = dict.fromkeys(result_data.keys())

    for i in download_time:
        if i == "5G":
            # print("yo",download_time[i])
            for j in download_time[i]:
                x = (j / 1000)
                y = round(x, 2)
                lst.append(y)
            print(lst)
            dwnld_time["5G"] = lst
        if i == "2.4G":
            # print("HIIIIII", download_time[i])
            for j in download_time[i]:
                x = (j / 1000)
                y = round(x, 2)
                lst1.append(y)
            print(lst)
            dwnld_time["2.4G"] = lst1
        if i == "Both":
            # print("yes", download_time[i])
            for j in download_time[i]:
                x = (j / 1000)
                y = round(x, 2)
                lst2.append(y)
            # print(lst2)
            dwnld_time["Both"] = lst2
    fig, ax = plt.subplots()
    bar_plot(ax, dwnld_time, total_width=0.8, single_width=0.8)
    my_dpi = 96
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(18, 6)
    # when saving, specify the DPI
    plt.savefig(graph_path + "/webpage.png", dpi=my_dpi)
    return str(graph_html(graph_path + "/webpage.png"))

def summary_table(result_data, band):
    col_head_list = ['Download']
    var_row = "<th></th>"
    for row in col_head_list:
        var_row = var_row + "<th>" + row + "</th>"
    x = []
    html_struct = dict.fromkeys(list(result_data.keys()))
    for fcc in list(result_data.keys()):
        fcc_type = result_data[fcc]["avg"]
        print(fcc_type)
        for i in fcc_type:
            x.append(i)
        #print(x)
    y = []
    for i in x:
        i = i / 1000
        y.append(i)
    #print(y)
    z = []
    for i in y:
        i = str(round(i, 2))
        z.append(i)
    #print(z)
    pass_fail_list = []
    #print(list(result_data.keys()))
    sumry2 = []
    sumry5 = []
    sumryB = []
    if band == ["5G", "2.4G", "Both"]:
        print("yes")
        # 5G
        if float(z[0]) < 60.0:
            print("PASS")
            pass_fail_list.append("PASS")
            sumry5.append("PASS")
        else:
            print("FAIL")
            pass_fail_list.append("FAIL")
            sumry5.append("FAIL")
        # 2.4g
        if float(z[1]) < 90.0:
            var = "PASS"
            pass_fail_list.append(var)
            sumry2.append("PASS")
        else:
            pass_fail_list.append("FAIL")
            sumry2.append("FAIL")
        # BOTH
        if float(z[2]) < 50.0:
            var = "PASS"
            pass_fail_list.append(var)
            sumryB.append("PASS")
        else:
            pass_fail_list.append("FAIL")
            sumryB.append("FAIL")

    elif band == ['5G']:
        if float(z[0]) < 60.0:
            print("PASS")
            pass_fail_list.append("PASS")
            sumry5.append("PASS")
        else:
            print("FAIL")
            pass_fail_list.append("FAIL")
            sumry5.append("FAIL")

    elif band == ['2.4G']:
        if float(z[0]) < 90.0:
            var = "PASS"
            pass_fail_list.append(var)
            sumry2.append("PASS")
        else:
            pass_fail_list.append("FAIL")
            sumry2.append("FAIL")
    elif band == ["Both"]:
        if float(z[0]) < 50.0:
            var = "PASS"
            pass_fail_list.append(var)
            sumryB.append("PASS")
        else:
            pass_fail_list.append("FAIL")
            sumryB.append("FAIL")
    elif band == ['5G', '2.4G']:
        if float(z[0]) < 60.0:
            print("PASS")
            pass_fail_list.append("PASS")
            sumry5.append("PASS")
        else:
            print("FAIL")
            pass_fail_list.append("FAIL")
            sumry5.append("FAIL")
        # 2.4g
        if float(z[1]) < 90.0:
            var = "PASS"
            pass_fail_list.append(var)
            sumry2.append("PASS")
        else:
            pass_fail_list.append("FAIL")
            sumry2.append("FAIL")

    elif band == ['5G', 'Both']:
        if float(z[0]) < 60.0:
            print("PASS")
            pass_fail_list.append("PASS")
            sumry5.append("PASS")
        else:
            print("FAIL")
            pass_fail_list.append("FAIL")
            sumry5.append("FAIL")
        if float(z[1]) < 50.0:
            var = "PASS"
            pass_fail_list.append(var)
            sumryB.append("PASS")
        else:
            pass_fail_list.append("FAIL")
            sumryB.append("FAIL")


    elif band == ['2.4G', 'Both']:
        if float(z[0]) < 90.0:
            var = "PASS"
            pass_fail_list.append(var)
            sumry2.append("PASS")
        else:
            pass_fail_list.append("FAIL")
            sumry2.append("FAIL")
        if float(z[1]) < 50.0:
            var = "PASS"
            pass_fail_list.append(var)
            sumryB.append("PASS")
        else:
            pass_fail_list.append("FAIL")
            sumryB.append("FAIL")

    # print(pass_fail_list)
    # print(sumry5 , sumry2 ,sumryB)
    var = " "
    for i in sumry5:
        if i == "FAIL":
            var = var + "<td colspan='1' bgcolor='orange'>FAIL</td>"
        else:
            var = var + "<td colspan='1' bgcolor='#90EE90'>PASS</td>"
    var1 = ""
    for i in sumry2:
        if i == "FAIL":
            var1 = var1 + "<td colspan='1' bgcolor='orange'>FAIL</td>"
        else:
            var1 = var1 + "<td colspan='1' bgcolor='#90EE90'>PASS</td>"
    var2 = ""
    for i in sumryB:
        if i == "FAIL":
            var2 = var2 + "<td colspan='1' bgcolor='orange'>FAIL</td>"
        else:
            var2 = var2 + "<td colspan='1' bgcolor='#90EE90'>PASS</td>"
    var_col = ""
    for col in list(result_data.keys()):
        print(col)
        if col == "5G":
            var_col = var_col + "<tr><th>" + str(col) + "</th>" + str(var) + "</tr>"
        if col == "2.4G":
            var_col = var_col + "<tr><th>" + str(col) + "</th>" + str(var1) + "</tr>"
        if col == "Both":
            var_col = var_col + "<tr><th>" + str(col) + "</th>" + str(var2) + "</tr>"

    html_data = """
                <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                    <th style="width:1000px;background-color:grey">SUMMARY TABLE DESCRIPTION</th>
                                    </table>
                                    <p align='left' width='900'>This Table shows you the summary result of Webpage Download Test as PASS or FAIL criteria.
                                     If the average time taken by 40 clients to access the webpage is less than 90s it's a PASS criteria for 2.4 ghz clients,
                                     If the average time taken by 40 clients to access the webpage is less than 60s it's a PASS criteria for 5 ghz clients and 
                                       If the average time taken by 40 clients to access the webpage is less than 50s it's a PASS criteria for 2.4 ghz and 5ghz  clients</p>
                    <table width='1000px' border='1' cellpadding='2' cellspacing='0' >

                      <tr>
                        <th colspan='2'>SUMMARY TABLE </th>
                      </tr>
                      <table width='1000px' border='1' >
                        <tr>
                            """ + var_row + """
                        </tr>
                        """ + var_col + """
                     </table>
                    </table>
                    <br>
                    """
    return str(html_data)


def download_time_table(final_dict):
    col_head_list = ["Minimum", "Maximum", "Average"]
    #this is used to add column header
    var_row = "<th></th>"
    for row in col_head_list:
        var_row = var_row + "<th>" + row + "</th>"

    x = []
    for fcc in list(final_dict.keys()):
        fcc_type = final_dict[fcc]["min"]
        print(fcc_type)
        for i in fcc_type:
            x.append(i)
        print(x)
    y = []
    for i in x:
        i = i / 1000
        y.append(i)
    print("hi", y)
    z = []
    for i in y:
        i = str(round(i, 2))
        z.append(i)
    print(z)
    x1 = []

    for fcc in list(final_dict.keys()):
        fcc_type = final_dict[fcc]["max"]
        print(fcc_type)
        for i in fcc_type:
            x1.append(i)
        print(x1)
    y1 = []
    for i in x1:
        i = i / 1000
        y1.append(i)
    print("hi", y1)
    z1 = []
    for i in y1:
        i = str(round(i, 2))
        z1.append(i)
    print(z1)
    x2 = []

    for fcc in list(final_dict.keys()):
        fcc_type = final_dict[fcc]["avg"]
        print(fcc_type)
        for i in fcc_type:
            x2.append(i)
        print(x2)
    y2 = []
    for i in x2:
        i = i / 1000
        y2.append(i)
    print("hi", y2)
    z2 = []
    for i in y2:
        i = str(round(i, 2))
        z2.append(i)
    print(z2)
    g5_lsyt = []
    g2_lst = []
    gb_lst = []

    print(list(final_dict.keys()))
    lst = list(final_dict.keys())

    if lst == ["5G", "2.4G", "Both"]:
        g5_lsyt.append(z[0])
        g5_lsyt.append(z1[0])
        g5_lsyt.append(z2[0])

        g2_lst.append(z[1])
        g2_lst.append(z1[1])
        g2_lst.append(z2[1])

        gb_lst.append(z[2])
        gb_lst.append(z1[2])
        gb_lst.append(z2[2])
    elif lst == ['5G']:
        g5_lsyt.append(z[0])
        g5_lsyt.append(z1[0])
        g5_lsyt.append(z2[0])
    elif lst == ['2.4G']:
        g2_lst.append(z[0])
        g2_lst.append(z1[0])
        g2_lst.append(z2[0])
    elif lst == ['Both']:
        gb_lst.append(z[0])
        gb_lst.append(z1[0])
        gb_lst.append(z2[0])
    elif lst == ['5G', '2.4G']:
        g5_lsyt.append(z[0])
        g5_lsyt.append(z1[0])
        g5_lsyt.append(z2[0])

        g2_lst.append(z[1])
        g2_lst.append(z1[1])
        g2_lst.append(z2[1])
    elif lst == ['5G', 'Both']:
        g5_lsyt.append(z[0])
        g5_lsyt.append(z1[0])
        g5_lsyt.append(z2[0])

        gb_lst.append(z[1])
        gb_lst.append(z1[1])
        gb_lst.append(z2[1])
    elif lst == ['2.4G', 'Both']:
        g2_lst.append(z[0])
        g2_lst.append(z1[0])
        g2_lst.append(z2[0])
        gb_lst.append(z[1])
        gb_lst.append(z1[1])
        gb_lst.append(z2[1])

    # used to calulate table value and print them in column wise
    final_data = ""
    for i in g5_lsyt:
        final_data = final_data + "<td colspan='1'bgcolor='#CCC6FE'>" + str(i) + "</td>"
        print(final_data)
    final_data1 = ""
    for i in g2_lst:
        final_data1 = final_data1 + "<td colspan='1'bgcolor='#CCC6FE'>" + str(i) + "</td>"
    final_data2 = ""
    for i in gb_lst:
        final_data2 = final_data2 + "<td colspan='1'bgcolor='#CCC6FE'>" + str(i) + "</td>"

    # this is used to get row header along with table values
    var_col = ""
    for col in final_dict.keys():
        if col == "5G":
            var_col = var_col + "<tr><th>" + str(col) + "</th>" + str(final_data) + "</tr>"
        if col == "2.4G":
            var_col = var_col + "<tr><th>" + str(col) + "</th>" + str(final_data1) + "</tr>"
        if col == "Both":
            var_col = var_col + "<tr><th>" + str(col) + "</th>" + str(final_data2) + "</tr>"

    html_data = """
                               <table border="1" width="1000px" cellpadding="2" cellspacing="0">
                                 <th style="width:1000px;background-color:grey">File Download Time (sec)</th>
                                </table>
                                <br>
                                <!-- Table information -->
                                <p align='left' width='900'>This Table will provide you information of the minimum, maximum and the average time taken by clients to download a webpages</p>
                                <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                              <tr>
                                <th colspan='2'>Download time (sec) </th>
                              </tr>
                              <table width='1000px' border='1' >
                                <tr>
                                    """ + str(var_row) + """
                                </tr>
                                """ + str(var_col) + """                      
                             </table>
                            </table>
                            <br>

                """
    return str(html_data)
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
                                  """ + var + """
                                </table>
                              </td>
                            </tr>
                        </table>

                        <br>
                        """
    return str(setup_information)


def generate_report(final_dict=None,
                    date=None,
                    test_setup_info={},
                    input_setup_info = {},
                    band= None,
                    graph_path="/home/lanforge/html-reports/webpage"):
    # Need to pass this to test_setup_information()
    input_setup_info = input_setup_info
    test_setup_data = test_setup_info
    final_dict = final_dict
    #print("hiiiiiiiiiiiiiiiii", final_dict)

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
                  generate_graph(final_dict, graph_path=reports_root) + \
                  summary_table(final_dict, band) + \
                  download_time_table(final_dict) + \
                  input_setup_info_table(input_setup_info)
    # write the html_report into a file in /home/lanforge/html_reports in a directory named DFS_TEST and html_report name should be having a timesnap with it
    f = open(reports_root + "/webpage_report.html", "a")
    # f = open("report.html", "a")
    f.write(html_report)
    f.close()
    # write logic to generate pdf here
    pdfkit.from_file(reports_root + "/webpage_report.html", reports_root + "/webpage_report.pdf")
if __name__ == '__main__':
    generate_report()
