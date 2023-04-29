from __future__ import annotations

import copy

from .point import Point

from shapely import Polygon


class _BaseBoundingBox(object):

    def __init__(self, *values):
        self._bounding_box = []
        self.__call__(*values)

    def __call__(self, *values) -> _BaseBoundingBox:
        if len(values) == 1:
            if len(values[0]) in [2, 4]:
                values = values[0]

        if len(values) == 2:  # ((x1, y1), (x2, y2))
            self._bounding_box = [Point(value) for value in values]
        elif len(values) == 4:  # (x1, y1, x2, y2)
            self._bounding_box = [Point(values[:2]), Point(values[2:])]

        if not self._bounding_box and values:
            raise ValueError(f"{self.__class__.__name__} does not accept {values}")
        return self

    def __round__(self, n: int = 0):
        round(self._bounding_box[0], n)
        round(self._bounding_box[1], n)

    def __int__(self):
        self._bounding_box[0].__int__()
        self._bounding_box[1].__int__()

    def __getitem__(self, index: int) -> int | float:
        if index > 4:
            raise IndexError("list index out of range, must be less than 4")
        return self._bounding_box[index // 2][index % 2]

    def __str__(self) -> str:
        return f"{self.pos1}, {self.pos2}"

    def __repr__(self) -> str:
        return f"BoundingBox({str(self)})"

    def __add__(self, values: int | float | list | tuple) -> list:
        _bounding_box = self._bounding_box
        if isinstance(values, (list, tuple)):
            if len(values) == 2:
                _bounding_box[0] += values
                _bounding_box[1] += values
                return _bounding_box
            elif len(values) == 4:
                _bounding_box[0] += values[:2]
                _bounding_box[1] += values[2:]
                return _bounding_box
        elif isinstance(values, (int, float)):
            _bounding_box[0] += values
            _bounding_box[1] += values
            return _bounding_box

    def __sub__(self, values: int | float | list | tuple) -> list:
        _bounding_box = self._bounding_box
        if isinstance(values, (list, tuple)):
            if len(values) == 2:
                _bounding_box[0] -= values
                _bounding_box[1] -= values
                return _bounding_box
            elif len(values) == 4:
                _bounding_box[0] -= values[:2]
                _bounding_box[1] -= values[2:]
                return _bounding_box
        elif isinstance(values, (int, float)):
            _bounding_box[0] -= values
            _bounding_box[1] -= values
            return _bounding_box

    def __mul__(self, values: int | float | list | tuple) -> list:
        _bounding_box = self._bounding_box
        if isinstance(values, (list, tuple)):
            if len(values) == 2:
                _bounding_box[0] *= values
                _bounding_box[1] *= values
                return _bounding_box
            elif len(values) == 4:
                _bounding_box[0] *= values[:2]
                _bounding_box[1] *= values[2:]
                return _bounding_box
        elif isinstance(values, (int, float)):
            _bounding_box[0] *= values
            _bounding_box[1] *= values
            return _bounding_box

    def __floordiv__(self, values: int | float | list | tuple) -> list:
        _bounding_box = self._bounding_box
        if isinstance(values, (list, tuple)):
            if len(values) == 2:
                _bounding_box[0] //= values
                _bounding_box[1] //= values
                return _bounding_box
            elif len(values) == 4:
                _bounding_box[0] //= values[:2]
                _bounding_box[1] //= values[2:]
                return _bounding_box
        elif isinstance(values, (int, float)):
            _bounding_box[0] //= values
            _bounding_box[1] //= values
            return _bounding_box

    def __truediv__(self, values: int | float | list | tuple) -> list:
        _bounding_box = self._bounding_box
        if isinstance(values, (list, tuple)):
            if len(values) == 2:
                _bounding_box[0] /= values
                _bounding_box[1] /= values
                return _bounding_box
            elif len(values) == 4:
                _bounding_box[0] /= values[:2]
                _bounding_box[1] /= values[2:]
                return _bounding_box
        elif isinstance(values, (int, float)):
            _bounding_box[0] /= values
            _bounding_box[1] /= values
            return _bounding_box

    def __iadd__(self, values) -> _BaseBoundingBox:
        self._bounding_box = self.__add__(values)
        return self

    def __isub__(self, values) -> _BaseBoundingBox:
        self._bounding_box = self.__sub__(values)
        return self

    def __imul__(self, values) -> _BaseBoundingBox:
        self._bounding_box = self.__mul__(values)
        return self

    def __ifloordiv__(self, values) -> _BaseBoundingBox:
        self._bounding_box = self.__floordiv__(values)
        return self

    def __itruediv__(self, values) -> _BaseBoundingBox:
        self._bounding_box = self.__truediv__(values)
        return self

    def toJson(self) -> list:
        return self._bounding_box

    def merge(self, *bounding_boxes):
        if len(bounding_boxes) == 1 and isinstance(bounding_boxes[0], (list, tuple)):
            bounding_boxes = bounding_boxes[0]

        if not self._bounding_box and len(bounding_boxes) >= 1:
            self._bounding_box = copy.deepcopy(bounding_boxes[0]._bounding_box)

        for bounding_box in bounding_boxes:
            self._bounding_box[0].x = min(self[0], bounding_box[0])
            self._bounding_box[0].y = min(self[1], bounding_box[1])
            self._bounding_box[1].x = max(self[2], bounding_box[2])
            self._bounding_box[1].y = max(self[3], bounding_box[3])

    def offset_x(self, *value):
        if len(value) == 1:
            self.__iadd__([value[0], 0])
        elif len(value) == 2:
            self.__iadd__([value[0], 0, value[1], 0])

    def offset_y(self, *value):
        if len(value) == 1:
            self.__iadd__([0, value[0]])
        elif len(value) == 2:
            self.__iadd__([0, value[0], 0, value[1]])

    def copy(self) -> BoundingBox:
        return BoundingBox(self.pos1, self.pos2)

    @property
    def bounding_box(self) -> list:
        return [*self.pos1, *self.pos2]

    @property
    def box(self) -> list:
        return [self.x1, self.y1, self.width, self.height]

    @property
    def coordinates(self) -> list:
        return [self.pos1, self.pos2]

    @property
    def polygon(self) -> list:
        return [self.pos1, (self.x2, self.y1), self.pos2, (self.x1, self.y2)]

    @property
    def pos1(self) -> tuple:
        return self._bounding_box[0].pos

    @property
    def pos2(self) -> tuple:
        return self._bounding_box[1].pos

    @property
    def x1(self) -> int | float:
        return self[0]

    @x1.setter
    def x1(self, value: int | float):
        self._bounding_box[0].x = value

    @property
    def x2(self) -> int | float:
        return self[2]

    @x2.setter
    def x2(self, value: int | float):
        self._bounding_box[1].x = value

    @property
    def y1(self) -> int | float:
        return self[1]

    @y1.setter
    def y1(self, value: int | float):
        self._bounding_box[0].y = value

    @property
    def y2(self) -> int | float:
        return self[3]

    @y2.setter
    def y2(self, value: int | float):
        self._bounding_box[1].y = value

    @property
    def area(self) -> int | float:
        return self.width * self.height

    @property
    def width(self) -> int | float:
        return self.x2 - self.x1

    @property
    def height(self) -> int | float:
        return self.y2 - self.y1

    @property
    def centre_x(self) -> int | float:
        return self.x2 - (self.width / 2)

    @property
    def centre_y(self) -> int | float:
        return self.y2 - (self.height / 2)

    @property
    def centre_pos(self) -> tuple:
        return self.centre_x, self.centre_y


class BoundingBox2(_BaseBoundingBox):

    def overlap(self, other: BoundingBox2) -> tuple:
        """
        Calculate the overlap of bounding boxes.

        :param other: Other bounding box, should be a BoundingBox
        :return: x_overlap, y_overlap, overlap_area - tuple[float, float] |
        tuple[tuple[float, float], float]
        """
        x_overlap = min(self.x2, other.x2) - max(self.x1, other.x1)
        y_overlap = min(self.y2, other.y2) - max(self.y1, other.y1)
        return x_overlap, y_overlap

    def isOverlap(self, other: BoundingBox2, touching: bool = True) -> bool:
        return all(map(lambda x: (x >= 0) if touching else (x > 0), self.overlap(other)))

    def overlapArea(self, other: BoundingBox2) -> float:
        """Calculate area of overlap"""
        x_overlap, y_overlap = self.overlap(other)
        overlap_area = 0.
        if x_overlap >= 0 and y_overlap >= 0:
            overlap_area = x_overlap * y_overlap
        return overlap_area

    def percentageOverlap(self, other: BoundingBox2, return_area: bool = False) -> tuple:
        """
        Calculate the minimal percentage overlap of the bounding boxes.

        :param other: Other bounding box, should be a BoundingBox
        :param return_area: Whether to return percentage of overlap, should be bool
        :return: x_overlap, y_overlap, overlap_area - tuple[float, float] |
        tuple[tuple[float, float], float]
        """
        x_overlap, y_overlap = self.overlap(other)
        x_percentage = min(self.width, other.width) * x_overlap
        y_percentage = min(self.height, other.height) * y_overlap
        if return_area:
            overlap_area = 0.
            if x_overlap >= 0 and y_overlap >= 0:
                overlap_area = x_percentage * y_percentage
            return (x_percentage, y_percentage), overlap_area
        return x_percentage, y_percentage

    def toShapelyPolygon(self) -> Polygon:
        return Polygon(self.polygon)


class BoundingBox(_BaseBoundingBox):

    def getDecimalOverlap(self, other: BoundingBox):
        # first get x and y overlaps, if negative take 0 as overlap
        x_overlap = max(min(self.x2, other.x2) - max(self.x1, other.x1), 0)
        y_overlap = max(min(self.y2, other.y2) - max(self.y1, other.y1), 0)

        area_overlap = x_overlap * y_overlap

        # return values as a fraction of the minimum area, width or height
        if self.area == 0 or other.area == 0:
            return 0, 0, 0
        return (area_overlap / min(self.area, other.area),
                x_overlap / min(self.width, other.width),
                y_overlap / min(self.height, other.height))

    def getHeightAndWidthSimilarity(self, other: BoundingBox):
        # similarity defined here as the distance between two quantities divided by the larger one

        height_similarity = abs(self.centre_y - other.centre_y) / (min(self.height, other.height))
        width_similarity = abs(self.centre_x - other.centre_x) / (min(self.width, other.width))

        # heightSimilarity = min(self.height,other.height)/(max(self.height, other.height))
        # widthSimilarity = min(self.width, other.width) / (max(self.width, other.width))

        # centreXSimilarity = abs(self.centre_x - other.centre_x) / (min(self.width, other.width))
        # centreYSimilarity = abs(self.centre_y - other.centre_y) / (min(self.height, other.height))

        return height_similarity, width_similarity

    def getLines(self):
        return [[(self.x1, self.y1), (self.x2, self.y1)],
                [(self.x2, self.y1), (self.x2, self.y2)],
                [(self.x2, self.y2), (self.x1, self.y2)],
                [(self.x1, self.y2), (self.x1, self.y1)]]

    def closestHorizontalDist(self, other):
        a = abs(self.x1 - other.x1)
        b = abs(self.x1 - other.x2)
        c = abs(self.x2 - other.x1)
        d = abs(self.x2 - other.x2)
        return min(a, b, c, d)

    def intersectsWithLine(self, line: list):
        # line is in the form [(x1,y1),(x2,y2)]

        width = abs(line[0][0] - line[1][0])
        height = abs(line[0][1] - line[1][1])

        x_overlap = max(min(self.x2, line[1][0]) - max(self.x1, line[0][0]), 0)
        y_overlap = max(min(self.y2, line[1][1]) - max(self.y1, line[0][1]), 0)

        if width == 0 and self.x1 <= line[0][0] <= self.x2 and y_overlap > 0:
            return True

        if height == 0 and self.y1 <= line[0][1] <= self.y2 and x_overlap > 0:
            return True

        if x_overlap > 0 and y_overlap > 0:
            return True
        return False

    def splitBox(self, line):
        # if vertical line, split vertically
        lx1, ly1, lx2, ly2 = tuple(line[0] + line[1])

        if abs(lx1 - lx2) < 3:
            bbox1 = BoundingBox(self.x1, self.y1, lx1, self.y2)
            bbox2 = BoundingBox(lx1, self.y1, lx1, self.y2)
            return bbox1, bbox2

        if abs(ly1 - ly2) < 3:
            bbox1 = BoundingBox(self.x1, self.y1, self.x2, self.y2)
            bbox2 = BoundingBox(lx1, self.y1, lx1, self.y2)
            return bbox1, bbox2

        return None

    def stretchVertically(self, decimal_percentage: float):
        dist = decimal_percentage * self.height
        self.__iadd__([0, -dist, 0, dist])

    def stretchHorizontally(self, decimal_percentage: float):
        dist = decimal_percentage * self.width
        self.__iadd__([-dist, 0, dist, 0])

    def stretchHorizontallyAbsolute(self, number_of_pixels: int):
        self.__iadd__([-number_of_pixels, 0, number_of_pixels, 0])

    def stretchVerticallyAbsolute(self, number_of_pixels: int):
        self.__iadd__([0, -number_of_pixels, 0, number_of_pixels])

    def __eq__(self, other):
        if isinstance(other, BoundingBox):
            if self._bounding_box == other._bounding_box:
                return True
        return False

    def __hash__(self):
        return hash((tuple(self.pos1), tuple(self.pos2)))
