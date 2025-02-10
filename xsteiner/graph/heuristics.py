from collections import defaultdict, deque
from xsteiner.graph.graph import Graph
from xsteiner.graph.trees import (
    prim_spanning_tree,
    kruskal_spanning_tree,
    boruvka_spanning_tree
)
from xsteiner.pqueue.pqueue import PriorityQueue
from xsteiner.graph.distances import shortest_path



def shortest_path_steiner_tree(graph, start, terminals):

    dist, prev = shortest_path(graph, start)

    distancias = defaultdict(dict)
    distancias[start] = dist

    previous = defaultdict(dict)
    previous[start] = prev

    pqueue = PriorityQueue()

    for t in terminals:
        pqueue.push(distancias[start][t], (start, t))

    steiner = Graph()

    while pqueue:
        _, (source, target) = pqueue.pop()
        if target not in distancias:
                dist, prev = shortest_path(graph, target)
                distancias[target] = dist
                previous[target] = prev
                for tr in terminals:
                    pqueue.push(distancias[target][tr], (target, tr))

        t = target
        if not steiner.has_node(target):
            while distancias[source][t]:
                # u = previous[source][t]
                edge = previous[source][t]
                u = edge.adj(t)
                steiner.add_edge(edge)
                t = u
                if u not in distancias:
                    dist, prev = shortest_path(graph, u)
                    distancias[u] = dist
                    previous[u] = prev
                    for tr in terminals:
                        pqueue.push(distancias[u][tr], (u, tr))

    steiner, cost = pruning_prim_minimum_spanning_tree(steiner, start, terminals)

    return steiner, cost


def shortest_path_with_origin(graph, start, terminals):
    '''
    Shortest Path with Origin Heuristic implementation
    '''

    dist, prev = shortest_path(graph,start)
    cost = 0
    tree = Graph()
    for u in terminals:
        while dist[u] :
            # v = prev[u]
            edge = prev[u]
            if not tree.has_edge(edge):
                tree.add_edge(edge)
                cost += edge.weight
            else:
                break
            # u = v
            u = edge.adj(u)

    return tree, cost


def shortest_path_origin_prim(graph : Graph, start, terminals):
    '''
    Shortest path heuristic with pruning a Prim MST tree.
    '''

    dist, prev = shortest_path(graph, start)
    subgraph = Graph()
    for t in terminals:
        u = t
        while dist[u]:
            edge = prev[u]
            if not subgraph.has_edge(edge):
                subgraph.add_edge(edge)
            u = edge.adj(u)

    tree, cost = pruning_prim_minimum_spanning_tree(subgraph, start, terminals)

    return tree, cost

def pruning_tree(tree: Graph, terminals : set):

    fifo = deque([v
                  for v in tree.nodes()
                  if (tree.degree(v) == 1) and (v not in terminals)])

    while fifo:
        v = fifo.popleft()
        for w in tree.adjacents(v):
            if (w not in terminals) and (tree.degree(w) == 2):
                fifo.append(w)
        tree.remove_node(v)

    return tree


def pruning_prim_minimum_spanning_tree(graph, start, terminals):
    '''
    Parameters:
        graph : Graph
            Base graph to compute the Steiner tree
        start : Node
            Where is to start Prim's algorithm
        terminals : Set
            Terminals Nodes from the STPG instance

    Return:
        prunning : A Steiner Tree
        total : Numeric - total cost of the tree

    Notes:
        Determina a MST do grafo por meio do algoritmo de Prim.
        Realiza a poda considerando os nós terminais como os nós folhas até a raiz <start>
        Se <start> for um vértice não terminal, o laço <while> verifica se <start> é um vértice folha da árvore resultande.
        Em caso afirmativo realiza uma poda iterativa a partir desse vértice para garantir que a árvore resultante seja
        uma árvore de Steiner.
        Resulta sempre na mesma árvore para qualquer vértice <start> considerado.
    '''
    tree = prim_spanning_tree(graph, start)
    tree = pruning_tree(tree, terminals)
    cost = sum(e.weight for e in tree.edges())
    return tree, cost


def pruning_kruskal_minimum_spanning_tree(graph:Graph, terminals):
    """
    Parameters:
        graph : Graph
        terminals : list of nodes

    Return:
        child : Graph
            Steiner Tree
    """
    tree = kruskal_spanning_tree(graph)
    tree = pruning_tree(tree, terminals)
    cost = sum(e.weight for e in tree.edges())
    return tree, cost

def pruning_boruvka_minimum_spanning_tree(graph: Graph, terminals):

    tree = boruvka_spanning_tree(graph)
    tree = pruning_tree(tree, terminals)
    cost = sum(e.weight for e in tree.edges())
    return tree, cost