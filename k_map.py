import traceback
import numpy as np
import matplotlib.pyplot as plt
from pac_analysis.file_parser import parse_file
from pac_analysis.pac_curve_fit import find_k_deluxe
from pac_analysis.process_pac_data import flip_data

from pathlib import Path

def k_map(folder, rg, a, zero_point):
    """Processes data at folder location, and creates an dictionary 
    that maps coordinates to k-values"""

    folder = Path(folder)
    files = sorted(folder.glob("*.txt"))

    k_values = {}

    for file in files:
        print(f"\nProcessing {file.name}")

        try:

            #Extracts data from each PAC file
            L_data, I_data = parse_file(str(file))
            L_data = flip_data(L_data)

            #For troubleshooting (open Powershell to see)
            print("Number of L points:", len(L_data))
            print("Number of I points:", len(I_data))

            if len(L_data) == 0 or len(I_data) == 0:
                print("SKIPPED: empty file")
                continue

            #Find k
            k = find_k_deluxe( 
                L_data,
                I_data,
                rg,
                a,
                zero_point
            )

            print("k =", k)

            #Each file will be named pos_x_y_xincr_yincr
            #They are extracted from the filename
            parts = file.stem.split("_")
            x = int(parts[-4]) 
            y = int(parts[-3]) 
            xincr = int(parts[-2]) 
            yincr = int(parts[-1]) 

            #Assigns k to the x and y coordinates in um
            k_values[(x*xincr, y*yincr)] = k 

        #For troubleshooting (open Powershell)
        except Exception as e:  
            print(f"FAILED: {file.name}")
            print(e)
            traceback.print_exc()

    return k_values, xincr, yincr

def plot_k_map(k_values, xincr, yincr):
    """Creates a 2D colour map of k-values"""

    xmax = max(x for x, y in k_values) #finds max x distance
    ymax = max(y for x, y in k_values) #finds max y distance
    xmax_i = int(xmax/xincr) #finds size of x list
    ymax_i = int(ymax/yincr) #size of y list

    #Creates an empty matrix
    k_array = np.full((ymax_i + 1, xmax_i + 1), np.nan) 

    #Assigns each matrix element to a 'k'
    for (x, y), k in k_values.items():  
        k_array[int(y/yincr), int(x/xincr)] = k 


    #Creates plot
    fig, ax = plt.subplots()  

    im = ax.imshow(
        k_array,
        origin="lower",
        extent=[0, xmax, 0, ymax],
        aspect="equal"
    )

    ax.set_xlabel("X (µm)")
    ax.set_ylabel("Y (µm)")
    ax.set_title("2D k Map")

    fig.colorbar(im, ax=ax, label="k")

    return fig