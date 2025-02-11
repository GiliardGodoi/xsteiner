from random import shuffle, sample, choice, randrange
from xsteiner.disjointset.disjointset import DisjointSet
from xsteiner.graph.graph import (
    Graph,
    SteinerGraphProblemInstance
)
from xsteiner.graph.heuristics import pruning_tree

def kruskal_random_spanning_tree(steiner:SteinerGraphProblemInstance, prune=True):
    tree = Graph()
    ds = DisjointSet()
    for v in steiner.nodes():
        ds.make_set(v)
    edges = [e for e in steiner.edges()]
    shuffle(edges)
    while edges :
        edge = edges.pop()
        u, v = edge
        if ds.find(u) != ds.find(v):
            tree.add_edge(edge)
            ds.union(u, v)

    if prune:
        tree = pruning_tree(tree, steiner.terminals)

    return tree


def prim_random_spanning_tree(steiner:SteinerGraphProblemInstance, prune=True):

    tree = Graph()
    terminals = steiner.terminals.copy()
    node = choice([v for v in steiner.nodes()])
    edges = [e for e in steiner.adjacents_edges(node)]
    terminals.discard(node)
    done = set()
    done.add(node)

    while terminals and edges:
        idx = randrange(0, len(edges))
        edge = edges.pop(idx)
        if not tree.has_edge(edge):
            tree.add_edge(edge)
            w = edge.y if edge.x in done else edge.x
            for edge in steiner.adjacents_edges(w):
                if not tree.has_edge(edge):
                    edges.append(edge)
            done.add(w)
            terminals.discard(w)

    return tree



