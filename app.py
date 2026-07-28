import io
import streamlit as st
import pandas as pd
from process_pac_data import normalize_data, flip_data
from pac_plotting import plot
from pac_curve_fit import model, plot_model, find_k, rms_error
from pac_selection import select_params, select_touchpoint
from pac_curve_fit import find_i_infi

col1,col2 = st.columns(2)


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

    L_data = data.iloc[:, 0].to_numpy()  #parses data from file
    I_data = data.iloc[:, 1].to_numpy()
    L_data = flip_data(L_data) #flips the raw data to reflect shape of theoretical curve
    
    rg = st.number_input("Enter value of rg: ")
    a = st.number_input("Enter value of a:")

    fig1 = plot(L_data, I_data, "Distance", "Current", "PAC Curve")
    st.write("Click a data-point to select a zero-point")

    touch_point = select_touchpoint(fig1)
    i_infi = find_i_infi(L_data, I_data, touch_point, a, rg)
    
   
    if (a > 0) & (rg >0) & (touch_point is not None) & (i_infi is not None):
        rel_L, rel_I = normalize_data(L_data, I_data, touch_point, a, i_infi)

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
        st.write("Error is minimised when bulk current is estimated as:", i_infi)
        st.write("RMS error =", rmse,"%")
    else:
        st.write("Error: a and rg must be a number greater than 0")
    





