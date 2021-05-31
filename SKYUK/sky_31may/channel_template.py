from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
import os.path
from os import path
import sys
print(sys.path)
sys.path.append('/home/lanforge/.local/lib/python3.6/site-packages')
import pdfkit

def banner_data(date):
    banner_data = """
                       <!DOCTYPE html>
                        <html lang='en'>
                        <head>
                        <meta charset='UTF-8'>
                        <meta name='viewport' content='width=device-width, initial-scale=1' />
                        <title>AP Auto Channel Selection Test</title>                        

                        </head>

                        <title>AP Auto Channel Selection Test</title></head>
                        <body>
                        <div class='Section report_banner-1000x205' style='background-image:url("/home/lanforge/LANforgeGUI_5.4.3/images/report_banner-1000x205.jpg");background-repeat:no-repeat;padding:0;margin:0;min-width:1000px; min-height:205px;width:1000px; height:205px;max-width:1000px; max-height:205px;'>
                        <br>
                        <img align='right' style='padding:25;margin:5;width:200px;' src="/home/lanforge/LANforgeGUI_5.4.3/images/CandelaLogo2-90dpi-200x90-trans.png" border='0' />


                        <div class='HeaderStyle'>
                        <br>
                        <h1 class='TitleFontPrint' style='color:darkgreen;'>AP Auto Channel Selection Test</h1>
                        <h3 class='TitleFontPrint' style='color:darkgreen;'>""" + date + """</h3>
                        </div>
                        </div>
                        <br>
                     """
    return str(banner_data)

def test_objective(objective='Test the Auto Channel Selectionn feature of the AP in 2.4GHz'):
    test_objective = """
                    <!-- Test Objective -->
                    <h3 align='left'>Objective</h3> 
                    <p align='left' width='900'>""" + str(objective) + """</p>
                    """
    return str(test_objective)

def test_steps():
    html = """
               <!-- Test Steps-->
               <h3 align='left'>Test Steps:</h3>  
               <ul>
                    <li>In each test trail,create different loads on Channel 1,6,11 representing various real world environments.</li>
                    <li>Reboot the AP for each trail and check what channel the AP chooses.</li>
                    <li>PLot the % of expected channel allocation and actual channel allocation</li>
                </ul>
    """
    return str(html)

def test_setup_information(test_setup_info=None):
    if test_setup_info is None:
        return None
    else:
        var = ""
        for i in test_setup_info:
            var = var + "<tr><td>" + i + "</td><td colspan='3'>" + str(test_setup_info[i]) + "</td></tr>"

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
    #print("hi",data)
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
        ax.legend(bars, data.keys(), bbox_to_anchor=(1.1, 1.05), loc='upper right')
    ax.set_ylabel('percentage')
    ax.set_xlabel("channels")
    ax.set_title("Percentage distribution of expected and actual Channel allocation across 2.4GHz channels")
    channels = [1, 2, 3]
    idx = np.asarray([i for i in range(len(channels))])
    ax.set_xticks(idx)

    ax.set_xticklabels(('1', '6', '11'))
def generate_graph1(expected_value, measured_value,graph_path):
    # expected_value = ['1', '11', '6', '11', '1', '6', '1', '11', '6', '11', '1', '6']
    # measured_value = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']

    count_1 = expected_value.count("1")
    count_6 = expected_value.count("6")
    count_11 = expected_value.count("11")
    exp_lst = []
    channel1_expected_per = round((count_1 * 100) / len(expected_value), 2)
    exp_lst.append(channel1_expected_per)
    channel6_expected_per = round((count_6 * 100) / len(expected_value), 2)
    exp_lst.append(channel6_expected_per)
    channel11_expected_per = round((count_11 * 100) / len(expected_value), 2)
    exp_lst.append(channel11_expected_per)
    #print(exp_lst)

    count_1a = measured_value.count("1")
    count_6a = measured_value.count("6")
    count_11a = measured_value.count("11")
    meas_lst = []
    channel1_measured_per = round((count_1a * 100) / len(measured_value), 2)
    meas_lst.append(channel1_measured_per)
    channel6_measured_per = round((count_6a * 100) / len(measured_value), 2)
    meas_lst.append(channel6_measured_per)
    channel11_measured_per = round((count_11a * 100) / len(measured_value), 2)
    meas_lst.append(channel11_measured_per)
    #print((meas_lst))



    data= {"expected":None, "measured":None}
    data['expected'] = exp_lst
    data['measured'] = meas_lst
    print(data)
    fig, ax = plt.subplots()
    bar_plot(ax, data=data, total_width=0.8, single_width=0.8)

    my_dpi = 96
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(18, 6)
    # when saving, specify the DPI
    plt.savefig(graph_path + "/channel.png", dpi=my_dpi)
    return str(graph_html(graph_path=graph_path + "/channel.png", graph_name="AP Auto Channel Selection Graph"))

