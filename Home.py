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


