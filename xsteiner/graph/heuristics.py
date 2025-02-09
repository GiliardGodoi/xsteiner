from collections import defaultdict, deque
from xsteiner.graph.graph import Graph
from xsteiner.graph.trees import prim_spanning_tree, kruskal_spanning_tree
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

    subtree = Graph()

    while pqueue:
        _, (source, target) = pqueue.pop()
        if target not in distancias:
                dist, prev = shortest_path(graph, target)
                distancias[target] = dist
                previous[target] = prev
                for tr in terminals:
                    pqueue.push(distancias[target][tr], (target, tr))

        t = target
        if not subtree.has_node(target):
            while distancias[source][t]:
                u = previous[source][t]
                w = graph[u][t] # obter o peso a partir das arestas do grafo
                subtree.add_edge(t,u,weight=w) # inserir uma nova aresta sem instanciar um novo objeto
                t = u

                if u not in distancias:
                    dist, prev = shortest_path(graph,u)
                    distancias[u] = dist
                    previous[u] = prev
                    for tr in terminals:
                        pqueue.push(distancias[u][tr], (u, tr))

    tree, cost = pruning_minimum_spanning_tree(subtree, start, terminals)

    return tree, cost


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


def shortest_path_origin_prim(graph, start, terminals):
    '''
    Determinar a árvore de caminhos mínimos <T> dos vértices terminais até o nó <start>
    Define um subgrafo formado pelos vértices presentes em T
    com as correspondentes arestas do grafo G <graph>.
    Calcula a MST do subgrafo considerado e realiza a poda da MST.
    '''

    dist, prev = shortest_path(graph, start)

    selectedNodes = set([start])

    for t in terminals:
        selectedNodes.add(t)
        u = t
        while dist[u]:
            v = prev[u]
            selectedNodes.add(v)
            u = v

    subgraph = Graph()

    for v in selectedNodes:
        for u in graph.adjacent_to(v):
            if (u in selectedNodes):
                w = graph.edges[v][u]
                subgraph.add_edge(v, u, weight=w)

    tree, cost = pruning_minimum_spanning_tree(subgraph, start, terminals)

    return tree, cost


def pruning_minimum_spanning_tree(graph, start, terminals):
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
    dict_tree, _ = prim_spanning_tree(graph, start)

    pruned = Graph()

    total = 0

    for terminal in terminals:
        current = terminal
        while current != start:
            previous = dict_tree[current]
            if pruned.has_edge(current, previous):
                current = start
            else :
                weight = graph.weight(current, previous)
                pruned.add_edge(current, previous, weight=weight)
                total += weight
                current = previous

    current = start
    while (current not in terminals) and (pruned.degree(current) == 1):
        previous = list(pruned.adjacent_to(current)).pop()
        total -= pruned.weight(current, previous)
        pruned.remove_node(current)
        current = previous

    return pruned, total


def pruning_kruskal_minimum_spanning_tree(graph : Graph, terminals):
    """
    Parameters:
        graph : Graph
        terminals : list of nodes

    Return:
        child : Graph
            Steiner Tree
    """
    child = kruskal_spanning_tree(graph)

    fifo = deque([v for v in child.vertices if (v not in terminals) and (child.degree(v) == 1)])

    while fifo:
        v = fifo.pop()
        for w in child.adjacent_to(v):
            if (w not in terminals) and (child.degree(w) == 2): # or child.degree(w) - 1 == 1 #
                fifo.appendleft(w)

        child.remove_node(v)

    return child