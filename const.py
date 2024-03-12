"""constants for the streamlit app and other general app configurations"""

import json
import os

CONFIG_PATH = "/workspaces/jerseys/config.json"
with open(CONFIG_PATH, "rt", encoding="utf-8") as f:
    CONFIG = json.load(f)

DEFAULT_APP_LANG = CONFIG["lang"]
TIMEOUT = CONFIG["timeout"]

with open(CONFIG["copy_path"], "rt", encoding="utf-8") as f:
    COPY = json.load(f)


def get_cached_asset_list(asset_path: str, extension: str) -> list[str]:
    """
    Retrieve a list of cached asset names with the specified extension.

    Args:
        asset_path (str): The path to the directory containing the assets.
        extension (str): The file extension to filter the assets.

    Returns:
        list[str]: A list of asset names without the specified extension.
    """
    return [
        name.rstrip(extension)
        for name in os.listdir(asset_path)
        if name.endswith(extension)
    ]


CACHED_TEXTURES = CONFIG["available_textures"]
CACHED_FONTS = CONFIG["available_fonts"]
CACHED_LOGOS = CONFIG["available_logos"]
CACHED_STICKERS = CONFIG["available_stickers"]
CACHED_SHIRTS = CONFIG["available_shirts"]
CACHED_ILLUSTRATIONS = CONFIG["available_illustrations"]

GENERATION_SERVICE_URL = CONFIG["url_to_generation_service"]
