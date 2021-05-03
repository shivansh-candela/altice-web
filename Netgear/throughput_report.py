#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import pdfkit
from lf_report import lf_report
from lf_graph import lf_bar_graph

def thrp_rept(util, sta_num, bps_rx_a,bps_rx_b, tbl_title, grp_title):
    '''dataframe = pd.DataFrame({
        'Utilization (%)': [20, 40, 60, 80],
        'Rx-bytes': ["min = 2 | max = 4 | avg = 2", 'min = 2 | max = 4 | avg = 2', 'min = 2 | max = 4 | avg = 2',
                     'min = 2 | max = 4 | avg = 2'],
    })'''
    rx_a = []
    rx_b = []
    for a,b in bps_rx_a,bps_rx_b:
        rx_a.append([f'min: {min(a.values())} | max: {max(a.values())} | avg: {sum(a.values())/len(a.values())}'])
        rx_b.append([f'min: {min(b.values())} | max: {max(b.values())} | avg: {sum(b.values())/len(b.values())}'])


    overall_tab = pd.DataFrame({
            'Channel Utilization (%)': util,"no.of.clients": [len(sta_num)]*len(util),
            'Bps-rx-a(mbps)': rx_a,
            'Bps-rx-b (mbps)': rx_b
    })
    print(overall_tab)

    passfail_tab = pd.DataFrame({
        'Channel Utilization (%)': util,
        'Upload': rx_a,
        'Download': rx_b
    })

    report = lf_report()
    report.set_title(tbl_title) #report.title = ""
    report.build_banner()
    #report.set_title("Banner Title Two")
    #report.build_banner()

    report.set_table_title(tbl_title)
    report.build_table_title()

    '''report.set_dataframe(dataframe)
    report.build_table()'''

    '''report.set_table_title("Title Two")
    report.build_table_title()'''

    report.set_table_dataframe(overall_tab)
    report.build_table()

    # test lf_graph in report
    dataset_a = [list(i.values()) for i in bps_rx_a]
    dataset = [[i[0] for i in dataset_a],[i[1] for i in dataset_a], [i[2] for i in dataset_a]]
    #dataset = [[min],[max],[avg]]
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
