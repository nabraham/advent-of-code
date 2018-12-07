import aoc_utils
import re
from collections import defaultdict, namedtuple
from pprint import pprint

step_rx = re.compile(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin')
Step = namedtuple('Step',['start', 'stop'])

def get_steps(lines):
    steps = []
    for line in lines:
        match = step_rx.match(line)
        steps.append(Step(match.group(1), match.group(2)))
    return steps


def get_first(queue, depends, walk):
    for q in queue:
        if len(depends[q]) == 0 or all(map(lambda x: x in walk, depends[q])):
            return q


def walk_graph(g, depends, queue):
    walk = []

    pprint(g)
    pprint(depends)

    while len(queue) > 0:
        first = get_first(queue, depends, walk)
        queue.remove(first)
        walk.append(first)
        if first in g:
            edges = g.pop(first)
            next = list(filter(lambda x: x not in walk and x not in queue, edges))
            queue = sorted(queue + next)
    return ''.join(walk)


        


def part1(lines):
    start_set = set([])
    stop_set = set([])
    graph = defaultdict(list)
    depends = defaultdict(list)
    for s in get_steps(lines):
        start_set.add(s.start)
        stop_set.add(s.stop)
        graph[s.start].append(s.stop)
        depends[s.stop].append(s.start)
    return walk_graph(graph, depends, sorted(list(start_set.difference(stop_set))))





def part2(lines):
    return None


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    #pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
