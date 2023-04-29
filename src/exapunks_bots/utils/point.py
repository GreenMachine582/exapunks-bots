from __future__ import annotations


class Point(object):
    def __init__(self, *values):
        if len(values) == 1:
            if isinstance(values[0], (tuple, list)):
                values = values[0]
            else:
                raise TypeError(f"{self.__class__.__name__}: values must be an int, float, list or tuple, not {type(values).__name__}")
        if len(values) == 2:
            _x, _y = values
        else:
            raise Exception(f"{self.__class__.__name__} only accepts 2 values or less")

        map(self.checkType, [_x, _y])

        self._x = _x
        self._y = _y

    def __round__(self, n=0):
        self._x = round(self._x, n)
        self._y = round(self._y, n)

    def __int__(self):
        self._x = int(self._x)
        self._y = int(self._y)

    def __getitem__(self, index) -> int | float:
        return self._x if index == 0 else self._y

    def __str__(self) -> str:
        return str(self.pos)

    def __repr__(self) -> str:
        return f"Point({self._x}, {self._y})"

    def __add__(self, values: int | float | tuple | list) -> tuple:
        if not isinstance(values, (tuple, list)):
            values = [values]
        map(self.checkType, values)
        pos = self.pos
        if len(values) == 1:
            pos = (pos[0] + values[0], pos[1] + values[0])
        elif len(values) == 2:
            pos = (pos[0] + values[0], pos[1] + values[1])
        return pos

    def __sub__(self, values: int | float | tuple | list) -> tuple:
        if not isinstance(values, (tuple, list)):
            values = [values]
        map(self.checkType, values)
        pos = self.pos
        if len(values) == 1:
            pos = (pos[0] - values[0], pos[1] - values[0])
        elif len(values) == 2:
            pos = (pos[0] - values[0], pos[1] - values[1])
        return pos

    def __mul__(self, values: int | float | tuple | list) -> tuple:
        if not isinstance(values, (tuple, list)):
            values = [values]
        map(self.checkType, values)
        pos = self.pos
        if len(values) == 1:
            pos = (pos[0] * values[0], pos[1] * values[0])
        elif len(values) == 2:
            pos = (pos[0] * values[0], pos[1] * values[1])
        return pos

    def __floordiv__(self, values: int | float | tuple | list) -> tuple:
        if not isinstance(values, (tuple, list)):
            values = [values]
        map(self.checkType, values)
        pos = self.pos
        if len(values) == 1:
            pos = (pos[0] // values[0], pos[1] // values[0])
        elif len(values) == 2:
            pos = (pos[0] // values[0], pos[1] // values[1])
        return pos

    def __truediv__(self, values: int | float | tuple | list) -> tuple:
        if not isinstance(values, (tuple, list)):
            values = [values]
        map(self.checkType, values)
        pos = self.pos
        if len(values) == 1:
            pos = (pos[0] / values[0], pos[1] / values[0])
        elif len(values) == 2:
            pos = (pos[0] / values[0], pos[1] / values[1])
        return pos

    def __iadd__(self, values) -> Point:
        self._x, self._y = self.__add__(values)
        return self

    def __isub__(self, values) -> Point:
        self._x, self._y = self.__sub__(values)
        return self

    def __imul__(self, values) -> Point:
        self._x, self._y = self.__mul__(values)
        return self

    def __ifloordiv__(self, values) -> Point:
        self._x, self._y = self.__floordiv__(values)
        return self

    def __itruediv__(self, values) -> Point:
        self._x, self._y = self.__truediv__(values)
        return self

    def toJson(self) -> tuple:
        return self.pos

    def copy(self) -> Point:
        return Point(*self.pos)

    @property
    def pos(self) -> tuple:
        return self.x, self.y

    @property
    def x(self) -> int | float:
        return self._x

    @x.setter
    def x(self, value: int | float):
        self.checkType(value)
        self._x = value

    @property
    def y(self) -> int | float:
        return self._y

    @y.setter
    def y(self, value: int | float):
        self.checkType(value)
        self._y = value

    @staticmethod
    def checkType(value: int | float):
        if not isinstance(value, (int, float)):
            raise TypeError(f"TypeError: must be int or float, not {type(value).__name__}")
