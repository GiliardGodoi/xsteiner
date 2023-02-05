import networkx as nx
import random

from disjointset import DisjointSet
from .edge import Edge


def random_spanning_tree(G: nx.Graph, terminals, how: str = ""):
    functions = {
        "prim": random_prim_st,
        "kruskal": random_kruskal_st,
        "random": random_walk_st,
        "random walk": random_walk_st,
    }
    if how.lower() not in functions:
        raise ValueError(f"`method` should be one of this: \n {list(functions.keys())}")

    return functions[how](G, terminals)


def random_prim_st(G: nx.Graph, terminals):
    """
    Random Steiner Tree based on Prim's algorithms
    """
    P = nx.Graph()
    nodes = set(G.nodes)
    terminals = set(terminals)
    done = set()
    candidates = set()

    v_star = random.choice(list(nodes))
    for u in G.adj[v_star]:
        candidates.add(Edge(v_star, u))

    nodes.remove(v_star)
    terminals.discard(v_star)
    done.add(v_star)

    n_count = 0
    n_edges = G.number_of_edges()

    while terminals:
        if n_count > n_edges + 2:
            raise RuntimeError(
                f"An unexpected error occurred: {n_count} > {n_edges + 2}"
            )
        edge = random.choice(list(candidates))
        u, v = edge

        if (u in done) and (v in nodes):
            P.add_edge(u, v)
            nodes.remove(v)
            terminals.discard(v)
            done.add(v)
            for w in G.adj[v]:
                if w != u:
                    candidates.add(Edge(v, w))
        elif (v in done) and (u in nodes):
            P.add_edge(v, u)
            nodes.remove(u)
            terminals.discard(u)
            done.add(u)
            for w in G.adj[u]:
                if w != v:
                    candidates.add(Edge(u, w))
        else:
            raise RuntimeError("An unexpected error occurred")
        candidates.remove(edge)

    return P


def random_kruskal_st(G: nx.Graph, terminals):
    """
    A random Steiner Tree based on Kruskal algorithm.
    """
    K = nx.Graph()

    disjointset = DisjointSet()
    for v in G.nodes:
        disjointset.make_set(v)

    # disjoints sets for all the terminals
    control_group = set(disjointset.find(t) for t in terminals)

    edges = list(G.edges)

    random.shuffle(edges)
    random.shuffle(edges)

    edges = iter(edges)

    # when all the terminals are connected, must be have just
    # one disjoint group in control group
    while len(control_group) != 1:
        v, u = next(edges)
        if disjointset.find(v) != disjointset.find(u):

            control_group.discard(disjointset.find(v))
            control_group.discard(disjointset.find(u))

            K.add_edge(v, u)
            disjointset.union(v, u)

            control_group.add(disjointset.find(v))

    return K


def random_walk_st(G: nx.Graph, terminals):
    """
    A random Steiner Tree based on a Random Walk algorithm
    """
    R = nx.Graph()

    nodes = set(G.nodes)
    terminals = set(terminals)
    done = set()

    v_star = random.choice(list(nodes))
    nodes.remove(v_star)
    terminals.discard(v_star)
    done.add(v_star)

    while terminals:
        u = random.choice(list(G[v_star]))
        if u not in done:
            R.add_edge(v_star, u)
            done.add(u)
            nodes.remove(u)
            terminals.discard(u)
        # walk through the next node
        v_star = u

    return R
