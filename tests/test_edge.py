import pytest
from xsteiner.graph.edge import Edge

def test_edge_weight():
    e1 = Edge(1, 2, 5)
    assert e1.weight == 5

    e2 = Edge(101, 105)
    with pytest.raises(ValueError):
        a = e2.weight

def test_hash_edges_with_different_weights():

    e1 = Edge(1, 2)
    e2 = Edge(2, 1)
    e3 = Edge(1, 2, 5)
    assert e1 == e2
    assert e2 != e3
    assert e1 != e3
    assert hash(e1) == hash(e2)
    assert hash(e1) != hash(e3)
    assert hash(e2) != hash(e3)

def test_edge_hash_on_sets():
    edges = [
        Edge(1, 2),
        Edge(2, 1),
        Edge(1, 2, 5)
    ]
    edges = set(edges)
    assert len(edges) == 2