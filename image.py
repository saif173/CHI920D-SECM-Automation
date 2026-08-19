import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(
    page_title="SECM Position Picker",
    layout="centered"
)

st.title("SECM Position Picker")

# -----------------------------
# Upload image
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload your image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is None:
    st.info("Upload an image of the 4000 µm circle.")
    st.stop()

image = Image.open(uploaded_file).convert("RGB")

width, height = image.size

st.write(f"Image size: {width} × {height} pixels")


# -----------------------------
# Circle size
# -----------------------------

circle_diameter_um = 4000

circle_diameter_px = st.number_input(
    "Circle diameter in pixels",
    min_value=1,
    value=min(width, height),
    step=1
)

# µm per pixel
um_per_pixel = circle_diameter_um / circle_diameter_px

st.write(f"Scale: **{um_per_pixel:.3f} µm/pixel**")


# -----------------------------
# Instructions
# -----------------------------

if "points" not in st.session_state:
    st.session_state.points = []

st.write("### Select points")
st.write(
    "Click the **initial point first**, followed by the other two points."
)

if len(st.session_state.points) == 0:
    st.info("Click the initial point.")

elif len(st.session_state.points) == 1:
    st.info("Initial point selected. Now click point 2.")

elif len(st.session_state.points) == 2:
    st.info("Point 2 selected. Now click point 3.")

else:
    st.success("All three points selected.")


# -----------------------------
# Display image and detect click
# -----------------------------

value = streamlit_image_coordinates(
    image,
    key="image"
)

if value is not None:

    clicked_x = value["x"]
    clicked_y = value["y"]

    # Only add the point if fewer than 3 exist
    if len(st.session_state.points) < 3:

        # Prevent Streamlit from adding the same click repeatedly
        if (
            len(st.session_state.points) == 0
            or st.session_state.points[-1] != (clicked_x, clicked_y)
        ):
            st.session_state.points.append(
                (clicked_x, clicked_y)
            )

            st.rerun()


# -----------------------------
# Draw selected points
# -----------------------------

display_image = image.copy()
draw = ImageDraw.Draw(display_image)

labels = ["Initial", "Point 2", "Point 3"]

for i, (x, y) in enumerate(st.session_state.points):

    # Draw marker
    r = 8

    draw.ellipse(
        [x-r, y-r, x+r, y+r],
        outline="red",
        width=3
    )

    # Draw label
    draw.text(
        (x + 10, y - 10),
        labels[i],
        fill="red"
    )


st.image(display_image)


# -----------------------------
# Calculate relative coordinates
# -----------------------------

if len(st.session_state.points) >= 1:

    x0, y0 = st.session_state.points[0]

    st.write("### Coordinates")

    st.write(
        f"Initial point: **({x0}, {y0}) px**"
    )


if len(st.session_state.points) >= 2:

    x1, y1 = st.session_state.points[1]

    dx1_px = x1 - x0
    dy1_px = y1 - y0

    dx1_um = dx1_px * um_per_pixel
    dy1_um = dy1_px * um_per_pixel

    st.write(
        f"Point 2 relative to initial: "
        f"**({dx1_um:.2f}, {dy1_um:.2f}) µm**"
    )


if len(st.session_state.points) >= 3:

    x2, y2 = st.session_state.points[2]

    dx2_px = x2 - x0
    dy2_px = y2 - y0

    dx2_um = dx2_px * um_per_pixel
    dy2_um = dy2_px * um_per_pixel

    st.write(
        f"Point 3 relative to initial: "
        f"**({dx2_um:.2f}, {dy2_um:.2f}) µm**"
    )


# -----------------------------
# Reset button
# -----------------------------

if st.button("Reset points"):

    st.session_state.points = []

    st.rerun()