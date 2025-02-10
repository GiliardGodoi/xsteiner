from typing import Iterable
from .edge import Edge

class Graph:

    def __init__(self):
        self.data = dict()

    def add_edge(self, *args):
        if len(args) == 1 and isinstance(args[0], Edge):
            edge = args[0]
        elif len(args) == 1:
            raise ValueError
        elif len(args) == 2:
            x0, x1 = args
            edge = Edge(x0, x1)
        elif len(args) == 3 and isinstance(args[2], int):
            x0, x1, weight = args
            edge = Edge(x0, x1, weight=weight)
        else:
            raise ValueError

        if self.has_edge(edge):
            raise ValueError

        if not self.has_node(edge.x):
            self.add_node(edge.x)
        if not self.has_node(edge.y):
            self.add_node(edge.y)

        self.data[edge.x].add(edge)
        self.data[edge.y].add(edge)
        return True

    def add_node(self, node):
        if node == None:
            raise ValueError('Cannot assign None as Graph Node')
        if node in self.data:
            raise ValueError(f'Node already exists: {node}')
        self.data[node] = set()
        return True

    def adjacents(self, node):
        if not self.has_node(node):
            raise ValueError(f'Node not in graph: {node}')
        for edge in self.data[node]:
            other = edge.x if node == edge.y else edge.y
            yield other

    def adjacents_edges(self, node):
        if not self.has_node(node):
            raise ValueError(f'Node not in graph: {node}')
        yield from self.data.get(node)

    def edges(self):
        visited = set()
        for node in self.data.keys():
            for edge in self.data[node]:
                if edge in visited:
                    continue
                visited.add(edge)
                yield edge

    def nodes(self):
        yield from self.data.keys()

    def degree(self, node):
        if not self.has_node(node):
            raise ValueError(f'Node not in graph: {node}')
        return len(self.data[node])

    def has_edge(self, *args):

        if len(args) == 1 and isinstance(args[0], Edge):
            edge = args[0]
        elif len(args) == 1:
            raise ValueError(f'Args is not a Edge type: received {type(args[0])}')
        elif len(args) == 2:
            edge = Edge(args[0], args[1], weight=None)
        elif len(args) == 3:
            edge = Edge(args[0], args[1], weight=args[2])
        else:
            raise ValueError(f'Parameters received: {args=}')

        return (self.has_node(edge.x)) \
                and (self.has_node(edge.y)) \
                and (edge in self.data.get(edge.x)) \
                and (edge in self.data.get(edge.y))

    def has_node(self, node):
        return (node in self.data)

    def remove_node(self, node):
        if node not in self.data:
            raise ValueError(f'Node not found in graph: {node}')

        if not self.data[node]:
            return

        for edge in self.data[node]:
            u, v = edge
            other = v if node == u else u
            if other in self.data and self.data[other]:
                self.data[other].remove(edge)

        del self.data[node]

    def remove_edge(self, *args):
        if len(args) == 1 and isinstance(args[0], Edge):
            edge = args[0]
        elif len(args) == 1:
            raise TypeError(f'Args is not a Edge type: received {type(args[0])}')
        elif len(args) == 2:
            edge = Edge(args[0], args[1], weight=None)
        elif len(args) == 3:
            edge = Edge(args[0], args[1], weight=args[2])
        else:
            raise ValueError(f'Parameters received: {args!s}')

        if not self.has_edge(edge):
            raise ValueError(f'Edge not found in graph: {edge!s}')

        self.data[edge.x].remove(edge)
        self.data[edge.y].remove(edge)

    def n_nodes(self):
        return len(self.data)

class SteinerGraphProblemInstance(Graph):

    def __init__(self):
        super().__init__()
        self.nro_nodes = 0
        self.nro_edges = 0
        self.nro_terminals = 0
        self.name = None
        self.remark = None
        self.creator = None
        self.file_name = None
        self.__terminals = None

    @property
    def terminals(self):
        return self.__terminals

    @terminals.setter
    def terminals(self, values):
        pass

    def update_terminals(self, terminals: Iterable):
        if self.__terminals is None:
            if isinstance(terminals, set):
                self.__terminals = terminals
            else:
                self.__terminals = set(terminals)
        else:
            raise ValueError('Cannot reasign terminals nodes for an already instatiate steiner graph')
