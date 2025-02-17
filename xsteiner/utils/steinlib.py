
import re
import requests
import os
from pathlib import Path
from xsteiner.graph.edge import Edge
from xsteiner.graph.graph import SteinerGraphProblemInstance

BASE_URL = f'https://steinlib.zib.de/download/'

# If the number in the Opt column is written in italics
# the optimum is not known.
# The number given is the best know upper bound.
# See more at <http://steinlib.zib.de/showset.php?PUC>

PUC = [
    ("bip42p.stp", 24657),
    ("bip42u.stp", 236),
    ("bip52p.stp", 24526),
    ("bip52u.stp", 234),
    ("bip62p.stp", 22843),
    ("bip62u.stp", 219),
    ("bipa2p.stp", 35326),
    ("bipa2u.stp", 338),
    ("bipe2p.stp", 5616),
    ("bipe2u.stp", 54),
    ("cc10-2p.stp", 35297),
    ("cc10-2u.stp", 342),
    ("cc11-2p.stp", 63491),
    ("cc11-2u.stp", 612),
    ("cc12-2p.stp", 121106),
    ("cc12-2u.stp", 1172),
    ("cc3-10p.stp", 12772),
    ("cc3-10u.stp", 125),
    ("cc3-11p.stp", 15582),
    ("cc3-11u.stp", 153),
    ("cc3-12p.stp", 18826),
    ("cc3-12u.stp", 185),
    ("cc3-4p.stp", 2338),
    ("cc3-4u.stp", 23),
    ("cc3-5p.stp", 3661),
    ("cc3-5u.stp", 36),
    ("cc5-3p.stp", 7299),
    ("cc5-3u.stp", 71),
    ("cc6-2p.stp", 3271),
    ("cc6-2u.stp", 32),
    ("cc6-3p.stp", 20270),
    ("cc6-3u.stp", 197),
    ("cc7-3p.stp", 56799),
    ("cc7-3u.stp", 549),
    ("cc9-2p.stp", 17199),
    ("cc9-2u.stp", 167),
    ("hc10p.stp", 59797),
    ("hc10u.stp", 575),
    ("hc11p.stp", 119492),
    ("hc11u.stp", 1145),
    ("hc12p.stp", 236949),
    ("hc12u.stp", 2262),
    ("hc6p.stp", 4003),
    ("hc6u.stp", 39),
    ("hc7p.stp", 7905),
    ("hc7u.stp", 77),
    ("hc8p.stp", 15322),
    ("hc8u.stp", 148),
    ("hc9p.stp", 30242),
    ("hc9u.stp", 292)
]

FILES = [
    "B.tgz",
    "C.tgz",
    "D.tgz",
    "E.tgz",
    "MC.tgz",
    "X.tgz",
    "SP.tgz",
    "PUC.tgz",
    "I080.tgz",
    "I160.tgz",
    "I320.tgz",
    "I640.tgz",
    "1R.tgz",
    "2R.tgz",
    "P4E.tgz",
    "P4Z.tgz",
    "P6E.tgz",
    "P6Z.tgz",
    "ALUE.tgz",
    "ALUT.tgz",
    "DIW.tgz",
    "DMXA.tgz",
    "GAP.tgz",
    "MSM.tgz",
    "TAQ.tgz",
    "LIN.tgz",
    "ES10FST.tgz",
    "ES20FST.tgz",
    "ES30FST.tgz",
    "ES40FST.tgz",
    "ES50FST.tgz",
    "ES60FST.tgz",
    "ES70FST.tgz",
    "ES80FST.tgz",
    "ES90FST.tgz",
    "ES100FST.tgz",
    "ES250FST.tgz",
    "ES500FST.tgz",
    "ES1000FST.tgz",
    "ES10000FST.tgz",
    "TSPFST.tgz",
    "GENE.tgz",
    "WRP3.tgz",
    "WRP4.tgz",
    "relay-large-1.7z",
    "relay-large-2.7z",
    "relay-large-3.7z",
    "relay-medium.7z",
    "relay-small.7z",
    "Relay-Complete.tar.bz2",
    "SteinLibEFST.zip"
]


def steinlib_parser(filepath):

    if not os.path.exists(filepath):
        raise FileNotFoundError(f'File not found: {filepath}')

    def _parser_section_comment(file, graph:SteinerGraphProblemInstance):
        for line in file:
            _list = re.findall(r'"(.*?)"',line)
            if "Name" in line :
                _name = _list[0] if len(_list) else "Name unviable"
                graph.name = _name

            elif "Creator" in line :
                _creator = _list[0] if len(_list) else "Creator unviable"
                graph.creator = _creator

            elif "Remark" in line :
                remark = _list[0] if len(_list) else "Creator unviable"
                graph.remark = remark

            elif "end" in line.lower():
                break
        return graph

    def _parser_section_graph(file, graph:SteinerGraphProblemInstance):
        for line in file:
            if line.startswith("E ") :
                entries = re.findall(r'(\d+)', line)
                vetor = [ e for e in entries if e.isdecimal() ]

                assert len(vetor) == 3, "The line must to have three values"
                v, u, peso = vetor
                v, u, peso = int(v), int(u), int(peso)
                edge = Edge(v, u, weight=peso)
                graph.add_edge(edge)

            elif line.startswith("Nodes"):
                nodes = re.findall(r'Nodes (\d+)$', line)
                graph.nro_nodes = int(nodes[0]) if len(nodes) else -1

            elif line.startswith("Edges"):
                edges = re.findall(r'Edges (\d+)$', line)
                graph.nro_edges = int(edges[0]) if len(edges) else -1
            elif "end" in line.lower() :
                break
        return graph

    def _parser_section_terminals(file, graph:SteinerGraphProblemInstance):
        pattern = re.compile(r'T\s+\b(\d+)\b')
        terminals = set()
        for line in file:
            if line.startswith("T "):
                group = pattern.search(line)
                if group is None:
                    raise RuntimeError(f'Line does not match with pattern: {line}')
                value = group.group(1)
                value = int(value) if value.isdecimal() else value
                terminals.add(value)
            elif line.startswith("Terminals"):
                group = re.search(r'Terminals\s+\b(\d+)\b', line)
                if group is None:
                    raise RuntimeError(f'Line does not match with pattern: {line}')
                value = group.group(1)
                value = int(value)
                graph.nro_terminals = value
            elif "end" in line.lower():
                break
        graph.update_terminals(terminals)
        return graph

    steiner = SteinerGraphProblemInstance()
    steiner.file_name = os.path.basename(filepath)
    with open(filepath, 'r') as file :
        for line in file :
            if re.search(r'section\s+comment', line, re.I):
                steiner = _parser_section_comment(file, steiner)

            elif re.search(r'section\s+graph', line, re.I):
                steiner = _parser_section_graph(file, steiner)

            elif re.search(r'section\s+terminals', line, re.I):
                steiner = _parser_section_terminals(file, steiner)
            elif re.search(r'EOF', line, re.I):
                break

    return steiner


if __name__ == "__main__":
    ...