def detailed_result(final_data, iteration):
    """final_data = [{'Traffic1': '10', 'Traffic2': '60', 'Traffic3': '50', 'expected channel': '1', 'channel_after': '1'},
                  {'Traffic1': '60', 'Traffic2': '50', 'Traffic3': '10', 'expected channel': '11', 'channel_after': '1'},
                  {'Traffic1': '60', 'Traffic2': '10', 'Traffic3': '50', 'expected channel': '6', 'channel_after': '1'},
                  {'Traffic1': '60', 'Traffic2': '60', 'Traffic3': '10', 'expected channel': '11', 'channel_after': '1'},
                  {'Traffic1': '10', 'Traffic2': '60', 'Traffic3': '60', 'expected channel': '1', 'channel_after': '1'},
                  {'Traffic1': '60', 'Traffic2': '10', 'Traffic3': '60', 'expected channel': '6', 'channel_after': '1'},
                  {'Traffic1': '5', 'Traffic2': '60', 'Traffic3': '50', 'expected channel': '1', 'channel_after': '1'}]
"""
    col_head_list= []
    print(list(final_data[0].keys()))
    x = list(final_data[0].keys())
    if "Traffic1" in x:
        col_head_list.append("channel 1 Load(Mbps)")
    if 'Traffic2' in x :
        col_head_list.append("channel 6 Load(Mbps)")
    if 'Traffic3' in x :
        col_head_list.append("Channel 11 Load(Mbps)")
    if 'expected channel' in x :
        col_head_list.append("Expected Channel")
    if 'channel_after' in x :
        col_head_list.append("Measured Channel")
    print(col_head_list)



    #col_head_list = ["channel 1 Throughput(Mbps) ", "channel 6 Throughput(Mbps)", "Channel 11 Throughput(Mbps)", "Expected Channel", "Measured Channel"]
    var_row = ""
    for row in col_head_list:
        var_row = var_row + "<th>" + row + "</th>"

    var1 = ""
    for i in final_data:
        # print(i['vap_channel'])

        var1 = var1 + "<tr><td>" + str(i['Traffic1']) + "</td>" + "<td>" + str(
            i['Traffic2']) + "</td>" + "<td>" + str(i['Traffic3']) + "</td>" + "<td>" + str(
            i['expected channel']) + "<td>" + str(i['channel_after']) + "</td></tr>"

    html_data = """
                                       <table border="1" width="1000px" cellpadding="2" cellspacing="0">
                                         <th style="width:1000px;background-color:grey">Detailed Results</th>
                                        </table>
                                        <!-- Table information -->
                                        <p align='left' width='900'>This Table will provide you information 
                                        of the measured channel after reboot and also the expected channel 
                                        value for every throughput combination, This test is performed on """ +str(iteration) + """ iterations.</p>
                                        <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                                      <tr>
                                        <th colspan='2'>Detailed Description </th>
                                      </tr>
                                      <table width='1000px' border='1' >
                                        <tr>
                                            """ + str(var_row) + """
                                        </tr>

                                        """ + str(var1) + """
                                     </table>
                                    </table>
                                    <br>
                        """
    return  str(html_data)

