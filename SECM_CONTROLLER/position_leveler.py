import numpy as np

def scan_mode():
    L_data = []
    I_data = []
    #move down until moved down 50 micrometers
    initial_current = #current when moved down 50micrometers
    perc_diff= np.abs((current-initialcurrent)/initialcurrent)*100
    while perc_diff<=25:
          #move down
          L_data.append()
          I_data.append()
    if perc_diff>=25:
        #stop
        #move back up (dont record anything moving back up)
    return L_data, I_data


def moving(positions, finish):      #positions will be some dictionary
  
    start_pos = position
    end_pos = positions[finish]
    #move

def stop_distances(positions):
     ordered_pos = []
     stop_distances=[]
     for i in range(len(positions)):
        ordered_pos.append(position)
        scan_mode()
        moving((position%len(positions))+1)


     return ordered_pos, stop_distances


def offsets(ordered_pos, stop_distances):
    offset1 = stop_distances[1]-stop_distances[0]
    offset2=stop_distances[2]-stop_distances[0]
    print("Height of", ordered_pos[1], "is off by", offset1, "relative to", ordered_pos[0])
    print("Height of", ordered_pos[1], "is off by", offset2, "relative to", ordered_pos[0])
