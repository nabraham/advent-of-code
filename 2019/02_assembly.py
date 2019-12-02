import aoc_utils
from pprint import pprint



def op(registers, i, f):
    a = registers[i+1]
    b = registers[i+2]
    c = registers[i+3]
    registers[c] = f(registers[a], registers[b])
    return registers


def op_add(registers, i):
    return op(registers, i, lambda x,y: x + y)


def op_mul(registers, i):
    return op(registers, i, lambda x,y: x * y)

HALT = 99
INST = {
    1: op_add,
    2: op_mul,
}

def part1(lines, r1, r2):
    registers = [int(x) for x in lines[0].split(',')] 
    if r1 is not None:
        registers[1] = r1
    if r2 is not None:
        registers[2] = r2
    i = 0
    op_code = registers[i]
    while op_code is not HALT:
        if len(registers) <= i:
            raise Exception('Register index out of bounds')
        if op_code not in INST:
            raise Exception('Unexpected op code')
        op = INST[op_code]
        registers = op(registers, i)
        i = i + 4
        op_code = registers[i]
    return registers[0]



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
    #pprint(part1(lines, r0, r1))
    pprint(part2(lines))


if __name__ == '__main__':
    #run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main(), 12, 2)
