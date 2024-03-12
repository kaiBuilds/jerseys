"""class for fonts and how they can be edited in the packaging picture"""

import streamlit as st
from app.utils import get_default_state_list, get_default_state
from app import copy as cp
import const


class TextField:
    """
    # A class representing a text field, including the typeset, color, size, and placement.

    Attributes:
        kind (str): The kind of font.

    Methods:
        font_type(): Selector for the font type.
        font_size(): Selector for the font size.
        font_color(): Selector for the font color.
        font_placement(default_x: float = 0.5, default_y: float = 0.5): Implements a rudimentary drag and drop for the text.
        font_angle(): Selector for the font angle.
    """

    def __init__(self, kind: str) -> None:
        self.kind = kind
        self.property_map = dict()

    def text(self):
        """
        Text field that allows the user to input text.

        Returns:
            None
        """
        state_name, default_text = get_default_state(
            kind=self.kind,
            property_name="text",
            default_val="",
        )

        self.property_map[f"{self.kind}_text"] = state_name

        st.text_area(
            label=cp.prompt_invite(),
            height=100,
            value=default_text,
            key=f"{self.kind}_text",
        )

    def font_type(self):
        """Selector for the font type.

        This method retrieves the default font type for a given kind and displays it in a selectbox.
        The selected font type is stored in the session state.

        Returns:
            None
        """
        state_name, font_value = get_default_state_list(
            kind=self.kind,
            options=const.CACHED_FONTS,
            property_name="font_type",
            default_val=0,
        )

        self.property_map[f"{self.kind}_font_type"] = state_name

        st.session_state[state_name] = st.selectbox(
            label=cp.font_type(),
            options=const.CACHED_FONTS,
            index=int(font_value),
            key=f"{self.kind}_font_selectbox",
        )

    def font_size(self):
        """
        Selector for the font size.

        This method allows the user to select the font size using a number input widget.
        The selected font size is stored in the session state for future use.

        Returns:
            None
        """
        state_name = f"{self.kind}_font_size"
        if state_name not in st.session_state:
            st.session_state[state_name] = 20

        self.property_map[f"{self.kind}_font_size"] = state_name

        st.number_input(
            label=cp.font_size(),
            min_value=0,
            step=1,
            value=st.session_state[state_name],
            key=f"{self.kind}_font_size",
        )

    def font_color(self):
        """Selector for the font color.

        Returns:
            str: The selected font color in hexadecimal format.
        """
        state_name, default_color = get_default_state(
            kind=self.kind,
            property_name="font_color",
            default_val="#000000",
        )

        self.property_map[f"{self.kind}_font_color"] = state_name

        st.color_picker(
            label=cp.color_picker(),
            value=str(default_color),
            key=state_name,
        )

    def font_placement(
        self,
        default_x: float = 0.5,
        default_y: float = 0.5,
    ):
        """
        Implements buttons to allow moving text around the image.

        Args:
            default_x (float, optional): The default x-coordinate of the text. Defaults to 0.5.
            default_y (float, optional): The default y-coordinate of the text. Defaults to 0.5.
        """

        state_name = f"{self.kind}_position"
        if f"{state_name}_x" not in st.session_state:
            st.session_state[f"{state_name}_x"] = default_x
        if f"{state_name}_y" not in st.session_state:
            st.session_state[f"{state_name}_y"] = default_y

        self.property_map[f"{state_name}_x"] = f"{state_name}_x"
        self.property_map[f"{state_name}_y"] = f"{state_name}_y"

        st.number_input(
            label=cp.font_x(),
            min_value=0.0,
            max_value=1.0,
            value=st.session_state[f"{state_name}_x"],
            key=f"{state_name}_x",
        )

        st.number_input(
            label=cp.font_y(),
            min_value=0.0,
            max_value=1.0,
            value=st.session_state[f"{state_name}_y"],
            key=f"{state_name}_y",
        )

    def text_angle(self):
        """Selector for the text angle.

        This method displays a number input widget that allows the user to select the angle of the font.
        The selected angle is stored in the session state and can be accessed later.

        Returns:
            None
        """
        state_name = f"{self.kind}_text_angle"
        if state_name not in st.session_state:
            st.session_state[state_name] = 0

        self.property_map[f"{self.kind}_text_angle"] = state_name

        st.number_input(
            label=cp.font_angle(),
            min_value=0,
            max_value=360,
            step=1,
            value=st.session_state[state_name],
            key=f"{self.kind}_text_angle",
        )
