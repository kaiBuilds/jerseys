"""image processing functions"""
from typing import Tuple
from PIL import Image, ImageFont, ImageDraw, ImageChops
from src.const import (
    LAYERS,
    TEXT_FIELDS,
    TEXTURE_PATH,
    MASKS_PATH,
    FONTS_PATH,
)
from src.gpt_response import GPTResponse


def hex2rbg(color_hex: str) -> Tuple[int, int, int]:
    """
    Converts a hexadecimal color value to an RGB tuple.

    Args:
        color_hex (str): The hexadecimal color value to convert.

    Returns:
        Tuple[int, int, int]: The RGB tuple representing the converted color.

    Example:
        >>> hex2rbg("#FF0000")
        (255, 0, 0)
    """
    color_hex = color_hex.lstrip("#")
    r = int(color_hex[0:2], 16)
    g = int(color_hex[2:4], 16)
    b = int(color_hex[4:], 16)
    return (r, g, b)


def recolor_image(
    image: Image.Image,
    color_hex: str,
    intensity: float,
) -> Image.Image:
    """
    Apply recoloring to the non-transparent part of an image based on a supplied
    hex code and intensity parameter.

    Args:
        image (Image.Image): A PIL Image object to be recolored.
        color_hex (str): Hex code of the color to be applied.
        intensity (float): Intensity of the recoloring, ranging from 0 (no recoloring)
          to 1 (full solid color).

    Returns:
        Image.Image: A PIL Image object with the recoloring applied.
    """

    if not 0 <= intensity <= 1:
        raise ValueError("Intensity must be between 0 and 1")

    color_rgb = hex2rbg(color_hex=color_hex)

    if image.mode != "RGBA":
        image = image.convert("RGBA")

    alpha = image.split()[3]

    new_image = Image.new("RGB", image.size, color_rgb)
    new_image.putalpha(alpha)

    blended_image = Image.blend(image, new_image, intensity)

    return blended_image


def write_in_image(
    image: Image.Image,
    text: str,
    font_path: str,
    font_size: int,
    coordinates: Tuple[int, int],
    color: str | Tuple[int, int, int],
    angle: int,
) -> Image.Image:
    """
    Adds text to an image at specified coordinates with a specified font.

    Args:
        image (Image.Image): The image to which text is to be added.
        text (str): The text to add to the image.
        font_path (str): The path to the font file to be used.
        font_size (int): The size of the font.
        coordinates (Tuple[int, int]): The coordinates (x, y) on the image where the
          text will be added.
        color (str | Tuple[int, int, int]): The color of the text.
        angle (int): The angle in degrees to rotate the text (0 to 360).

    Returns:
        Image.Image: The image with the text added.
    """
    font = ImageFont.truetype(font_path, font_size)

    text_image = Image.new("RGBA", image.size, (255, 255, 255, 0))

    draw = ImageDraw.Draw(text_image)
    draw.text(coordinates, text, font=font, fill=color)

    rotated_text_image = text_image.rotate(angle, expand=True)

    image.paste(rotated_text_image, (0, 0), rotated_text_image)

    return image


def overlay_images(image_list: list[Image.Image]) -> Image.Image:
    """
    Overlays a list of images sequentially on top of each other.

    Args:
        image_list (list[Image.Image]): A list of PIL Image objects to be overlaid.

    Returns:
        Image.Image: The final image that is a composition of all the individual images.
    """
    if not image_list:
        raise ValueError("The image list is empty")

    # Start with the first image as the base
    base_image = image_list[0].copy()

    for image in image_list[1:]:
        # Overlay each image on top of the base
        base_image.paste(image, (0, 0), image)

    return base_image


def cut_out_image(
    picture: Image.Image,
    mask: Image.Image,
) -> Image.Image:
    """
    Cuts out the image using the provided mask.

    Args:
        picture (PIL.Image.Image): The original image.
        mask (PIL.Image.Image): The mask to be applied.

    Returns:
        PIL.Image.Image: The cutout image.
    """
    mask = mask.convert("RGBA")
    cutout = ImageChops.multiply(picture, mask)

    return cutout


def same_aspect_ratio(
    base: Image.Image,
    new: Image.Image,
) -> bool:
    """
    Checks if the aspect ratio of the new image matches the aspect ratio
      of the base image.

    Args:
        base (PIL.Image.Image): The base image.
        new (PIL.Image.Image): The new image.

    Returns:
        bool: True if the aspect ratios match, False otherwise.
    """
    return new.width / new.height == base.width / base.height


def smaller_than_base_image(
    base: Image.Image,
    new: Image.Image,
) -> bool:
    """
    Checks if the new image is smaller than the base image.

    Args:
        base (PIL.Image.Image): The base image.
        new (PIL.Image.Image): The new image.

    Returns:
        bool: True if the new image is smaller than the base image, False otherwise.
    """
    return new.width < base.width and new.height < base.height


def crop_image(
    base: Image.Image,
    new: Image.Image,
) -> Image.Image:
    """
    Crops the new image to match the size of the base image.
    The new image is cropped so its center is preserved.

    Args:
        base (PIL.Image.Image): The base image to match the size.
        new (PIL.Image.Image): The new image to be cropped.

    Returns:
        PIL.Image.Image: The cropped image.

    Raises:
        None
    """
    width_diff = new.width - base.width
    height_diff = new.height - base.height
    left = width_diff // 2
    top = height_diff // 2
    right = left + base.width
    bottom = top + base.height

    cropped_image = new.crop((left, top, right, bottom))

    return cropped_image


