import aoc_utils
import re
from collections import defaultdict

patt = re.compile('([a-z]+) (inc|dec) ([\-\d]+) if ([a-z]+) ([!><=]+) ([\-0-9]+)')

class Instruction:
    target = None
    cmd = None
    val = None
    cond_target = None
    cond = None
    cond_val = None

    def __init__(self, line):
        matches = patt.match(line) 
        self.target = matches.group(1)
        self.cmd = matches.group(2)
        self.val = int(matches.group(3))
        self.cond_target = matches.group(4)
        self.cond = matches.group(5)
        self.cond_val = int(matches.group(6))

    def __repr__(self):
        return '%s %s %d %s %s %d' % (self.target, self.cmd, self.val, self.cond_target, self.cond, self.cond_val)

COMMANDS = {
    'dec': lambda x: -x,
    'inc': lambda x: x
}

def main(instructions):
    registers = defaultdict(int)
    all_max = 0
    for i in instructions:
        rcv = registers[i.cond_target]
        should_execute = eval('%d %s %d' % (rcv, i.cond, i.cond_val))
        if should_execute:
            registers[i.target] += COMMANDS[i.cmd](i.val)
        mx = max(registers.values())
        if mx > all_max:
            all_max = mx
    return max(registers.values()), all_max



if __name__ == '__main__':
    program = [Instruction(line) for line in aoc_utils.get_input()]
    print(main(program))
