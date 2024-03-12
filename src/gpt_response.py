"""Pydantic model for GPT response."""

from pydantic import BaseModel
from src.typing import ColorHexString, FloatBetween0And1


class GPTResponse(BaseModel):
    """Pydantic model for GPT response."""

    shirt_logo: str
    shirt_type: str

    foreground_texture: str
    foreground_color: ColorHexString
    foreground_intensity: FloatBetween0And1

    background_texture: str
    background_color: ColorHexString
    background_intensity: FloatBetween0And1

    sponsor_name_text: str
    sponsor_name_font_type: str
    sponsor_name_font_size: int
    sponsor_name_font_color: ColorHexString
    sponsor_name_text_angle: int
    sponsor_name_position_x: FloatBetween0And1
    sponsor_name_position_y: FloatBetween0And1
