import aoc_utils
import re
from collections import defaultdict, namedtuple
from functools import reduce
from pprint import pprint

step_rx = re.compile(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin')
Step = namedtuple('Step',['start', 'stop'])
Task = namedtuple('Task',['name', 'finish_time'])
FREE = Task('.', -1)

def finish(char, tick, offset):
    return tick + ord(char) - ord('A') + 1 + offset


class Worker:
    def __init__(self, id):
        self.id = id
        self.task = FREE

    def assign(self, task_id, tick, offset):
        self.task = Task(task_id, finish(task_id, tick, offset))

    def free(self):
        return self.task.name == '.'

    def process(self, tick):
        if not self.free() and tick >= self.task.finish_time:
            t = self.task.name
            self.task = FREE
            return t
        return None

    def __repr__(self):
        return '%s - %s' % (self.id, self.task)



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
    while len(queue) > 0:
        first = get_first(queue, depends, walk)
        queue.remove(first)
        walk.append(first)
        if first in g:
            edges = g.pop(first)
            next = list(filter(lambda x: x not in walk and x not in queue, edges))
            queue = sorted(queue + next)
    return ''.join(walk)


def still_working(workers):
    return any(map(lambda x: not x.free(), workers))


def any_free(workers):
    return any(map(lambda x: x.free(), workers))

def in_progress(workers):
    return set(map(lambda x: x.task.name, workers)).difference(set(['.']))


def assign_tasks(graph, walk, depends, queue, workers, tick, offset):
    should_continue = True
    while should_continue and len(queue) > 0 and any_free(workers):
        first = get_first(queue, depends, walk)
        if first != None:
            queue.remove(first)
            w = list(filter(lambda x: x.free(), workers))[0]
            w.assign(first, tick, offset)
        else:
            should_continue = False
    return queue


def add_edges(queue, finished, graph, walk, workers):
    if len(finished) > 0:
        all_edges = [graph[f] for f in finished]
        uniq_new = list(set(reduce(lambda x,y: x + y, all_edges)))
        new_edges = list(filter(lambda x: x not in walk and x not in in_progress(workers) and x not in queue, uniq_new))
        return sorted(queue + new_edges)
    return queue

def print_state(tick, workers, walk, queue):
    print('%d: %s' % (tick, '\t'.join(
        [w.task.name for w in workers] + 
        [''.join(walk)] + 
        ['<%s>' % ','.join(queue)])))
    
    

def walk_with_workers(graph, depends, queue, n_workers, offset):
    tick = 0
    workers = [Worker(i) for i in range(1,n_workers + 1)]
    walk = []
    while len(queue) > 0 or still_working(workers):
        processed = map(lambda x: x.process(tick), workers)
        finished = list(filter(lambda x: x != None, processed))
        queue = add_edges(queue, finished, graph, walk, workers)
        walk += finished
        queue = assign_tasks(graph, walk, depends, queue, workers, tick, offset)
        #print_state(tick, workers, walk, queue)
        tick += 1
    return tick - 1, ''.join(walk)


def part1(lines):
    graph, depends, queue = build_start(lines)
    return walk_graph(graph, depends, queue)

def build_start(lines):
    start_set = set([])
    stop_set = set([])
    graph = defaultdict(list)
    depends = defaultdict(list)
    for s in get_steps(lines):
        start_set.add(s.start)
        stop_set.add(s.stop)
        graph[s.start].append(s.stop)
        depends[s.stop].append(s.start)
    return graph, depends, sorted(list(start_set.difference(stop_set)))


def part2(lines):
    graph, depends, queue = build_start(lines)
    n_workers = [2, 5][len(lines) > 10]
    offset = [0, 60][len(lines) > 10]
    return walk_with_workers(graph, depends, queue, n_workers, offset)



def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
