import pytest
from xsteiner.graph.graph import Graph
from xsteiner.graph.search import (
    breadth_first_search,
    depth_first_search,
    shortest_edge_search
)


@pytest.fixture
def cyclic():
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

def test_breadth_fisrt_search_on_cyclic_graph(cyclic):
    start = 1
    previous = dict()
    previous[start] = None
    for adj, prev in breadth_first_search(cyclic, start):
        assert adj != prev
        previous[adj] = prev

    assert (previous[2] == 1) and (previous[20] == 1)


def test_depth_first_search_on_cyclic_graph(cyclic):
    start = 1
    previous = dict()
    previous[start] = None
    for adj, prev in depth_first_search(cyclic, start):
        assert adj != prev
        previous[adj] = prev

    assert (previous[2] == 1) or (previous[20] == 1)
    assert previous[2] != previous[20]

def test_shortest_edge_search(cyclic):
    start = 1
    previous = dict()
    previous[start] = None
    for adj, prev in shortest_edge_search(cyclic, start):
        assert adj != prev
        previous[adj] = prev

    assert previous[1] is None
    assert previous[2] == 1
    assert previous[19] == 18
    assert previous[20] == 19
