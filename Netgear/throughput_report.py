'''
------------------------------------------------------------------------------------
Throughput report generation when the clients are created under channel utilization,
the channel is utilized by creating VAP along with some stations
------------------------------------------------------------------------------------
'''
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import pdfkit,sys,os
if 'lf_report' not in sys.path:
    sys.path.append(os.path.abspath('..'))
from lf_report import lf_report
from lf_graph import lf_bar_graph

def table(report,title,data,dis=""):
    # creating table
    report.set_obj_html(_obj_title="",
                        _obj= dis)
    report.set_table_title(title)
    report.build_table_title()
    report.build_objective()
    report.set_table_dataframe(data)
    report.build_table()

def grph_build(data_set = None,         xaxis_name = "stations",    yaxis_name = "Throughput 2 (Mbps)",
            xaxis_categories = None,    label = None,               graph_image_name = "",
            bar_width = 0.25,           xticks_font = 10,  color = ['darkorange','forestgreen','blueviolet'],
            color_name =  ['darkorange','forestgreen','blueviolet'],
            color_edge = 'black',       figsize = (10, 5)):
    if color is None:
        i = 0
        color = []
        for col in data_set:
            color.append(color_name[i])
            i = i + 1

    fig = plt.subplots(figsize = figsize)
    i = 0
    for data in data_set:
        if i > 0:
            br = br1
            br2 = [x + bar_width for x in br]
            plt.bar(br2, data_set[i], color=color[i], width= bar_width,
                    edgecolor=color_edge, label=label[i])
            br1 = br2
            i = i + 1
        else:
            br1 = np.arange(len(data_set[i]))
            plt.bar(br1, data_set[i], color=color[i], width= bar_width,
                    edgecolor=color_edge, label=label[i])
            i = i + 1
    plt.xlabel(xaxis_name, fontweight='bold', fontsize=15)
    plt.ylabel(yaxis_name, fontweight='bold', fontsize=15)
    plt.xticks([r + bar_width for r in range(len(data_set[0]))],
               xaxis_categories,fontsize = xticks_font)
    plt.legend(bbox_to_anchor=(1.0,0.5))

    fig = plt.gcf()
    plt.savefig("%s.png" % graph_image_name, dpi=96)
    plt.close()
    print("{}.png".format(graph_image_name))

    return "%s.png" % graph_image_name

def grph(report,dis = "", data_set = None, xaxis_name = "stations", yaxis_name = "Throughput 2 (Mbps)",
          xaxis_categories = None, label = None, graph_image_name = "",
         bar_width = 0.25, xticks_font = 10):
    # creating bar graph
    report.set_obj_html(_obj_title="",
                        _obj=dis)
    report.set_graph_title(graph_image_name)
    report.build_graph_title()
    report.build_objective()
    '''graph = lf_bar_graph(_data_set = data_set,
                         _xaxis_name = xaxis_name,
                         _yaxis_name = yaxis_name,
                         _xaxis_categories = xaxis_categories,
                         _graph_image_name = graph_image_name.replace(" ","_"),
                         _label = label,
                         _color = ['darkorange','forestgreen','blueviolet'],
                         _color_edge = 'black',
                         _bar_width = bar_width,
                         _figsize = (10, 5),
                         _xticks_font= xticks_font)
    graph_png = graph.build_bar_graph()'''

    graph_png = grph_build(data_set = data_set, xaxis_name = xaxis_name, yaxis_name = yaxis_name,
          xaxis_categories = xaxis_categories, label = label, graph_image_name = graph_image_name.replace(" ","_"),
         bar_width = bar_width, xticks_font = xticks_font)
    print("graph name {}".format(graph_png))
    report.set_graph_image(graph_png)
    report.move_graph_image()
    report.build_graph()

def test_setup_information(test_setup_data=None):
    '''test_setup_info = {
        "AP Name": self.ap,
        "SSID": self.ssid,
        "Test Duration": datetime.strptime(test_end, '%b %d %H:%M:%S') - datetime.strptime(test_time, '%b %d %H:%M:%S')
    }'''
    if test_setup_data is None:
        return None
    else:
        var = ""
        for i in test_setup_data:
            var = var + "<tr><td>" + i + "</td><td colspan='3'>" + str(test_setup_data[i]) + "</td></tr>"
    setup_information = """
                        <!-- Test Setup Information -->
                        <br><br>
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
                        <br><br>
                        """
    return str(setup_information)