def summary_result(expected_value, measured_value):
    # expected_value = ['1', '11', '6', '11', '1', '6', '1', '11', '6', '11', '1', '6']
    # measured_value = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']

    count_1 = expected_value.count("1")
    count_6 = expected_value.count("6")
    count_11 = expected_value.count("11")
    #print(count_1)
    # print(count_6)
    # print(count_11)
    channel1_expected_per = round((count_1 * 100)/ len(expected_value),2)
    # print(channel1_expected_per)
    channel6_expected_per = round((count_6 * 100) / len(expected_value),2)
    #print(channel6_expected_per)
    channel11_expected_per = round((count_11 * 100)/ len(expected_value),2)
    #print(channel11_expected_per)

    count_1a = measured_value.count("1")
    count_6a = measured_value.count("6")
    count_11a = measured_value.count("11")
    #print(count_1a)
    #print(count_6a)
    #print(count_11a)
    channel1_measured_per = round((count_1a * 100) / len(measured_value), 2)
    print(channel1_measured_per)
    channel6_measured_per = round((count_6a * 100) / len(measured_value),2)
    print(channel6_measured_per)
    channel11_measured_per = round((count_11a * 100) / len(measured_value),2)
    print(channel11_measured_per)
    lst = []

    for i in range(3):
        dict2 = {" ": None, "expected": None, "measured": None}
        lst.append(dict2)
    print(lst)
    lst[0][' '] = "Channel 1"
    lst[0]["expected"] = channel1_expected_per
    lst[0]["measured"] = channel1_measured_per
    lst[1][" "] = "channel 6"
    lst[1]["expected"] = channel6_expected_per
    lst[1]["measured"] = channel6_measured_per
    lst[2][" "] = "Channel 11"
    lst[2]["expected"] = channel11_expected_per
    lst[2]["measured"] = channel11_measured_per
    print(lst)
    col_head_list = [" ", "Expected Channel Percentage", "Measured Channel Percentage"]
    var_row = ""
    for row in col_head_list:
        var_row = var_row + "<th>" + row + "</th>"
    var1 = ""
    for i in lst:
        # print(i['vap_channel'])

        var1 = var1 + "<tr><td>" + str(i[' ']) + "</td>" + "<td>" + str(i['expected']) + "</td>" + "<td>" + str(i['measured']) + "</td></tr>"

    html_data = """
                                           <table border="1" width="1000px" cellpadding="2" cellspacing="0">
                                             <th style="width:1000px;background-color:grey">SUMMARY TABLE</th>
                                            </table>
                                            <!-- Table information -->
                                            <p align='left' width='900'>This Table will provide you information of the measured channel percentage after reboot and also the expected channel percentage for every throughput combination.</p>
                                            <table width='1000px' border='1' cellpadding='2' cellspacing='0' >
                                          <tr>
                                            <th colspan='2'>SUMMARY TABLE</th>
                                          </tr>
                                          <table width='1000px' border='1' >
                                            <tr>
                                                """ + str(var_row) + """
                                            </tr>
                                            """ + str(var1) + """
                                         </table>
                                        </table>
                                        <br>
                            """
    return str(html_data)

def generate_report(final_data=None,
                    date=None,
                    expected_value=None,
                    measured_value=None,
                    test_setup_info={},
                    iteration=None,
                    graph_path="/home/lanforge/html-reports/skyuk"):
    reports_root = graph_path + "/" + str(date)
    if path.exists(graph_path):
        os.mkdir(reports_root)
        print("Reports Root is Created")

    else:
        os.mkdir(graph_path)
        os.mkdir(reports_root)
        print("Reports Root is created")
    print("Generating Reports in : ", reports_root)

    html_report = banner_data(date) + \
                  test_setup_information(test_setup_info) + \
                  test_objective() + \
                  test_steps() + \
                  generate_graph1(expected_value=expected_value, measured_value=measured_value,graph_path=reports_root) + \
                  summary_result(expected_value=expected_value, measured_value=measured_value) + \
                  detailed_result(final_data, iteration=iteration)
    # write the html_report into a file in /home/lanforge/html_reports in a directory named DFS_TEST and html_report name should be having a timesnap with it
    f = open(reports_root + "/channel_selection_test.html", "a")
    # f = open("report.html", "a")
    f.write(html_report)
    f.close()
    # write logic to generate pdf here
    pdfkit.from_file(reports_root + "/channel_selection_test.html", reports_root + "/channel_selection_test.pdf")


if __name__ == '__main__':
    generate_report()
