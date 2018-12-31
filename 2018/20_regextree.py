# Unfortunately this approach did not work out.  In summary:
#
# 1.  Compress the input to atoms by repeatedly substituting simple groups (those without parentheses inside of them) with
#     a reserved token + count.
# 2.  Create compressed nodes of all remaining simple characters (NESW)
#
#  Example:
#  (string)                (substitution dictionary)
#  NESW(E|W(NN|S)W)E(W|E)  { }
#  NESW(E|WZ1W)EZ2         {'Z1': 'NN|S', 'Z2': 'W|E'}
#  NESWZ3EZ2               {'Z1': 'NN|S', 'Z2': 'W|E', 'Z3': 'E|WZ1W'}
#  Z4Z3Z5Z2                {'Z1': 'NN|S', 'Z2': 'W|E', 'Z3': 'E|WZ1W', 'Z4': 'NESW', 'Z5': 'E'}
#
# 4. Create serial nodes from the compressed string
#
#  ^ -> Z4 -> Z3 -> Z5 -> Z2 -> $
#
# 5.  Expand nodes until they have no more reserved tokens.  '|' creates parallel nodes; everything else is serial
# 6.  BFS the tree, walking the character strings, and updating the 2D point and creating a 2D graph
# 7.  Use networkx and profit.
# 8.  But it never finishes building 2D :(

from pprint import pprint
import aoc_utils
import networkx as nx
import re

group_rx = re.compile('\\([NESWZ0-9|]+\\)')
plain_rx = re.compile('[NEWS]+')
lookup_rx = re.compile('Z\\d+')
id = 0
START, END = '^', '$'


def add_parent_child(parent, child):
    parent.add_child(child)
    child.add_parent(parent)


class Node:
    def __init__(self, raw):
        self.raw = raw
        self.id = get_id()
        self.parents = []
        self.children = []

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def add_child(self, other):
        self.children.append(other)

    def add_parent(self, other):
        self.parents.append(other)

    def remove_child(self, other):
        self.children = list(filter(lambda x: x.id != other.id, self.children))

    def remove_parent(self, other):
        self.parents = list(filter(lambda x: x.id != other.id, self.parents))

    def expand(self, lookup):
        if len(self.raw) == 0 or plain_rx.fullmatch(self.raw):
            # regular node, no need to expand
            pass
        elif '|' in self.raw:
            groups = self.raw.split('|')
            new_nodes = [Node(g) for g in groups]

            for n in new_nodes:
                for p in self.parents:
                    add_parent_child(p, n)
                for c in self.children:
                    add_parent_child(n, c)
                n.expand(lookup)
            self.delete()
        else:
            chunks = chunk_by_regex(lookup_rx, self.raw, lookup)
            new_nodes = [Node(chunk) for chunk in chunks]
            for i in range(1, len(new_nodes)):
                add_parent_child(new_nodes[i - 1], new_nodes[i])
            for p in self.parents:
                add_parent_child(p, new_nodes[0])
            for c in self.children:
                add_parent_child(new_nodes[-1], c)
            [n.expand(lookup) for n in new_nodes]
            self.delete()

    def delete(self):
        [p.remove_child(self) for p in self.parents]
        [c.remove_parent(self) for c in self.children]

    def fill_graph(self, point, graph):
        q = []
        for c in self.children:
            prev = Point(point.x, point.y)
            for char in c.raw:
                next_point = prev + COMPASS[char]
                graph.add_node(next_point)
                graph.add_edge(prev, next_point)
                prev = next_point
            q.append((c, next_point))
        return q

    def __repr__(self):
        return '%d: (%s) Children: %d, Parents: %d' % (self.id, self.raw, len(self.children), len(self.parents))


def get_id():
    global id
    id += 1
    return id


def parse_puzz(puzz):
    s = puzz
    subs = {}
    while '(' in s:
        s = compact_by_regex(s, subs, group_rx, 1)
    s = compact_by_regex(s, subs, plain_rx)

    return s, subs


def chunk_by_regex(regex, s, lookup):
    last = 0
    chunks = []
    groups = list(regex.finditer(s))
    for g in groups:
        chunks.append(s[last:g.start(0)])
        chunks.append(lookup[s[g.start(0):g.end(0)]])
        last = g.end(0)
    chunks.append(s[groups[-1].end(0):])
    return list(filter(lambda x: len(x) > 0, chunks))


def compact_by_regex(s, subs, regex, trim_key=0):
    last = 0
    sout = ''
    groups = list(regex.finditer(s))
    if len(groups) > 0:
        for g in groups:
            sout += s[last:g.start(0)]
            key = 'Z%d' % get_id()
            sout += key
            subs[key] = s[(g.start(0) + trim_key):(g.end(0) - trim_key)]
            last = g.end(0)
        sout += s[last:]
    else:
        sout = s
    return sout


def build_tree(compacted, lookup):
    start = Node(START)
    end = Node(END)
    middle = Node(compacted)
    add_parent_child(start, middle)
    add_parent_child(middle, end)
    middle.expand(lookup)
    return start, end


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '%d,%d' % (self.x, self.y)


ORIGIN = Point(0, 0)
COMPASS = {'N': Point(0, 1), 'S': Point(0, -1), 'E': Point(1, 0), 'W': Point(-1, 0), '$': Point(0, 0)}


def shortest_paths(lines):
    parsed, lookup = parse_puzz(lines[0][1:-1])
    print('len(input) = ', len(lines[0][1:-1]))
    print('len(parsed) = ', len(parsed))
    tree, end = build_tree(parsed, lookup)

    print('filling map graph')
    map_graph = nx.DiGraph()
    map_graph.add_node(ORIGIN)

    q = [(tree, ORIGIN)]
    while len(q) > 0:
        next_q = []
        for node, pt in q:
            next_q += node.fill_graph(pt, map_graph)
        q = next_q

    return list(nx.shortest_path(map_graph, ORIGIN).values())


def part1(lines):
    paths = shortest_paths(lines)
    return max(map(lambda x: len(x), paths)) - 1


def part2(lines):
    pass


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
