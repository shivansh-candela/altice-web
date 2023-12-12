#!/usr/bin/env python3
'''

The script generates heatmaps for rssi and throughput values by fetching the values from a csv and the co-ordinates from a JSon.

Capabilities:
    It can generate heatmap for one node having 3 multiple bands 2.4G,5G and 6G 
    Also it can generate heatmaps for less than or equal to 3 nodes (example: gateway,leaf1,leaf2) Note: the names are to be used as it is.
    For different bands of different nodes the points on heatmap are distinguished by giving different shapes to different nodes (i.e gateway-circle | leaf1-rectangle | leaf2-triangle)

Pre-requisites:
    Need to install some packages if not already present
        -numpy
        -matplotlib
        -scipy
        -pillow (python imaging library)
    
How to run:
    step1: create an empty folder with a particular name in the same directory where this script is placed.
    step2: place the csv and json and the image on which heatmap should be generated in that particular folder.
        Note: make sure to place only single csv and single json and single png in the folder.
    step3: run the script using CLI from its location, and all the heatmaps will be saved in that particular folder.

example CLI:
         python3 generate_heatmap.py --folder_name check_heatmap_1 --rssi_scale="-90to-30" --throughput_scale="0to400" 

sample CSV format:
        
        SI.NO	RSSI	AP	          BSSID	       Band	Channel	TCP UPLOAD	TCP DOWNLOAD	UDP UPLOAD	UDP DOWNLOAD
        1	    -35	  gateway	30:34:22:A0:92:26	5G	 36	        232	        291	            236	        179	            
        2	    -33	  leaf1	    30:34:22:A0:92:26	5G	 36	        250	        289	            181	        178	            

    Note: AP and Band columns are mandatory 
'''

import argparse
import json as jsn
import os
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
from PIL import Image
from matplotlib.patches import Polygon
# import matplotlib.colors as mcolors
from scipy.interpolate import Rbf
import matplotlib.pyplot as plt
from matplotlib.image import imread


