# Copyright (c) OpenMMLab. All rights reserved.
from PIL import Image


def apply_exif_orientation(image):
    """Applies the exif orientation correctly.

    This code exists per the bug:
      https://github.com/python-pillow/Pillow/issues/3973
    with the function `ImageOps.exif_transpose`.
    The Pillow source raises errors with
    various methods, especially `tobytes`
    Function based on:
      https://github.com/facebookresearch/detectron2/\
      blob/78d5b4f335005091fe0364ce4775d711ec93566e/\
      detectron2/data/detection_utils.py#L119
    Args:
        image (PIL.Image): a PIL image
    Returns:
        (PIL.Image): the PIL image with exif orientation applied, if applicable
    """
    _EXIF_ORIENT = 274
    if not hasattr(image, 'getexif'):
        return image

    try:
        exif = image.getexif()
    except Exception:
        # https://github.com/facebookresearch/detectron2/issues/1885
        exif = None

    if exif is None:
        return image

    orientation = exif.get(_EXIF_ORIENT)

    method = {
        2: Image.FLIP_LEFT_RIGHT,
        3: Image.ROTATE_180,
        4: Image.FLIP_TOP_BOTTOM,
        5: Image.TRANSPOSE,
        6: Image.ROTATE_270,
        7: Image.TRANSVERSE,
        8: Image.ROTATE_90,
    }.get(orientation)
    if method is not None:
        return image.transpose(method)
    return image
