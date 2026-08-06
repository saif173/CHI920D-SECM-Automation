import os
import subprocess
from secm_controller.cv import parameters



macro_commands = ["xgoto:0.5"]

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
    commands.append(f"run")
    return commands


def run_chi_macro(macro_commands):

    chi_exe = r"C:\chi\chi920d.exe"
    macro_file = r"C:\chi\macro_commands.mcr"
    
    with open(macro_file, "w", encoding="utf-8") as file:
        for command in macro_commands:
            file.write(command + "\n")

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

run_chi_macro(cv_commands(parameters))



