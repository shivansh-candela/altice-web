#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import pdfkit
from lf_report import lf_report
from lf_graph import lf_bar_graph

def thrp_rept(util, sta_num, bps_rx_a,bps_rx_b, tbl_title, grp_title, upload = 1000000, download = 1000000):
    '''dataframe = pd.DataFrame({
        'Utilization (%)': [20, 40, 60, 80],
        'Rx-bytes': ["min = 2 | max = 4 | avg = 2", 'min = 2 | max = 4 | avg = 2', 'min = 2 | max = 4 | avg = 2',
                     'min = 2 | max = 4 | avg = 2'],
    })'''

    rx_a = []
    rx_b = []
    pas_fail_up = []
    pas_fail_down = []
    thrp_a = upload * len(sta_num)
    # else:
    thrp_b = download * len(sta_num)
    #index = -1
    for a,b,util in bps_rx_a,bps_rx_b,util:
        #index += 1
        try:
            rx_a.append([f'min: {min(a)} | max: {max(a)} | avg: {sum(a)/len(a)}'])
            rx_b.append([f'min: {min(b)} | max: {max(b)} | avg: {sum(b)/len(b)}'])
        except ValueError as e:
            if len(a) == 0:
                rx_a.append(0)
            if len(b) == 0:
                rx_b.append(0)
        if upload:
            if (thrp_a /100)*(100 - int(util)) <= a * len(sta_num):
                pas_fail_up.append("PASS")
            else:
                pas_fail_up.append("FAIL")
        if download:
            if (thrp_b / 100) * (100 - int(util)) <= b * len(sta_num):
                pas_fail_down.append("PASS")
            else:
                pas_fail_down.append("FAIL")
    if upload == 0 and len(pas_fail_up) == 0:
        pas_fail_up = ['NA'] * util
    if download == 0 and len(pas_fail_down) == 0:
        pas_fail_down = ['NA'] * util


    overall_tab = pd.DataFrame({
            'Channel Utilization (%)': util,"no.of.clients": [len(sta_num)]*len(util),
            'Bps-rx-a(mbps)': rx_a,
            'Bps-rx-b (mbps)': rx_b
    })
    print(overall_tab)

    pasfail_tab = pd.DataFrame({
        'Channel Utilization (%)': util,
        'Upload': pas_fail_up,
        'Download': pas_fail_down
    })
    print(pasfail_tab)
    report = lf_report()
    report.set_title(tbl_title) #report.title = ""
    report.build_banner()
    #report.set_title("Banner Title Two")
    #report.build_banner()

    report.set_table_title("Overall throughput")
    report.build_table_title()
    report.set_table_dataframe(overall_tab)
    report.build_table()
    report.set_table_title("Throughput Pass/Fail")
    report.build_table_title()
    report.set_table_dataframe(pasfail_tab)
    report.build_table()

    # test lf_graph in report
    #dataset_a = [i for i in bps_rx_a]
    dataset = [[i[0] for i in bps_rx_a],[i[1] for i in bps_rx_a], [i[2] for i in bps_rx_a]]
    x_axis_values = [util]
    report.set_graph_title(tbl_title)
    report.build_graph_title()
    graph = lf_bar_graph(_data_set=dataset,
                        _xaxis_name="stations",
                        _yaxis_name="Throughput 2 (Mbps)",
                        _xaxis_categories=x_axis_values,
                        _graph_image_name="client-Throughput_5GHz",#"Bi-single_radio_2.4GHz",
                        _label=["min", "max",'avg'],
                        _color=None,
                        _color_edge='red')
    for i in util:
        dataset = [bps_rx_a]
        x_axis_values = [i[4:] for i in sta_num]
        report.set_graph_title(f"{i}% utilization")
        report.build_graph_title()
        graph = lf_bar_graph(_data_set=dataset,
                             _xaxis_name="stations",
                             _yaxis_name="Throughput 2 (Mbps)",
                             _xaxis_categories=x_axis_values,
                             _graph_image_name="client-Throughput_5GHz",  # "Bi-single_radio_2.4GHz",
                             _label=["throughput"],
                             _color=None,
                             _color_edge='red')


    graph_png = graph.build_bar_graph()

    print("graph name {}".format(graph_png))

    report.set_graph_image(graph_png)
    report.move_graph_image()
    report.build_graph()

    #report.build_all()

    html_file = report.write_html()
    print("returned file {}".format(html_file))
    print(html_file)
    report.write_pdf()

    report.generate_report()
