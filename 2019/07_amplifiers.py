import aoc_utils
import itertools
from assembly import parse_input, run_program, HALTED
from pprint import pprint


def part1(lines):
    scores = []
    for perm in itertools.permutations([0,1,2,3,4]):
        key = ''.join(map(lambda x: str(x), perm))
        prev_output = 0
        for phase in perm:
            program = parse_input(lines[0])
            program.inpt = [phase, prev_output]
            run_program(program)
            prev_output = program.out[-1]
        scores.append((key, program.out[-1]))
    return max(scores, key=lambda x: x[1])


def part2(lines):
    scores = []
    for perm in itertools.permutations([5,6,7,8,9]):
        key = ''.join(map(lambda x: str(x), perm))
        amps = []
        for phase in perm:
            amp = parse_input(lines[0])
            amp.inpt = [phase]
            amps.append(amp)
        amps[0].inpt.append(0)
        while amps[-1].status is not HALTED:
            for i, a in enumerate(amps):
                run_program(a)
                amps[(i + 1) % 5].inpt.append(a.out[-1])
        scores.append((key, amps[-1].out[-1]))
    return max(scores, key=lambda x: x[1])


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
