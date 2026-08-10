import subprocess

import streamlit as st
from test_file import cv_commands, pac_commands, position_leveling, position_leveling_commands, run_chi_macro


st.set_page_config(
    # Title and icon for the browser's tab bar:
    page_title="SECM CONTROLLER",
    # Make the content take up the width of the page:
    layout="wide",
)
col1, col2 = st.columns(2)
st.title("SECM Controller")

mode = st.selectbox("Select Mode", ["Cyclic Voltammetry", "Position Leveling", "PAC Analysis"])

if mode == "Cyclic Voltammetry":
    st.title("Cyclic Voltammetry Parameters")
    col1, col2 = st.columns(2)

    with col1:
        st.header("Electrode 1 Parameters")

        v_ini=st.number_input("Initial voltage (V) (-10 to 10)", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)
        v_high=st.number_input("High voltage (V) (-10 to 10)", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)
        v_low=st.number_input("Low voltage (V) (-10 to 10)", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)
        v_final=st.number_input("Final voltage (V) (-10 to 10)", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)
        ini_direction=st.selectbox("Initial direction", ["Positive", "Negative"])
        scan_rate=st.number_input("Scan rate (V/s) (1e-6 to 1e4)", min_value=1e-6, max_value=1e4,format="%.2e")
        sweep_segments=st.number_input("Sweep segments (1 to 1e6)", min_value=1.0, max_value=1e6, value=1.0, step=1.0)
        sample_interval=st.number_input("Sample interval (s) (1e-3 to 0.064)", min_value=1e-3, max_value=0.064, value=0.001, step=0.001, format="%.4f")
        quiet_time=st.number_input("Quiet time (s) (0.0 to 1e5)", min_value=0.0, max_value=1e5, value=2.0, step=0.1)
        sensitivity=st.number_input("Sensitivity (A/V) (1e-12 to 0.1)", min_value=1e-12, max_value=0.1, value=1e-9,key="sensitivity1", format="%.2e" )
        auto_sens=st.checkbox("Auto Sensitivity")
        enable_final_e=st.checkbox("Allow potential scan to end at Final E")
        aux_signal_rec=st.checkbox("Record auxiliary signal")

    with col2:
        st.header("Electrode 2 Parameters")

        potential=st.number_input("Potential (V) (-10 to 10)", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)
        diff_scan = st.checkbox("Scan 2nd channel at constant potential difference with 1st channel")
        diff_e=st.number_input("Potential difference with 1st channel (V) (-0.2 to 0.2)", min_value=-0.2, max_value=0.2, value=0.0, step=0.1, disabled=not diff_scan)
        sensitivity2=st.number_input("Sensitivity (A/V) (1e-12 to 0.1)", min_value=1e-12, max_value=0.1, key="sensitivity2", format="%.2e")
        off =st.checkbox("Second working electrode off")
        constant_e=st.checkbox("Hold second working electrode at constant potential")
        scan = st.checkbox("Scan 2nd channel with 1st channel")

    if v_high - v_low <0.01:
        st.error("Error: High voltage must be greater than Low voltage by at least 0.01 V")

    if st.button("Submit Parameters"):
        st.session_state.cv_parameters = {
        "v_ini": v_ini,
        "v_high": v_high, "v_low": v_low, "v_final": v_final, "ini_direction": ini_direction,
        "scan_rate": scan_rate, "sweep_segments": sweep_segments, "sample_interval": sample_interval,  
        "quiet_time": quiet_time, "sensitivity": sensitivity,
        "auto_sens": auto_sens, "enable_final_e": enable_final_e, "aux_signal_rec": aux_signal_rec, "potential": potential, 
        "diff_scan": diff_scan, "diff_e": diff_e, "sensitivity2": sensitivity2, "off": off, "constant_e": constant_e, "scan": scan}
        st.write("Parameters submitted successfully!")

    if "cv_parameters" in st.session_state:
        if st.button("Run Cyclic Voltammetry"):
            run_chi_macro(cv_commands(st.session_state.cv_parameters))

if mode == "PAC Analysis":
    st.title("PAC Analysis Parameters")
    col1, col2 = st.columns(2)

    with col1:

        probe_pot=st.number_input("Probe potential (V) (-10 to 10)", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)
        sensitivity=st.number_input("Probe sensitivity (A/V) (1e-12 to 0.1)", min_value=1e-12, max_value=0.1, value=1e-9,key="sensitivity1", format="%.2e" )
        pulse_duration=st.number_input("Pulse duration (s) (1e-6 to 1e3)", min_value=1e-6, max_value=1e3, value=0.001, step=0.001, format="%.4f")
        time_delay=st.number_input("Time delay (s) (0.1 to 50)", min_value=0.0, max_value=100.0, value=0.1, step=0.01)
        sensitivity2=st.number_input("Substrate sensitivity (A/V) (1e-12 to 0.1)", min_value=1e-12, max_value=0.1, value=1e-9, key="sensitivity2", format="%.2e")
    with col2:
        substrate_pot=st.number_input("Substrate potential (V) (-10 to 10)", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)
        pulse_pot=st.number_input("Pulse potential (V) (-10 to 10)", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)
        current_ratio=st.number_input("Current ratio (I2/I1) (1 to 400)", min_value=1.0, max_value=400.0, value=1.0, step=0.01)
        current_abs=st.number_input("Current absolute value (A) (0 to 0.01)", min_value=0.0, max_value=0.01, value=1e-9,key="current_abs", format="%.2e" )
        max_incr = st.number_input("Maximum increment during approach (0.0001 to 1)", min_value=1e-6, max_value=10.0,value = 0.01, step = 0.001, format="%.4f")
        withdraw = st.number_input("Withdraw distance for probe retraction (um) (0 to 10000)", min_value=0.0,max_value = 10000.0,value = 5.0,step = 1.0)
        incrtime = st.number_input("Increment time (s) (0 to 100)", min_value=0.0,max_value = 100.0,value = 0.01,step = 0.01, format="%.2e")
        probe_stop = st.selectbox("Probe stop mode", ["Current ratio", "Absolute current"])
        e2on = st.checkbox("Enable substrate potential")
        epon = st.checkbox("Enable pulse potential")
        i2on = st.checkbox("Substrate current measurement")

    if st.button("Submit Parameters"):
        st.session_state.pac_parameters = {
        "probe_pot": probe_pot, "sensitivity": sensitivity, "pulse_duration": pulse_duration,
        "time_delay": time_delay, "sensitivity2": sensitivity2, "substrate_pot": substrate_pot,
        "pulse_pot": pulse_pot, "current_ratio": current_ratio, "current_abs": current_abs,
        "max_incr": max_incr, "withdraw": withdraw, "incrtime": incrtime, "probe_stop": probe_stop,
        "e2on": e2on, "epon": epon, "i2on": i2on}
        st.write("Parameters submitted successfully!")
        #st.text_input("Enter file name:", key="file_name")
    
    if "pac_parameters" in st.session_state:
        if st.button("Run PAC Analysis"):
    
            #filename = st.session_state.file_name
            run_chi_macro(pac_commands(st.session_state.pac_parameters))

        elif st.button("Run Position Leveling"):
            run_chi_macro(position_leveling_commands(st.session_state.pac_parameters))
            file1 = r"C:\chi\pos_level\pos1.txt"
            file2 = r"C:\chi\pos_level\pos2.txt"
            file3 = r"C:\chi\pos_level\pos3.txt"
            position_leveling(file1, file2, file3)

