from xsteiner.disjointset.disjointset import DisjointSet
from xsteiner.graph.graph import Graph
from xsteiner.pqueue.pqueue import PriorityQueue

def prim_spanning_tree(graph : Graph, source):
    ''' Prim's Algorithm: Compute the Minimum Spanning Tree for the graph.

    Parameters:
        graph : GraphDictionary
        start : <a graph's node>

    Returns:
        dict :

        int :

    TO DO:
        Verificar se para diferentes pontos de inicialização retorna a mesma árvore
        se sim, parece que está funcionando ok.
    '''
    if not graph.has_node(source):
        raise ValueError(f'Source node found in graph: {source}')
    tree = Graph()
    visited = set()
    queue = PriorityQueue()
    best_weight = dict()
    queue.push(0, (source, None, None))

    while queue:
        _, (node, prev, edge) = queue.pop()
        if node in visited:
            continue
        visited.add(node)
        if prev is not None:
            tree.add_edge(edge)

        for edge in graph.adjacents_edges(node):
            adj = edge.adj(node)
            if adj not in visited:
                if (adj not in best_weight) or (edge.weight < best_weight[adj]):
                    best_weight[adj] = edge.weight
                    queue.push(edge.weight, (adj, node, edge))
    return tree


def kruskal_spanning_tree(graph : Graph):
    '''Kruskal Algorithm to determine a Minimum Spanning Tree froma a Graph

    Parameter
        graph : Graph

    Return
        Minimum Spanning Tree Graph
    '''
    ds = DisjointSet()
    tree = Graph()
    nro_nodes = 0
    for v in graph.nodes():
        ds.make_set(v)
        nro_nodes += 1

    edges = [e for e in graph.edges()]
    edges = sorted(edges, key=lambda e: e.weight)
    nro_tree_edges = 0
    for edge in edges:
        v, u = edge
        if ds.find(v) != ds.find(u):
            tree.add_edge(edge)
            ds.union(v, u)
            nro_tree_edges += 1
            if nro_tree_edges == (nro_nodes - 1):
                break
    return tree

def boruvka_spanning_tree(graph : Graph):
    ds = DisjointSet()
    nro_components = 0
    for v in graph.nodes():
        ds.make_set(v)
        nro_components += 1
    edges = {e for e in graph.edges()}
    tree = Graph()
    while nro_components > 1:
        cheapest = dict()
        done = set()
        for edge in edges:
            u, v = edge
            comp_u = ds.find(u)
            comp_v = ds.find(v)
            if comp_u == comp_v:
                done.add(edge)
                continue
            if comp_u not in cheapest or cheapest[comp_u].weight > edge.weight:
                cheapest[comp_u] = edge
            if comp_v not in cheapest or cheapest[comp_v].weight > edge.weight:
                cheapest[comp_v] = edge

        for comp, edge in cheapest.items():
            u, v = edge
            comp_u = ds.find(u)
            comp_v = ds.find(v)
            if comp_u == comp_v:
                continue
            ds.union(v, u)
            tree.add_edge(edge)
            nro_components -= 1
        edges = edges - done

    return tree