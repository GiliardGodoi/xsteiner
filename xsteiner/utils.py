import networkx as nx

from . import edge


def check_steiner(T: nx.Graph, G: nx.Graph, terminals, silent=True):

    T_edges = {edge.Edge(v, u) for v, u in T.edges}
    G_edges = {edge.Edge(v, u) for v, u in G.edges}
    leaves = {v for v in T.nodes if T.degree(v) == 1}

    is_tree = nx.is_tree(T)
    have_all_terminals = set(T.nodes).issuperset(set(terminals))
    have_all_nodes_from_instance = set(G.nodes).issuperset(set(T.nodes))
    have_all_edges_from_instance = set(G_edges).issuperset(T_edges)
    all_leaves_are_also_terminals = set(terminals).issuperset(leaves)

    if not silent:
        assert is_tree, "The given T is not a tree"
        assert have_all_terminals, "The given T does not have all terminals from G"
        assert (
            have_all_nodes_from_instance
        ), "The given T does not have all nodes from G"
        assert (
            have_all_edges_from_instance
        ), "The given T does not have all edges from G"
        assert (
            all_leaves_are_also_terminals
        ), "Not all leaf node is also a terminal node"

    return (
        is_tree
        and have_all_terminals
        and have_all_nodes_from_instance
        and have_all_edges_from_instance
        and all_leaves_are_also_terminals
    )
