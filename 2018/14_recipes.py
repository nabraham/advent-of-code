import aoc_utils
from collections import deque
from pprint import pprint

def print_state(q, e0, e1):
    pretty = []
    special = { e1: '[]', e0: '()' }
    for i, v  in enumerate(q):
        borders = special.get(i, ['',''])
        pretty.append('%s%d%s' % (borders[0], v, borders[1]))
    print(' '.join(pretty))

def part1(lines):
    n = int(lines[0])
    q = deque([3,7])
    e0 = 0
    e1 = 1
    count = 0
    while len(q) < n + 10:
        #print_state(q, e0, e1)
        r0 = q[e0]
        r1 = q[e1]
        s = r0 + r1
        digits = list(map(int, list(str(s))))
        q += digits
        e0 = (e0 + 1 + r0) % len(q)
        e1 = (e1 + 1 + r1) % len(q)
        count += 1
    return ''.join(map(str, list(q)[n:n+11]))


def part2(lines):
    pattern = lines[-1]
    n = len(pattern)
    q = [3,7]
    e0 = 0
    e1 = 1
    count = 0
    ending = ''
    while pattern not in ending:
        r0 = q[e0]
        r1 = q[e1]
        s = r0 + r1
        digits = list(map(int, list(str(s))))
        q += digits
        e0 = (e0 + 1 + r0) % len(q)
        e1 = (e1 + 1 + r1) % len(q)
        count += 1
        if len(q) > n + 2:
            ending = ''.join(map(str, q[(-n-2):]))
    return len(q) - n - 2 + ending.index(pattern)



def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
