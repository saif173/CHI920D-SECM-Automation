
import streamlit as st




from commands import cv_commands, run_chi_macro



st.set_page_config(
    page_title="CV",
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


st.title("Cyclic Voltammetry")
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