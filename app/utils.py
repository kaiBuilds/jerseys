"""utility functions used accross classes"""

from typing import Tuple, List, Any
from io import BytesIO
import requests
from PIL import Image
import streamlit as st

from src.image import (
    compose_image_from_response,
    GPTResponse,
)  # TODO: remove and use services instead

from const import (
    TIMEOUT,
    CACHED_STICKERS,
    GENERATION_SERVICE_URL,
)


def get_default_state(
    kind: str,
    property_name: str,
    default_val: str | bool | int | float,
) -> Tuple[str, str | bool | int | float]:
    """
    Validates if a streamlit state exists and assigns a default value if it doesn't.

    Args:
        kind (str): The kind of state.
        property_name (str): The name of the property.
        default_val (str | bool | int): The default value to assign if the state doesn't exist.

    Returns:
        Tuple[str, str | bool | int]: A tuple containing the state name and its value.
    """
    state_name = f"{kind}_{property_name}"
    if state_name in st.session_state:
        value = st.session_state[state_name]
    else:
        value = default_val

    return state_name, value


def get_default_state_list(
    kind: str,
    property_name: str,
    options: List[str],
    default_val: int,
) -> Tuple[str, int]:
    """
    Validates if a streamlit state exists and assigns a default value if it doesn't.

    Args:
        kind (str): The kind of state.
        property_name (str): The name of the property.
        options (List[str]): The list of available options.
        default_val (int): The default value to assign if the state doesn't exist.

    Returns:
        Tuple[str, int]: A tuple containing the state name and its corresponding value.
    """
    state_name = f"{kind}_{property_name}"
    if state_name in st.session_state:
        value = options.index(st.session_state[state_name])
    else:
        value = default_val

    return state_name, value


def toggle_with_two_labels(
    label_left: str,
    label_right: str,
    state_name: str,
) -> None:
    """
    Streamlit toggle button with two labels that stores result in session state

    Args:
        label_left (str): The label for the left side of the toggle button.
        label_right (str): The label for the right side of the toggle button.
        state_name (str): The name of the session state variable to store the toggle state.

    Returns:
        None
    """
    if state_name not in st.session_state:
        st.session_state[state_name] = False
    left_state, right_state = st.columns([0.3, 0.7])
    with left_state:
        st.write(label_left)
    with right_state:
        st.session_state[state_name] = st.toggle(label_right)


def form_request_body_from_session_state(
    pack: dict[str, Any],
    layers: list[dict],
    text_fields: list[dict],
) -> dict[str, Any]:
    """
    Creates a request body from the session state.

    Args:
        pack (dict[str, Any]): The initial request body.
        layers (list[dict]): A list of dictionaries representing layers.
        text_fields (list[dict]): A list of dictionaries representing text fields.

    Returns:
        dict[str, Any]: The updated request body.

    """
    request_body = dict()
    for request_key, state in pack.items():
        request_body[request_key] = st.session_state[state]

    for layer in layers:
        for request_key, state in layer.items():
            request_body[request_key] = st.session_state[state]

    for field in text_fields:
        for request_key, state in field.items():
            request_body[request_key] = st.session_state[state]

    return request_body


def request_image(
    url: str,
    pack: dict[str, Any],
    layers: list[dict[str, Any]],
    text_fields: list[dict[str, Any]],
) -> Image.Image:
    """
    Retrieves an image either from a local file or from a URL using the streamlit session state.

    Args:
        url (str): The URL of the image.
          #TODO: if the url is none, we are directly coupling with the backend, that should
          actually be a service with an API (but we're keeping that way for now due to the
          inability of dataiku to handle multiple services)
        pack (dict[str, Any]): The pack information.
        layers (list[dict[str, Any]]): The list of layers.
        text_fields (list[dict[str, Any]]): The list of text fields.
        #TODO: working in progress, we need to change the way we handle the layers and text fields

    Returns:
        Image.Image: The retrieved image.
    """
    body = form_request_body_from_session_state(
        pack=pack,
        layers=layers,
        text_fields=text_fields,
    )
    if url:
        response = requests.post(url, json=body, timeout=TIMEOUT)
        image = Image.open(BytesIO(response.content))
    else:
        image = compose_image_from_response(
            response=GPTResponse(**body),
        )

    return image
