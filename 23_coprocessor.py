import aoc_utils
from pprint import pprint
from math import sqrt
from itertools import count, islice

def val(r, x):
    if x in r:
        return r[x]
    else:
        return int(x)


def set(r, x, y):
    r[x] = val(r,y)


def sub(r, x, y):
    r[x] -= val(r,y)


def mul(r, x, y):
    r[x] *= val(r,y)


def jnz(r, x, y):
    return [1, val(r,y)][val(r,x) != 0]

COMMANDS = {'set':set, 'sub':sub, 'mul':mul, 'jnz':jnz }

def init_registers(overrides):
    registers = dict()
    for r in 'abcdefgh':
        registers[r] = 0
    for o in overrides:
        registers[o[0]] = o[1]
    return registers

def main(program, overrides, verbose, stop=-1):
    index = 0
    registers = init_registers(overrides)
    stack = []
    while index != stop and index >= 0 and index < len(program):
        cmd = program[index]
        stack.append(cmd)
        if verbose:
            print('%d:' % index, cmd)
        if cmd[0] in COMMANDS:
            jmp = COMMANDS[cmd[0]](registers, *cmd[1:])
            if jmp != None:
                try:
                    index += int(jmp)
                except:
                    raise Exception('Unexpected response: ' + jmp)
            else:
                index += 1
        else:
            raise Exception('Unknown instruction')
        if verbose:
            pprint(dict(registers))
            print()
    return stack, registers


def run(filename, overrides=[], verbose=False, stop=-1):
    print('\n' + aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    program = [line.split(' ') for line in lines]
    return main(program, overrides, verbose, stop)


def is_composite(n):
        return not all(n%i for i in islice(count(2), int(sqrt(n)-1)))


if __name__ == '__main__':
    stack = run(aoc_utils.puzzle_main())[0]
    print('PART 1:',  len(list(filter(lambda x: x[0] == 'mul', stack))))

    registers = run(aoc_utils.puzzle_main(), [('a',1)], False, 9)[1]
    r = range(registers['b'], registers['c'] + 1, 17)
    print('PART 2:', len(list(filter(is_composite, r))))
