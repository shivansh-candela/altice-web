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
                    <h1 class='TitleFontPrint' style='color:darkgreen;'>  FTP Test  </h1>
                    <h3 class='TitleFontPrint' style='color:darkgreen;'>""" + str(date) + """</h3>
                    </div>
                    </div>
                    <br><br>
                 """
    return str(banner_data)
def test_objective(objective= 'This FTP Test is used to "Verify that N clients connected on Specified band and can simultaneously download some amount of file from FTP server and measuring the time taken by client to Download/Upload the file."'):
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

    for size in [200000000,500000000,1000000000]:
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
                var1 = var1 + "<td>N/A</td>"

    for size in [200000000,500000000,1000000000]:
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
                var2 = var2 + "<td>N/A</td>"


    for size in [200000000,500000000,1000000000]:
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
                var3 = var3 + "<td>N/A</td>"




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


def download_upload_time_table(result_data):
    var1 = "<th>40 Clients-2.4GHz</th>"
    var2 = "<th>40 Clients-5GHz</th>"
    var3 = " <th>20+20 Clients-2.4GHz+5GHz</th>"

    for size in [200000000,500000000,1000000000]:
        for d in ["Download", "Upload"]:
            c = 0
            for data in result_data.values():
                data_time = data['time']
                Min = min(data_time)
                Max = max(data_time)
                Sum = sum(data_time)
                Len = len(data_time)
                Avg = Sum // Len
                string_data = "<span style='font-weight:bolder'>Min=</span>" + str(Min)+"<br>" + "<span style='font-weight:bolder'>Max=</span>" + str(Max)+"<br>" + "<span style='font-weight:bolder'>Avg=</span>" + str(Avg)

                if data["band"] == "2.4G" and data["direction"] == d and data["file_size"] == size:
                    c = c + 1
                    var1 = var1 + """<td style='text-align:center'>""" + string_data + """</td>"""
            if c == 0:
                var1 = var1 + "<td style='text-align:center'><span style='font-weight:bolder'>Min</span>=N/A<br><span style='font-weight:bolder'>Max</span>=N/A<br><span style='font-weight:bolder'>Avg</span>=N/A</td>"

    for size in [200000000,500000000,1000000000]:
        for d in ["Download", "Upload"]:
            c = 0
            for data in result_data.values():
                data_time = data['time']
                Min = min(data_time)
                Max = max(data_time)
                Sum = sum(data_time)
                Len = len(data_time)
                Avg = Sum // Len
                string_data = "<span style='font-weight:bolder'>Min=</span>" + str(Min)+"<br>" + "<span style='font-weight:bolder'>Max=</span>" + str(Max)+"<br>" + "<span style='font-weight:bolder'>Avg=</span>" + str(Avg)

                if data["band"] == "5G" and data["direction"] == d and data["file_size"] == size:
                    c = c + 1
                    var2 = var2 + """<td style='text-align:center'>""" + string_data + """</td>"""
            if c == 0:
                var2 = var2 + "<td style='text-align:center'><span style='font-weight:bolder'>Min</span>=N/A<br><span style='font-weight:bolder'>Max</span>=N/A<br><span style='font-weight:bolder'>Avg</span>=N/A</td>"

    for size in [200000000,500000000,1000000000]:
        for d in ["Download", "Upload"]:
            c = 0
            for data in result_data.values():
                data_time = data['time']
                Min = min(data_time)
                Max = max(data_time)
                Sum = sum(data_time)
                Len = len(data_time)
                Avg = Sum // Len
                string_data = "<span style='font-weight:bolder'>Min=</span>" + str(Min)+"<br>" + "<span style='font-weight:bolder'>Max=</span>" + str(Max)+"<br>" + "<span style='font-weight:bolder'>Avg=</span>" + str(Avg)

                if data["band"] == "Both" and data["direction"] == d and data["file_size"] == size:
                    c = c + 1
                    var3 = var3 + """<td style='text-align:center'>""" + string_data + """</td>"""
            if c == 0:
                var3 = var3 + "<td style='text-align:center'><span style='font-weight:bolder'>Min</span>=N/A<br><span style='font-weight:bolder'>Max</span>=N/A<br><span style='font-weight:bolder'>Avg</span>=N/A</td>"

    time_table = """
                   <table border="1" width="1000px" cellpadding="2" cellspacing="0">
                     <th style="width:1000px;background-color:grey">File Download/Upload Time (sec)</th>
                    </table>
                    <br>
                    <!-- Table information -->
                    <p align='left' width='900'>This Table will give  FTP Download/Upload Time of Clients.</p>
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
                        <th>Download<br>(sec)</br></th>
                        <th>Upload<br>(sec)</br></th>
                          <th>Download<br>(sec)</br></th>
                        <th>Upload<br>(sec)</br></th>
                          <th>Download<br>(sec)</br></th>
                        <th>Upload<br>(sec)</br></th>
                      </tr>
                      <tr>
                        """ + var1 + """

                     </tr>
                      <tr>
                        """ + var2 + """

                     </tr>
                       <tr>
                        """ + var3 + """

                     </tr>
                    </table>
                    <br> 



    """

    return str(time_table)

def graph_html(graph_path="",graph_name=""):
    graph_html_obj = """
    <h3>""" +graph_name+ """</h3> 
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

