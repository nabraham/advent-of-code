from collections import defaultdict

def parse_line(line):
    parts = line.strip('\n').split(' <-> ')
    return parts[0], parts[1].split(', ')


def walk(graph, start):
    queue = set([start])
    neighbors = set(queue)
    while len(queue) > 0:
        to_visit = set()
        for q in queue:
            for n in graph[q]:
                if n not in neighbors:
                    neighbors.add(n)
                    to_visit.add(n)
        queue = to_visit
    return neighbors


def create_graph(edges):
    graph = defaultdict(list)
    for k, v in edges:
        graph[k] = v
    return graph


def main(edges):
    graph = create_graph(edges)
    all_nodes = set([k for k,v in edges])
    groups = []
    while len(all_nodes) > 0:
        neighbors = walk(graph, list(all_nodes)[0])
        groups.append(neighbors)
        all_nodes = all_nodes.difference(neighbors)

    zero_group = list(filter(lambda x: '0' in x, groups))[0]
    return len(zero_group), len(groups)


def run_file(filename):
    with open(filename) as f:
        edges = [parse_line(line) for line in f.readlines()]
        rez = main(edges)
        print('%s\n%s\n0-length: %d\nAll-groups: %d\n' % (filename, '-'*len(filename), rez[0], rez[1]))


if __name__ == '__main__':
    run_file('data/12_test.txt')
    run_file('data/12.txt')
