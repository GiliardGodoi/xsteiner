import networkx as nx
from collections import deque
import random

from disjointset import DisjointSet


def all_key_paths(T: nx.Graph):
    key_nodes = set(v for v in T.nodes if T.degree(v) != 2)
    stack = deque([key_nodes.pop()])
    visited = set()
    paths = list()

    path = list()
    while stack:
        node = stack[-1]
        visited.add(node)

        path.append(node)
        if (T.degree(node) != 2) and (len(path) > 1):
            paths.append(path)
            path = list()
            path.append(node)

        remove_from_stack = True  # A princípio todos os vértices devem ser removidos
        for u in T.adj[node]:
            if u not in visited:
                stack.append(u)
                remove_from_stack = False
                break

        if remove_from_stack:
            # isso previne que os caminhos
            # sejam novamente identificados
            # quando o algoritmo percorre a ordem inversa
            path.pop()  # isso aqui
            stack.pop()

    return paths


def random_key_path(T: nx.Graph, terminals, n_edges=3):
    key_nodes = list(v for v in T.nodes if T.degree(v) > 2)
    terminals = set(terminals)
    stack = deque(random.choices(key_nodes, k=1))
    visited = set()
    # paths = list()

    path = list()
    while stack:
        node = stack[-1]
        visited.add(node)

        path.append(node)
        is_stop_node = (T.degree(node) != 2) or (node in terminals)
        if (is_stop_node) and len(path) > 1:  # closing one path
            if (
                len(path) > n_edges
                and T.degree(path[0]) != 1
                and T.degree(path[-1]) != 1
            ):  # stop searching
                # paths.append(path)
                break
            else:  # open another path
                path = list()
                path.append(node)

        remove_from_stack = True  # A princípio todos os vértices devem ser removidos
        for u in T.adj[node]:
            if u not in visited:
                stack.append(u)
                remove_from_stack = False
                break

        if remove_from_stack:
            path.pop()
            stack.pop()

    return path


def replace_random_key_path(T: nx.Graph, G: nx.Graph, terminals, n_edges=3, cutoff=6):

    path = random_key_path(T, terminals, n_edges=n_edges)
    if len(path) == 0:
        return T

    T2 = T.copy()

    ebunch = list(nx.utils.pairwise(path))
    T2.remove_edges_from(ebunch)
    for v in path:
        if T2.degree(v) == 0:
            T2.remove_node(v)

    disjointset = DisjointSet()

    for v in T2.nodes:
        disjointset.make_set(v)

    for v, u in T2.edges:
        disjointset.union(v, u)

    s, t = path[0], path[-1]
    for n_path in nx.all_simple_paths(G, source=s, target=t, cutoff=cutoff):

        for v in n_path:
            if v not in disjointset:
                disjointset.make_set(v)

        for v, u in nx.utils.pairwise(n_path):
            if disjointset.find(v) != disjointset.find(u):
                T2.add_edge(v, u)
                disjointset.union(v, u)
        break

    return T2