def pad_image(
    base: Image.Image,
    new: Image.Image,
) -> Image.Image:
    """
    Pads the new image to match the size of the base image.

    Args:
        base (PIL.Image.Image): The base image to match the size of.
        new (PIL.Image.Image): The new image to be padded.

    Returns:
        PIL.Image.Image: The padded image.

    Raises:
        None

    Examples:
        >>> base_image = Image.open("base_image.png")
        >>> new_image = Image.open("new_image.png")
        >>> padded_image = pad_image(base_image, new_image)
    """
    width_diff = base.width - new.width
    height_diff = base.height - new.height
    left = width_diff // 2
    top = height_diff // 2
    right = left + new.width
    bottom = top + new.height

    padded_image = Image.new("RGBA", base.size)
    padded_image.paste(new, (left, top, right, bottom))

    return padded_image


def resize_image(
    base: Image.Image,
    new: Image.Image,
) -> Image.Image:
    """
    Resizes the new image to fit within the base image by scaling the new image
    to fit within the base image.

    Args:
        base (PIL.Image.Image): The base image.
        new (PIL.Image.Image): The new image.

    Returns:
        PIL.Image.Image: The resized image that fits within the base image.
    """
    resized_image = new.resize((base.width, base.height))

    return resized_image


def match_base_image_size(
    base: Image.Image,
    new: Image.Image,
) -> Image.Image:
    """
    Resizes the new image to match the size of the base image.
    If the new image is smaller than the base image,
      it will be padded.
    If the new image is larger than the base image with a different aspect ratio,
      it will be cropped.
    If the new image is larger than the base image with the same aspect ratio,
      it will be resized.

    Parameters:
    - base (PIL.Image.Image): The base image to match the size with.
    - new (PIL.Image.Image): The new image to be resized, padded, or cropped.

    Returns:
    - PIL.Image.Image: The resized, padded, or cropped image.
    """
    if new.size == base.size:
        return new

    if same_aspect_ratio(base, new):
        new = resize_image(base, new)
    elif smaller_than_base_image(base, new):
        new = pad_image(base, new)
    else:
        new = crop_image(base, new)

    return new


def transform_layer_from_response(
    response: GPTResponse,
    layer: str,
) -> Image.Image:
    """
    Transforms a layer from the GPTResponse object into an Image object.

    Args:
        response (GPTResponse): The GPTResponse object containing the layer information.
        layer (str): The name of the layer to transform.

    Returns:
        Image.Image: The transformed layer as an Image object.

    Raises:
        FileNotFoundError: If the layer texture or mask file is not found.

    This function executes the following process to transform a layer from the GPTResponse object into an Image object:
    - Loads the layer texture using the texture path from the GPTResponse object.
    - Recolors the layer using the color and intensity values from the GPTResponse object.
    - Applies the corresponding mask for the layer.
    - Returns the transformed layer as an Image object.

    Example:
        response = GPTResponse(...)
        layer = "background"
        transformed_layer = transform_layer_from_response(response, layer)
    """
    texture = Image.open(
        f'{TEXTURE_PATH}/{getattr(response, f"{layer}_texture")}.png',
    )
    image = recolor_image(
        texture,
        getattr(response, f"{layer}_color"),
        getattr(response, f"{layer}_intensity"),
    )
    image = cut_out_image(
        image,
        Image.open(f"{MASKS_PATH}/{response.shirt_type}/{layer}.png"),
    )
    return image


def write_text_in_composite_image_from_response(
    response: GPTResponse,
    kind: str,
    composite: Image.Image,
) -> Image.Image:
    """
    Writes the text for the sponsor line and sponsor name in the composite image.

    Args:
        response (GPTResponse): The response object containing the text and font
          information.
        kind (str): The kind of text to write (e.g., 'sponsor_line', 'sponsor_name').
        composite (Image.Image): The composite image to write the text on.

    Returns:
        Image.Image: The composite image with the text written on it.
    """
    coordinates = (
        int(getattr(response, f"{kind}_position_x") * composite.width),
        int(composite.height * (1 - getattr(response, f"{kind}_position_y"))),
    )

    composite = write_in_image(
        composite,
        text=getattr(response, f"{kind}_text"),
        font_path=f"{FONTS_PATH}/{getattr(response, f'{kind}_font_type')}.ttf",
        font_size=getattr(response, f"{kind}_font_size"),
        coordinates=coordinates,
        color=getattr(response, f"{kind}_font_color"),
        angle=getattr(response, f"{kind}_text_angle"),
    )
    return composite


def compose_image_from_response(
    response: GPTResponse,
) -> Image.Image:
    """
    Composes an image from a GPTResponse object.

    Args:
        response (GPTResponse): The GPTResponse object containing the necessary
          information for processing the layers.

    Returns:
        Image.Image: The composed image.

    Raises:
        None

    Notes:
        This function performs the following steps to compose the image:
        - Loads the layer texture for each of the layers:
            foreground, background, artistic frame, illustration, and sticker layers.
        - Recolors each layer.
        - Applies the masks for each layer.
        - Overlays the layers.
        - Writes the text for the sponsor line and sponsor name.
    """
    images = list()

    for layer in LAYERS:
        images.append(
            transform_layer_from_response(
                response=response,
                layer=layer,
            )
        )

    composite = overlay_images(images)
    for field in TEXT_FIELDS:
        composite = write_text_in_composite_image_from_response(
            response=response,
            kind=field,
            composite=composite,
        )

    return composite
