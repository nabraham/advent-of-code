import aoc_utils
from pprint import pprint


def part1(freqs):
    return sum(freqs)


def part2(freqs):
    seen = set([0])
    summ = 0
    while True:
        for f in freqs:
            summ += f
            if summ in seen:
                return summ
            seen.add(summ)


def run(filename):
    print(aoc_utils.file_header(filename))
    freqs = list(map(lambda x: int(x), aoc_utils.get_input(filename)))
    pprint(part1(freqs))
    pprint(part2(freqs))


if __name__ == '__main__':
    #run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
