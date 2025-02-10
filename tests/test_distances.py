import pytest
from collections import defaultdict
from xsteiner.graph.distances import (
    shortest_path
)
from xsteiner.graph.graph import Graph
from xsteiner.graph.edge import Edge

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