def generate_graph_1(result_data, x_axis, graph_path):
    dict_of_graph = {}
    color = []
    graph_name = ""
    count = 0

    for data in result_data.values():
        if data["band"] == "2.4G" and data["file_size"] == 200000000 and data["direction"] == "Download":
            dict_of_graph["Download"] = data["time"]
            color.append("Orange")
            graph_name = "Small File Size (200MB) 40 Clients 2.4G-File Download Times(secs)"
            count = count + 1
        if data["band"] == "2.4G" and data["file_size"] == 200000000 and data["direction"] == "Upload":
            dict_of_graph["Upload"] = data["time"]
            color.append("Blue")
            graph_name = "Small File Size (200MB) 40 Clients 2.4G-File Upload Times(secs)"
            count = count + 1
    if count == 2:
        graph_name = "Small File Size (200MB) 40 Clients 2.4G-File Download and Upload Times(secs)"
    if len(dict_of_graph) != 0:
        fig, ax = plt.subplots()
        bar_plot(ax, dict_of_graph, total_width=.8, single_width=.9, colors=color)
        my_dpi = 96
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(18, 6)

        # when saving, specify the DPI
        str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
        plt.savefig(graph_path + "/image_1.png", dpi=my_dpi)
        return str(graph_html(graph_path + "/image_1.png", graph_name))
    else:
        return ""


def generate_graph_2(result_data, x_axis, graph_path):
    dict_of_graph = {}
    color = []
    graph_name = ""
    count = 0
    for data in result_data.values():
        if data["band"] == "2.4G" and data["file_size"] == 500000000 and data["direction"] == "Download":
            dict_of_graph["Download"] = data["time"]
            color.append("Orange")
            graph_name = "Medium File Size (500MB) 40 Clients 2.4G-File Download Times(secs)"
            count = count + 1
        if data["band"] == "2.4G" and data["file_size"] == 500000000 and data["direction"] == "Upload":
            dict_of_graph["Upload"] = data["time"]
            color.append("Blue")
            graph_name = "Medium File Size (500MB) 40 Clients 2.4G-File Upload Times(secs)"
            count = count + 1
    if count == 2:
        graph_name = "Medium File Size (500MB) 40 Clients 2.4G-File Download and Upload Times(secs)"
    if len(dict_of_graph) != 0:
        fig, ax = plt.subplots()
        bar_plot(ax, dict_of_graph, total_width=.8, single_width=.9, colors=color)
        my_dpi = 96
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(18, 6)

        # when saving, specify the DPI
        str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
        plt.savefig(graph_path + "/image_2.png", dpi=my_dpi)
        return str(graph_html(graph_path + "/image_2.png", graph_name))
    else:
        return ""


def generate_graph_3(result_data, x_axis, graph_path):
    dict_of_graph = {}
    color = []
    graph_name = ""
    count = 0
    for data in result_data.values():
        if data["band"] == "2.4G" and data["file_size"] == 1000000000 and data["direction"] == "Download":
            dict_of_graph["Download"] = data["time"]
            color.append("Orange")
            graph_name = "Big File Size (1000MB) 40 Clients 2.4G-File Download Times(secs)"
            count = count + 1
        if data["band"] == "2.4G" and data["file_size"] == 1000000000 and data["direction"] == "Upload":
            dict_of_graph["Upload"] = data["time"]
            color.append("Blue")
            graph_name = "Big  File Size (1000MB) 40 Clients 2.4G-File Upload Times(secs)"
            count = count + 1
    if count == 2:
        graph_name = "Big  File Size (1000MB) 40 Clients 2.4G-File Download and Upload Times(secs)"
    if len(dict_of_graph) != 0:
        fig, ax = plt.subplots()
        bar_plot(ax, dict_of_graph, total_width=.8, single_width=.9, colors=color)
        my_dpi = 96
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(18, 6)

        # when saving, specify the DPI
        str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
        plt.savefig(graph_path + "/image_3.png", dpi=my_dpi)
        return str(graph_html(graph_path + "/image_3.png", graph_name))

    else:
        return ""


