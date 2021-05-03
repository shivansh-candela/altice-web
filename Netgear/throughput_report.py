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


    dataframe = pd.DataFrame({
        'Utilization (%)': util,"no.of.clients": [len(sta_num)]*len(util),
        'Bps-rx-a(bps)': bps_rx_a,
        'Bps-rx-b (bps)': bps_rx_a})
    print(dataframe)
        #"Bps-rx-a (bps)": [f"min = {} | max = {bps_rx_a[1]} | avg = {bps_rx_a[2]}"],
        #"Bps-rx-b (bps)": [f"min = {bps_rx_b[0]} | max = {bps_rx_b[1]} | avg = {bps_rx_b[2]}"],

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

    report.set_table_dataframe(dataframe)
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
