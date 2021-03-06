import aoc_utils
import re
import string
from pprint import pprint


def pretty(line, n=10):
    if len(line) > n:
        return line[:n] + '...' + line[:n]
    return line


def part1(lines):
    line = lines[0]
    index = 0
    while index < (len(line) - 1):
        curr = line[index]
        next = line[index + 1]
        if index >= 0 and curr.lower() == next.lower() and curr != next:
            line = line[:index] + line[index+2:]
            index -= 1
        else:
            index += 1
    return len(line), pretty(line)


def part2(lines):
    line = lines[0]
    results = []
    for c in string.ascii_lowercase:
        pattern = '[%s%s]' % (c, c.upper())
        replacement = re.sub(pattern, '', line)
        results.append([c, part1([replacement])])
    m = min(results, key=lambda x: x[1][0])
    return m[1][0], (m[0], m[1][1])


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
