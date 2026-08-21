import numpy as np

from pathlib import Path


folder = Path(__file__).parent



#finding touch point where second derivative is maximum


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



        