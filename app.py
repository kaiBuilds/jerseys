"""main streamlit app"""

from io import BytesIO
import streamlit as st

from app.layer import Layer
from app.textfield import TextField
from app.shirt import Shirt
from app.utils import toggle_with_two_labels, request_image
from const import GENERATION_SERVICE_URL, CACHED_STICKERS, CACHED_ILLUSTRATIONS

if "show_pane" not in st.session_state:
    st.session_state["show_pane"] = True

shirt = Shirt(kind="shirt")
background = Layer(kind="background")
foreground = Layer(kind="foreground")
artistic_frame = Layer(kind="artistic_frame")
illustration = Layer(kind="illustration", cached_textures=CACHED_ILLUSTRATIONS)
sticker = Layer(kind="sticker", cached_textures=CACHED_STICKERS)
sponsor = TextField(kind="sponsor")

all_layers = [
    background.property_map,
    foreground.property_map,
    artistic_frame.property_map,
    illustration.property_map,
    sticker.property_map,
]
text_fields = [sponsor.property_map]

if "generated_image" not in st.session_state:
    st.session_state["generated_image"] = None

with st.sidebar:
    st.title("Football Kit Creator :soccer:")
    st.subheader("Using AI to create new shirts!")

    st.session_state["sponsor_idea"] = st.text_area(
        "Enter idea here:",
        height=200,
    )

    shirt.logo_selectbox()
    shirt.type_selectbox()

    st.write("How to generate the image?")
    toggle_with_two_labels(
        label_left="Prompted",
        label_right="Controlled",
        state_name="structured_generation",
    )

    with st.expander("Background"):
        background.texture_ui()
        background.color_picker()
        background.recolor_intensity()

    with st.expander("Foreground"):
        foreground.texture_ui()
        foreground.color_picker()
        foreground.recolor_intensity()

    with st.expander("Artistic Frames"):
        artistic_frame.texture_ui()
        artistic_frame.color_picker()
        artistic_frame.recolor_intensity()

    with st.expander("Illustration"):
        illustration.texture_ui()
        illustration.color_picker()
        illustration.recolor_intensity()

    with st.expander("Sticker"):
        sticker.texture_ui()
        sticker.color_picker()
        sticker.recolor_intensity()

    with st.expander("Sponsor"):
        sponsor.text()
        sponsor.font_type()
        sponsor.font_size()
        sponsor.font_color()
        sponsor.font_placement()
        sponsor.text_angle()

st.subheader("Generated Image")
# TODO: below needs tidying up

if st.button(label="Generate", type="primary"):
    st.session_state["generated_image"] = request_image(
        url=GENERATION_SERVICE_URL,
        pack=shirt.property_map,
        layers=all_layers,
        text_fields=text_fields,
    )
    st.session_state["generate_input_button"] = False

if st.session_state["generated_image"]:
    st.image(st.session_state["generated_image"], width=500)

    buffer = BytesIO()
    st.session_state["generated_image"].save(buffer, format="PNG")

    st.download_button(
        label="Download image",
        type="primary",
        data=buffer,
        file_name="generated_image.png",
    )
