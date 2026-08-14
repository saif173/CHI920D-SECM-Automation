import subprocess
import tkinter as tk
from tkinter import filedialog


import streamlit as st


def folder_picker(label="Output folder"):

    if "selected_folder" not in st.session_state:
        st.session_state.selected_folder = ""

    col1, col2 = st.columns([2, 1])

    with col1:
        st.text_input(
            label,
            value=st.session_state.selected_folder,
            disabled=True
        )

    with col2:
        if st.button("Browse", key=f"browse_{label}"):
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)

            folder = filedialog.askdirectory(
                title=f"Select {label}"
            )

            root.destroy()

            if folder:
                st.session_state.selected_folder = folder
                st.rerun()

    return st.session_state.selected_folder