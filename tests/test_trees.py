import pytest
from pathlib import Path
from xsteiner.graph.graph import Graph
from xsteiner.graph.edge import Edge
from xsteiner.graph.trees import (
    prim_spanning_tree,
    kruskal_spanning_tree,
)
from xsteiner.utils.steinlib import steinlib_parser
from xsteiner.graph.search import shortest_edge_search

@pytest.fixture
def bigger():
    return steinlib_parser(Path('datasets', 'cc10-2p.stp'))

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

def test_prim_spanning_tree_on_cyclic_graph(cyclic):
    cyclic.add_edge(5, 18, 9)

    tree = prim_spanning_tree(cyclic, 1)
    edges = [e for e in tree.edges()]
    assert all(isinstance(e, Edge) for e in edges)
    assert isinstance(tree, Graph)

    assert cyclic.has_edge(17, 18, 19)
    assert not tree.has_edge(17, 18, 19)

    assert cyclic.has_edge(1, 20, 32)
    assert not tree.has_edge(1, 20, 32)

    tree_weight = sum(e.weight for e in edges)
    total_weight = sum([e.weight for e in cyclic.edges()])
    assert 0 < tree_weight <= total_weight


@pytest.mark.skip
def test_prim_mst_on_bigger_graph(bigger):
    tree = prim_spanning_tree(bigger, 5)
    assert tree

    result = [tree.has_edge(i,j) for i, j in shortest_edge_search(bigger, 5)]
    assert all(result), 'Vai falhar aqui!'


def test_kruskal_spanning_tree_on_cyclic_graph(cyclic):

    tree = kruskal_spanning_tree(cyclic)
    edges = [e for e in tree.edges()]
    tree_weight   = sum(e.weight for e in edges)
    expected_sum = sum(i for i in range(3, 22))
    assert isinstance(tree, Graph)
    assert all(isinstance(e, Edge) for e in edges)
    assert expected_sum == tree_weight

    total_weight = sum([e.weight for e in cyclic.edges()])
    assert 0 < tree_weight <= total_weight