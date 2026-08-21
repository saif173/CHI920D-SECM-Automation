

import pandas as pd
import io

def parse_file(filename):
    """Extracts column data from a given .txt or .csv file"""
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    data_lines = []

    for line in lines:
        line = line.replace(",", " ")

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

    return L_data, I_data

def parse_file_st(uploaded_file):
    """Extracts column data from uploaded file, on streamlit"""
    lines = uploaded_file.getvalue().decode("utf-8").splitlines()

    data_lines = []

    for line in lines:
        line = line.replace(",", " ")  # replace commas with spaces

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

    return L_data, I_data