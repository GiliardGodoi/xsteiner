import networkx as nx


def induced_mst(T: nx.Graph, G: nx.Graph):

    G_star = nx.subgraph(G, T.nodes)
    MST = nx.minimum_spanning_tree(G_star)

    return MST
