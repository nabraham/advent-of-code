import aoc_utils
from assembly import parse_input, run_program
from pprint import pprint


def part1(lines):
    program = parse_input(lines[0])
    program.inpt = [1]
    run_program(program)
    return program.out


def part2(lines):
    program = parse_input(lines[0])
    program.inpt = [5]
    run_program(program)
    return program.out


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
