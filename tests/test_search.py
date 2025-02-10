import pytest
from xsteiner.graph.graph import Graph
from xsteiner.graph.search import (
    breadth_first_search,
    depth_first_search,
    shortest_edge_search
)

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
