#snd X plays a sound with a frequency equal to the value of X.
#set X Y sets register X to the value of Y.
#add X Y increases register X by the value of Y.
#mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
#mod X Y sets register X to the remainder of dividing the value contained in register X by the value of Y (that is, it sets X to the result of X modulo Y).
#rcv X recovers the frequency of the last sound played, but only when the value of X is not zero. (If it is zero, the command does nothing.)
#jgz X Y jumps with an offset of the value of Y, but only if the value of X is greater than zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)
from collections import defaultdict
from pprint import pprint

def val(r, x):
    if x in r:
        return r[x]
    else:
        return int(x)

def snd(r, x):
    r['snd'] = r[x]


def set(r, x, y):
    r[x] = val(r,y)


def add(r, x, y):
    r[x] += val(r,y)


def mul(r, x, y):
    r[x] *= val(r,y)


def mod(r, x, y):
    r[x] = r[x] % val(r,y)


def rcv(r, x):
    if val(r,x) != 0:
        r[rcv] = r['snd']
        return 'DONE'


def jgz(r, x, y):
    return [1, val(r,y)][val(r,x) > 0]

COMMANDS = {'snd':snd, 'set':set, 'add':add, 'mul':mul, 'mod':mod, 'rcv':rcv, 'jgz':jgz }
def main(program, verbose):
    index = 0
    registers = defaultdict(int)
    while True:
        if index < 0 or index >= len(program):
            raise Exception('Instruction index OOB')

        cmd = program[index]
        if verbose:
            print('%d:' % index, cmd)
        if cmd[0] in COMMANDS:
            jmp = COMMANDS[cmd[0]](registers, *cmd[1:])
            if jmp != None:
                if jmp == 'DONE':
                    return registers['snd']
                else:
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


def run(filename, verbose=False):
    print('%s\n%s' % (filename, '-' * len(filename)))
    program = []
    with open(filename) as f:
        program = [line.strip('\n').split(' ') for line in f.readlines()]
        pprint(program)
        print(main(program, verbose))

if __name__ == '__main__':
    run('data/18_test.txt', True)
    run('data/18.txt', True)

