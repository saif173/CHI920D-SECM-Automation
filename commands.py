
from pathlib import Path
import subprocess


from pac_analysis.file_parser import parse_file



PROJECT_DIR = Path(__file__).resolve().parent


def k_map_commands(parameters):
    commands = []

    commands.append(f"zgoto:{parameters['initialz']}")

    for y in range(int(parameters['ydist']//parameters['yincr'])+1):
        for x in range(int(parameters['xdist']//parameters['xincr'])+1):

            # Run PAC
            commands += pac_commands(parameters)

            # Save result
            commands += [
            f"folder:{parameters['output_folder']}",
            f"tsave:pos_{x}_{y}_{parameters['xincr']}a{parameters['yincr']}", 
            f"zgoto:{parameters['initialz']}"
            ]

            # Move to next point in row
            if x < ((parameters['xdist']//parameters['xincr'])):
                commands.append(f"x:{parameters['xincr']}")

        # Move to beginning of next row
        if y < (parameters['ydist']//parameters['yincr']):
            commands.append(f"x:{-1*parameters['xdist']}")
            commands.append(f"y:{-1*parameters['yincr']}")

    if parameters['originon'] == True:
        commands= commands + [f"y:{parameters['ydist']}", f"x:{-1*parameters['xdist']}"]
    return commands


def cv_commands(parameters):
    commands = [f"tech:cv",
        f"ei:{parameters['v_ini']}",
        f"eh:{parameters['v_high']}",
        f"el:{parameters['v_low']}",
        f"ef:{parameters['v_final']}",
        f"v:{parameters['scan_rate']}",
        f"cl:{parameters['sweep_segments']}",
        f"si:{parameters['sample_interval']}",
        f"qt:{parameters['quiet_time']}",
        f"sens:{parameters['sensitivity']}"]
    if parameters['ini_direction'] == "Positive":
        commands.append("pn:p")
    elif parameters['ini_direction'] == "Negative":
        commands.append("pn:n")
    if parameters['auto_sens'] == True:
        commands.append("autosens")
    commands.append("run")
    return commands



def pac_commands(parameters):
    commands = [f"tech:pac",
        f"ei:{parameters['probe_pot']}",
        f"sens:{parameters['sensitivity']}",
        f"tp:{parameters['pulse_duration']}",
        f"td:{parameters['time_delay']}",
        f"sens2:{parameters['sensitivity2']}",
        f"iratio:{parameters['current_ratio']}",
        f"iabs:{parameters['current_abs']}",
        f"maxincr:{parameters['max_incr']}",
        f"withdraw:0.0",
        f"incrtime:{parameters['incrtime']}",
        ]
    if parameters['epon'] == True:
        commands.append("epon")
        commands.append(f"ep:{parameters['pulse_pot']}")
    elif parameters['epon'] == False:
        commands.append("epoff")
    if parameters['e2on'] == True:
        commands.append("e2on")
        commands.append(f"e2:{parameters['substrate_pot']}")
    elif parameters['e2on'] == False:
        commands.append("e2off")
    if parameters['i2on'] == True:
        commands.append("i2on")
    elif parameters['i2on'] == False:
        commands.append("i2off")
    if parameters['probe_stop'] == "Current ratio":
        commands.append("iratioon")
    elif parameters['probe_stop'] == "Absolute current":
        commands.append("iabson")  
    commands = commands + [f"run"]

    return commands

def pure_pac_commands(parameters):
    commands = [f"tech:pac",
        f"ei:{parameters['probe_pot']}",
        f"sens:{parameters['sensitivity']}",
        f"tp:{parameters['pulse_duration']}",
        f"td:{parameters['time_delay']}",
        f"sens2:{parameters['sensitivity2']}",
        f"iratio:{parameters['current_ratio']}",
        f"iabs:{parameters['current_abs']}",
        f"maxincr:{parameters['max_incr']}",
        f"withdraw:{parameters['withdraw']}",
        f"incrtime:{parameters['incrtime']}",
        ]
    if parameters['epon'] == True:
        commands.append("epon")
        commands.append(f"ep:{parameters['pulse_pot']}")
    elif parameters['epon'] == False:
        commands.append("epoff")
    if parameters['e2on'] == True:
        commands.append("e2on")
        commands.append(f"e2:{parameters['substrate_pot']}")
    elif parameters['e2on'] == False:
        commands.append("e2off")
    if parameters['i2on'] == True:
        commands.append("i2on")
    elif parameters['i2on'] == False:
        commands.append("i2off")
    if parameters['probe_stop'] == "Current ratio":
        commands.append("iratioon")
    elif parameters['probe_stop'] == "Absolute current":
        commands.append("iabson")  
    commands = commands + [f"run", f"folder:{parameters['output_folder']}",
                            f"tsave:{parameters['filename']}"]

    return commands

def position_leveling_commands(parameters):

    return (
        [f"zgoto:{parameters['initialz']}"]
        + pac_commands(parameters)
        + [f"folder:{PROJECT_DIR / 'pos_level'}", "tsave:pos1", 
           f"zgoto:{parameters['initialz']}", f"x:{parameters['xdist']}"]
        + pac_commands(parameters)
        + [f"folder:{PROJECT_DIR / 'pos_level'}", "tsave:pos2", 
           f"zgoto:{parameters['initialz']}", f"x:{-1*(parameters['xdist']/2)}", 
           f"y:{parameters['ydist']}"]
        + pac_commands(parameters)
        + [f"folder:{PROJECT_DIR / 'pos_level'}", "tsave:pos3", 
           f"zgoto:{parameters['initialz']}", f"x:{-1*(parameters['xdist']/2)}", 
           f"y:{-1*parameters['ydist']}"]
    )



def position_leveling(file1, file2, file3):
    #parse the files to get the stop distances
    dist1, cur1 = parse_file(file1)
    dist2, cur2 = parse_file(file2)
    dist3, cur3 = parse_file(file3)

    #calculate the offsets
    offset1 = dist2[-1] - dist1[-1]
    offset2 = dist3[-1] - dist1[-1]

    print("Height of position 2 is off by", offset1,"um relative to position 1")
    print("Height of position 3 is off by", offset2,"um relative to position 1")

    return offset1, offset2

def secm_commands(parameters):
    commands = [f"tech:secm",
                f"ei:{parameters['ei']}",
                f"qt:{parameters['qt']}",
                f"sens:{parameters['sens']}",
                f"e2:{parameters['e2']}",
                f"sens2:{parameters['sens2']}",
                f"ep:{parameters['ep']}",
                f"tp:{parameters['tp']}",
                f"ep2:{parameters['ep2']}",
                f"tp2:{parameters['tp2']}",
                f"td:{parameters['td']}",
                f"sens2:{parameters['sens2']}",
                f"ci:{parameters['ci']}",
                f"tol:{parameters['tol']}",
                f"xdist:{parameters['xdist']}",
                f"ydist:{parameters['ydist']}",
                f"incrdist:{parameters['incrdist']}",
                f"incrtime:{parameters['incrtime']}",
                f"maxincr:{parameters['maxincr']}",
                f"freq:{parameters['freq']}",
                f"amp:{parameters['amp']}",
                ]
    if parameters['i2on']== True:
        commands.append("i2on")
    elif parameters['i2on']== False:
        commands.append("i2off")
    if parameters['e2on']==True:
        commands.append("e2on")
    elif parameters['e2on']==False:
        commands.append("e2off")
    if parameters['ibias'] == True:
        commands.append("ibias")
    if parameters['autosens'] == True:
        commands.append("autosen")
    if parameters['epon']==True:
        commands.append("epon")
    elif parameters['epon']==False:
        commands.append("epoff")
    if parameters['e2on']==True:
        commands.append("e2on")
    elif parameters['e2on']==False:
        commands.append("e2off")
    if parameters['i2on']==True:
        commands.append("i2on")
    elif parameters['i2on']==False:
        commands.append("i2off")
    if parameters['secmmode']== "Amperometry":
        commands.append("secmmode:i")
    elif parameters['secmmode']== "Potentiometry":
        commands.append("secmmode:e")
    elif parameters['secmmode']=="Constant Current":
        commands.append("secmmode:ci")
    elif parameters['secmmode']=="Impedance":
        commands.append("secmmode:imp")
    if parameters['motor']=="Stepper":
        commands.append("stepper")
    elif parameters['motor']=="Piezo":
        commands.append("piezo")
    elif parameters['motor']=="Auto":
        commands.append("automotor")
    if parameters['longdir']=="X-axis":
        commands.append("xlong")
    elif parameters['longdir']=="Y-axis":
        commands.append("ylong")
    if parameters['originon']==True:
        commands.append("originon")
    elif parameters['originon']==False:
        commands.append("originoff")

    commands = commands + [f"run", f"fileoverride", f"folder:{parameters['output_folder']}", 
                            f"tsave:{parameters['filename']}"]

    return commands

def run_chi_macro(macro_commands):
    """Creates a .mcr file using the given commands, and instructs the chi920d.exe software to run it"""

    chi_exe = r"C:\chi\chi920d.exe"
    macro_file = PROJECT_DIR / "macro_files" / "test.mcr"
    
    with open(PROJECT_DIR / "macro_files" / "test.mcr", "wb") as f:
        f.write(b"\xff\xff\x01\x00")
        f.write("\r\n".join(macro_commands).encode("ascii"))

    # run the subprocess using the variables
    try:
        print("Launching CHI Software and executing macro...")
        
        macro_flag = f"/runmacro:{macro_file}"
        
        subprocess.run([chi_exe, macro_flag], check=True)
        print("Macro execution triggered successfully!")

    except FileNotFoundError:
        print(f"Error: Could not find the CHI software at {chi_exe}")
    except subprocess.CalledProcessError as e:
        print(f"Error during software execution: {e}")