def input_setup_info_table(input_setup_info=None):
    if input_setup_info is None:
        return None
    else:
        var = ""
        for i in input_setup_info:
            var = var + "<tr><td>" + i + "</td><td colspan='3'>" + str(input_setup_info[i]) + "</td></tr>"

    setup_information = """
                        <!-- Test Setup Information -->
                        <br><br>
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

def thrp_rept(util, sta_num, bps_rx_a,bps_rx_b, rep_title, upload = 1000000, download = 1000000,
              test_setup_info = None,input_setup_info = None):
    # report generation main function
    rx_a = []
    rx_b = []
    pas_fail_up = []
    pas_fail_down = []
    thrp_b = upload * len(sta_num)  # get overall upload values
    thrp_a = download * len(sta_num)    ## get overall download values
    print(f"given upload--{thrp_b} and download--{thrp_a} values")
    index = -1
    for a in bps_rx_a:
        index += 1
        if len(a):
            rx_a.append(f'min: {min(a)} | max: {max(a)} | avg: {(sum(a)/len(a)):.2f}')
            if thrp_a:
                print(f"getting overall download values '{index}'----- {sum(a)} \n {(thrp_a/100)*(100 - int(util[index]))}")
                if (thrp_a /100)*(100 - int(util[index])) <= sum(a):
                    pas_fail_down.append("PASS")
                else:
                    pas_fail_down.append("FAIL")
        else:
            pas_fail_down.append("NA")
            rx_a.append(0)

        if len(bps_rx_b[index]):
            rx_b.append(f'min: {min(bps_rx_b[index])} | max: {max(bps_rx_b[index])} | '
                         f'avg: {(sum(bps_rx_b[index])/len(bps_rx_b[index])):.2f}')

            if thrp_b:
                print(f"getting overall upload values '{index}'----- {sum(bps_rx_b[index])} \n {(thrp_b / 100) * (100 - int(util[index]))}")
                if (thrp_b / 100) * (100 - int(util[index])) <= sum(bps_rx_b[index]):
                    pas_fail_up.append("PASS")
                else:
                    pas_fail_up.append("FAIL")
        else:
            pas_fail_up.append("NA")
            rx_b.append(0)

        util[index] = f'{util[index]}%' #append % to the util values

    overall_tab = pd.DataFrame({
            'Channel Utilization (%)': util,"No.of.clients": [len(sta_num)]*len(util),
            'Intended Throughput(Mbps)': [f'upload: {upload} | download: {download}']*len(util),
            'Achieved Upload Throughput(Mbps)': rx_b,    'Achieved Download Throughput(Mbps)': rx_a
    })
    print(f"overall table \n{overall_tab}")

    pasfail_tab = pd.DataFrame({
        'Channel Utilization (%)': util,
        'Upload': pas_fail_up,
        'Download': pas_fail_down
    })
    print(f"pass-fail table \n {pasfail_tab}")

    report = lf_report()
    report.set_title(rep_title)
    report.build_banner()
    report.set_obj_html(_obj_title="Objective",
                        _obj = f"This test is designed to measure the throughput of {len(sta_num)} clients connected on 5GHz"
                               " radio when the channel was already utilized with different percentage")
    report.build_objective()
    table(report,"Min, Max, Avg Throughput",overall_tab,dis=f"The below table gives the information about Min, Max, and Avg throughput "
                                                        f"for the clients when channel utilized with {', '.join(util)}")
    table(report,"Pass/Fail Criteria",pasfail_tab,dis = f"This table breif about Pass/Fail criteria  "
                                                          f"for {', '.join(util)} channel throughput")

    if download:
        grph(report,
         data_set=[[min(i) for i in bps_rx_a],[max(i) for i in bps_rx_a], [sum(i)/len(i) for i in bps_rx_a]],
         dis=f"This graph represents the minimum, maximum and average throughput of "
             f"stations when channel was utilized with {', '.join(util)} for download traffic",
          xaxis_name="Utilizations", yaxis_name="Throughput (Mbps)",
          xaxis_categories=util, label=["min", "max", 'avg'],
             graph_image_name="Download Throughput for all channel utilizations",
          bar_width = 0.25)
    if upload:
        grph(report,
         data_set=[[min(i) for i in bps_rx_b], [max(i) for i in bps_rx_b], [sum(i) / len(i) for i in bps_rx_b]],
         dis=f"This graph represents the minimum, maximum and average throughput of "
             f"stations when channel was utilized with {', '.join(util)} for upload traffic",
         xaxis_name="Utilizations", yaxis_name="Throughput (Mbps)",
         xaxis_categories=util, label=["min", "max", 'avg'],
         graph_image_name="Upload Throughput for all channel utilization",
         bar_width = 0.25)

    for i in range(len(util)):
        if download:
            grph(report, data_set=[bps_rx_a[i]],
                 dis=f"The graph shows the individual throughput for all the connected stations on 5GHz radio "
                     f"when channel was utilized with {util[i]} in download traffic",
                 xaxis_name="Stations",
                 yaxis_name="Throughput (Mbps)", xaxis_categories = range(0,len(sta_num)),
                 label=[util[i]], graph_image_name=f"Individual download throughput - CH{util[i]}",
                 xticks_font = 6)
        if upload:
            grph(report, data_set=[bps_rx_b[i]],
                 dis=f"The graph shows the individual throughput for all the connected stations on 5GHz radio "
                     f"when channel was utilized with {util[i]} in upload traffic",
                 xaxis_name="stations",
                 yaxis_name="Throughput (Mbps)", xaxis_categories = range(0,len(sta_num)),
                 label=[util[i]], graph_image_name=f"Individual upload throughput - CH{util[i]}"
                 ,xticks_font = 6)
    # test setup information and input setup information
    report.set_custom_html(_custom_html = test_setup_information(test_setup_data = test_setup_info))
    report.build_custom()
    report.set_custom_html(_custom_html = input_setup_info_table(input_setup_info = input_setup_info))
    report.build_custom()

    html_file = report.write_html()
    print("returned file {}".format(html_file))
    print(html_file)
    report.write_pdf()

    report.generate_report()
