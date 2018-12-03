import aoc_utils
import re
from collections import defaultdict, namedtuple
from pprint import pprint

Patch = namedtuple('Patch', ['id', 'x', 'y', 'width', 'height'])

def parse(line):
    parts = re.split('[ x:#,]', line)
    ints =  list(map(lambda x: int(x), [parts[1], parts[3], parts[4], parts[6], parts[7]]))
    return Patch(*ints)


def part1(lines):
    patches = list(map(parse, lines))
    quilt = defaultdict(list)
    for p in patches:
        for j in range(p.width):
            for i in range(p.height):
                quilt['%d,%d' % (p.x + j, p.y + i)].append(p.id)

    return quilt
    

def part2(quilt):
    singles = set([])
    multiples = set([])

    for spot in quilt:
        if len(quilt[spot]) > 1:
            for id in quilt[spot]:
                multiples.add(id)
        else:
            singles.add(quilt[spot][0])

    for s in singles:
        if s not in multiples:
            return s
    

def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)

    quilt = part1(lines)
    two_or_more = list(filter(lambda x: len(x) > 1, quilt.values()))
    pprint(len(two_or_more))
    pprint(part2(quilt))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
