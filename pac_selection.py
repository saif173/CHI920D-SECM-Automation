import streamlit as st


def select_params(fig):
    """Allows user to click on the plot to set the touch-point or i-infinity, or 
    to type them directly"""
    # initialise variables
    if "click_count" not in st.session_state:
        st.session_state.click_count = 0

    if "touch_point" not in st.session_state:
        st.session_state.touch_point = 0.0

    if "i_infi" not in st.session_state:
        st.session_state.i_infi = "0"

    if "last_point_index" not in st.session_state:
        st.session_state.last_point_index = None


    # interactive plot
    event = st.plotly_chart(
        fig,
        on_select="rerun",
        selection_mode="points"
    )


    # handle graph clicks
    if event.selection.points:
        point = event.selection.points[0]
        point_index = point["point_index"]

        # prevents typing in boxes from counting as clicks
        if point_index != st.session_state.last_point_index:

            st.session_state.last_point_index = point_index

            if st.session_state.click_count % 2 == 0:
                st.session_state.touch_point = point["x"]
            else:
                st.session_state.i_infi = str(point["y"])

            st.session_state.click_count += 1


    # manual input
    st.number_input(
        "Selected zero-point",
        key="touch_point"
    )

    st.text_input(
        "Selected I-infinity",
        key="i_infi"
    )


    # convert I infinity to float
    try:
        i_infi = float(st.session_state.i_infi)
    except ValueError:
        st.error("Invalid I-infinity value")
        i_infi = None


    return st.session_state.touch_point, i_infi



def select_touchpoint(fig):

    touch_point = None

    event = st.plotly_chart(
        fig,
        on_select="rerun",
        selection_mode="points"
    )

    if event.selection.points:
        touch_point = event.selection.points[0]["x"]
    st.write("Selected zero-point is:", touch_point)

    return touch_point