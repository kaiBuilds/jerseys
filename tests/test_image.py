"""unit tests for the image module"""

from PIL import Image
from src.image import (
    recolor_image,
    hex2rbg,
    write_in_image,
    overlay_images,
    cut_out_image,
    match_base_image_size,
    same_aspect_ratio,
    smaller_than_base_image,
    pad_image,
    resize_image,
)

BASE_IMAGE = "/workspaces/jerseys/tests/data/base.png"
RECOLOR_REFERENCE = "/workspaces/jerseys/tests/data/recolored.png"
WRITTEN_REFERENCE = "/workspaces/jerseys/tests/data/written.png"
OVERLAY_IMAGE = "/workspaces/jerseys/tests/data/triangle.png"
OVERLAY_REFERENCE = "/workspaces/jerseys/tests/data/overlay.png"
CUTOUT_MASK = "/workspaces/jerseys/tests/data/mask.png"
CUTOUT_REFERENCE = "/workspaces/jerseys/tests/data/cut.png"
INCORRECTLY_SIZED_IMAGE = "/workspaces/jerseys/tests/data/incorrectly_sized.png"
RESIZED_IMAGE = "/workspaces/jerseys/tests/data/resized.png"
TEST_FONT = "/workspaces/jerseys/tests/data/Roboto.ttf"


def images_are_equal(img1: Image.Image, img2: Image.Image) -> bool:
    """
    Check if two images are equal by comparing their pixel data.

    Args:
        img1 (PIL.Image.Image): The first image to compare.
        img2 (PIL.Image.Image): The second image to compare.

    Returns:
        bool: True if the images are equal, False otherwise.
    """
    if img1.size != img2.size:
        return False
    if img1.mode != img2.mode:
        return False

    pixels1 = img1.getdata()
    pixels2 = img2.getdata()

    for p1, p2 in zip(pixels1, pixels2):
        if p1 != p2:
            print(p1)
            print(p2)
            return False

    return True


def test_images_are_equal_equal_case():
    """
    Test for images_are_equal, case when they are equal
    """
    img1 = Image.open(BASE_IMAGE)
    img2 = Image.open(BASE_IMAGE)
    assert (
        images_are_equal(img1, img2) is True
    ), "test for images_are_equal failed, equal case"


def test_images_are_equal_not_equal_case():
    """
    Test for images_are_equal, case when they are not equal
    """
    img1 = Image.open(BASE_IMAGE)
    img2 = Image.open(RECOLOR_REFERENCE)
    assert (
        images_are_equal(img1, img2) is False
    ), "test for images_are_equal failed, not equal case"


def test_images_are_equal_mode_not_equal_case():
    """
    Test for images_are_equal, case when they are not equal
    """
    img1 = Image.open(RECOLOR_REFERENCE).convert("RGB")
    img2 = Image.open(RECOLOR_REFERENCE).convert("L")
    assert (
        images_are_equal(img1, img2) is False
    ), "test for images_are_equal failed, mode not equal case"


def test_rgb_r():
    """
    Test case for converting a hex color code to RGB.
    """
    color = (255, 0, 0)
    hex_str = "#ff0000"
    output = hex2rbg(color_hex=hex_str)
    for i in range(3):
        assert color[i] == output[i], "RGB values do not match - red."


def test_rgb_g():
    """
    Test case for converting a hex color code to RGB.
    """
    color = (0, 255, 0)
    hex_str = "#00ff00"
    output = hex2rbg(color_hex=hex_str)
    for i in range(3):
        assert color[i] == output[i], "RGB values do not match - green."


def test_rgb_b():
    """
    Test case for converting a hex color code to RGB.
    """
    color = (0, 0, 255)
    hex_str = "#0000ff"
    output = hex2rbg(color_hex=hex_str)
    for i in range(3):
        assert color[i] == output[i], "RGB values do not match - blue."


def test_recolor_image_no_recoloring():
    """
    Unit test for the recolor_image function.
    """
    base = Image.open(BASE_IMAGE)
    reference = Image.open(BASE_IMAGE)
    recolored = recolor_image(base, "#00ff00", 0.0)

    assert images_are_equal(reference, recolored), "Image recolored when it should be."


def test_recolor_image_full_recoloring():
    """
    Unit test for the recolor_image function.
    """
    base = Image.open(BASE_IMAGE)
    reference = Image.open(RECOLOR_REFERENCE)

    recolored = recolor_image(base, "00ff00", 1.0)

    assert images_are_equal(reference, recolored), "Image not correclty recolored."


def test_recolor_image_invalid_intensity():
    """
    Unit test for the recolor_image function.
    """
    base = Image.open(BASE_IMAGE)
    color_hex = "#ff0000"
    intensity = -0.5

    try:
        recolor_image(base, color_hex, intensity)
        assert False, "Expected ValueError to be raised."
    except ValueError as e:
        assert str(e) == "Intensity must be between 0 and 1", "Incorrect error message."


