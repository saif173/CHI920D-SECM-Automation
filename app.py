import streamlit as st
import numpy as np
import pandas as pd
from process_pac_data import process_data_touchpoint
from pac_plotting import plot
from pac_curve_fit import model, plot_model, find_k, rms_error


# 1. App Title and Description
st.title("Probe Approach Curve Analyzer")
st.write("Upload your experiment text file")


# 2. File Uploader Widget
uploaded_file = st.file_uploader("Choose a text or CSV file", type=["txt", "csv"])

if uploaded_file is not None:

    # Load two columns
    data = pd.read_csv(
    uploaded_file,
    sep=r"\s+",
    header=None
)

    L_data= data.iloc[:, 0].to_numpy()
    I_data= data.iloc[:, 1].to_numpy()

    rg = st.number_input("Enter value of rg: ")
    a = st.number_input("Enter value of a:")
    
    if (a > 0) & (rg >0):
        rel_L, rel_I = process_data_touchpoint(L_data, I_data, a)

        mask = (rel_L > 0) & (rel_L < 3)
        rel_L = rel_L[mask]
        rel_I = rel_I[mask]
        k=find_k(rel_L,rel_I,rg)
        pred = model(rel_L,k,rg)
        rmse = rms_error(rel_I,pred)

        fig1 = plot(L_data, I_data, "Distance", "Current", "PAC Curve")
        fig2 = plot(rel_L, rel_I, "Normalized Distance", 
                "Normalized Current", "Normalized PAC curve")
        fig3 = plot_model(rel_L, rel_I, k,rg)
        st.pyplot(fig1)
        st.pyplot(fig2)
        st.pyplot(fig3)
        st.write("k =", k)
        st.write("RMS error =", rmse,"%")
    else:
        st.write("Error: a and rg must be a number greater than 0")
    





