import networkx as nx


def pruner(T: nx.Graph, terminals):
    '''
    Prunes all leaves nodes that are not terminals.
    '''
    leaves = set(v for v in T.nodes if T.degree(v) == 1)
    terminals = set(terminals)
    no_terminal_leaves = leaves - terminals

    # assert all(T.degree(v) == 1 for v in no_terminal_leaves)
    # assert all(v not in terminals for v in no_terminal_leaves)

    while no_terminal_leaves:
        v_star = no_terminal_leaves.pop()
        adjacents = list(T.adj[v_star])
        T.remove_node(v_star)
        for u in adjacents:
            if T.degree(u) == 1 and u not in terminals:
                no_terminal_leaves.add(u)

    return T