class heatmap():
    def __init__(self,
                 folder_name=None,
                 throuput_scale="0to100",
                 rssi_scale="-90to-30"

                 ):

        self.folder_name = folder_name
        self.x_cords = []
        self.y_cords = []
        self.individual_colors = []
        self.rssi_scale = rssi_scale
        self.throuput_scale= throuput_scale


    def get_coords(self):  # fetches the coordinates from the json and stores in instance variable
        base_directory = os.getcwd()

        self.folder_path = os.path.join(base_directory, self.folder_name)

        self.folder_contents = os.listdir(self.folder_path)
        files = [file for file in self.folder_contents if file.endswith('.json')]

        if len(files) == 1:
            json_file_path = os.path.join(self.folder_path, files[0])
            print("fecthing co-ordinates")
            with open(json_file_path, 'r') as json_file:
                data = jsn.load(json_file)
                for cords in data["survey_points"]:
                    self.x_cords.append(cords["x"])
                    self.y_cords.append(cords["y"])

                # print(self.x_cords)
                # print(self.y_cords)

        else:
            if len(files) == 0:
                print(f"No JSON file found in the folder:{self.folder_name}")
                exit(0)
            else:
                print("More than one JSON file found. Please ensure there's only one JSON file in the folder.")
                exit(0)


   
    def get_heatmap_png(self,x_coordinates,y_coordinates,image_name,values,image_png,scale): #generates heatmap and saves.
        img = imread(image_png)
        img1 = Image.open(image_png)
        img1 = img1.transpose(Image.FLIP_TOP_BOTTOM)

        # print(x_coordinates,"---x_coordinates---",y_coordinates,"---y_coordinates---")
        # print(values,"---values---")
        grid_x, grid_y = np.meshgrid(np.linspace(0, img.shape[1], 100), np.linspace(0, img.shape[0], 100))
        rbf = Rbf(x_coordinates, y_coordinates, values, function="linear", epsilon=0.5)
        grid_rssi = rbf(grid_x, grid_y)
        cmap = plt.get_cmap('RdYlGn')
        width, height = img1.size

        # sets the output image size same as input image and increase width and height by 200 to fit the color bar
        fig, ax = plt.subplots(figsize=((width + 200) / 100, (height + 200) / 100)) 
        # fig, ax = plt.subplots(figsize=(20, 10))
        
        ax.imshow(img1, extent=[0, img.shape[1], img.shape[0], 0])
        ax.imshow(grid_rssi, extent=[0, img.shape[1], 0, img.shape[0]], zorder=1, alpha=0.5, cmap=cmap, vmin=scale.split("to")[0],
                  vmax=scale.split("to")[1])
        
        # remove the x and y axis ticks
        ax.set_xticks([])
        ax.set_yticks([])

        
        y_coordinates = [img.shape[0] - y for y in y_coordinates]
        for i, (x_val, y_val) in enumerate(zip(x_coordinates, y_coordinates)):

            if not self.individual_shape_list:
                circle = plt.Circle((x_val, y_val), radius=16, color=self.individual_colors[i], fill=True,alpha =1,zorder=10)
                ax.add_patch(circle)
            else:
                if self.individual_shape_list[i] == "rectangle":
                    rect = plt.Rectangle((x_val - 20, y_val - 12), 30, 20, color=self.individual_colors[i], fill=True,alpha =1,zorder=10)
                    ax.add_patch(rect)
                    # plt.text(x_val-20, y_val - 30, f"{str(values[i])}")
                    # if image_name.replace("TCP ","").replace("UDP ","") != "RSSI":
                    #     plt.text(x_val+10, y_val + 10, f"{str(self.rssi_values[i])}")
                elif self.individual_shape_list[i] == "triangle":
                    triangle = Polygon([(x_val - 20, y_val - 10), (x_val + 20, y_val - 10), (x_val, y_val + 20)], closed=True, color=self.individual_colors[i], fill=True,alpha =1,zorder=10)    
                    ax.add_patch(triangle)
                    # plt.text(x_val-20, y_val - 30, f"{str(values[i])}")
                    # if image_name.replace("TCP ","").replace("UDP ","") != "RSSI":
                    #     plt.text(x_val+10, y_val + 10, f"{str(self.rssi_values[i])}")
                else:
                    circle = plt.Circle((x_val, y_val), radius=16, color=self.individual_colors[i], fill=True,alpha =1,zorder=10)
                    ax.add_patch(circle)
                    # plt.text(x_val-20, y_val - 30, f"{str(values[i])}")
                    # if image_name.replace("TCP ","").replace("UDP ","") != "RSSI":
                    #     plt.text(x_val+10, y_val + 10, f"{str(self.rssi_values[i])}")



            ax.text(x_val - 3, y_val - 3, self.coord_number[i], color='black', fontsize=10, ha='center', va='center',zorder=10)
        cbar = plt.colorbar(
            ax.imshow(grid_rssi, extent=[0, img.shape[1], 0, img.shape[0]], zorder=1, alpha=0.5, cmap=cmap, vmin=scale.split("to")[0],
                      vmax=scale.split("to")[1]))
        if image_name.replace("TCP ","").replace("UDP ","") == "RSSI":
            cbar.set_label( "RSSI in (dBm)")
            plt.title("Signal quality [dBm]", fontsize=10)
            [plt.text(i+13, j + 10, f"{str(values[index])}") for index, (i, j) in enumerate(zip(x_coordinates, y_coordinates))]

        else:
            # [plt.text(i-20, j - 40, f"{str(values[index])}") for index, (i, j) in enumerate(zip(x_coordinates, y_coordinates))]

            [plt.text(i-20, j -30, f"{str(values[index])}({str(self.rssi_values[index])})",fontsize=9) for index, (i, j) in enumerate(zip(x_coordinates, y_coordinates))]

            heading = f'{image_name.replace("TCP ","").replace("UDP ","").replace("udp ","").replace("tcp ","")} ({image_name.replace("DOWNLOAD","").replace("UPLOAD","").replace("Download","").replace("Upload","")}) [MBit/s]'

            plt.title(heading, fontsize=10)
            cbar.set_label("Throughput " + "in (Mbps)")
            # print(image_name)
        legend_handles = []
        ncol = 3
        legend_handles_node1 = []
        legend_handles_node2 = []
        legend_handles_node3 = []
        for key, color in self.color_map.items():
            if key[0] == 'gateway' :
                legend_handles_node1.append(
                    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color[0], label=f"{key[0]} - {key[1]}"))
            elif key[0] == 'leaf1':
                legend_handles_node2.append(
                    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=color[0], label=f"{key[0]} - {key[1]}"))
            elif key[0] == 'leaf2':
                legend_handles_node3.append(
                    plt.Line2D([0], [0], marker='^', color='w', markerfacecolor=color[0], label=f"{key[0]} - {key[1]}"))
        if len(list(set(self.Access_points))) == 2:
            ncol = 2
        plt.legend(handles=legend_handles_node1 + legend_handles_node2 + legend_handles_node3, loc='upper center', bbox_to_anchor=(0.5, 0.0),
                    ncol=ncol)
        # fig.savefig(buffer, bbox_inches='tight', pad_inches=0, format='png')

        
        plt.savefig(f'./{image_name}.png', bbox_inches='tight', pad_inches=0, format='png')

    def generate_heatmap(self):
        files = [file for file in self.folder_contents if file.endswith('.csv')]
        image_png = [file for file in self.folder_contents if file.endswith('.png')]
        floorplan_index = 0
        if "First_floor_PNG.png" not in image_png:
            floorplan_index = image_png.index("Ground_floor_PNG.png")
        else:
            floorplan_index = image_png.index("First_floor_PNG.png")





        if len(files) == 1:
            csv_file_path = os.path.join(self.folder_path, files[0])
            # main_colors = ["blue","grey",'yellow']
            # main_colors_rgb_values = [mcolors.to_rgb(color) for color in main_colors]
            
            # shapes and colors are hardcoded for now to maintain same colors and shapes every time 

            main_colors_rgb_values = [(128/255,128/255,128/255),(102/255,178/255,255/255),(127/255,0/255,255/255)]
            shapes_list = ["circle","rectangle","triangle"]
            
            self.individual_shape_list = []
            os.chdir(self.folder_path)
            with open(csv_file_path, 'r') as csv_file:
                reader = csv.reader(csv_file)
                # data = [row for row in reader]
                # print(data)
                csv_file.seek(0)
                headers = next(reader)
                # print(headers)
                node_index = None
                band_index = None
                self.Access_points = []
                bands = []
                # node_type_and_band_map = []
                self.color_map= {}
                
                # print(headers.index('Band'))
                node_index = headers.index('AP')
                band_index = headers.index('Band')
                if node_index is not None:

                    for row in reader:
                        self.Access_points.append(row[node_index])
                        bands.append(row[band_index])
                    # print(list(set(bands)),"bands check")
                    # print(list(set(self.Access_points)),"check accesspoints")
                    order = {'2.4G': 0, '5G': 1, '6G': 2}

                    sorted_bands = sorted(set(bands), key=lambda x: order[x])
                    print("Nodes:",list(set(self.Access_points)))
                    print("Bands list :",sorted_bands)
                    # mapped the shapes and colors to maintain a particular standard.
                    for index , node in enumerate(list(set(self.Access_points))):
                        for band in sorted_bands:
                            
                            shape = shapes_list[0] if node == "gateway" else shapes_list[1] if node == "leaf1" else shapes_list[2]
                            color =  main_colors_rgb_values[0] if band == "2.4G" else main_colors_rgb_values[1] if band == "5G" else main_colors_rgb_values[2]
                            # print(node)
                            # print(shape,'shape')
                            self.color_map[(node,band)] = (color,shape)

                            # print(i,"-------")
                            # if i == "2.4G":
                            #     self.color_map[(node,i)] = main_colors_rgb_values[index]
                            #     print(main_colors_rgb_values[index],"---")
                            # elif i == "5G":
                            #     # lighter_rgb = tuple(max(c * 0.7, 0.0) for c in main_colors_rgb_values[index])
                            #     # print(lighter_rgb,"light----")
                            #     # self.color_map[(node, i)] = lighter_rgb
                            #     # print(tuple(max(c * 0.7, 0.0) for c in main_colors_rgb_values[index]),"dark------")
                            #     self.color_map[(node,i)] = main_colors_rgb_values[index]
                            # else:
                            #     # darker_rgb = tuple(max(c * 0.45, 0.0) for c in main_colors_rgb_values[index])
                            #     # self.color_map[(node, i)] = darker_rgb
                            #     self.color_map[(node,i)] = main_colors_rgb_values[index]
                            # node_type_and_band_map.append({'node': node, 'type': i})
                    # print(node_type_and_band_map)
                    # print(self.color_map,"colormap")
                    # self.color_map = {('leaf1', '5G'): (0.7, 0.42, 0.42), ('leaf1', '2.4G'): (1.0, 0.6, 0.6), ('leaf1', '6G'): (0.5, 0.3, 0.3), ('gateway', '5G'): (0.5599999999999999, 0.5599999999999999, 0.7), ('gateway', '2.4G'): (0.8, 0.8, 1.0), ('gateway', '6G'): (0.4, 0.4, 0.5), ('leaf2', '5G'): (0.5599999999999999, 0.7, 0.5599999999999999), ('leaf2', '2.4G'): (0.8, 1.0, 0.8), ('leaf2', '6G'): (0.4, 0.5, 0.4)}
                    csv_file.seek(0)

                    for row in reader:
                        if row[headers.index("Band")] != "Band":
                            # print((row[headers.index("AP")], row[headers.index("Band")]),"--aps and bands--")
                            color_shape = self.color_map.get((row[headers.index("AP")], row[headers.index("Band")]))
                            self.individual_colors.append(color_shape[0])
                            self.individual_shape_list.append(color_shape[1])
                    # print(self.individual_colors,"individual_colors")
                    # print(self.individual_shape_list,"individual_shape_list")
                    csv_file.seek(0)
                    self.rssi_values = [row[headers.index("RSSI")] for row in reader][1:]
                    csv_file.seek(0)
                    self.coord_number = [row[headers.index("SI.NO")] for row in reader][1:]
                    for header in headers:
                        csv_file.seek(0)

                        # skipping the headers ["SI.NO","AP","Band","BSSID","Channel"] in the csv and generating heatmap for the rest of the headers like RSSI , TCP UPLOAD...
                        if header not in ["SI.NO","AP","Band","BSSID","Channel"]:  
                            
                            column_values = [row[headers.index(header)] for row in reader]
                            csv_file.seek(0)

                            # print(self.coord_number,"-------------")
                            # print(self.rssi_values,"-------------")
                            values = [int(value) for value in column_values[1:]]
                            # print(values)
                            scale = self.throuput_scale if header != "RSSI" else self.rssi_scale
                            # print(scale,"scale")

                            # Check if the file already exists
                            if os.path.exists(f'./{header}.png'):
                                os.remove(f'./{header}.png')
                                # print(os.path.exists(f'./{header}.png'))
                            self.get_heatmap_png(self.x_cords, self.y_cords, header, values, image_png[floorplan_index],scale)
                    print(f"The heatmaps are saved in the folder:{self.folder_name}")


        else:
            if len(files) == 0:
                print("No CSV files found in the specified folder.")
                exit(0)
            else:
                print("More than one CSV file found. Please make sure there's only one CSV file in the folder.")
                exit(0)



