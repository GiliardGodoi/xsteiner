
from xsteiner.disjointset.disjointset import DisjointSet
from xsteiner.graph.graph import (
    Graph,
    SteinerGraphProblemInstance,
)
from xsteiner.populate.populate import (
    kruskal_random_spanning_tree,
    prim_random_spanning_tree
)

def test_kruskal_random_spanning_tree(bigger:SteinerGraphProblemInstance):
    tree = kruskal_random_spanning_tree(bigger)
    assert isinstance(tree, Graph)
    assert all(tree.has_node(t) for t in bigger.terminals)

    ds = DisjointSet()
    for v in tree.nodes() : ds.make_set(v)
    for edge in tree.edges():
        i, j = edge
        ds.union(i, j)
    components = ds.parents_components()
    assert len(components) == 1


def test_prim_random_spanning_tree(bigger:SteinerGraphProblemInstance):
    tree = prim_random_spanning_tree(bigger)
    assert isinstance(tree, Graph)
    assert all(tree.has_node(t) for t in bigger.terminals)

    ds = DisjointSet()
    for v in tree.nodes() : ds.make_set(v)
    for edge in tree.edges():
        i, j = edge
        ds.union(i, j)
    components = ds.parents_components()
    assert len(components) == 1