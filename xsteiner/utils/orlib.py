import argparse
import re
import requests
import os

from xsteiner.graph.edge import Edge
from xsteiner.graph.graph import SteinerGraphProblemInstance

problems_class = {
        'b' : {'min' : 1, 'max' : 18},
        'c' : {'min' : 1, 'max' : 20},
        'd' : {'min' : 1, 'max' : 20},
        'e' : {'min' : 1, 'max' : 20},
        'others' : ['dv80.txt', 'dv160.txt', 'dv320.txt' ]
    }

STEIN_B = [
    ("steinb1.txt",   82),  # 0
    ("steinb2.txt",   83),
    ("steinb3.txt",  138),
    ("steinb4.txt",   59),
    ("steinb5.txt",   61),  # 4
    ("steinb6.txt",  122),
    ("steinb7.txt",  111),
    ("steinb8.txt",  104),
    ("steinb9.txt",  220),  # 8
    ("steinb10.txt",  86),
    ("steinb11.txt",  88),
    ("steinb12.txt", 174),
    ("steinb13.txt", 165),  # 12
    ("steinb14.txt", 235),
    ("steinb15.txt", 318),  # 14
    ("steinb16.txt", 127),  # 15
    ("steinb17.txt", 131),  # 16
    ("steinb18.txt", 218),  # 17
]

STEIN_C = [
    ("steinc1.txt", 85),
    ("steinc2.txt", 144),
    ("steinc3.txt", 754),
    ("steinc4.txt", 1079),
    ("steinc5.txt", 1579),
    ("steinc6.txt", 55),
    ("steinc7.txt", 102),
    ("steinc8.txt", 509),
    ("steinc9.txt", 707),
    ("steinc10.txt", 1093),
    ("steinc11.txt", 32),
    ("steinc12.txt", 46),
    ("steinc13.txt", 258),
    ("steinc14.txt", 323),
    ("steinc15.txt", 556),
    ("steinc16.txt", 11),
    ("steinc17.txt", 18),
    ("steinc18.txt", 113),
    ("steinc19.txt", 146),
    ("steinc20.txt", 267),
]

STEIN_D = [
    ("steind1.txt", 106),
    ("steind2.txt", 220),
    ("steind3.txt", 1565),
    ("steind4.txt", 1935),
    ("steind5.txt", 3250),
    ("steind6.txt", 67),
    ("steind7.txt", 103),
    ("steind8.txt", 1072),
    ("steind9.txt", 1448),
    ("steind10.txt", 2110),
    ("steind11.txt", 29),
    ("steind12.txt", 42),
    ("steind13.txt", 500),
    ("steind14.txt", 667),
    ("steind15.txt", 1116),
    ("steind16.txt", 13),
    ("steind17.txt", 23),
    ("steind18.txt", 223),
    ("steind19.txt", 310),
    ("steind20.txt", 537),
]


STEIN_E = [
    ("steine1.txt", 111),
    ("steine2.txt", 214),
    ("steine3.txt", 4013),
    ("steine4.txt", 5101),
    ("steine5.txt", 8128),
    ("steine6.txt", 73),
    ("steine7.txt", 145),
    ("steine8.txt", 2640),
    ("steine9.txt", 3604),
    ("steine10.txt", 5600),
    ("steine11.txt", 34),
    ("steine12.txt", 67),
    ("steine13.txt", 1280),
    ("steine14.txt", 1732),
    ("steine15.txt", 2784),
    ("steine16.txt", 15),
    ("steine17.txt", 25),
    ("steine18.txt", 564),
    ("steine19.txt", 758),
    ("steine20.txt", 1342),
]

def download(file_name):
    url = f'http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/{file_name}'
    response = requests.get(url)
    data = response.content
    return data

def save(content, file_name, folder):
    local = os.path.join(folder, file_name)
    with open(local, "wb") as file:
        file.write(content)
    return True

