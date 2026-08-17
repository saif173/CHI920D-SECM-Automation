import sys
from pathlib import Path
import matplotlib.pyplot as plt

sys.path.append(str(Path(__file__).parent.parent))

from secm_controller.commands import k_map, plot_k_map

k_values = k_map(r"C:\chi\k-map1", 10, 5, 3, 0)

"""k_values = {
    (0, 0): 0.8,
    (1, 0): 0.9,
    (2, 0): 1.1,
    (0, 1): 0.7,
    (1, 1): 1.0,
    (2, 1): 1.2,
    (0, 2): 0.6,
    (1, 2): 0.95,
    (2, 2): 1.3,
}"""

plot = plot_k_map(k_values, 3)

plt.show()

