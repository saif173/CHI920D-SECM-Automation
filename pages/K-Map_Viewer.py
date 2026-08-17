import subprocess
import tkinter as tk
import streamlit as st
import os

from folder_select import folder_picker

from commands import cv_commands, pac_commands,position_leveling, position_leveling_commands, run_chi_macro, secm_commands, k_map_commands
from k_map import k_map, plot_k_map


st.subheader("K-Map")

output_folder = folder_picker("Select a folder containing K-Map data")


files = os.listdir(output_folder)

last_file = files[-1]

x, y = last_file.removesuffix(".txt").split("_")[-2:]

x = int(x)
y = int(y)

rg = st.number_input("Enter value of RG")
a=st.number_input("Enter value of a")
shift = 0.5

if (rg>0) & (a>0):
    if st.button( "▶ Display K-Map", use_container_width=True):

        if not output_folder:
            st.warning("Please select folder first.")

        else:

            with st.spinner("Running K-map..."):
                k_values = k_map(output_folder, rg, a, 0)
                fig = plot_k_map(k_values, x, y)
                st.pyplot(fig)