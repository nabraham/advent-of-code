import aoc_utils
import re
from pprint import pprint
from collections import defaultdict, namedtuple

Observation = namedtuple('Observation', ['before', 'instruction', 'after'])
OP,A,B,C = (0,1,2,3)

def inst(f):
    def op(instruction, registers):
        ro = registers[::]
        ro[instruction[C]] = f(instruction, registers)
        return ro
    return op

OPERATIONS = {
    'addi': inst(lambda i, r: r[i[A]] + r[i[B]]),
    'addr': inst(lambda i, r: r[i[A]] + i[B]),
    'bani': inst(lambda i, r: r[i[A]] & i[B]),
    'banr': inst(lambda i, r: r[i[A]] & r[i[B]]),
    'borr': inst(lambda i, r: r[i[A]] | r[i[B]]),
    'bori': inst(lambda i, r: r[i[A]] | i[B]),
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

def parse_observations(lines):
    observations = []
    before, instruction, after = [], [], []
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
    matches = []
    for obv in observations:
        matched_operations = []
        for op in sorted(OPERATIONS.keys()):
            if obv.after == OPERATIONS[op](obv.instruction, obv.before):
                matched_operations.append(op)
        matches.append((obv.instruction[0], matched_operations))
    p1_ans = len(list(filter(lambda x: len(x[1]) >= 3, matches)))
    return (p1_ans, matches)

def run_program(op_dict, program_str):
    r = [0, 0, 0, 0]
    for instruction in program_str.strip().split('\n'):
        i = [int(x) for x in instruction.split(' ')]
        r = OPERATIONS[op_dict[i[0]]](i, r)
    return r[0]


def part2(lines):
    file_str = '\n'.join(lines)
    captured, program = file_str.split('\n\n\n')
    matches = part1(captured.split('\n'))[1]

    op_to_instructions = defaultdict(list)
    for m in matches:
        op_to_instructions[m[0]].append(set(m[1]))

    for opcode in op_to_instructions:
        op_to_instructions[opcode] = set.intersection(*op_to_instructions[opcode])

    op_dict = {}
    while len(op_to_instructions) > 0:
        for opcode in op_to_instructions:
            if len(op_to_instructions[opcode]) == 1:
                op_dict[opcode] = op_to_instructions[opcode].pop()
            else:
                op_to_instructions[opcode] = op_to_instructions[opcode].difference(set(op_dict.values()))
        for o in op_dict:
            if o in op_to_instructions:
                del op_to_instructions[o]

    return run_program(op_dict, program)

    
def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines)[0])
    pprint(part2(lines))


if __name__ == '__main__':
    #run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
