import networkx as nx

def parse_line(line):
    parts = line.strip('\n').split(' <-> ')
    return parts[0], parts[1].split(', ')


def main(edges):
    G = nx.Graph()
    for n, es in edges:
        G.add_node(n)
        for e in es:
            G.add_node(e)
            G.add_edge(n,e)
    ccs = list(nx.connected_components(G))
    zero_group = list(filter(lambda x: '0' in x, ccs))[0]
    return len(zero_group), len(ccs)


def run_file(filename):
    with open(filename) as f:
        edges = [parse_line(line) for line in f.readlines()]
        rez = main(edges)
        print('%s\n%s\n%d, %d\n' % (filename, '-'*len(filename), rez[0], rez[1]))


if __name__ == '__main__':
    run_file('data/12_test.txt')
    run_file('data/12.txt')
