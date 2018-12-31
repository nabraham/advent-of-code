import aoc_utils
import networkx as nx
from pprint import pprint
from collections import defaultdict


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '<%d, %d>' % (self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


COMPASS = {'N': Point(0, 1), 'S': Point(0, -1), 'E': Point(1, 0), 'W': Point(-1, 0)}


def find_shortest_paths(lines):
    heads = {Point(0, 0)}
    currs = {Point(0, 0)}
    tails = set()
    edges = defaultdict(list)
    stack = []
    G = nx.DiGraph()
    G.add_node(Point(0, 0))
    for c in lines[0][1:-1]:
        if c in 'NEWS':
            next_currs = set()
            for pt in currs:
                other = pt + COMPASS[c]
                G.add_node(other)
                G.add_edge(pt, other)
                edges[pt].append(other)
                next_currs.add(other)
            currs = next_currs
        elif c == '(':
            stack.append((heads, tails))
            heads = {c for c in currs}
            tails = set()
        elif c == '|':
            [tails.add(c) for c in currs]
            currs = heads
        elif c == ')':
            currs = {t for t in tails}
            heads, tails = stack.pop()

    return nx.shortest_path(G, Point(0, 0)).values()


def part1(lines):
    paths = find_shortest_paths(lines)
    mx = max(map(lambda x: (len(x), x), paths), key=lambda x: x[0])
    return mx[0] - 1


def part2(lines):
    paths = find_shortest_paths(lines)
    return len(list(filter(lambda x: len(x) > 1000, paths)))


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
