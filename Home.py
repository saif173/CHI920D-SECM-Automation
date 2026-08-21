import subprocess
import tkinter as tk
import streamlit as st
import sys
from pathlib import Path
import os



from folder_select import folder_picker

from commands import cv_commands, pac_commands,position_leveling, position_leveling_commands, run_chi_macro, secm_commands, k_map_commands, pure_pac_commands

st.set_page_config(
    page_title="Home",
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

st.title("CHI 920D Extra Functions")

st.subheader("Introduction")
st.write("This program grants the user the ability to perform extra " \
"functions using the CHI 920D Scanning Electrochemcial Microscope. It acts as an extension to the chi920d.exe software, providing automation for tedious tasks.")

st.write("Two new methods are included, the 'Position Leveler' and the 'K-Map', which can be accessed from the side-bar on the left of the screen. These are explained further below.")

selection = st.selectbox("Select method", ["Position Leveler", "K-Map"])

if selection == "Position Leveler":
    st.write("This method is used to level a sample.")
    st.write("It works by taking Probe Approach Curves (PACs) at three distinct points on the sample, which form an isoceles triangle, and compares the approach distance of the second and third points relative to the first. " \
    "The offsets are displayed, and the user can adjust the screws below the stage to " \
    "minimise these offsets to level their sample.")
    st.write("For this method to be effective, the user must first use the chi920d.exe software to move the probe close to the left edge of the sample, on the same horizontal line as the back two screws.")

    st.write("The user should adjust the scan positions carefully, with the guidance of the provided grid.")

if selection == "K-Map":
    st.write("This method creates a 2D colour map of k-values by scanning a certain region of the sample.")
    st.write("The 'Run Mapping' task scans an area by taking Probe Approach Curves at set intervals. The scan x-length and y-length as well as the respective increments are specified by the user. This data is output to the user's selected folder." \
    "The file for each position will be named 'pos_x coordinate_y coordinate_x increment_y increment'")
    st.write("The 'Plot K-Map' task can then be used to plot the gathered data. The user then specifies the folder containing the PAC files." \
    " The data for each position is processed, and approximate k-values are provided for each position. This process will take around 1 second for each pixel, " \
    "after which the 2D map will be presented. This image can be downloaded, along with a .txt file containing the positions and k-values.")




