import aoc_utils
from collections import deque
from pprint import pprint

class Rule:
    def __init__(self, line):
        parts = line.split(' => ')
        self.condition = list(parts[0])
        self.outcome = parts[1]

    def next(self, q, index):
        if index > 1 and index < len(q) - 2:
            if all(map(lambda i: q[index - 2 + i] == self.condition[i], range(len(self.condition)))):
                return self.outcome
        return None

    def __repr__(self):
        return '%s | %s' % (''.join(self.condition), self.outcome)


def get_state(line):
    return deque(list(line.split(': ')[1]))


def get_rules(lines):
    return list(map(lambda x: Rule(x), lines))


def pad_state(state, pad_left):
    pl = 0
    first = state.index('#')
    for i in range(5 - first):
        pl += 1
        state.appendleft('.')

    r = 0
    while r < 5 and state[len(state) - 1 - r] == '.':
        r += 1

    for i in range(5-r):
        state.append('.')

    return pl + pad_left



def find_next(state, i, rules):
    for r in rules:
        n = r.next(state, i)
        if n is not None:
            return n
    return None


def print_state(generation, state, pad_left):
    print('%d(%d): %s' % (generation, pad_left, ''.join(state)))


def sum_state(state, pad_left):
    pots = list(filter(lambda x: x[1] == '#', enumerate(state)))
    return sum(map(lambda x: x[0] - pad_left, pots))


def state_hash(state):
    return ''.join(state).strip('.')


def part1(lines, n_gen=20, break_cycle=False):
    state = get_state(lines[0])
    rules = get_rules(lines[2:])
    generation = 0
    pad_left = 0
    seen = {}
    while generation < n_gen:
        h = state_hash(state)
        if break_cycle:
            if h in seen:
                break
            else:
                seen[h] = generation
        pad_left = pad_state(state, pad_left)
        next_state = deque(['.']*len(state))
        for i in range(2,len(state)-2):
            next_value = find_next(state, i, rules)
            if next_value:
                next_state[i] = next_value
        state = next_state
        generation += 1

    return sum_state(state, pad_left), state, generation


def part2(lines):
    summ, state, gen = part1(lines, 50e9, True)
    pot_count = state.count('#')
    remaining = (50e9 - gen)
    return summ + remaining * pot_count


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    #run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
