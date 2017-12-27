import aoc_utils
import re
from pprint import pprint
from collections import deque

RIGHT = 1
LEFT = -1

class TuringRule:
    write = [-1,-1]
    move = [0,0]
    cont = [None, None]

    def __init__(self,w,m,c):
        self.write = w
        self.move = m
        self.cont = c

    def __repr__(self):
        return 'W: %s, M: %s, T: %s' % (self.write, self.move, self.cont)

def parse_rule(lines):
    state = lines[0][-2]
    write, move, cont = [], [], []
    for i in [0,1]:
        write.append(int(lines[i*4+2][-2]))
        move.append([LEFT, RIGHT]['right' in lines[i*4+3]])
        cont.append(lines[i*4+4][-2])
    return state, TuringRule(write, move, cont)

def parse_rules(lines, N=8):
    rules = {}
    i = 0
    while i < len(lines)-N:
        s, r = parse_rule(lines[i:i+N+1])
        rules[s] = r
        i += (N+2)
    return rules

def grow_tape(tape, index):
    if index == -1:
        tape.appendleft(0)
        return 0
    elif index == len(tape):
        tape.append(0)
    return index

def main(rules, state, n):
    index = 0
    tape = deque([0])
    for i in range(n):
        tv = tape[index]
        to_write = rules[state].write[tv]
        to_move = rules[state].move[tv]
        to_cont = rules[state].cont[tv]

        tape[index] = to_write
        index += to_move
        state = to_cont
        index = grow_tape(tape, index)
    return tape



def run(filename):
    print('\n' + aoc_utils.file_header(filename))
    input = aoc_utils.get_input(filename)
    state_init = input[0][-2]
    n_steps = int(re.findall('\d+', input[1])[0])
    rules = parse_rules(input[3:])
    print(sum(main(rules, state_init, n_steps)))
    

if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
