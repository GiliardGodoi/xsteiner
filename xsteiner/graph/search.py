from collections import deque
from xsteiner.graph.graph import Graph
from xsteiner.pqueue.pqueue import PriorityQueue

def breadth_first_search(graph : Graph, start):
    '''Breadth First Search

    Parameters
        graph : GraphDictonary
        start : a graph's vertice

    Returns
        Generator that yields (visiting node, parent node)

    Raises
        ValueError
    '''
    if start is None:
        raise ValueError("Start node cannot be None")
    elif not graph.has_node(start):
        raise ValueError("Start node is not in graph: {start!s}")


    visisted = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        visisted.add(node)
        for adj in graph.adjacents(node):
            if not adj in visisted:
                queue.append(adj)
                yield (adj, node)


def depth_first_search(graph: Graph, start):
    '''Deep First Search

    Parameters
        graph : GraphDictionary

                start : graph's vertice

    Returns
        Generator that yields (visited node, parent node)

    Raises:
        TypeError
        ValueError
    '''
    if start is None:
        raise ValueError("Start node cannot be None")
    elif not isinstance(graph, Graph):
        raise ValueError("Graph should be a steiner.graph.graph.Graph instance")
    elif not graph.has_node(start):
        raise ValueError("Start node is not in graph: {start!s}")

    visisted = set()
    stack = deque([start])

    while stack:
        prev = stack.pop()
        visisted.add(prev)
        for adj in graph.adjacents(prev):
            if not adj in visisted:
                stack.append(adj)
                yield adj, prev


def shortest_edge_search(graph:Graph, start):

    if not graph.has_node(start):
        raise ValueError(f'Source node is not in graph: {start}')

    visited = set()
    queue = PriorityQueue()
    queue.push(0, (start, None))

    while queue:
        _, (node, prev) = queue.pop()
        if node in visited:
            continue
        visited.add(node)
        for edge in graph.adjacents_edges(node):
            adj = edge.adj(node)
            if adj not in visited:
                weight = edge.weight
                queue.push(weight, (adj, node))
        if prev is not None:
            yield node, prev