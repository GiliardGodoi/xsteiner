"""
A simple class to represent an Edge.

Given to vertices v1 < v0, does not matter the order where the vertice is initialized.
A `hash` operation ensures that Edge(v0, v1) is equal to Edge(v1, v0).

author: Giliard Godoi
"""


class Edge:
    def __init__(self, v0, v1):
        if hash(v1) < hash(v0):
            v0, v1 = v1, v0
        self._edge = (v0, v1)

    def __str__(self):
        return f"Edge {self._edge}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self._edge)

    def __contains__(self, v):
        return v in self._edge

    def __iter__(self):
        return iter(self._edge)

    def __eq__(self, other):
        return self._edge == other._edge
