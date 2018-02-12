import aoc_utils
from collections import defaultdict

def max_count(counter, direction):
    items = sorted(list(counter.items()), key=lambda x: direction * x[1])
    return items[0][0]


def solve(input, direction=-1):
    counters = defaultdict(lambda: defaultdict(int))
    for line in input:
        for i, c in enumerate(line):
            counters[i][c] += 1

    rez = [max_count(counters[k], direction) for k in counters]
    print(''.join(rez))


def run(filename):
    print('\n' + aoc_utils.file_header(filename))
    input = aoc_utils.get_input(filename)
    solve(input)
    solve(input, 1)



if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
