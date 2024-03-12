"""Module for interacting with the Azure OpenAI API."""

import os
from dotenv import load_dotenv
import time
from uuid import uuid4
import re
import json
import requests
from const import (
    CACHED_FONTS,
    CACHED_ILLUSTRATIONS,
    CACHED_LOGOS,
    CACHED_SHIRTS,
    CACHED_TEXTURES,
)
from src.gpt_response import GPTResponse

from src.errors import ResponseExtractionError
from . import const


class OpenAIClient:
    """
    Class for interacting with the OpenAI API.
    """

    def __init__(
        self,
    ):
        load_dotenv()
        self.gpt_api_key = os.getenv("OPENAI_API_KEY")
        self.gpt_endpoint = os.getenv("OPENAI_GPT_ENDPOINT")

        self.dalle_api_key = os.getenv("DALLE_API_KEY")
        self.dalle_endpoint = os.getenv("OPENAI_DALLE_ENDPOINT")

    def send_gpt_prompt(self, prompt: str):
        """
        Send a prompt to the GPT API and return the response.

        Args:
            prompt (str): The prompt to send to the GPT API.

        Returns:
            dict: The response from the GPT API as a JSON object.

        Raises:
            requests.exceptions.RequestException: If there is an error sending
              the request.
        """
        headers = {
            "Authorization": f"Bearer {self.gpt_api_key}",
            "Content-Type": "application/json",
        }

        data = {"prompt": prompt, "max_tokens": 150}

        response = requests.post(
            self.gpt_endpoint,
            headers=headers,
            json=data,
            timeout=const.TIMEOUT,
        )
        return response.json()

    def send_dalle_prompt(self, prompt: str, size: str = "256x256"):
        """
        Send a prompt to the DALL-E API and return the generated image.

        Args:
            prompt (str): The prompt to send to the DALL-E API.
            size (str, optional): The desired size of the generated image. Defaults to "256x256".

        Returns:
            None

        Raises:
            requests.exceptions.RequestException: If there is an error in sending
            or receiving the API request.
        """
        headers = {
            "Authorization": f"Bearer {self.dalle_api_key}",
            "Content-Type": "application/json",
        }

        data = {"prompt": prompt, "n": 1, "size": size}

        response = requests.post(
            self.dalle_endpoint,
            headers=headers,
            json=data,
            timeout=const.TIMEOUT,
        )

        operation_location = response.headers["operation-location"]
        status = ""
        while status != "succeeded":
            time.sleep(1)
            response = requests.get(
                operation_location,
                headers=headers,
                timeout=const.TIMEOUT,
            )
            status = response.json()["status"]

        image_url = response.json()["result"]["data"][0]["url"]
        generated_image = requests.get(
            image_url,
            timeout=const.TIMEOUT,
        ).content

        with open(f"{uuid4()}.png", "wb") as image_file:
            image_file.write(generated_image)

    def extract_json_from_gpt_response(self, response):
        """
        Extracts and validates JSON from GPT response.

        Args:
            response (dict): The GPT response dictionary.

        Returns:
            GPTResponse: An instance of the GPTResponse class.

        Raises:
            ResponseExtractionError: If failed to extract valid JSON from GPT response.
        """
        text = response["choices"][0]["text"]
        matches = re.match(pattern=r"\{.*?\}", string=text)
        if matches:
            json_data = json.loads(matches.group(0))
            return GPTResponse(**json_data)

        raise ResponseExtractionError("Failed to extract valid JSON from GPT response")


def designer_prompt(idea: str) -> str:
    """
    Returns the prompt for a text-based AI design the layout.

    Args:
        idea (str): The idea to be used in the prompt.

    Returns:
        str: The prompt.
    """
    return (
        f"You are an expert in designing creative and spontaneous shirts"
        f"for established brands. You have been tasked with designing a shirt."
        f"The club for the shirt has this idea: \n\n {idea}.\n\n"
        f"Considering the following assets: \n\n"
        f"\n\n"
        f"Available shirt types: {', '.join(CACHED_SHIRTS)}"
        f"\n\n"
        f"Available textures: {', '.join(CACHED_TEXTURES)}"
        f"\n\n"
        f"Available font types: {', '.join(CACHED_FONTS)}"
        f"\n\n"
        f"Create a JSON file with the format below translating the idea"
        f" into a beautiful shirt:\n\n"
        f"{{\n"
        f'    "shirt_logo": <one of the logos>,\n'
        f'    "shirt_type": <one of the shirt types>,\n'
        f'    "foreground_texture": <one of the textures>,\n'
        f'    "foreground_color": <color hex string>,\n'
        f'    "foreground_intensity": <float between 0 and 1>,\n'
        f'    "background_texture": <one of the textures>,\n'
        f'    "background_color": <color hex string>,\n'
        f'    "background_intensity": <float between 0 and 1>,\n'
        f'    "sticker_texture": <one of the textures>,\n'
        f'    "sticker_color": <color hex string>,\n'
        f'    "sticker_intensity": <float between 0 and 1>,\n'
        f'    "sponsor_name_text": <string>,\n'
        f'    "sponsor_name_font_type": <one of the font types>,\n'
        f'    "sponsor_name_font_size": <float between 0 and 1>,\n'
        f'    "sponsor_name_font_color": <color hex string>,\n'
        f'    "sponsor_name_position_x": <float between 0 and 1>,\n'
        f'    "sponsor_name_position_y": <float between 0 and 1>,\n'
        f'    "sponsor_name_angle": <int between 0 and 360>,\n'
        f"}}"
    )
