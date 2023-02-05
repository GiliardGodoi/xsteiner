import re
import networkx as nx
from pathlib import Path


def read(path_file: str):
    path_file = Path(path_file)
    if not path_file.suffix == ".stp":
        raise ValueError(
            f"Path should have an extension `.stp`; but was given:\n\t {path_file}"
        )

    # with open(path_file, 'r') as file:
    #    text = file.read()
    with path_file.open() as file:
        text = file.read_text()

    ptr_edges = re.compile(r"E (\d+) (\d+) (\d+)", re.M)
    ptr_terminals = re.compile(r"T (\d+)", re.M)

    ptr_n_nodes = re.compile(r"Nodes (\d+)", re.M)
    ptr_n_edges = re.compile("Edges (\d+)", re.M)
    ptr_n_terminals = re.compile(r"Terminals (\d+)", re.M)

    G = nx.Graph()
    G.graph["terminals"] = list()

    n_count_edges = 0
    n_count_terminals = 0

    for m in ptr_edges.finditer(text):
        if m is None:
            break
        else:
            v = int(m.group(1))
            u = int(m.group(2))
            w = int(m.group(3))
            G.add_edge(v, u, weight=w)
            n_count_edges += 1  # optional validation

    for m in ptr_terminals.finditer(text):
        if m is None:
            break
        else:
            t = int(m.group(1))
            G.graph["terminals"].append(t)
            n_count_terminals += 1  # optional validation

    n_nodes = ptr_n_nodes.search(text)
    n_edges = ptr_n_edges.search(text)
    n_terminals = ptr_n_terminals.search(text)

    n_nodes = int(n_nodes.group(1)) if type(n_nodes) == re.Match else 0
    n_edges = int(n_edges.group(1)) if type(n_edges) == re.Match else 0
    n_terminals = int(n_terminals.group(1)) if type(n_terminals) == re.Match else 0

    assert G.number_of_nodes() == n_nodes
    assert G.number_of_edges() == n_edges
    assert n_count_edges == n_edges
    assert len(G.graph["terminals"]) == n_terminals
    assert n_count_terminals == n_terminals

    return G
