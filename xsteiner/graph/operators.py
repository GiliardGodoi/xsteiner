from collections import deque
from xsteiner.graph.graph import Graph


def union(red:Graph, blue:Graph):
    """
    Creates a union of two graphs.
    Args:
        red (Graph): The first graph.
        blue (Graph): The second graph.
    Returns:
        Graph: A new graph containing all edges from both input graphs.
    """

    subgraph = Graph()
    for edge in red.edges():
        subgraph.add_edge(edge)
    for edge in blue.edges():
        if not subgraph.has_edge(edge):
            subgraph.add_edge(edge)

    return subgraph

def induced_subgraph(subset: Graph, base: Graph):
    """
    Generate an induced subgraph from a subset of nodes.
    Considering the graphs subset(V_1, E_1) and base(V_2, E_2).
    The operation takes the vertices set V_1 from subset and the edges set E_2 from base.
    It includes an edge e(u, v) from E_2 if the adjcent nodes v and u are in V_1.
    Args:
        subset (Graph): A graph containing the subset of nodes.
        base (Graph): The base graph from which the subgraph is induced.
    Returns:
        Graph: The induced subgraph containing only the nodes from the subset.
    """
    subgraph = Graph()
    for v in subset.nodes():
        subgraph.add_node(v)
    for edge in base.edges():
        if subgraph.has_node(edge.x) and subgraph.has_node(edge.y):
            subgraph.add_edge(edge)

    return subgraph

def is_subset(sub:Graph, super:Graph):
    """
    Check if one graph is a subset of another graph.
    Args:
        sub (Graph): The graph to check as a subset.
        super (Graph): The graph to check as a superset.
    Returns:
        bool: True if `sub` is a subset of `super`, False otherwise.
    """
    set(sub.nodes()).issubset(super.nodes()) \
        and set(sub.edges()).issubset(super.edges())

def pruning_tree(tree: Graph, terminals : set):
    """
    Prunes a tree by removing non-terminal leaf nodes and their adjacent nodes
    with degree 2 until no more such nodes exist.
    Args:
        tree (Graph): The input tree to be pruned.
        terminals (set): A set of terminal nodes that should not be pruned.
    Returns:
        Graph: The pruned tree.
    """
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