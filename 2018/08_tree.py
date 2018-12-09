import aoc_utils
from pprint import pprint
from functools import reduce

class Node:
    def __init__(self, name, n_child, n_meta):
        self.name = name
        self.n_child = n_child
        self.n_meta = n_meta
        self.children = []
        self.meta = []


    def child_sum(self, value_dict):
        if self.n_child == 0:
            return sum(self.meta)
        else:
            meta_children = []
            for m in self.meta:
                if m > 0 and m <= len(self.children):
                    meta_children.append(self.children[m-1].name)

            if all(map(lambda x: x in value_dict, meta_children)):
                return sum(map(lambda x: value_dict[x], meta_children))

            return None

    def __repr__(self):
        return '%s [%s,%s] (%s,%s)' % (self.name, self.n_child, self.n_meta, len(self.children), len(self.meta))

count = 0
def id():
    global count
    count += 1
    return count


def print_state(tape, queue, nodes):
    print('\ntape: ', tape)
    print('queue: ', ' || '.join(map(str, queue)))
    print('nodes: ', ', '.join(map(str, nodes)))

def part1(lines):
    tape = list(map(int, lines[0].split(' ')))
    queue = []
    nodes = []
    while len(tape) > 0:
        if len(queue) == 0:
            n = Node(id(), tape[0], tape[1])
            queue.append(n)
            tape = tape[2:]
        else:
            curr = queue.pop()
            if len(curr.children) < curr.n_child:
                c = Node(id(), tape[0], tape[1])
                curr.children.append(c)
                queue.append(curr)
                queue.append(c)
                tape = tape[2:]
            elif len(curr.meta) < curr.n_meta:
                curr.meta = tape[:curr.n_meta]
                tape = tape[curr.n_meta:]
                nodes.append(curr)
            else:
                nodes.append(curr)

    p1_ans = sum(reduce(lambda x,y: x + y, map(lambda x: x.meta, nodes)))
    return p1_ans, nodes


def part2(lines):
    global count
    count = 0
    p1, nodes = part1(lines)
    node_dict = {}
    for n in nodes:
        node_dict[n.name] = n
    to_process = set(list(range(1,len(nodes) + 1)))
    values = {}

    while len(to_process) > 0:
        for id in to_process:
            child_sum = node_dict[id].child_sum(values)
            if child_sum is not None:
                values[id] = child_sum
        to_process = to_process.difference(set(values.keys()))
            
    return values[1], values


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines)[0])
    pprint(part2(lines)[0])


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
