import aoc_utils
from collections import defaultdict, deque
from pprint import pprint

def val(r, x):
    if x in r:
        return r[x]
    else:
        return int(x)

def set(r, x, y):
    r[x] = val(r,y)
    return 1


def add(r, x, y):
    r[x] += val(r,y)
    return 1


def mul(r, x, y):
    r[x] *= val(r,y)
    return 1


def mod(r, x, y):
    r[x] = r[x] % val(r,y)
    return 1


def jgz(r, x, y):
    return [1, val(r,y)][val(r,x) > 0]

COMMANDS = {'set':set, 'add':add, 'mul':mul, 'mod':mod, 'jgz':jgz }

def print_buffers(b):
    for p in b:
        print(p, '-', list(b[p]))

class Program:
    def __init__(self, pid, other_pid, buffers, instructions):
        self.pid = pid
        self.other_pid = other_pid
        self.buffers = buffers
        self.instructions = instructions
        self.index = 0
        self.registers = defaultdict(int)
        self.registers['p'] = pid
        self.send_count = 0

    def __repr__(self):
        return 'PID: %d, SEND_COUNT: %d' % (self.pid, self.send_count)

    def run(self, verbose=False):
        run_any = False
        while True:
            if self.index < 0 or self.index >= len(self.instructions):
                raise Exception('Instruction index OOB')

            cmd = self.instructions[self.index]
            if verbose:
                print('[%d]%d:' % (self.pid, self.index), cmd)
                print('Buffers:')
                print_buffers(self.buffers)
            if cmd[0] in COMMANDS:
                jmp = COMMANDS[cmd[0]](self.registers, *cmd[1:])
                self.index += jmp
            elif cmd[0] == 'snd':
                self.buffers[self.other_pid].append(val(self.registers, cmd[1]))
                self.index += 1
                self.send_count += 1
            elif cmd[0] == 'rcv':
                if len(self.buffers[self.pid]) == 0:
                    return run_any
                else:
                    self.registers[cmd[1]] = self.buffers[self.pid].popleft()
                    self.index += 1
            else:
                raise Exception('unexpected instruction: ' + cmd)
            if verbose:
                pprint(dict(self.registers))
                print()
            run_any = True


def main(filename, verbose=False):
    print('\n%s\n%s' % (filename, '-' * len(filename)))
    with open(filename) as f:
        instructions = [line.strip('\n').split(' ') for line in f.readlines()]
        buffers = dict()
        buffers[0] = deque()
        buffers[1] = deque()
        programs = [Program(i, 1-i, buffers, instructions) for i in range(2)]
        while True:
            state = [p.run(verbose) for p in programs]
            #if program 1 does nothing, we know that program 0 is done since it ran first
            #if there were more than 2 programs, we would have to check the whole tail: any(state[1:])
            if state[1] == False:
                break
        for p in programs:
            print(p)

if __name__ == '__main__':
    main('data/18_test2.txt', True)
    main(aoc_utils.puzzle_main())

