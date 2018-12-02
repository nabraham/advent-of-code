import aoc_utils
from pprint import pprint
from collections import Counter
from functools import reduce


def count_n(n, line):
    return [0, 1][n in list(Counter(list(line)).values())]


def part1(lines):
    counts = map(lambda x: [count_n(2, x), count_n(3, x)], lines)
    sum_count = reduce(lambda x, y: [x[0] + y[0], x[1] + y[1]], counts)
    return sum_count[0] * sum_count[1]


def part2(lines):
    seen = {}
    for li, line in enumerate(lines):
        for i, c in enumerate(line):
            removed = line[0:i] + '.' +  line[i+1:]
            if removed in seen:
                return removed.replace('.',''), '(%d, %d)' % (li, seen[removed])
            seen[removed] = li
    

def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
