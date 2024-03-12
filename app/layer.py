"""class that defines the layers in the packaging picture"""

import streamlit as st
from app import copy as cp
import const
from app.utils import get_default_state, get_default_state_list


class Layer:
    """
    Represents a layer in the application.

    Attributes:
        kind (str): The kind of layer.
        cached_textures (list[str]): A list of cached textures for the layer.
        property_map (dict): A dictionary containing the property name and its
          corresponding state name.

    Methods:
        __init__(self, kind: str, cached_textures: list[str] = const.CACHED_TEXTURES) -> None:
            Initializes a new instance of the Layer class.
        __texture_toggle(self):
            Toggles the texture option for the layer.
        __texture_prompt(self):
            Prompts the user for a texture input.
        __texture_selectbox(self):
            Displays a selectbox for choosing a texture.
        texture_ui(self):
            Handles the UI options for the texture selection.
        color_picker(self):
            Displays a color picker for recoloring the layer.
        recolor_intensity(self):
            Displays a slider for selecting the recolor intensity.
    """

    def __init__(
        self, kind: str, cached_textures: list[str] = const.CACHED_TEXTURES
    ) -> None:
        """
        Initializes a new instance of the Layer class.

        Args:
            kind (str): The kind of layer.
            cached_textures (list[str], optional): A list of cached textures for the layer. Defaults to const.CACHED_TEXTURES.

        Returns:
            None
        """
        self.kind = kind
        self.cached_textures = cached_textures
        self.property_map = dict()

    def __texture_toggle(self):
        """
        Toggles the texture option for the layer.

        Returns:
            bool: The value of the texture toggle.
        """
        state_name, checkbox_value = get_default_state(
            kind=self.kind, property_name="toggle", default_val=False
        )

        st.session_state[state_name] = st.toggle(
            label=cp.texture_prompt(),
            value=bool(checkbox_value),
            key=f"{self.kind}_texture_toggle",
        )

        return st.session_state[state_name]

    def __texture_prompt(self):
        """
        Prompts the user for a texture input.

        Returns:
            None
        """
        state_name = f"{self.kind}_prompt_text"
        if state_name not in st.session_state:
            st.session_state[state_name] = ""

        self.property_map[f"{self.kind}_texture"] = state_name

        st.text_area(
            label=cp.prompt_invite(),
            height=200,
            value=st.session_state[state_name],
            key=state_name,
        )

    def __texture_selectbox(self):
        """
        Displays a selectbox for choosing a texture.

        Returns:
            None
        """
        state_name, selectbox_value = get_default_state_list(
            kind=self.kind,
            property_name="texture",
            options=self.cached_textures,
            default_val=0,
        )

        self.property_map[f"{self.kind}_texture"] = state_name

        st.session_state[state_name] = st.selectbox(
            label=cp.texture_label(),
            options=self.cached_textures,
            index=selectbox_value,
            key=f"{self.kind}_texture_selectbox",
        )

    def texture_ui(self):
        """
        Handles the UI options for the texture selection.

        This method checks the texture toggle and prompts the user for texture selection
        if the toggle is enabled. Otherwise, it displays a select box for texture selection.

        Returns:
            None
        """
        if self.__texture_toggle():
            self.__texture_prompt()
        else:
            self.__texture_selectbox()

    def color_picker(self):
        """
        Displays a color picker for recoloring the layer.

        Returns:
            None
        """
        state_name, color_value = get_default_state(
            kind=self.kind,
            property_name="color",
            default_val="#ffffff",
        )
        self.property_map[f"{self.kind}_color"] = state_name

        st.session_state[state_name] = st.color_picker(
            label=cp.color_picker(),
            value=str(color_value),
            key=f"{self.kind}_color_picker",
        )

    def recolor_intensity(self):
        """
        Displays a slider for selecting the recolor intensity.

        Returns:
            None
        """
        state_name, recolor_value = get_default_state(
            kind=self.kind,
            property_name="recolor_intensity",
            default_val=0,
        )

        self.property_map[f"{self.kind}_intensity"] = state_name

        st.session_state[state_name] = st.slider(
            label=cp.recolor_intensity(),
            min_value=0.0,
            max_value=1.0,
            value=float(recolor_value),
            key=f"{self.kind}_recolor_slider",
        )
