import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def show_position_grid(xdist, ydist):

    fig, ax = plt.subplots()

    # Positions
    x1, y1 = 0, 0
    x2, y2 = xdist, 0
    x3, y3 = xdist / 2, ydist

    # Plot points
    ax.scatter(
        [x1, x2, x3],
        [y1, y2, y3],
        s=100
    )

    # Labels
    ax.text(x1, y1, "  Position 1")
    ax.text(x2, y2, "  Position 2")
    ax.text(x3, y3, "  Position 3")

    # Connect positions
    ax.plot([x1, x2], [y1, y2], "--")
    ax.plot([x1, x3], [y1, y3], "--")
    ax.plot([x2, x3], [y2, y3], "--")

    # Grid
    ax.grid(True)

    # Make downwards positive
    ax.invert_yaxis()

    ax.set_aspect("equal", adjustable="box")

    ax.set_xlabel("X distance (µm)")
    ax.set_ylabel("Y distance (µm)")
    ax.set_title("Scan locations")

    return fig