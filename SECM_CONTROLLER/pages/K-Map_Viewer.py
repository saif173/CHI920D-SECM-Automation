import subprocess
import tkinter as tk
import streamlit as st

from folder_select import folder_picker

from commands import cv_commands, pac_commands,position_leveling, position_leveling_commands, run_chi_macro, secm_commands, k_map_commands
from k_map import k_map, plot_k_map


st.subheader("K-Map")

output_folder = folder_picker("Select a folder containing K-Map data")

rg = st.number_input("Enter value of RG")
a=st.number_input("Enter value of a")
box_length=3
shift = 0.5

if (rg>0) & (a>0):
    if st.button( "▶ Display K-Map", use_container_width=True):

        if not output_folder:
            st.warning("Please select folder first.")

        else:

            with st.spinner("Running K-map..."):
                k_values = k_map(output_folder, rg, a, box_length, 0, shift)
                fig = plot_k_map(k_values, box_length)
                st.pyplot(fig)