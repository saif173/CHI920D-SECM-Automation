import os
import subprocess
import traceback
import numpy as np
import matplotlib.pyplot as plt
from pac_analysis.file_parser import parse_file
from pac_analysis.pac_curve_fit import find_k_deluxe_shift, find_k_deluxe
from pac_analysis.process_pac_data import flip_data
from pathlib import Path

def k_map(folder, rg, a, box_length, zero_point, shift):

    folder = Path(folder)
    files = sorted(folder.glob("*.txt"))

    k_values = {}

    for file in files:
        print(f"\nProcessing {file.name}")

        try:
            L_data, I_data = parse_file(str(file))

            print("Number of L points:", len(L_data))
            print("Number of I points:", len(I_data))

            if len(L_data) == 0 or len(I_data) == 0:
                print("SKIPPED: empty file")
                continue

            k = find_k_deluxe(
                L_data,
                I_data,
                rg,
                a,
                zero_point
            )

            print("k =", k)

            parts = file.stem.split("_")
            x = int(parts[-2])
            y = int(parts[-1])

            k_values[(x, y)] = k

        except Exception as e:
            print(f"FAILED: {file.name}")
            print(e)
            traceback.print_exc()

    return k_values


def plot_k_map(k_values, box_length):

    # Create array
    k_array = np.full((box_length, box_length), np.nan)

    # Put each k value into the correct position
    for (x, y), k in k_values.items():
        k_array[y, x] = k

    # Plot
    fig, ax = plt.subplots()

    im = ax.imshow(
        k_array,
        origin="lower",
        extent=[0, box_length-1, 0, box_length-1],
        aspect="equal"
    )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("2D k Map")

    fig.colorbar(im, ax=ax, label="k")

    return fig