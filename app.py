import io
from streamlit_plotly_events import plotly_events
import streamlit as st
import numpy as np
import pandas as pd
from process_pac_data import normalize_data, flip_data
from pac_plotting import plot
from pac_curve_fit import model, plot_model, find_k, rms_error


# app title and description
st.title("Probe Approach Curve Analyzer")
st.write("Upload your experiment text file")


# file uploader
uploaded_file = st.file_uploader("Choose a text or CSV file", type=["txt", "csv"])

if uploaded_file is not None:
    lines = uploaded_file.getvalue().decode("utf-8").splitlines()

    data_lines = []
    for line in lines:
        line = line.replace(",", " ")   # remove commas
        if not line.strip():
            continue

        try:
            float(line.split()[0])
            data_lines.append(line)
        except ValueError:
            pass

    data = pd.read_csv(
        io.StringIO("\n".join(data_lines)),
        sep=r"\s+",
        header=None
    )

    L_data = data.iloc[:, 0].to_numpy()
    I_data = data.iloc[:, 1].to_numpy()
    L_data = flip_data(L_data)

    rg = st.number_input("Enter value of rg: ")
    a = st.number_input("Enter value of a:")

    fig1 = plot(L_data, I_data, "Distance", "Current", "PAC Curve")
    st.write("Click a data-point to select a zero-point, click-again to select i-infinity point. (Or type directly into box)")

    if "click_count" not in st.session_state:
        st.session_state.click_count = 0

    if "touch_point" not in st.session_state:
        st.session_state.touch_point = None

    if "i_infi" not in st.session_state:
        st.session_state.i_infi = None


    event = st.plotly_chart(
    fig1,
    on_select="rerun",
    selection_mode="points"
    )

    if event.selection.points:
        point = event.selection.points[0]

        if st.session_state.click_count % 2 == 0:
            st.session_state.touch_point = point["x"]

        else:
            st.session_state.i_infi = point["y"]

        st.session_state.click_count += 1

    st.session_state.touch_point = st.number_input(
    "Selected zero-point",
    value=float(st.session_state.touch_point)
    if st.session_state.touch_point is not None else 0.0
    )
    i_infi_text = st.text_input(
    "Selected I-infinity",
    value=str(st.session_state.i_infi) if st.session_state.i_infi is not None else "0"
    )

    try:
        st.session_state.i_infi = float(i_infi_text)
    except ValueError:
        st.error("Please enter a valid number (e.g. 0.000001 or 1e-6).")

    touch_point = st.session_state.touch_point
    i_infi = st.session_state.i_infi
    
   
    if (a > 0) & (rg >0) & (touch_point is not None):
        rel_L, rel_I = normalize_data(L_data, I_data, touch_point, a, i_infi)

        mask= (rel_L>0)&(rel_L<3)
        rel_L=rel_L[mask]
        rel_I=rel_I[mask]

        k=find_k(rel_L,rel_I,rg)
        pred = model(rel_L,k,rg)
        rmse = rms_error(rel_I,pred)

        #define and show plots
        fig2 = plot(rel_L, rel_I, "Normalized Distance", 
                "Normalized Current", "Normalized PAC curve")
        fig3 = plot_model(rel_L, rel_I, k,rg)
        st.plotly_chart(fig2)
        st.plotly_chart(fig3)
        st.write("k =", k)
        st.write("RMS error =", rmse,"%")
    else:
        st.write("Error: a and rg must be a number greater than 0")
    





