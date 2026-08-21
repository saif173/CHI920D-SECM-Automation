
import streamlit as st

import pandas as pd

from folder_select import folder_picker

from commands import run_chi_macro, k_map_commands
from k_map import k_map, plot_k_map


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

st.title("K-Map")


mode = st.selectbox("Select Task", ["Run Mapping","Plot K-Map"])

if mode == "Run Mapping":

    st.subheader("K-Map Parameters")
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

    col5, col6 = st.columns(2)

    with col5:
            with st.container(border=True):
                st.subheader("Scan parameters")
                initial_z=st.number_input("Initial Z-coordinate (check chi920d.exe software)", value=17000.0, 
                             min_value=100.0, max_value=25000.0, 
                             placeholder="Open the chi920d.exe program to set initial z-coordinate")
                x_dist = st.number_input("X-length (µm)", value =100.0, min_value=0.0)
                y_dist = st.number_input("Y-length (µm)", value =100.0, min_value=0.0)
                x_incr = st.number_input("Increment in x (µm)", value=10.0, min_value=0.0, max_value=1000.0)
                y_incr = st.number_input("Increment in y (µm)" , value = 10.0, min_value=0.0, max_value=1000.0)
                x_pixels = int(x_dist // x_incr) + 1
                y_pixels = int(y_dist // y_incr) + 1
                real_x_dist = x_incr * (x_pixels-1)
                real_y_dist = y_incr * (y_pixels-1)
                total = int(x_pixels * y_pixels)

    with col6:
        with st.container(border=True): 
            st.write("True scan distance X (µm):", real_x_dist, "True scan distance Y (µm):", real_y_dist)
            st.write(x_pixels, " X pixels", y_pixels, "Y pixels", total, "pixels in total")
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
            "incrtime": incrtime,
            "probe_stop": probe_stop,
            "e2on": e2on,
            "epon": epon,
            "i2on": i2on,
            "initialz":initial_z,
            "originon":returntostart, "xdist":real_x_dist, 
            "ydist":real_y_dist, "xincr":x_incr, "yincr":y_incr
        }

            st.success("Parameters submitted successfully!")

    
    # run
    if "kmap_parameters" in st.session_state:

            output_folder = folder_picker("Select or create an empty folder")

            if st.button(
                "▶ Run K-Map (the initial position will be the bottom left corner of scan)",
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
                        




if mode == "Plot K-Map":

    st.subheader("K-Map Plotter")

    output_folder = folder_picker("Select a folder containing K-Map data")

    if output_folder is not "":

        rg = st.number_input("Enter value of RG")
        a=st.number_input("Enter value of a (µm)")

        if (rg>0) & (a>0):
            if st.button( "▶ Display K-Map", use_container_width=True):

                if not output_folder:
                    st.warning("Please select folder first.")

                else:

                    with st.spinner("Running K-map..."):
                        k_values, xincr, yincr = k_map(output_folder, rg, a, 0)

                        # Store results in session state
                        st.session_state.k_values = k_values
                        st.session_state.xincr = xincr
                        st.session_state.yincr = yincr

                # Display K-map if it exists
            if "k_values" in st.session_state:

                        fig = plot_k_map(st.session_state.k_values,st.session_state.xincr,
                            st.session_state.yincr)

                        st.pyplot(fig)

                        # Create download data
                        df = pd.DataFrame([(x, y, k) for (x, y), k 
                                           in st.session_state.k_values.items()],
                                    columns=["X (um)", "Y (um)", "k (/m)"])

                        txt = df.to_csv(index=False)

                        st.download_button(label="Download as .txt", data=txt, 
                                           file_name="k_values.txt",
                                            mime="text/plain",
                                            use_container_width=True)