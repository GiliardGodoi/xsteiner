from collections import defaultdict
from random import shuffle, random, choice, randrange
from xsteiner.disjointset.disjointset import DisjointSet
from xsteiner.graph.graph import Graph

def kruskal_random_spanning_tree(graph:Graph):
    tree = Graph()
    ds = DisjointSet()
    for v in graph.nodes():
        ds.make_set(v)
    edges = [e for e in graph.edges()]
    shuffle(edges)
    while edges :
        edge = edges.pop()
        u, v = edge
        if ds.find(u) != ds.find(v):
            tree.add_edge(edge)
            ds.union(u, v)

    return tree


def prim_random_spanning_tree(graph:Graph):

    tree = Graph()
    node = choice([v for v in graph.nodes()])
    edges = [e for e in graph.adjacents_edges(node)]
    visited = set()
    visited.add(node)

    while edges:
        idx = randrange(0, len(edges))
        edge = edges.pop(idx)
        connected = (tree.has_node(edge.x) and tree.has_node(edge.y))
        if not connected:
            tree.add_edge(edge)
            adj = edge.y if edge.x in visited else edge.x
            edges.extend([e
                          for e in graph.adjacents_edges(adj)
                          if not tree.has_edge(e) ])
            visited.add(adj)
    return tree


def random_walk_spanning_tree(graph:Graph):
    tree = Graph()
    vertices = list(graph.nodes())
    v = vertices.pop()
    while vertices:
        edge = choice([e for e in graph.adjacents_edges(v)])
        u = edge.adj(v)
        if not tree.has_node(u):
            tree.add_edge(edge)
            vertices.discard(u)
        v = u

    return tree

def boruvka_random_spanning_tree(graph:Graph):
    ds = DisjointSet()
    nro_components = 0
    for v in graph.nodes():
        ds.make_set(v)
        nro_components += 1
    edges = set(graph.edges())
    tree = Graph()
    while nro_components > 1:
        cheapest = defaultdict(dict)
        done = set()
        for edge in edges:
            if tree.has_edge(edge):
                continue
            comp_u = ds.find(edge.x)
            comp_v = ds.find(edge.y)
            if comp_u == comp_v:
                done.add(edge)
                continue
            if comp_u not in cheapest or cheapest[comp_u]['weight'] > random():
                cheapest[comp_u]['edge'] = edge
                cheapest[comp_u]['weight'] = random()
            if comp_v not in cheapest or cheapest[comp_v]['weight'] > random():
                cheapest[comp_v]['edge'] = edge
                cheapest[comp_v]['weight'] = random()

        for comp in cheapest.values():
            edge = comp['edge']
            u, v = edge
            comp_u = ds.find(u)
            comp_v = ds.find(v)
            if comp_u == comp_v:
                done.add(edge)
                continue
            ds.union(v, u)
            tree.add_edge(edge)
            nro_components -= 1
        # edges = edges - done

    return tree