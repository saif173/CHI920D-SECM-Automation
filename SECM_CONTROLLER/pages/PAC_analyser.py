import io
import streamlit as st
import pandas as pd
from pac_analysis.file_parser import parse_file
from pac_analysis.process_pac_data import normalize_data, flip_data
from pac_analysis.pac_plotting import plot
from pac_analysis.pac_curve_fit import model, plot_model, find_k, rms_error
from pac_analysis.pac_selection import select_touchpoint
from pac_analysis.pac_curve_fit import find_i_infi

col1,col2 = st.columns(2)


# app title and description
st.title("Probe Approach Curve Analyzer")
st.write("Upload your experiment text file")



uploaded_file = rf"C:\chi\pac_data\pac.txt"


L_data, I_data = parse_file(uploaded_file)
L_data = flip_data(L_data) #flips the raw data to reflect shape of theoretical curve
    
rg = st.number_input("Enter value of rg: ")
a = st.number_input("Enter value of a:")

fig1 = plot(L_data, I_data, "Distance/micrometers (arbitrary)", "Current/amps", "PAC Curve")
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
    st.write("Error is minimised when bulk current is estimated as:", i_infi, "Amperes")
    st.write("RMS error =", rmse,"%")
else:
    st.write("Error: a and rg must be a number greater than 0")