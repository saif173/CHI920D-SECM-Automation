import subprocess
import tkinter as tk
import streamlit as st
import sys
from pathlib import Path

from folder_select import folder_picker

from commands import cv_commands, pac_commands,position_leveling, position_leveling_commands, run_chi_macro, secm_commands, k_map_commands




st.set_page_config(
    # Title and icon for the browser's tab bar:
    page_title="SECM CONTROLLER",
    # Make the content take up the width of the page:
    layout="wide",
)

st.title("SECM Controller")

mode = st.selectbox("Select Mode", ["Cyclic Voltammetry", "K-Map", "PAC Analysis", "SECM Scan"])

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
        scan_rate=st.number_input("Scan rate (V/s) (1e-6 to 1e4)", min_value=1e-6, max_value=1e4,value= 0.1, format="%.2e")
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
        sensitivity2=st.number_input("Sensitivity (A/V) (1e-12 to 0.1)", min_value=1e-12, max_value=0.1,value=1e-9, key="sensitivity2", format="%.2e")
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

    st.title("PAC Analysis")
    st.caption("Configure the probe approach curve experiment")

    filename = st.text_input(
        "Output file name",
        placeholder="e.g. pac_scan_001"
    )

    # ─────────────────────────────────────────────
    # ROW 1
    # ─────────────────────────────────────────────

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("Probe Electrode")

            probe_pot = st.number_input(
                "Probe potential (V)",
                min_value=-10.0,
                max_value=10.0,
                value=0.0,
                step=0.1,
                key="pac_probe_pot"
            )

            sensitivity = st.number_input(
                "Probe sensitivity (A/V)",
                min_value=1e-12,
                max_value=0.1,
                value=1e-9,
                format="%.2e",
                key="pac_sensitivity"
            )

    with col2:
        with st.container(border=True):
            st.subheader("Probe E Pulse Before Sampling")

            pulse_pot = st.number_input(
                "Pulse potential (V)",
                min_value=-10.0,
                max_value=10.0,
                value=0.0,
                step=0.1,
                key="pac_pulse_pot"
            )

            pulse_duration = st.number_input(
                "Pulse duration (s)",
                min_value=1e-6,
                max_value=1e3,
                value=0.001,
                step=0.001,
                format="%.4f",
                key="pac_pulse_duration"
            )

            time_delay = st.number_input(
                "Time delay (s)",
                min_value=0.0,
                max_value=100.0,
                value=0.1,
                step=0.01,
                key="pac_time_delay"
            )

            epon = st.checkbox(
                "Enable pulse potential",
                key="pac_epon"
            )

    # ─────────────────────────────────────────────
    # ROW 2
    # ─────────────────────────────────────────────

    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):
            st.subheader("Substrate Electrode")

            substrate_pot = st.number_input(
                "Substrate potential (V)",
                min_value=-10.0,
                max_value=10.0,
                value=0.0,
                step=0.1,
                key="pac_substrate_pot"
            )

            sensitivity2 = st.number_input(
                "Substrate sensitivity (A/V)",
                min_value=1e-12,
                max_value=0.1,
                value=1e-9,
                format="%.2e",
                key="pac_sensitivity2"
            )

            e2on = st.checkbox(
                "Enable substrate potential",
                key="pac_e2on"
            )

            i2on = st.checkbox(
                "Substrate current measurement",
                key="pac_i2on"
            )

    with col4:
        with st.container(border=True):
            st.subheader("Stop Parameters")

            current_ratio = st.number_input(
                "Current ratio (%)",
                min_value=1.0,
                max_value=400.0,
                value=50.0,
                step=0.01,
                key="pac_current_ratio"
            )

            current_abs = st.number_input(
                "Current absolute value (A)",
                min_value=0.0,
                max_value=0.01,
                value=1e-9,
                format="%.2e",
                key="pac_current_abs"
            )

            max_incr = st.number_input(
                "Maximum increment during approach (µm)",
                min_value=1e-6,
                max_value=10.0,
                value=0.01,
                step=0.001,
                format="%.4f",
                key="pac_max_incr"
            )

            withdraw = st.number_input(
                "Withdraw distance (µm)",
                min_value=0.0,
                max_value=10000.0,
                value=5.0,
                step=1.0,
                key="pac_withdraw"
            )

            incrtime = st.number_input(
                "Increment time (s)",
                min_value=0.0,
                max_value=100.0,
                value=0.01,
                step=0.01,
                format="%.2e",
                key="pac_incrtime"
            )

            probe_stop = st.selectbox(
                "Probe stop mode",
                ["Current ratio", "Absolute current"],
                key="pac_probe_stop"
            )

    # ─────────────────────────────────────────────
    # SUBMIT PARAMETERS
    # ─────────────────────────────────────────────

    st.divider()

    if st.button(
        "Submit Parameters",
        type="secondary",
        use_container_width=True
    ):
        st.session_state.pac_parameters = {
            "probe_pot": probe_pot,
            "sensitivity": sensitivity,
            "pulse_duration": pulse_duration,
            "time_delay": time_delay,
            "sensitivity2": sensitivity2,
            "substrate_pot": substrate_pot,
            "pulse_pot": pulse_pot,
            "current_ratio": current_ratio,
            "current_abs": current_abs,
            "max_incr": max_incr,
            "withdraw": withdraw,
            "incrtime": incrtime,
            "probe_stop": probe_stop,
            "e2on": e2on,
            "epon": epon,
            "i2on": i2on,
            "filename": filename
        }

        st.success("Parameters submitted successfully!")

    
    # run
    if "pac_parameters" in st.session_state:

        st.divider()

        st.subheader("Experiment Controls")

        run_col1, run_col2 = st.columns(2)


        with run_col2:
            if st.button("⚙ Run Position Leveling", use_container_width=True
                            ):
                with st.spinner("Running position leveling..."):

                    run_chi_macro(
                    position_leveling_commands(
                    st.session_state.pac_parameters
                    )
                    )

                    file1 = r"C:\secm\pos_level\pos1.txt"
                    file2 = r"C:\secm\pos_level\pos2.txt"
                    file3 = r"C:\secm\pos_level\pos3.txt"

                    offset1, offset2 = position_leveling(
                    file1, file2, file3
                        )


        with run_col1:

            st.subheader("PAC Analysis")

            folder = folder_picker("Select an output folder")

            if st.button(
                "▶ Run PAC Analysis",
                use_container_width=True
                ):

                if not folder:
                    st.warning("Please select an output folder first.")

                elif "pac_parameters" not in st.session_state:
                    st.warning("Please submit the PAC parameters first.")

                else:
                    st.session_state.pac_parameters["output_folder"] = folder

                    with st.spinner("Running K-map..."):
                        run_chi_macro(
                        pac_commands(st.session_state.pac_parameters)
                             )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
            "Offset 1",
            f"{offset1:.2f} µm"
            )

            if offset1 < 0:
                st.info(
                f"Position 2 is **{abs(offset1):.2f} µm higher** "
                "than Position 1."
                )
            elif offset1 > 0:
                st.info(
                f"Position 2 is **{offset1:.2f} µm lower** "
                "than Position 1."
                )
            else:
                st.info("Position 2 is level with Position 1.")

        with col2:
            st.metric(
            "Offset 2",
            f"{offset2:.2f} µm"
            )

            if offset2 < 0:
                st.info(
                f"Position 3 is **{abs(offset2):.2f} µm higher** "
                "than Position 1."
                )
            elif offset2 > 0:
                st.info(
                f"Position 3 is **{offset2:.2f} µm lower** "
                "than Position 1."
                )
            else:
                st.info("Position 3 is level with Position 1.")

