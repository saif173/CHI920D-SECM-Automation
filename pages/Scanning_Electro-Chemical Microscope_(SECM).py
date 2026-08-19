import subprocess
import tkinter as tk
import streamlit as st
import os

from folder_select import folder_picker

from commands import cv_commands, pac_commands,position_leveling, position_leveling_commands, run_chi_macro, secm_commands, k_map_commands
from k_map import k_map, plot_k_map


st.set_page_config(
    page_title="SECM",
    layout="wide"
)

st.markdown("""
<style>
    

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


st.title("Scanning Electro-Chemical Microscopy")

mode = st.selectbox("Select Task", ["Run Scan", "Plot Scan"])

if mode == "Run Scan":

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

        secmfolder = folder_picker("Select an output folder")
            
        if st.button("▶ Run SECM Scan",use_container_width=True):
            
            if not secmfolder:
                st.warning("Please select an output folder first.")
            
            elif "secm_parameters" not in st.session_state:
                st.warning("Please submit the SECM parameters first.")
            
            else:
                st.session_state.secm_parameters["output_folder"] = secmfolder
            
                with st.spinner("Running SECM Scan..."):
                    run_chi_macro(secm_commands(st.session_state.secm_parameters)
                                         )