def main():
    parser = argparse.ArgumentParser(
        prog="generate_heatmap.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
---------------------------------------------------------------------------------

Objective:
    
The script generates heatmaps for rssi and throughput values by fetching the values from a csv and the co-ordinates from a JSon.

Capabilities:
    It can generate heatmap for one node having 3 multiple bands 2.4G,5G and 6G 
    Also it can generate heatmaps for less than or equal to 3 nodes (example: gateway,leaf1,leaf2) Note: the names are to be used as it is.
    For different bands of different nodes the points on heatmap are distinguished by giving different shapes to different nodes (i.e gateway-circle | leaf1-rectangle | leaf2-triangle)

Pre-requisites:
    Need to install some packages if not already present
        -numpy
        -matplotlib
        -scipy
        -pillow (python imaging library)
    
How to run:
    step1: create an empty folder with a particular name in the same directory where this script is placed.
    step2: place the csv and json and the image on which heatmap should be generated in that particular folder.
        Note: make sure to place only single csv and single json in the folder.
    step3: run the script from its location, and all the heatmaps will be saved in that particular folder.

example CLI:
         python3 generate_heatmap.py --folder_name check_heatmap_1 --rssi_scale="-90to-30" --throughput_scale="0to400" 

sample CSV format:
        
        SI.NO	RSSI	AP	          BSSID	       Band	Channel	TCP UPLOAD	TCP DOWNLOAD	UDP UPLOAD	UDP DOWNLOAD
        1	    -35	  gateway	30:34:22:A0:92:26	5G	 36	        232	        291	            236	        179	            
        2	    -33	  leaf1	    30:34:22:A0:92:26	5G	 36	        250	        289	            181	        178	            


---------------------------------------------------------------------------------
""")
    parser.add_argument("-folder_name", "--folder_name", type=str,
                        help="provide the folder name in which the json and csv are present", required=True)
    parser.add_argument("-throughput_scale", "--throughput_scale", type=str,
                        help="provide the scale for throughput values, eg: 0to300" ,default="0to300")
    parser.add_argument("-rssi_scale", "--rssi_scale", type=str,
                        help="provide the scale for RSSI values, eg: '-90to-30'",default="-30to-90" )

    args = parser.parse_args()

    heatmap_obj = heatmap(
        folder_name=args.folder_name,
        throuput_scale= args.throughput_scale,
        rssi_scale=args.rssi_scale,

    )

    heatmap_obj.get_coords()
    heatmap_obj.generate_heatmap()


if __name__ == "__main__":
    main()
