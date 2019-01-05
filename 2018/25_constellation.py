import aoc_utils
from pprint import pprint

class Point:
    def __init__(self, pt_tuple):
        self.pt_tuple = pt_tuple

    def dist(self, other):
        return sum(map(lambda x: abs(x[1] - x[0]), zip(self.pt_tuple, other.pt_tuple)))

    def __repr__(self):
        return '<%s>' % ','.join([str(x) for x in self.pt_tuple])


class Constellation:
    def __init__(self):
        self.points = []

    def add(self, pt):
        self.points.append(pt)

    def contains(self, pt, r=3):
        return any(map(lambda x: x.dist(pt) <= r, self.points))

    def merge(self, other):
        self.points += other.points

    def __repr__(self):
        return '{ %s }' % '\n  '.join([str(p) for p in self.points])


def parse(lines):
    return [Point([int(x) for x in line.split(',')]) for line in lines]


def part1(lines):
    points = parse(lines)
    constellations = dict()
    count = 0

    for p in points:
        contained_by = []
        for c in constellations:
            if constellations[c].contains(p):
                contained_by.append(c)

        if len(contained_by) == 0:
            con = Constellation()
            con.add(p)
            constellations[count] = con
            count += 1
        else:
            constellations[contained_by[0]].add(p)
            for c in contained_by[1:]:
                constellations[contained_by[0]].merge(constellations[c])
                del constellations[c]

    return len(constellations)




def part2(lines):
    return None


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    #pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
