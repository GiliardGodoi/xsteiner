import pytest
from collections import defaultdict
from xsteiner.graph.distances import (
    shortest_path
)
from xsteiner.graph.graph import Graph
from xsteiner.graph.edge import Edge

@pytest.fixture
def empty_graph():
    return Graph()

@pytest.fixture
def medium_graph():
    g = Graph()
    nodes = range(1, 21)
    for node in nodes:
        g.add_node(node)
    edges = [
        (1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (5, 6, 7),
        (6, 7, 8), (7, 8, 9), (8, 9, 10), (9, 10, 11), (10, 11, 12),
        (11, 12, 13), (12, 13, 14), (13, 14, 15), (14, 15, 16), (15, 16, 17),
        (16, 17, 18), (17, 18, 19), (18, 19, 20), (19, 20, 21), (20, 1, 32)
    ]
    for edge in edges:
        g.add_edge(*edge)
    return g

def test_shortest_path_return_type_obj(medium_graph):
    node = 10
    dist, prev = shortest_path(medium_graph, node)
    assert isinstance(dist, defaultdict)
    assert isinstance(prev, dict)

def test_shortest_path_with_empty_graph(empty_graph):
    with pytest.raises(ValueError):
        _, _ = shortest_path(empty_graph, 10)

def test_shortest_path_with_inexistent_node_in_graph(medium_graph):
        with pytest.raises(ValueError):
            _, _ = shortest_path(medium_graph, 55)

def test_shortest_path_with_medium_graph(medium_graph):
    dist, prev = shortest_path(medium_graph, 5)

    assert prev[5] is None
    assert dist[5] == 0

    assert isinstance(prev[1], Edge)
    assert prev[1].adj(1) == 2
    assert dist[1] == 18

    assert isinstance(prev[20], Edge)
    assert dist[20] == (18 + 32)
    assert prev[20].adj(20) == 1