if mode == "SECM Scan":

    st.title("SECM Scan")
    st.caption("Configure the parameters for the SECM experiment")

    filename = st.text_input(
        "Output file name",
        placeholder="e.g. scan_001"
    )

    # ─────────────────────────────────────────────
    # ROW 1
    # ─────────────────────────────────────────────

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("Probe Electrode")

            ei = st.number_input(
                "Probe E (V)",
                min_value=-10.0,
                max_value=10.0,
                value=0.0,
                step=0.1,
                format="%.2f",
                key="secm_ei"
            )

            sens = st.number_input(
                "Probe sensitivity (A/V)",
                min_value=1e-12,
                max_value=0.1,
                value=1e-9,
                step=1e-12,
                format="%.2e",
                key="secm_sens"
            )

            qt = st.number_input(
                "Quiet Time (s)",
                min_value=0.0,
                max_value=100000.0,
                value=0.0,
                step=0.1,
                format="%.3f",
                key="secm_qt"
            )

            st.subheader("Substrate Electrode")

            e2 = st.number_input(
                "Substrate E (V)",
                min_value=-10.0,
                max_value=10.0,
                value=0.0,
                step=0.1,
                format="%.2f",
                key="secm_e2"
            )

            sens2 = st.number_input(
                "Substrate sensitivity (A/V)",
                min_value=1e-12,
                max_value=0.1,
                value=1e-9,
                step=1e-12,
                format="%.2e",
                key="secm_sens2"
            )

            e2on = st.checkbox(
                "E On",
                key="secm_e2on"
            )

            i2on = st.checkbox(
                "i2 On",
                key="secm_i2on"
            )

    with col2:
        with st.container(border=True):
            st.subheader("Probe E Pulse Before Sampling")

            ep = st.number_input(
                "Pulse E (V)",
                min_value=-10.0,
                max_value=10.0,
                value=0.0,
                step=0.1,
                format="%.2f",
                key="secm_ep"
            )

            tp = st.number_input(
                "Pulse duration (s)",
                min_value=0.0,
                max_value=10.0,
                value=0.001,
                step=0.001,
                format="%.6f",
                key="secm_tp"
            )

            ep2 = st.number_input(
                "Pulse 2 E (V)",
                min_value=-10.0,
                max_value=10.0,
                value=0.0,
                step=0.1,
                format="%.2f",
                key="secm_ep2"
            )

            tp2 = st.number_input(
                "Pulse 2 duration (s)",
                min_value=0.0,
                max_value=10.0,
                value=0.0,
                step=0.001,
                format="%.6f",
                key="secm_tp2"
            )

            td = st.number_input(
                "Time delay (s)",
                min_value=0.1,
                max_value=50.0,
                value=0.1,
                step=0.01,
                format="%.3f",
                key="secm_td"
            )

            epon = st.checkbox(
                "Enable Pulse E",
                key="secm_epon"
            )

    # ─────────────────────────────────────────────
    # ROW 2
    # ─────────────────────────────────────────────

    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):
            st.subheader("Constant Current Mode")

            ci = st.number_input(
                "Constant Current (A)",
                min_value=5e-12,
                max_value=1e-6,
                value=1e-9,
                step=1e-12,
                format="%.2e",
                key="secm_ci"
            )

            tol = st.number_input(
                "Tolerance (%)",
                min_value=0.1,
                max_value=10.0,
                value=1.0,
                step=0.1,
                format="%.2f",
                key="secm_tol"
            )

            maxincr = st.number_input(
                "Max Z increment (µm)",
                min_value=0.0001,
                max_value=1.0,
                value=0.01,
                step=0.0001,
                format="%.4f",
                key="secm_maxincr"
            )

    with col4:
        with st.container(border=True):
            st.subheader("Probe Travel")

            xdist = st.number_input(
                "X Distance (µm)",
                min_value=0.01,
                max_value=50000.0,
                value=100.0,
                step=1.0,
                format="%.2f",
                key="secm_xdist"
            )

            ydist = st.number_input(
                "Y Distance (µm)",
                min_value=0.01,
                max_value=50000.0,
                value=100.0,
                step=1.0,
                format="%.2f",
                key="secm_ydist"
            )

            incrdist = st.number_input(
                "Increment Distance (µm)",
                min_value=0.0001,
                max_value=100.0,
                value=0.01,
                step=0.0001,
                format="%.4f",
                key="secm_incrdist"
            )

            incrtime = st.number_input(
                "Increment Time (s)",
                min_value=0.002,
                max_value=0.2,
                value=0.01,
                step=0.001,
                format="%.4f",
                key="secm_incrtime"
            )

    # ─────────────────────────────────────────────
    # ROW 3
    # ─────────────────────────────────────────────

    col5, col6 = st.columns(2)

    with col5:
        with st.container(border=True):
            st.subheader("Impedance Mode")

            freq = st.number_input(
                "Frequency (Hz)",
                min_value=1000.0,
                max_value=1000000.0,
                value=10000.0,
                step=1000.0,
                format="%.0f",
                key="secm_freq"
            )

            amp = st.number_input(
                "Amplitude (V)",
                min_value=0.1,
                max_value=0.4,
                value=0.1,
                step=0.01,
                format="%.2f",
                key="secm_amp"
            )

            ibias = st.checkbox(
                "Bias DC Current",
                key="secm_ibias"
            )

            autosens = st.checkbox(
                "AutoSens",
                key="secm_autosens"
            )

    with col6:
        with st.container(border=True):
            st.subheader("Selections")

            secmmode = st.selectbox(
                "SECM Mode",
                [
                    "Amperometry",
                    "Potentiometry",
                    "Constant Current",
                    "Impedance"
                ],
                key="secm_mode"
            )

            motor = st.selectbox(
                "Motor Selection",
                ["Auto", "Stepper", "Piezo"],
                key="secm_motor"
            )

            longdir = st.selectbox(
                "Long Travel Direction",
                ["X-axis", "Y-axis"],
                key="secm_longdir"
            )

            originon = st.checkbox(
                "Return to Origin after Run",
                key="secm_originon"
            )

    # ─────────────────────────────────────────────
    # SUBMIT PARAMETERS
    # ─────────────────────────────────────────────

    st.divider()

    if st.button(
        "Submit Parameters",
        type="secondary",
        use_container_width=True
    ):
        st.session_state.secm_parameters = {
            "ei": ei,
            "sens": sens,
            "qt": qt,
            "e2": e2,
            "sens2": sens2,
            "ep": ep,
            "e2on": e2on,
            "i2on": i2on,
            "tp": tp,
            "ep2": ep2,
            "tp2": tp2,
            "td": td,
            "epon": epon,
            "ci": ci,
            "tol": tol,
            "maxincr": maxincr,
            "xdist": xdist,
            "ydist": ydist,
            "incrdist": incrdist,
            "incrtime": incrtime,
            "freq": freq,
            "amp": amp,
            "ibias": ibias,
            "autosens": autosens,
            "secmmode": secmmode,
            "motor": motor,
            "longdir": longdir,
            "originon": originon,
            "filename": filename
        }

        st.success("Parameters submitted successfully!")

    # ─────────────────────────────────────────────
    # RUN
    # ─────────────────────────────────────────────

    if "secm_parameters" in st.session_state:

        st.divider()

        if st.button(
            "▶ Run SECM",
            type="primary",
            use_container_width=True
        ):
            run_chi_macro(
                secm_commands(
                    st.session_state.secm_parameters
                )
            )

