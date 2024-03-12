"""This module contains all the copy for the app. It is imported by the app.py module and used to populate the app"""

import streamlit as st
import const


if "lang" in st.session_state:
    LANG = st.session_state.lang
else:
    LANG = const.DEFAULT_APP_LANG


def logo_label(lang=LANG) -> str:
    """returns the logo label in the chosen language"""
    return const.COPY[lang]["logo_label"]


def shirt_label(lang=LANG) -> str:
    """returns the shirt label in the chosen language"""
    return const.COPY[lang]["shirt_label"]


def texture_prompt(lang=LANG) -> str:
    """returns the texture prompt checkbox in the chosen language"""
    return const.COPY[lang]["texture_prompt"]


def prompt_invite(lang=LANG) -> str:
    """returns the default prompt text for inviting prompting in the chosen language"""
    return const.COPY[lang]["prompt_invite"]


def texture_label(lang=LANG) -> str:
    """returns the texture name in the chosen language"""
    return const.COPY[lang]["texture_select"]


def color_picker(lang=LANG) -> str:
    """returns the color picker name in the chosen language"""
    return const.COPY[lang]["color_picker"]


def recolor_intensity(lang=LANG) -> str:
    """returns the recolor intensity name in the chosen language"""
    return const.COPY[lang]["recolor_intensity"]


def font_type(lang=LANG) -> str:
    """returns the font label checkbox copy in the chosen language"""
    return const.COPY[lang]["font_type"]


def font_size(lang=LANG) -> str:
    """returns the font label checkbox in the chosen language"""
    return const.COPY[lang]["font_size"]


def font_location_picker(lang=LANG) -> str:
    """returns the font label checkbox copy in the chosen language"""
    return const.COPY[lang]["font_location_picker"]


def font_x(lang=LANG) -> str:
    """returns the font horizontal position copy in the chosen language"""
    return const.COPY[lang]["font_x"]


def font_y(lang=LANG) -> str:
    """returns the font vertical position copy in the chosen language"""
    return const.COPY[lang]["font_y"]


def font_angle(lang=LANG) -> str:
    """returns the font angle copy in the chosen language"""
    return const.COPY[lang]["font_angle"]
