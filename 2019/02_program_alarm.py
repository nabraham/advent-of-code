import aoc_utils
from pprint import pprint
from assembly import ProgramState, run_program


def part1(lines, r1, r2):
    registers = [int(x) for x in lines[0].split(',')] 
    if r1 is not None:
        registers[1] = r1
    if r2 is not None:
        registers[2] = r2

    ps = ProgramState(registers)
    run_program(ps)
    return ps.registers[0]


def part2(lines):
    for i in range(366):
        for j in range(366):
            try:
                r = part1(lines, i, j)
                if r == 19690720:
                    return '%d%d' % (i,j)
            except:
                pass



def run(filename, r0=None, r1=None):
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines, r0, r1))
    pprint(part2(lines))


if __name__ == '__main__':
    #run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main(), 12, 2)
