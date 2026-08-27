
import matplotlib.pyplot as plt
import numpy as np

def show_position_grid(xdist, ydist):
    """Creates an image which responds to user inputs, mapping out the positions used for sample leveling"""

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
    ax.plot([(x2-x1)/2, x3], [y1, y3], "--")

    # Grid
    ax.grid(True)

    # Make downwards positive
    ax.invert_yaxis()

    ax.set_aspect("equal", adjustable="box")

    ax.set_xlabel("X distance (µm)")
    ax.set_ylabel("Y distance (µm)")
    ax.set_title("Scan locations")

    return fig

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def show_k_map_region(xdist, ydist, xincr, yincr):
    """Shows the K-map scan region and measurement positions."""

    fig, ax = plt.subplots()

    # Generate scan positions
    x_positions = np.arange(0, xdist + xincr, xincr)
    y_positions = np.arange(0, ydist + yincr, yincr)

    # Plot measurement positions
    for y in y_positions:
        ax.scatter(
            x_positions,
            np.full(len(x_positions), y),
            s=30
        )

    # Highlight initial position
    ax.scatter(
        0, 0,
        s=100
    )

    ax.text(
        0, 0,
        "  Initial Position",
        verticalalignment="bottom"
    )

    # Set scan grid at the actual measurement increments
    ax.set_xticks(x_positions, minor=True)
    ax.set_yticks(y_positions, minor=True)

    # Let Matplotlib choose sensible major axis labels
    ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=6))

    # Grid
    ax.grid(True, which="minor", linewidth=0.5)
    ax.grid(True, which="major", linewidth=0.8)

    # Set limits
    ax.set_xlim(0, xdist)
    ax.set_ylim(0, ydist)

    # Equal X/Y scaling
    ax.set_aspect("equal", adjustable="box")

    # Labels
    ax.set_xlabel("X distance (µm)")
    ax.set_ylabel("Y distance (µm)")
    ax.set_title("K-map Scan Locations")

    return fig