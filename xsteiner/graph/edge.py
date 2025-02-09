
class Edge:

    __slots__ = ('_x', '_y', '_w')

    def __init__(self, x, y, weight=None):
        self._x, self._y, self._w = x, y, weight

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        raise AttributeError('Cannot set a new value')

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        raise AttributeError('Cannot set a new value')

    @property
    def weight(self):
        if self._w is None:
            raise ValueError('There is no weight assigned')
        return self._w

    @weight.setter
    def weight(self, value):
        raise AttributeError('Cannot set a new value')

    def __copy__(self):
        return Edge(self._x, self._y, weight=self._w)

    def __contains__(self, node):
        return (node == self._x) or (node == self._y)

    def __eq__(self, edge):
        if not isinstance(edge, Edge):
            return False
        return (edge.x in self) \
                and (edge.y in self) \
                and (edge._w == self._w)

    def __iter__(self):
        return iter((self._x, self._y))

    def __hash__(self):
        start, end, weight = self._x, self._y, self._w
        if hash(end) < hash(start):
            start, end = end, start
        return hash((self.__class__, start, end, weight))

    def __str__(self):
        if self._w is None:
            return f'Edge({self._x}, {self._y})'
        return f'Edge({self._x}, {self._y}, weight={self._w})'

    def __repr__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()