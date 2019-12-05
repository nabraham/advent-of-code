import aoc_utils
from pprint import pprint

def fuel_required(n):
    return n // 3 - 2


def recursive_fuel(n):
    summ = 0
    fuel = fuel_required(n)
    while fuel > 0:
        summ = summ + fuel
        fuel = fuel_required(fuel)
    return summ


def part1(lines):
    modules = [int(line) for line in lines]
    fr = list(map(lambda x: fuel_required(x), modules))
    return sum(fr)


def part2(lines):
    modules = [int(line) for line in lines]
    fr = list(map(lambda x: recursive_fuel(x), modules))
    return sum(fr)


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
