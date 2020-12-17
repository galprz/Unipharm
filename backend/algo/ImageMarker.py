import cv2
import numpy

Image = numpy.ndarray


def draw_box_on_image(image: Image, top_left_corner: tuple, bottom_right_corner: tuple, color=(0, 0, 255), width=2) -> Image:
    """This function draws a box on an image.

    Args:
        image (Image): The image on which the box is to be drawn.
        top_left_corner (tuple): Coordinates of the box's top left corner in the image.
        bottom_right_corner (tuple): Coordinates of the box's bottom right corner in the image.
        color (tuple, optional): An RGB tuple to determine the color of the box's perimeter. Defaults to (0, 0, 255).
        width (int, optional): The width of the box perimeter. Defaults to 2.

    Returns:
        Image: The image given as argument with the box drawn on it.
    """
    return cv2.rectangle(image, top_left_corner, bottom_right_corner, color, width)
  #  return image


def add_text_on_image(image: Image, text: str, text_start_position: tuple, font: int, font_scale: float, color=(0, 0, 255), width=2) -> Image:
    """This function addes text on an image.

    Args:
        image (Image): The image on which the text is added.
        text (str): The text to be added on the image.
        text_start_position (tuple): The position from which start adding the text.
        font (int): The text's font
        font_scale (float): The font scale.
        color (tuple, optional): RGB tuple representing the color of the text. Defaults to (0, 0, 255).
        width (int, optional): The width. Defaults to 2.

    Returns:
        Image: The image with the test on it.
    """
    return cv2.putText(image, text, text_start_position,
                       font, font_scale, color, width)
    # return image
