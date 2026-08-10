import sys
from position_leveler import scan_mode, moving, stop_distances, offsets
from pac_analysis.process_pac_data import normalize_data
from pac_analysis.pac_curve_fit import find_k_deluxe



def two_d_scan_k(positions, rg, a):
    positions_and_ks = {}

    moving(positions, postion1)
    for i in range(len(positions)):
        L_data, I_data = scan_mode()
        k = find_k_deluxe(L_data, I_data, rg , a, 0)
        positions_and_ks[position]=k

        moving(positions, (position%len(positions))+1)
    
    
    return positions_and_ks

def two_d_scan(positions):
    positions_and_is = {}
    moving(positions, position1)
    for i in range(len(positions)):
        positions_and_is[position]=current
        moving(positions, (position%len(positions))+1)

    return positions_and_is



