import networkx as nx
import random

from disjointset import DisjointSet
from .edge import Edge


def replace_random_edge(T: nx.Graph, G: nx.Graph):
    '''
    Replace a random edge by another random edge.
    '''
    control_limit = T.number_of_nodes() + 100
    control_counter = 0
    nodes = list(T.nodes)

    while True:
        if control_counter >= control_limit:
            raise StopIteration("An unexpected error occurred")
        control_counter += 1
        v_line = random.choice(nodes)
        if G.degree(v_line) > 1:
            break

    u_line = random.choice(list(T.adj[v_line]))

    T.remove_edge(v_line, u_line)
    components = [c for c in nx.connected_components(T)]

    # assert len(components) == 2
    # assert v_line in T
    # assert u_line in T
    # assert not T.has_edge(v_line, u_line)

    disjointset = DisjointSet()
    for component in components:
        for v in component:
            disjointset.make_set(v)

    for v, u in T.edges:
        disjointset.union(v, u)

    candidate_edges = set()
    for v, u in G.edges:
        if (
            (v in disjointset)
            and (u in disjointset)
            and disjointset.find(v) != disjointset.find(u)
        ):
            candidate_edges.add(Edge(v, u))

    # assert v_line in G
    # assert u_line in G
    # assert G.has_edge(v_line, u_line)
    # assert v_line in disjointset
    # assert u_line in disjointset
    # assert disjointset.find(v_line) != disjointset.find(u_line)

    if len(candidate_edges) == 0:
        raise RuntimeError("An unexpected error occurred")

    elif len(candidate_edges) == 1:
        candidate_edges.add(Edge(v_line, u_line))
        T.add_edge(v_line, u_line)

    elif len(candidate_edges) > 1:
        candidate_edges.remove(Edge(v_line, u_line))
        v, u = random.choice(list(candidate_edges))
        T.add_edge(v, u)

    # assert nx.is_tree(T)

    return T
