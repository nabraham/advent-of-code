import aoc_utils
from pprint import pprint
from functools import reduce


def wait():
    input('Enter to continue')


A, B, C = 0, 1, 2


def inst(f):
    def op(instruction, registers):
        ro = registers[::]
        ro[instruction[C]] = f(instruction, registers)
        return ro

    return op


OPERATIONS = {
    'addi': inst(lambda i, r: r[i[A]] + i[B]),
    'addr': inst(lambda i, r: r[i[A]] + r[i[B]]),
    'bani': inst(lambda i, r: r[i[A]] & i[B]),
    'banr': inst(lambda i, r: r[i[A]] & r[i[B]]),
    'bori': inst(lambda i, r: r[i[A]] | i[B]),
    'borr': inst(lambda i, r: r[i[A]] | r[i[B]]),
    'eqir': inst(lambda i, r: [0, 1][i[A] == r[i[B]]]),
    'eqri': inst(lambda i, r: [0, 1][r[i[A]] == i[B]]),
    'eqrr': inst(lambda i, r: [0, 1][r[i[A]] == r[i[B]]]),
    'gtir': inst(lambda i, r: [0, 1][i[A] > r[i[B]]]),
    'gtri': inst(lambda i, r: [0, 1][r[i[A]] > i[B]]),
    'gtrr': inst(lambda i, r: [0, 1][r[i[A]] > r[i[B]]]),
    'muli': inst(lambda i, r: r[i[A]] * i[B]),
    'mulr': inst(lambda i, r: r[i[A]] * r[i[B]]),
    'seti': inst(lambda i, r: i[A]),
    'setr': inst(lambda i, r: r[i[A]])
}


def parse_program(lines):
    fp = int(lines[0].split(' ')[1])
    program = []
    for line in lines[1:]:
        parts = line.split(' ')
        program.append((parts[0], [int(x) for x in parts[1:]]))
    return fp, program


def run_program(pr, program, registers, abort_length):
    ip = 0
    count = 0
    while ip < len(program) and count < abort_length:
        instruction = program[ip]
        op = OPERATIONS[instruction[0]]
        registers[pr] = ip
        rout = registers[::]
        rafter = op(instruction[1], rout)
        registers = rafter
        ip = rafter[pr] + 1
        count = count + 1
        # wait()
    return ip >= len(program)


def part1(lines):
    ip, program = parse_program(lines)
    halted = False
    N = 10000
    i = 0
    while not halted and i < 10000:
        print('testing', i)
        registers = [i] + [0] * 5
        halted = run_program(ip, program, registers, N)
        i += 1
    return i - 1


def part2(lines):
    ip, program = parse_program(lines)
    registers = [1, 0, 0, 0, 0, 0]
    return run_program(ip, program, registers)[0]


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    #pprint(part2(lines))


if __name__ == '__main__':
    # run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
