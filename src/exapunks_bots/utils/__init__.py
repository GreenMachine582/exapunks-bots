from __future__ import annotations

import uuid

from .utils import *
from .config import Config
from .bounding_box import BoundingBox, BoundingBox2
from .point import Point


def getKey(data: dict | list | tuple, key: str = None) -> str:
    """
    Finds a unique ID that is not in use.

    :param data: Extracted data from document, should be a dict[str | Any: Any]
    :param key: Initial key to be checked, should be a str
    :return: key - str
    """
    key = str(uuid.uuid4()) if key is None else key

    # Explore sub arrays
    keys = []
    if isinstance(data, (list, tuple)):
        keys = condense(data)
    elif isinstance(data, dict):
        keys = getDictKeys(data)

    # Find key that is not in use
    while key in keys:
        key = str(uuid.uuid4())
    return key
