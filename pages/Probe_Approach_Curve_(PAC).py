import subprocess
import tkinter as tk
import streamlit as st
import os
import pandas as pd
from pac_analysis.file_parser import parse_file_st
from pac_analysis.process_pac_data import normalize_data, flip_data
from pac_analysis.pac_plotting import plot
from pac_analysis.pac_curve_fit import model, plot_model, find_k, rms_error, find_k_deluxe, find_k_deluxe_shift, find_i_infi_shift, find_k_shift, shifted_model
from pac_analysis.pac_selection import select_touchpoint
from pac_analysis.pac_curve_fit import find_i_infi

from folder_select import folder_picker

from commands import cv_commands, pac_commands,position_leveling, position_leveling_commands, run_chi_macro, secm_commands, k_map_commands, pure_pac_commands
from k_map import k_map, plot_k_map


st.set_page_config(
    page_title="PAC",
    layout="wide"
)

st.markdown("""
<style>
    header {
        visibility: hidden;
    }

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

st.title("Probe Approach Curve")

mode = st.selectbox("Select Task", ["Run PAC Scan", "Touch-point PAC Analyser"])

if mode == "Run PAC Scan":

    st.title("PAC Parameters")
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

                    st.session_state.offset1, st.session_state.offset2 = position_leveling(
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

                    with st.spinner("Running PAC Analysis..."):
                        run_chi_macro(
                        pure_pac_commands(st.session_state.pac_parameters)
                             )

        col1, col2 = st.columns(2)

    if (st.session_state.offset1 is not None) & (st.session_state.offset2 is not None):
        with col1:
            st.metric(
            "Offset 1",
            f"{st.session_state.offset1:.2f} µm"
            )

            if st.session_state.offset1 < 0:
                st.info(
                f"Position 2 is **{abs(st.session_state.offset1):.2f} µm higher** "
                "than Position 1."
                )
            elif st.session_state.offset1 > 0:
                st.info(
                f"Position 2 is **{st.session_state.offset1:.2f} µm lower** "
                "than Position 1."
                )
            else:
                st.info("Position 2 is level with Position 1.")

        with col2:
            st.metric(
            "Offset 2",
            f"{st.session_state.offset2:.2f} µm"
            )

            if st.session_state.offset2 < 0:
                st.info(
                f"Position 3 is **{abs(st.session_state.offset2):.2f} µm higher** "
                "than Position 1."
                )
            elif st.session_state.offset2 > 0:
                st.info(
                f"Position 3 is **{st.session_state.offset2:.2f} µm lower** "
                "than Position 1."
                )
            else:
                st.info("Position 3 is level with Position 1.")

if mode == "Touch-point PAC Analyser":

    col1,col2 = st.columns(2)



    st.subheader("Touch-Point Probe Approach Curve Analyzer")
    st.write("Upload your experiment text file")


    # file uploader
    uploaded_file = st.file_uploader("Choose a text or CSV file", type=["txt", "csv"])

    if uploaded_file is not None:
        L_data, I_data = parse_file_st(uploaded_file)
        L_data = flip_data(L_data) #flips the raw data to reflect shape of theoretical curve
    
        rg = st.number_input("Enter value of rg: ")
        a = st.number_input("Enter value of a:")

        fig1 = plot(L_data, I_data, "Distance/micrometers (arbitrary)", "Current/amps", "PAC Curve")
        st.write("Click a data-point to select a zero-point")

        touch_point = select_touchpoint(fig1)
        i_infi = find_i_infi(L_data, I_data, touch_point, a, rg)
    
   
        if (a > 0) & (rg >0) & (touch_point is not None) & (i_infi is not None):
            rel_L, rel_I = normalize_data(L_data, I_data, touch_point, a, i_infi)

            k=find_k_deluxe(L_data, I_data, rg, a, touch_point)
            pred = model(rel_L,k,rg) 
            rmse = rms_error(rel_I,pred)

            #define and show plots
            fig2 = plot(rel_L, rel_I, "Normalized Distance", 
                "Normalized Current", "Normalized PAC curve")
            fig3 = plot_model(rel_L, rel_I, k,rg)
            st.plotly_chart(fig2)
            st.plotly_chart(fig3)
            st.write("k =", k)
            st.write("Error is minimised when bulk current is estimated as:", i_infi, "Amperes")
            st.write("RMS error =", rmse,"%")
        else:
            st.write("Error: a and rg must be a number greater than 0")