def generate_graph_4(result_data, x_axis, graph_path):
    dict_of_graph = {}
    color = []
    graph_name = ""
    count = 0
    for data in result_data.values():
        if data["band"] == "5G" and data["file_size"] == 200000000 and data["direction"] == "Download":
            dict_of_graph["Download"] = data["time"]
            color.append("Orange")
            graph_name = "Small File Size (200MB) 40 Clients 5G-File Download Times(secs)"
            count = count + 1
        if data["band"] == "5G" and data["file_size"] == 200000000 and data["direction"] == "Upload":
            dict_of_graph["Upload"] = data["time"]
            color.append("Blue")
            graph_name = "Small File Size (200MB) 40 Clients 5G-File Upload Times(secs)"
            count = count + 1
    if count == 2:
        graph_name = "Small File Size (200MB) 40 Clients 5G-File Download and Upload Times(secs)"
    if len(dict_of_graph) != 0:
        fig, ax = plt.subplots()
        bar_plot(ax, dict_of_graph, total_width=.8, single_width=.9, colors=color)
        my_dpi = 96
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(18, 6)

        # when saving, specify the DPI
        str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
        plt.savefig(graph_path + "/image_4.png", dpi=my_dpi)
        return str(graph_html(graph_path + "/image_4.png", graph_name))
    else:
        return ""


def generate_graph_5(result_data, x_axis, graph_path):
    dict_of_graph = {}
    color = []
    graph_name = ""
    count = 0
    for data in result_data.values():
        if data["band"] == "5G" and data["file_size"] == 500000000 and data["direction"] == "Download":
            dict_of_graph["Download"] = data["time"]
            color.append("Orange")
            graph_name = "Medium File Size (500MB) 40 Clients 5G-File Download Times(secs)"
            count = count + 1
        if data["band"] == "5G" and data["file_size"] == 500000000 and data["direction"] == "Upload":
            dict_of_graph["Upload"] = data["time"]
            color.append("Blue")
            graph_name = "Medium File Size (500MB) 40 Clients 5G-File Upload Times(secs)"
            count = count + 1
    if count == 2:
        graph_name = "Medium File Size (500MB) 40 Clients 5G-File Download and Upload Times(secs)"
    if len(dict_of_graph) != 0:
        fig, ax = plt.subplots()
        bar_plot(ax, dict_of_graph, total_width=.8, single_width=.9, colors=color)
        my_dpi = 96
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(18, 6)

        # when saving, specify the DPI
        str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
        plt.savefig(graph_path + "/image_5.png", dpi=my_dpi)
        return str(graph_html(graph_path + "/image_5.png", graph_name))
    else:
        return ""


def generate_graph_6(result_data, x_axis, graph_path):
    dict_of_graph = {}
    color = []
    graph_name = ""
    count = 0
    for data in result_data.values():
        if data["band"] == "5G" and data["file_size"] == 1000000000 and data["direction"] == "Download":
            dict_of_graph["Download"] = data["time"]
            color.append("Orange")
            graph_name = "Big File Size (1000MB) 40 Clients 5G-File Download Times(secs)"
            count = count + 1
        if data["band"] == "5G" and data["file_size"] == 1000000000 and data["direction"] == "Upload":
            dict_of_graph["Upload"] = data["time"]
            color.append("Blue")
            graph_name = "Big File Size (1000MB) 40 Clients 5G-File Upload Times(secs)"
            count = count + 1
    if count == 2:
        graph_name = "Big File Size (1000MB) 40 Clients 5G-File Download and Upload Times(secs)"
    if len(dict_of_graph) != 0:
        fig, ax = plt.subplots()
        bar_plot(ax, dict_of_graph, total_width=.8, single_width=.9, colors=color)
        my_dpi = 96
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(18, 6)

        # when saving, specify the DPI
        str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
        plt.savefig(graph_path + "/image_6.png", dpi=my_dpi)
        return str(graph_html(graph_path + "/image_6.png", graph_name))
    else:
        return ""