def test_recolor_image_not_rgba():
    """
    Unit test for the recolor_image function.
    """
    base = Image.open(BASE_IMAGE).convert("RGB")
    color_hex = "#ff0000"
    intensity = -0.5

    try:
        recolor_image(base, color_hex, intensity)
        assert False, "Expected ValueError to be raised."
    except ValueError as e:
        assert str(e) == "Intensity must be between 0 and 1", "Incorrect error message."


def test_write_in_image():
    """
    Unit test for the recolor_image function.
    """
    base = Image.open(BASE_IMAGE)
    text = "Hello World"
    font_path = TEST_FONT
    font_size = 10
    coordinates = (25, 50)
    color = (255, 255, 255)
    angle = 15
    written = write_in_image(
        image=base,
        text=text,
        font_path=font_path,
        font_size=font_size,
        coordinates=coordinates,
        color=color,
        angle=angle,
    )
    reference = Image.open(WRITTEN_REFERENCE)

    assert images_are_equal(reference, written), "Text not written correctly on image."


def test_overlay_images():
    """
    Unit test for the recolor_image function.
    """
    base = Image.open(BASE_IMAGE)
    overlay = Image.open(OVERLAY_IMAGE)
    composite = overlay_images([base, overlay])

    reference = Image.open(OVERLAY_REFERENCE)

    assert images_are_equal(reference, composite), "Images not overlayed correclty."


def test_cut_out_image():
    """
    Unit test for the cut_out_image function.
    """
    picture = Image.open(BASE_IMAGE)
    mask = Image.open(CUTOUT_MASK)
    result = cut_out_image(picture, mask)

    expected_result = Image.open(CUTOUT_REFERENCE)

    assert images_are_equal(expected_result, result), "Image not cut out correctly."


def test_match_base_image_size():
    """
    Unit test for the resize_image function.
    """
    base = Image.open(BASE_IMAGE)
    new = Image.open(INCORRECTLY_SIZED_IMAGE)
    resized = match_base_image_size(base, new)

    expected_results = Image.open(RESIZED_IMAGE)

    assert images_are_equal(
        expected_results, resized
    ), "Image does not match base image size."


def test_same_aspect_ratio_true():
    """
    Unit test for the same_aspect_ratio function.
    """
    base = Image.new("RGB", (100, 200))
    new = Image.new("RGB", (50, 100))

    assert same_aspect_ratio(base, new) is True, "Aspect ratios should match."


def test_same_aspect_ratio_false():
    """
    Unit test for the same_aspect_ratio function.
    """
    base = Image.new("RGB", (100, 200))
    new = Image.new("RGB", (100, 150))

    assert same_aspect_ratio(base, new) is False, "Aspect ratios should not match."


def test_same_aspect_ratio_equal_dimensions():
    """
    Unit test for the same_aspect_ratio function with equal dimensions.
    """
    base = Image.new("RGB", (100, 100))
    new = Image.new("RGB", (100, 100))

    assert same_aspect_ratio(base, new) is True, "Aspect ratios should match."


def test_smaller_than_base_image_true():
    """
    Unit test for the smaller_than_base_image function.
    """
    base = Image.new("RGB", (100, 100))
    new = Image.new("RGB", (50, 50))
    result = smaller_than_base_image(base, new)
    assert result is True, "Expected the new image to be smaller than the base image."


def test_smaller_than_base_image_false():
    """
    Unit test for the smaller_than_base_image function.
    """
    base = Image.new("RGB", (100, 100))
    new = Image.new("RGB", (150, 150))
    result = smaller_than_base_image(base, new)
    assert (
        result is False
    ), "Expected the new image to be larger or equal to the base image."


def test_pad_image():
    """
    Unit test for the pad_image function.
    """
    base = Image.new("RGB", (100, 100))
    new = Image.new("RGB", (50, 50))
    padded = pad_image(base, new)

    expected_result = Image.open(RESIZED_IMAGE)

    assert expected_result.size == padded.size, "Image not padded correctly."


def test_overlay_images_empty_list():
    """
    Unit test for the overlay_images function with an empty image list.
    """
    try:
        overlay_images([])
    except ValueError as e:
        assert str(e) == "The image list is empty", "Incorrect error message."


def test_resize_image():
    """
    Unit test for the resize_image function.
    """
    base = Image.new("RGB", (100, 100))
    new = Image.new("RGB", (50, 50))
    resized = resize_image(base, new)

    expected_result = Image.new("RGB", (100, 100))

    assert images_are_equal(expected_result, resized), "Image not resized correctly."
