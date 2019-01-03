import aoc_utils
import re
from z3 import If, Int, Optimize
from pprint import pprint


class Particle:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def __repr__(self):
        return '<%d,%d,%d> (%d)' % (self.x, self.y, self.z, self.r)

    def dist(self, other):
        return abs(other.x - self.x) + abs(other.y - self.y) + abs(other.z - self.z)

    def in_range(self, other):
        return self.dist(other) <= self.r


def parse(lines):
    particles = []
    line_rx = re.compile('pos=<(-?\\d+),(-?\\d+),(-?\\d+)>, r=(\\d+)')
    for line in lines:
        groups = line_rx.match(line).groups()
        particles.append(Particle(*[int(x) for x in groups]))
    return particles


def part1(lines):
    bots = parse(lines)
    max_bot = max(bots, key=lambda x: x.r)
    return len(list(filter(lambda x: max_bot.in_range(x), bots)))


def zabs(x):
    return If(x > 0, x, -x)


def part2(lines):
    bots = parse(lines)
    const_in_range = [Int('in_range_%d' % i) for i in range(len(bots))]
    const_range_count = Int('sum')
    x, y, z = Int('x'), Int('y'), Int('z')
    o = Optimize()
    for i, p in enumerate(bots):
        o.add(const_in_range[i] == If(zabs(x - p.x) + zabs(y - p.y) + zabs(z - p.z) <= p.r, 1, 0))
    o.add(const_range_count == sum(const_in_range))
    const_dist = Int('dist')
    o.add(const_dist == zabs(x) + zabs(y) + zabs(z))
    h1 = o.maximize(const_range_count)
    h2 = o.minimize(const_dist)
    pprint(o.check())
    pprint(o.model())
    pprint(o.lower(h2))


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
