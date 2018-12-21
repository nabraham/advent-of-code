import aoc_utils
import re
from pprint import pprint
from collections import namedtuple

Observation = namedtuple('Observation', ['before', 'instruction', 'after'])


def valid_registers(instruction, indices, n = 4):
    return all([0 <= instruction[i] < n for i in indices])


def genr(i, r, operation, indices=[1,2,3]):
    if valid_registers(i, indices):
        r_out = r[:]
        r_out[i[3]] = operation(r_out[i[1]], r_out[i[2]])
        return r_out


def geni(i, r, operation, indices=[1,2,3]):
    if valid_registers(i, indices):
        r_out = r[:]
        r_out[i[3]] = operation(r_out[i[1]], i[2])
        return r_out


def addr(i, r):
    return genr(i, r, lambda x, y: x + y)


def addi(i, r):
    return geni(i, r, lambda x, y: x + y)


def mulr(i, r):
    return genr(i, r, lambda x, y: x * y)


def muli(i, r):
    return geni(i, r, lambda x, y: x * y)


def banr(i, r):
    return genr(i, r, lambda x, y: x & y)


def bani(i, r):
    return geni(i, r, lambda x, y: x & y)


def borr(i, r):
    return genr(i, r, lambda x, y: x | y)


def bori(i, r):
    return geni(i, r, lambda x, y: x | y)
# banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
# bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
# Bitwise OR:
#
# borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
# bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
# Assignment:
#
# setr (set register) copies the contents of register A into register C. (Input B is ignored.)
# seti (set immediate) stores value A into register C. (Input B is ignored.)
# Greater-than testing:
#
# gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
# gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
# gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
# Equality testing:
#
# eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
# eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
# eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.

OPERATIONS = {
    'addr': addr,
    'addi': addi,
    'banr': banr,
    'bani': bani,
    'borr': borr,
    'bori': bori,
    'mulr': mulr,
    'muli': muli
}

def parse_observations(lines):
    observations = []
    for line in lines:
        if 'Before' in line:
            before = re.split('[\\[\\],]', line)[-5:-1]
        elif 'After' in line:
            after = re.split('[\\[\\],]', line)[-5:-1]
            observations.append(Observation(*[[int(y) for y in x] for x in [before, instruction, after]]))
        else:
            instruction = re.split(' ', line)
    return observations


def part1(lines):
    observations = parse_observations(lines)
    for obv in observations:
        print(obv)
        for op in OPERATIONS:
            print(op, '-', OPERATIONS[op](obv.instruction, obv.before))


def part2(lines):
    return None


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    # pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    # run(aoc_utils.puzzle_main())
