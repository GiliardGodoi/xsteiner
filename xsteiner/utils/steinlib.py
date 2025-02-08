import argparse
import re
import requests
import os

from xsteiner.graph.graph import SteinerGraphProblemInstance

# If the number in the Opt column is written in italics
# the optimum is not known.
# The number given is the best know upper bound.
# See more at <http://steinlib.zib.de/showset.php?PUC>

PUC = [
    ("bip42p", 24657),
    ("bip42u", 236),
    ("bip52p", 24526),
    ("bip52u", 234),
    ("bip62p", 22843),
    ("bip62u", 219),
    ("bipa2p", 35326),
    ("bipa2u", 338),
    ("bipe2p", 5616),
    ("bipe2u", 54),
    ("cc10-2p", 35297),
    ("cc10-2u", 342),
    ("cc11-2p", 63491),
    ("cc11-2u", 612),
    ("cc12-2p", 121106),
    ("cc12-2u", 1172),
    ("cc3-10p", 12772),
    ("cc3-10u", 125),
    ("cc3-11p", 15582),
    ("cc3-11u", 153),
    ("cc3-12p", 18826),
    ("cc3-12u", 185),
    ("cc3-4p", 2338),
    ("cc3-4u", 23),
    ("cc3-5p", 3661),
    ("cc3-5u", 36),
    ("cc5-3p", 7299),
    ("cc5-3u", 71),
    ("cc6-2p", 3271),
    ("cc6-2u", 32),
    ("cc6-3p", 20270),
    ("cc6-3u", 197),
    ("cc7-3p", 56799),
    ("cc7-3u", 549),
    ("cc9-2p", 17199),
    ("cc9-2u", 167),
    ("hc10p", 59797),
    ("hc10u", 575),
    ("hc11p", 119492),
    ("hc11u", 1145),
    ("hc12p", 236949),
    ("hc12u", 2262),
    ("hc6p", 4003),
    ("hc6u", 39),
    ("hc7p", 7905),
    ("hc7u", 77),
    ("hc8p", 15322),
    ("hc8u", 148),
    ("hc9p", 30242),
    ("hc9u", 292)
]

'''
    This class parses the Steiner Tree Problem instance's file and fill the Steiner Tree Problem class above.

    Based on Bruna Osti's propose
    from: <https://github.com/brunaostii/Steiner_Tree>
'''

def steinlib_parser(filepath):

    if not os.path.exists(filepath):
        raise FileExistsError(f'File not found: {filepath}')

    def _parser_section_comment(self,file):
        for line in file:
            _list = re.findall(r'"(.*?)"',line)
            if "Name" in line :
                _name = _list[0] if len(_list) else "Name unviable"
                self.STP.name = _name

            elif "Creator" in line :
                _creator = _list[0] if len(_list) else "Creator unviable"
                self.STP.creator = _creator

            elif "Remark" in line :
                remark = _list[0] if len(_list) else "Creator unviable"
                steiner_graph.remark = remark

            elif "END" in line:
                break

    def _parser_section_graph(self, file):
        for line in file:
            if line.startswith("E ") :
                entries = re.findall(r'(\d+)', line)
                vetor = [ e for e in entries if e.isdecimal() ]

                assert len(vetor) == 3, "The line must to have three values"
                v, w, peso = vetor

                v = int(v)
                w = int(w)
                peso = int(peso)

                self.STP.graph.add_edge(v,w, weight=peso)

            elif line.startswith("Nodes"):
                nodes = re.findall(r'Nodes (\d+)$', line)
                self.STP.nro_nodes = int(nodes[0]) if len(nodes) else -1

            elif line.startswith("Edges"):
                edges = re.findall(r'Edges (\d+)$', line)
                self.STP.nro_edges = int(edges[0]) if len(edges) else -1

            elif "END" in line :
                break

    def _parser_section_terminals(self,file):

        for line in file:
            if line.startswith("T "):
                _string = re.findall(r"(\d+)$", line)
                v_terminal = int(_string[0]) if len(_string) == 1 else -1
                self.STP.terminals.add(v_terminal)

            elif line.startswith("Terminals"):
                terminal = re.findall(r'Terminals (\d+)$', line)
                self.STP.nro_terminals = int(terminal[0]) if len(terminal) else -1

            elif "END" in line:
                break

    steiner_graph = SteinerGraphProblemInstance()

    steiner_graph.file_name = os.path.basename(filepath)

    with open(filepath, 'r') as file :
        for line in file :
            if "SECTION Comment" in line :
                _parser_section_comment(file)

            elif "SECTION Graph" in line :
                _parser_section_graph(file)

            elif "SECTION Terminals" in line :
                _parser_section_terminals(file)

    return steiner_graph