if mode == "K-Map":

    st.title("K-Map")
    st.caption("Configure the K-map")

    # ─────────────────────────────────────────────
    # ROW 1
    # ─────────────────────────────────────────────

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("Probe Electrode")

            probe_pot = st.number_input(
                "Probe potential (V)",
                min_value=-10.0,
                max_value=10.0,
                value=0.0,
                step=0.1,
                key="pac_probe_pot"
            )

            sensitivity = st.number_input(
                "Probe sensitivity (A/V)",
                min_value=1e-12,
                max_value=0.1,
                value=1e-9,
                format="%.2e",
                key="pac_sensitivity"
            )

    with col2:
        with st.container(border=True):
            st.subheader("Probe E Pulse Before Sampling")

            pulse_pot = st.number_input(
                "Pulse potential (V)",
                min_value=-10.0,
                max_value=10.0,
                value=0.0,
                step=0.1,
                key="pac_pulse_pot"
            )

            pulse_duration = st.number_input(
                "Pulse duration (s)",
                min_value=1e-6,
                max_value=1e3,
                value=0.001,
                step=0.001,
                format="%.4f",
                key="pac_pulse_duration"
            )

            time_delay = st.number_input(
                "Time delay (s)",
                min_value=0.0,
                max_value=100.0,
                value=0.1,
                step=0.01,
                key="pac_time_delay"
            )

            epon = st.checkbox(
                "Enable pulse potential",
                key="pac_epon"
            )

    # ─────────────────────────────────────────────
    # ROW 2
    # ─────────────────────────────────────────────

    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):
            st.subheader("Substrate Electrode")

            substrate_pot = st.number_input(
                "Substrate potential (V)",
                min_value=-10.0,
                max_value=10.0,
                value=0.0,
                step=0.1,
                key="pac_substrate_pot"
            )

            sensitivity2 = st.number_input(
                "Substrate sensitivity (A/V)",
                min_value=1e-12,
                max_value=0.1,
                value=1e-9,
                format="%.2e",
                key="pac_sensitivity2"
            )

            e2on = st.checkbox(
                "Enable substrate potential",
                key="pac_e2on"
            )

            i2on = st.checkbox(
                "Substrate current measurement",
                key="pac_i2on"
            )

    with col4:
        with st.container(border=True):
            st.subheader("Stop Parameters")

            current_ratio = st.number_input(
                "Current ratio (%)",
                min_value=1.0,
                max_value=400.0,
                value=50.0,
                step=0.01,
                key="pac_current_ratio"
            )

            current_abs = st.number_input(
                "Current absolute value (A)",
                min_value=0.0,
                max_value=0.01,
                value=1e-9,
                format="%.2e",
                key="pac_current_abs"
            )

            max_incr = st.number_input(
                "Maximum increment during approach (µm)",
                min_value=1e-6,
                max_value=10.0,
                value=0.01,
                step=0.001,
                format="%.4f",
                key="pac_max_incr"
            )

            withdraw = st.number_input(
                "Withdraw distance (µm)",
                min_value=0.0,
                max_value=10000.0,
                value=5.0,
                step=1.0,
                key="pac_withdraw"
            )

            incrtime = st.number_input(
                "Increment time (s)",
                min_value=0.0,
                max_value=100.0,
                value=0.01,
                step=0.01,
                format="%.2e",
                key="pac_incrtime"
            )

            probe_stop = st.selectbox(
                "Probe stop mode",
                ["Current ratio", "Absolute current"],
                key="pac_probe_stop"
            )
    initial_z=st.number_input("Initial Z-coordinate (check chi920d.exe software)", value=17000.0, 
                             min_value=100.0, max_value=25000.0, 
                             placeholder="Open the chi920d.exe program to set initial z-coordinate")
    x_dist = st.number_input("X-length (µm)")
    y_dist = st.number_input("Y-length (µm)")
    x_incr = st.number_input("Increment in x (µm)")
    y_incr = st.number_input("Increment in y (µm)")
    x_pixels = int(x_dist // x_incr) + 1
    y_pixels = int(y_dist // y_incr) + 1
    total = int(x_pixels * y_pixels) 
    st.write(x_pixels, "x", y_pixels)
    st.write(total, "pixels in total")
    returntostart = st.checkbox("Return to starting position after run")

    # ─────────────────────────────────────────────
    # SUBMIT PARAMETERS
    # ─────────────────────────────────────────────

    st.divider()
    if (x_incr >0) & (y_incr>0):
        if st.button(
        "Submit Parameters",
        type="secondary",
        use_container_width=True
        ):
            st.session_state.kmap_parameters = {
            "probe_pot": probe_pot,
            "sensitivity": sensitivity,
            "pulse_duration": pulse_duration,
            "time_delay": time_delay,
            "sensitivity2": sensitivity2,
            "substrate_pot": substrate_pot,
            "pulse_pot": pulse_pot,
            "current_ratio": current_ratio,
            "current_abs": current_abs,
            "max_incr": max_incr,
            "withdraw": withdraw,
            "incrtime": incrtime,
            "probe_stop": probe_stop,
            "e2on": e2on,
            "epon": epon,
            "i2on": i2on,
            "initialz":initial_z,
            "originon":returntostart
        }

            st.success("Parameters submitted successfully!")

    
    # run
    if "kmap_parameters" in st.session_state:

            st.subheader("K-Map")

            output_folder = folder_picker("Select or create an empty folder")

            if st.button(
                "▶ Run K-Map (the current position will be the bottom left corner of scan)",
                use_container_width=True
                ):

                if not output_folder:
                    st.warning("Please select an output folder first.")

                elif "kmap_parameters" not in st.session_state:
                    st.warning("Please submit the K-Map parameters first.")

                else:
                    st.session_state.kmap_parameters["output_folder"] = output_folder

                    with st.spinner("Running K-map..."):
                        run_chi_macro(
                        k_map_commands(st.session_state.kmap_parameters)
                             )
                        