def generate_all_filenames(key = None):
    key = key.lower()
    if isinstance(problems_class[key], list) :
        for item in problems_class[key]:
            yield item
    elif isinstance(problems_class[key], dict) :
        counter = 1
        MAX = problems_class[key]['max']
        while counter <= MAX :
            yield f"stein{key}{counter}.txt"
            counter += 1

def orlib_parser(filepath):

    if not os.path.exists(filepath):
        raise FileExistsError(f'File not found: {filepath}')

    steiner_graph = SteinerGraphProblemInstance()
    steiner_graph.file_name = os.path.basename(filepath)

    if steiner_graph.file_name.startswith("stein"):
        # "An SST-based algorithm for the Steiner problem in graphs" Networks 19 (1989) 1-16.
        steiner_graph.name = steiner_graph.file_name.strip('steinx.').upper()
        steiner_graph.creator = "J. E. Beasley"
        steiner_graph.remark = "Sparse graph with random weights"
    elif steiner_graph.file_name.startswith("dv") :
        ## "Efficient path and vertex exchange in Steiner tree algorithms", Networks 29, 89-105 (1997)
        steiner_graph.name = steiner_graph.file_name.upper()
        steiner_graph.creator = "C. Duin and S. Voss"
        steiner_graph.remark = "Incidence weights problems"

    with open(filepath, 'r') as file:
        # number of vertices, number of edges
        line = file.readline()
        entries = [ int(e) for e in re.findall(r'(\d+)', line) if e.isdecimal()]
        assert len(entries) == 2, "First line isn't equal 2 numbers"

        steiner_graph.nro_nodes = entries[0]
        steiner_graph.nro_edges = entries[1]

        # for each edge: the end vertices and the cost of the edge
        counter = 1
        while counter <= steiner_graph.nro_edges:
            line = file.readline()
            entries = [ int(e) for e in re.findall(r'(\d+)', line) if e.isdecimal()]
            assert len(entries) == 3, f'Edge line has not 3 values. Line {counter}'
            u = entries[0]
            v = entries[1]
            weight = entries[2]
            edge = Edge(u, v, weight=weight)
            steiner_graph.add_edge(edge)
            counter += 1

        # number of vertices to be connected together
        line = file.readline()
        entry = [ int(e) for e in re.findall(r'(\d+)', line) if e.isdecimal()]
        assert len(entry) == 1, "Number of terminals have to be just one"
        steiner_graph.nro_terminals = entry[0]

        # the vertex numbers for the vertices that are to be connected together
        line = file.readline()

        # for some problems' instance, the terminals are represented in more than one line
        terminals = set()
        while line:
            entries = [ int(e) for e in re.findall(r'(\d+)', line) if e.isdecimal()]
            terminals.update(entries)
            line = file.readline()

    assert len(terminals) == entry[0], "Numer of terminals is not ok"
    steiner_graph.update_terminals(terminals)

    return steiner_graph


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Download dataset from ORLibrary")
    parser.add_argument('-d', '--datafolder', type=str, required=True, help="Folder to save or parse data")
    parser.add_argument('-b', '--basename', type=str, required=True, help="Base name of the file (b, c, d, e, others)")
    parser.add_argument('-n', '--number', type=int, help="Number of the file (only for types b, c, d, e)")
    args = parser.parse_args()

    INPUT_FOLDER = os.path.join(args.datafolder)

    if not os.path.exists(INPUT_FOLDER):
        os.mkdir(INPUT_FOLDER)

    if args.basename == 'others':
        for file_name in generate_all_filenames(args.basename):
            data = download(file_name)
            save(data, file_name, INPUT_FOLDER)
    elif args.basename in problems_class and args.number:
        file_name = f"stein{args.basename}{args.number}.txt"
        data = download(file_name)
        save(data, file_name, INPUT_FOLDER)

    elif args.basename in problems_class:
        for file_name in generate_all_filenames(args.basename):
            data = download(file_name)
            save(data, file_name, INPUT_FOLDER)
    else:
        print(f"Invalid basename: {args.basename}")


