import streamlit as st


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

st.title("CHI 920D Automation")

st.subheader("Introduction")
st.write("This program grants the user the ability to perform extra " \
"functions using the CHI 920D Scanning Electrochemical Microscope. It acts as an extension to the chi920d.exe software, providing automation for tedious tasks.")

st.subheader("General Information")
st.write("As previously mentioned, this software depends on the existing chi920d.exe software to operate. Before running any methods using this software, ensure that the chi920d.exe is closed. " \
"Also ensure that the chi920d.exe is located at following path 'C:\chi\chi920d.exe'.")
st.write("To stop any method, use the stop button in the chi920d.exe software. This will work when the probe is performing a pure vertical scanning operation, such as Probe Approach Curve as part of K-Map or Sample Leveling. **Unfortunately when the probe is moving to new positions, there is no software method to stop this**. " \
"This is due to a limitiation of the chi920d.exe software. The user should be careful when selecting dimensions for scans, and **in case of emergency to use the hardware to power-off the microscope**.")

st.write("Two new methods are included, the 'Sample Leveler' and the 'K-Map', which can be accessed from the side-bar on the left of the screen. A data analysis tool, the 'Touch Point PAC Analyser' is also included, and can be accessed through 'Probe Approach Curve (PAC)' on the sidebar. These are explained further below.")

selection = st.selectbox("Select method", ["Sample Leveler", "K-Map", "Touch-point PAC Analyser"])

if selection == "Sample Leveler":
    st.write("This method is used to level a sample.")
    st.write("It works by taking Probe Approach Curves (PACs) at three distinct points on the sample, which form an isoceles triangle, and compares the approach distance of the second and third points relative to the first. " \
    "The offsets are displayed, and the user can adjust the screws below the stage to " \
    "minimise these offsets to level their sample.")
    st.write("For this method to be effective, the user must first use the chi920d.exe software to move the probe close to the left edge of the sample, on the same horizontal line as the back two screws.")

    st.write("The user should adjust the scan positions carefully, with the guidance of the provided grid.")

if selection == "K-Map":
    st.write("This method creates a 2D colour map of k-values by scanning a certain region of the sample.")
    st.write("The 'Run Mapping' task scans an area by taking Probe Approach Curves at set intervals. The scan x-length and y-length as well as the respective increments are specified by the user. **The initial position will be the bottom left corner of the scan**, so ensure that there is sufficient space. This data is output to the user's selected folder." \
    " The file for each position will be named 'pos_x coordinate_y coordinate_x increment_y increment'")
    st.write("The 'Plot K-Map' task can then be used to plot the gathered data. The user then specifies the folder containing the PAC files." \
    " The data for each position is processed, and approximate k-values are provided for each position. This process will take around 1 second for each pixel, " \
    "after which the 2D map will be presented. This image can be downloaded, along with a .txt file containing the positions and k-values.")
    st.write("**Save time when scanning**: Run a Probe approach curve at the initial position first to get a rough estimate of the approach distance." \
    " Then, check the z-position using the chi920d.exe software, and adjust the 'Initial z-coordinate' parameter **(the probe will move to this position before starting the scan)** in this software to optimise the time required to approach. This can save alot of time.")

if selection == "Touch-point PAC Analyser":
    st.write("This method enables user to process their Probe Approach Curve data to make it presentable, and find a least-squares curve-fit to estimate a value of k for their data.")
    st.write("This is accessible by clicking 'Probe Approach Curve (PAC)' on the sidebar, then use the dropdown named 'Select Task' to select 'Touch-point PAC Analyser'.")
    st.write("The user uploads their .txt or .csv file, and the data is flipped to make it match the theoretical curves and presented. The user then clicks on the plot to select a 'touch-point' (zero-point). This is used to process and normalise the data. The normalised data can be downloaded as .txt. A least-squares curve-fit is used to find an estimate for k, and the root-mean-square error is displayed.")





