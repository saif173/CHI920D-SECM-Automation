import subprocess
import tkinter as tk
import streamlit as st
import os
from pathlib import Path
from folder_select import folder_picker
from image import show_position_grid

from commands import cv_commands, pac_commands,position_leveling, position_leveling_commands, run_chi_macro, secm_commands, k_map_commands
from k_map import k_map, plot_k_map

PROJECT_DIR = Path(__file__).resolve().parent.parent

if "offset1" not in st.session_state:
    st.session_state.offset1 = None

if "offset2" not in st.session_state:
    st.session_state.offset2 = None

if "pagenum" not in st.session_state:
    st.session_state.pagenum = 1

st.set_page_config(
    page_title="K-Map",
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

st.title("Position Leveler")


st.caption("Configure the PAC Parameters")

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
        
    # ─────────────────────────────────────────────
    # ROW 2
    # ─────────────────────────────────────────────

col3, col4 = st.columns(2)

with col3:
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

initialz = st.number_input("Initial Z coordinate (check chi920d.exe software)", 
                           value=17000, min_value=0, max_value=25000)
xdist = st.number_input("Distance travelled to position 2 (x)", value=1000.0, min_value=0.0, max_value=4000.0)
ydist = st.number_input("Distance travelled to position 3 (y)", value=1000.0, min_value=0.0, max_value=4000.0)

fig = show_position_grid(xdist, ydist)
st.pyplot(fig)





    # ───────────────────────────────────────────   # SUBMIT PARAMETERS
    # ─────────────────────────────────────────────
st.divider()

if st.button(
        "Submit Parameters",
        type="secondary",
        use_container_width=True
        ):
        st.session_state.pl_parameters = {
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
            "i2on": i2on, "initialz":initialz, "xdist": xdist, "ydist": ydist
        }

        st.success("Parameters submitted successfully!")
        
    

if "pl_parameters" in st.session_state:

            if st.button("⚙ Run Position Leveling", use_container_width=True
                            ):
                with st.spinner("Running position leveling..."):


                    run_chi_macro(
                    position_leveling_commands(
                    st.session_state.pl_parameters
                    )
                    )

                    file1 = PROJECT_DIR / "pos_level" / "pos1.txt"
                    file2 = PROJECT_DIR / "pos_level" / "pos2.txt"
                    file3 = PROJECT_DIR / "pos_level" / "pos3.txt"

                    st.session_state.offset1, st.session_state.offset2 = position_leveling(
                    file1, file2, file3
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