def generate_graph_7(result_data, x_axis, graph_path):
    dict_of_graph = {}
    color = []
    graph_name = ""
    count = 0
    for data in result_data.values():
        if data["band"] == "Both" and data["file_size"] == 200000000 and data["direction"] == "Download":
            dict_of_graph["Download"] = data["time"]
            color.append("Orange")
            graph_name = "Small File Size (200MB) 40 Clients Both-File Download Times(secs)"
            count = count + 1
        if data["band"] == "Both" and data["file_size"] == 200000000 and data["direction"] == "Upload":
            dict_of_graph["Upload"] = data["time"]
            color.append("Blue")
            graph_name = "Small File Size (200MB) 40 Clients Both-File Upload Times(secs)"
            count = count + 1
    if count == 2:
        graph_name = "Small File Size (200MB) 40 Clients Both-File Download and Upload Times(secs)"
    if len(dict_of_graph) != 0:
        fig, ax = plt.subplots()
        bar_plot(ax, dict_of_graph, total_width=.8, single_width=.9, colors=color)
        my_dpi = 96
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(18, 6)

        # when saving, specify the DPI
        str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
        plt.savefig(graph_path + "/image_7.png", dpi=my_dpi)
        return str(graph_html(graph_path + "/image_7.png", graph_name))
    else:
        return ""


def generate_graph_8(result_data, x_axis, graph_path):
    dict_of_graph = {}
    color = []
    graph_name = ""
    count = 0
    for data in result_data.values():
        if data["band"] == "Both" and data["file_size"] == 500000000 and data["direction"] == "Download":
            dict_of_graph["Download"] = data["time"]
            color.append("Orange")
            graph_name = "Medium File Size (500MB) 40 Clients Both-File Download Times(secs)"
            count = count + 1
        if data["band"] == "Both" and data["file_size"] == 500000000 and data["direction"] == "Upload":
            dict_of_graph["Upload"] = data["time"]
            color.append("Blue")
            graph_name = "Medium File Size (500MB) 40 Clients Both-File Upload Times(secs)"
            count = count + 1
    if count == 2:
        graph_name = "Medium File Size (500MB) 40 Clients Both-File Download and Upload Times(secs)"
    if len(dict_of_graph) != 0:
        fig, ax = plt.subplots()
        bar_plot(ax, dict_of_graph, total_width=.8, single_width=.9, colors=color)
        my_dpi = 96
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(18, 6)

        # when saving, specify the DPI
        str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
        plt.savefig(graph_path + "/image_8.png", dpi=my_dpi)
        return str(graph_html(graph_path + "/image_8.png", graph_name))
    else:
        return ""


def generate_graph_9(result_data, x_axis, graph_path):
    dict_of_graph = {}
    color = []
    graph_name = ""
    count = 0
    for data in result_data.values():
        if data["band"] == "Both" and data["file_size"] == 1000000000 and data["direction"] == "Download":
            dict_of_graph["Download"] = data["time"]
            color.append("Orange")
            graph_name = "Big File Size (1000MB) 40 Clients Both-File Download Times(secs)"
            count = count + 1
        if data["band"] == "Both" and data["file_size"] == 1000000000 and data["direction"] == "Upload":
            dict_of_graph["Upload"] = data["time"]
            color.append("Blue")
            graph_name = "Big File Size (1000MB) 40 Clients Both-File Upload Times(secs)"
            count = count + 1
    if count == 2:
        graph_name = "Big File Size (1000MB) 40 Clients Both-File Download and Upload Times(secs)"
    if len(dict_of_graph) != 0:
        fig, ax = plt.subplots()
        bar_plot(ax, dict_of_graph, total_width=.8, single_width=.9, colors=color)
        my_dpi = 96
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(18, 6)

        # when saving, specify the DPI
        str(datetime.now()).split(",")[0].replace(" ", "-").split(".")[0]
        plt.savefig(graph_path + "/image_9.png", dpi=my_dpi)
        return str(graph_html(graph_path + "/image_9.png", graph_name))
    else:
        return ""

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
    x_axis = []
    for i in range(40):
        x_axis.append(i)

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
                  download_upload_time_table(ftp_data) + \
                  generate_graph_1(ftp_data, x_axis, graph_path=reports_root) + \
                  generate_graph_2(ftp_data, x_axis, graph_path=reports_root) + \
                  generate_graph_3(ftp_data, x_axis, graph_path=reports_root) + \
                  generate_graph_4(ftp_data, x_axis, graph_path=reports_root) + \
                  generate_graph_5(ftp_data, x_axis, graph_path=reports_root) + \
                  generate_graph_6(ftp_data, x_axis, graph_path=reports_root) + \
                  generate_graph_7(ftp_data, x_axis, graph_path=reports_root) + \
                  generate_graph_8(ftp_data, x_axis, graph_path=reports_root) + \
                  generate_graph_9(ftp_data, x_axis, graph_path=reports_root) + \
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