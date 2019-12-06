import aoc_utils
import networkx as nx
from pprint import pprint


def build_graph(edge_list):
    nodes = set([])
    graph = dict()
    for e in edge_list:
        nodes.add(e[1])
        graph[e[1]] = e[0]
    return nodes, graph


def walk_graph(node, graph):
    count = 0
    visited = set([])
    while node is not None and node not in visited:
        visited.add(node)
        if node in graph:
            count += 1
        node = graph.get(node)
    return count


def part1(lines):
    edges = [line.split(')') for line in lines]
    nodes, graph = build_graph(edges)
    counts = [walk_graph(n, graph) for n in nodes]
    return sum(counts)


def part2(lines):
    edges = [line.split(')') for line in lines]
    G = nx.Graph()
    for n1, n2 in edges:
        G.add_node(n1)
        G.add_node(n2)
        G.add_edge(n1, n2)
    all_nodes = list(G)
    if 'YOU' in all_nodes and 'SAN' in all_nodes:
        return nx.shortest_path_length(G, 'YOU', 'SAN') - 2
    else:
        return -1


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
