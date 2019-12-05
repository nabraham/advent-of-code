class ProgramState:
    def __init__(self, registers=[], inpt=[], out=[], parameter_modes=[], instruction_idx=0):
        self.registers = registers
        self.parameter_modes = parameter_modes
        self.i_idx = instruction_idx
        self.inpt = inpt
        self.out = out
        self.jumped = False

    def current(self):
        return self.registers[self.i_idx]

    def curr_pretty(self):
        return 'registers = %s\nidx = %d\nmodes = %s' % \
                (self.registers[self.i_idx:self.i_idx + 8], self.i_idx, self.parameter_modes)

    def __repr__(self):
        return self.curr_pretty()


POSITION, IMMEDIATE = (0, 1)


def parse_input(s):
    return ProgramState([int(x) for x in s.split(',')])


def get_val(registers, v, mode, rel_mode):
    return registers[v] if mode == rel_mode else v


def get_arguments(ps, n, modes=[]):
    args = []
    for i in range(n):
        v = ps.registers[ps.i_idx + i + 1]
        v_mode = 0 if len(ps.parameter_modes) < (i + 1) else ps.parameter_modes[i]
        rel_mode = POSITION if i >= len(modes) else modes[i]
        args.append(get_val(ps.registers, v, v_mode, rel_mode))
    return args


def op3(f):
    def op(ps):
        a, b, c = get_arguments(ps, 3, [POSITION, POSITION, IMMEDIATE])
        ps.registers[c] = f(a, b)
    return (4, op)


def op_add():
    return op3(lambda x,y: x + y)


def op_mul():
    return op3(lambda x,y: x * y)


def op_input():
    def op(ps):
        a = ps.registers[ps.i_idx + 1]
        ps.registers[a] = ps.inpt[0]
    return (2, op)


def op_output():
    def op(ps):
        a = get_arguments(ps, 1)[0]
        ps.out.append(a)
    return (2, op)


def op_jump(inverse=False):
    def op(ps):
        a, b = get_arguments(ps, 2)
        if (a != 0 and not inverse) or (a == 0 and inverse):
            ps.i_idx = b
            ps.jumped = True
    return (3, op)

def op_compare(f):
    def op(ps):
        a, b, c = get_arguments(ps, 3, [POSITION, POSITION, IMMEDIATE])
        ps.registers[c] = [0, 1][f(a, b)]
    return (4, op)


def op_less_than():
    return op_compare(lambda x, y: x < y)


def op_equals():
    return op_compare(lambda x, y: x == y)


        
HALT = 99
INST = {
    1: op_add(),
    2: op_mul(),
    3: op_input(),
    4: op_output(),
    5: op_jump(),
    6: op_jump(True),
    7: op_less_than(),
    8: op_equals()
}

#1003 => (3, [0, 1])
#   3 => (3, [])
def parse_code(n):
    s = str(n)
    code = int(s[-2:])
    modes = [int(x) for x in s[:-2][::-1]]
    return (code, modes)


def run_program(ps):
    op_code, modes = parse_code(ps.current())
    while op_code is not HALT:
        if len(ps.registers) <= ps.i_idx:
            raise Exception('Register index out of bounds')
        if op_code not in INST:
            raise Exception('Unexpected op code: %s' % op_code)
        offset, op = INST[op_code]
        ps.parameter_modes = modes
        op(ps)
        if not ps.jumped:
            ps.i_idx += offset
        ps.jumped = False
        
        op_code, modes = parse_code(ps.current())
    return ps


if __name__ == '__main__':
    print(parse_code(1003))
    print(parse_code(3))
    print(parse_code(404))
