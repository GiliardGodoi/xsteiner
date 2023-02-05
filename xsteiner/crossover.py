import networkx as nx

from .main import random_prim_st, random_kruskal_st, random_walk_st


def mate(T1: nx.Graph, T2: nx.Graph, terminals, how: str = "prim"):
    functions = {
        "prim": random_prim_st,
        "kruskal": random_kruskal_st,
        "random": random_walk_st,
        "random walk": random_walk_st,
    }
    if how.lower() not in functions:
        raise ValueError(
            f"`how` method should be one of this: \n {list(functions.keys())}"
        )
    G = nx.compose(T1, T2)
    return functions[how](G, terminals)


def mate_prim(T1: nx.Graph, T2: nx.Graph, terminals):
    G = nx.compose(T1, T2)
    T_star = random_prim_st(G, terminals)
    return T_star


def mate_krukal(T1: nx.Graph, T2: nx.Graph, terminals):
    G = nx.compose(T1, T2)
    T_star = random_kruskal_st(G, terminals)
    return T_star


def mate_randomwalk(T1: nx.Graph, T2: nx.Graph, terminals):
    G = nx.compose(T1, T2)
    T_star = random_walk_st(G, terminals)
    return T_star
