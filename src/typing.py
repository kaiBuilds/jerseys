"""Typing definitions for the project."""
from typing import Tuple
from typing_extensions import Annotated
from pydantic import Field


ColorHexString = Annotated[str, Field(pattern=r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")]

FloatBetween0And1 = Annotated[float, Field(strict=True, ge=0, le=1)]

ImageCoordinates = Tuple[int, int]

Angle = Annotated[int, Field(strict=True, ge=0, le=360)]
