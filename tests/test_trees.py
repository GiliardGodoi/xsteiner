import pytest
from xsteiner.graph.graph import Graph
from xsteiner.graph.edge import Edge
from xsteiner.graph.trees.minimum_spanning import (
    prim_spanning_tree,
    kruskal_spanning_tree,
    boruvka_spanning_tree,
)


def test_spanning_tree_on_cyclic_graph(cyclic):

    tree = prim_spanning_tree(cyclic, 1)
    edges = [e for e in tree.edges()]
    assert isinstance(tree, Graph)
    assert all(isinstance(e, Edge) for e in edges)

    assert cyclic.has_edge(1, 20, 32)
    assert not tree.has_edge(1, 20, 32)

    edges = [e for e in tree.edges()]
    tree_weight = sum(e.weight for e in edges)

    total_weight = sum([e.weight for e in cyclic.edges()])
    assert 0 < tree_weight <= total_weight

    nro_nodes_in = len([_ for _ in cyclic.nodes()])
    nro_edges = len([_ for _ in tree.edges()])
    nro_nodes = len([_ for _ in tree.nodes()])
    assert nro_nodes_in == nro_nodes
    assert nro_edges == (nro_nodes - 1)

    A_edges = [e for e in cyclic.edges() if tree.has_edge(e)]
    B_edges = [e for e in tree.edges()]
    for a in A_edges:
        for b in B_edges:
            if a == b:
                assert a is b


def test_prim_mst_on_bigger_graph(bigger):
    tree = prim_spanning_tree(bigger, 5)
    assert tree
    nro_nodes_in = len([_ for _ in bigger.nodes()])
    nro_edges = len([_ for _ in tree.edges()])
    nro_nodes = len([_ for _ in tree.nodes()])
    assert nro_nodes_in == nro_nodes
    assert nro_edges == (nro_nodes - 1)


@pytest.mark.parametrize('name',['cyclic', 'bigger'])
def test_with_tree_shares_edges_using_prim_mst(name, request):
    graph = request.getfixturevalue(name)

    tree = prim_spanning_tree(graph, 1)
    assert all(graph.has_edge(e) for e in tree.edges())

    A_edges = [e for e in graph.edges() if tree.has_edge(e)]
    B_edges = [e for e in tree.edges()]
    for a in A_edges:
        for b in B_edges:
            if a == b:
                assert a is b

def test_kruskal_spanning_tree_on_cyclic_graph(cyclic):

    tree = kruskal_spanning_tree(cyclic)
    edges = [e for e in tree.edges()]
    assert isinstance(tree, Graph)
    assert all(isinstance(e, Edge) for e in edges)

    tree_weight   = sum(e.weight for e in edges)
    expected_sum = sum(i for i in range(3, 22))
    assert expected_sum == tree_weight

    total_weight = sum([e.weight for e in cyclic.edges()])
    assert 0 < tree_weight <= total_weight

    nro_nodes_in = len([_ for _ in cyclic.nodes()])
    nro_edges = len([_ for _ in tree.edges()])
    nro_nodes = len([_ for _ in tree.nodes()])
    assert nro_nodes_in == nro_nodes
    assert nro_edges == (nro_nodes - 1)

    A_edges = [e for e in cyclic.edges() if tree.has_edge(e)]
    B_edges = [e for e in tree.edges()]
    for a in A_edges:
        for b in B_edges:
            if a == b:
                assert a is b

def test_boruvka_spanning_tree(cyclic):

    tree = boruvka_spanning_tree(cyclic)
    edges = [e for e in tree.edges()]
    assert isinstance(tree, Graph)
    assert all(isinstance(e, Edge) for e in edges)

    tree_weight   = sum(e.weight for e in edges)
    expected_sum = sum(i for i in range(3, 22))
    assert expected_sum == tree_weight

    total_weight = sum([e.weight for e in cyclic.edges()])
    assert 0 < tree_weight <= total_weight

    nro_nodes_in = len([_ for _ in cyclic.nodes()])
    nro_edges = len([_ for _ in tree.edges()])
    nro_nodes = len([_ for _ in tree.nodes()])
    assert nro_nodes_in == nro_nodes
    assert nro_edges == (nro_nodes - 1)

    A_edges = [e for e in cyclic.edges() if tree.has_edge(e)]
    B_edges = [e for e in tree.edges()]
    for a in A_edges:
        for b in B_edges:
            if a == b:
                assert a is b

def test_boruvka_spanning_tree_on_bigger(bigger):

    tree = boruvka_spanning_tree(bigger)
    edges = [e for e in tree.edges()]
    tree_weight   = sum(e.weight for e in edges)
    total_weight = sum([e.weight for e in bigger.edges()])

    assert isinstance(tree, Graph)
    assert all(isinstance(e, Edge) for e in edges)
    assert 0 < tree_weight <= total_weight

    A_edges = [e for e in bigger.edges() if tree.has_edge(e)]
    B_edges = [e for e in tree.edges()]
    for a in A_edges:
        for b in B_edges:
            if a == b:
                assert a is b