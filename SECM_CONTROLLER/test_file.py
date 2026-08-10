import os
import subprocess

from pac_analysis.file_parser import parse_file




test = ["tech:cv","eh:0.3","ei:0.1","run"]
print(test)
test2 = ["x:3000", "xreset"]
empty = ["run"]

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
    commands = commands + [f"run", f"folder: C:\chi\pac_data", f"tsave:pac_data"]

    return commands

def position_leveling_commands(parameters):
    commands = (pac_commands(parameters) 
    + [f"folder:C:\chi\pos_level", f"tsave:pos1", f"x:1500", f"zgoto:10000"]
    + pac_commands(parameters)
    + [f"folder:C:\chi\pos_level", f"tsave:pos2", f"x:-750", f"y:1500", f"zgoto:10000"]
    +pac_commands(parameters)
    + [f"folder:C:\chi\pos_level", f"tsave:pos3", f"x:-750", f"y:-1500", f"zgoto:10000"])

    return commands


def position_leveling(file1, file2, file3):
    #parse the files to get the stop distances
    stop1 = parse_file(file1)[-1]
    stop2 = parse_file(file2)[-1]
    stop3 = parse_file(file3)[-1]

    #calculate the offsets
    offset1 = stop2 - stop1
    offset2 = stop3 - stop1

    print("Height of position 2 is off by", offset1, "relative to position 1")
    print("Height of position 3 is off by", offset2, "relative to position 1")

    return offset1, offset2


def run_chi_macro(macro_commands):

    chi_exe = r"C:\chi\chi920d.exe"
    macro_file = r"C:\chi\test.mcr"
    
    with open(r"C:\chi\test.mcr", "wb") as f:
        f.write(b"\xff\xff\x00\x00")
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




#subprocess.run([r"C:\chi\chi920d.exe", "/runmacro:C:\\chi\\test.mcr"], check=True)
#subprocess.run([r"C:\chi\chi920d.exe", "/runmacro:C:\\chi\\cv_ideal.mcr"], check=True)

"""run_chi_macro(test)"""

"""with open(r"C:\chi\ideal.mcr", "rb") as f:
    print(f.read(20))"""

"""with open(r"C:\chi\test.mcr", "rb") as f:
    print(f.read(40))

with open(r"C:\chi\macro\pop.mcr", "rb") as f:
    print(f.read(40))"""
