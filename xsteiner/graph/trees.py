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
    for v in graph.nodes():
        ds.make_set(v)

    edges = [e for e in graph.edges()]
    edges = sorted(edges, key=lambda e: e.weight)

    for edge in edges:
        v, u = edge
        if ds.find(v) != ds.find(u):
            tree.add_edge(v, u, edge.weight)
            ds.union(v,u)
    return tree