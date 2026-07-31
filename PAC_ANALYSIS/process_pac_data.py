import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


folder = Path(__file__).parent

"""L_data, I_data = np.loadtxt(folder / "gold_data.txt", unpack=True)
pure_L, pure_I = np.loadtxt(folder / "n_f.txt", unpack=True)"""

a = 5

from scipy.signal import savgol_filter

"""I_smooth = savgol_filter(
    I_data,
    window_length=31,
    polyorder=3
)"""

#finding second derivative of PAC curve to find touch point
def second_derivative(x,y):
    second_derivatives = []
    for i in range(len(x) - 2):
        if x[i+2] - x[i] == 0:
            second_derivatives.append(np.nan)
        else:
            second_derivatives.append((y[i+2] - 2*y[i+1] + y[i])/(x[i+2] - x[i])**2)
    return second_derivatives

def derivative(x,y):
    derivatives = []
    for i in range(len(x)-1):
        if x[i+1]-x[i] == 0:
            derivatives.append(np.nan)
        else:
            derivatives.append((y[i+1]-y[i])/(x[i+1]-x[i]))
    return derivatives

#finding touch point where second derivative is maximum

def find_touchpoint(L_data, I_data):
    second_deriv = second_derivative(L_data, I_data)
    index = np.argmax(np.abs(second_deriv)) 
    touch_point = L_data[index +1]
    return touch_point

"""print(find_touchpoint(L_data, I_data))"""

#normalizing L and I data

def flip_data(L_data):
    """Flips the distance data so that the curve looks more like you expect"""
    return np.abs(L_data - L_data[-1])

def normalize_data(L_data, I_data, touch_point, a, I_infinity):
    """Normalises data based on touch-point (zero-point) and bulk-current (I-infinity)"""
    rel_L =(L_data - touch_point) / a
    rel_I = (I_data/I_infinity)
    mask= (rel_L>0)&(rel_L<5) #sets range of 0 to 5 for the normalised curve. removes x=0 to avoid numerical instability
    rel_L=rel_L[mask]
    rel_I=rel_I[mask]
    
    return rel_L, rel_I


"""def process_data_touchpoint(L_data, I_data, a):
    touch_point = find_touchpoint(L_data, I_data)
    return normalize_data(L_data, I_data, touch_point, a)



rel_L, rel_I = process_data_touchpoint(L_data, I_data, a)
#rel_L1,rel_I1 = process_data_touchpoint(L_data,I_smooth,a)
"""



#plotting PAC curve
"""plt.plot(L_data, I_data, label='PAC curve')
plt.xlabel("L")
plt.ylabel("I")
plt.title("PAC Curve")
plt.grid(True)
plt.show()"""

"""plt.plot(L_data, I_smooth, label='PAC curve')
plt.xlabel("L")
plt.ylabel("I")
plt.title("PAC Curve")
plt.grid(True)
plt.show()"""


# plotting normalized PAC curve

"""plt.plot(rel_L, rel_I, label='Normalized PAC curve')
plt.xlabel("Relative L")
plt.ylabel("Relative I")
plt.title("Normalized PAC Curve")
plt.grid(True)
plt.show()"""

"""plt.plot(rel_L1, rel_I1, label='Normalized PAC curve')
plt.xlabel("Relative L")
plt.ylabel("Relative I")
plt.title("Normalized PAC Curve")
plt.grid(True)
plt.show()"""

        