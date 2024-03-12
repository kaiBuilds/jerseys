"""class that defines the packaging type and brand in the packaging picture"""

import streamlit as st
from .utils import get_default_state_list
from . import copy as cp
import const


class Shirt:
    """A class that represents the most high-level jersey choices.

    This class provides methods for selecting a logo and a shirt from pre-defined options.
    The selected logo and shirt will be stored in the session state.

    Attributes:
        kind (str): The kind of pack.
        cached_logos (list[str]): A list of pre-defined logos.
        cached_shirts (list[str]): A list of pre-defined shirts.
        property_map (dict): A dictionary to store the selected logo and shirt.

    Methods:
        __init__(self, kind: str, cached_logos: list[str] = const.CACHED_LOGOS, cached_shirts: list[str] = const.CACHED_SHIRTS) -> None:
            Initializes a Pack object.

        logo_selectbox(self) -> None:
            Displays a selectbox for logo selection from a list of pre-defined logos.

        shirt_selectbox(self) -> None:
            Displays a selectbox for shirt selection.
    """

    def __init__(
        self,
        kind: str,
        cached_logos: list[str] = const.CACHED_LOGOS,
        cached_shirts: list[str] = const.CACHED_SHIRTS,
    ) -> None:
        """
        Initializes a Pack object.

        Args:
            kind (str): The kind of pack.
            cached_logos (list[str], optional): A list of pre-defined logos. Defaults to const.CACHED_LOGOS.
            cached_shirts (list[str], optional): A list of pre-defined shirts. Defaults to const.CACHED_SHIRTS.
        """
        self.kind = kind
        self.cached_logos = cached_logos
        self.cached_shirts = cached_shirts
        self.property_map = dict()

    def logo_selectbox(self):
        """
        Displays a selectbox for logo selection from a list of pre-defined logos.

        This method allows the user to select a logo from a list of pre-defined logos.
        The selected logo will be stored in the session state under the appropriate key.

        Returns:
            None
        """
        state_name, selectbox_value = get_default_state_list(
            kind=self.kind,
            options=self.cached_logos,
            property_name="logo",
            default_val=0,
        )

        self.property_map[f"{self.kind}_logo"] = state_name

        st.session_state[state_name] = st.selectbox(
            label=cp.logo_label(),
            options=self.cached_logos,
            index=selectbox_value,
            key=f"{self.kind}_logo_selectbox",
        )

    def type_selectbox(self):
        """
        Displays a selectbox for shirt type.

        This method generates a selectbox widget using the `st.selectbox` function from the Streamlit library.
        The selectbox allows the user to choose a shirt from a list of available options.

        Returns:
            None
        """
        state_name, selectbox_value = get_default_state_list(
            kind=self.kind,
            options=self.cached_shirts,
            property_name="type",
            default_val=0,
        )

        self.property_map[f"{self.kind}_type"] = state_name

        st.session_state[state_name] = st.selectbox(
            label=cp.shirt_label(),
            options=self.cached_shirts,
            index=selectbox_value,
            key=f"{self.kind}_shirt_selectbox",
        )
