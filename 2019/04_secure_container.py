import aoc_utils
from pprint import pprint
from collections import Counter

# * It is a six-digit number.
# * The value is within the range given in your puzzle input.
# * Two adjacent digits are the same (like 22 in 122345).
# * Going from left to right, the digits never decrease; 
#   they only ever increase or stay the same (like 111123 or 135679)
#
# Part 2
# * the two adjacent matching digits are not part of a larger group of matching digits.

def valid(n, only2=False):
    seq = [int(x) for x in list(str(n))]
    z = list(zip([-1] + seq[:-1], seq))
    invalid_inc = any(map(lambda x: x[1] < x[0], z))
    if invalid_inc:
        return False
    c = Counter(seq)
    if only2:
        return 2 in list(c.values())
    return max(list(c.values())) >= 2


def part1(lines):
    start, stop = [int(x) for x in lines[0].split('-')]
    n_valid = len(list(filter(lambda x: valid(x), range(start, stop + 1))))
    return n_valid


def part2(lines):
    start, stop = [int(x) for x in lines[0].split('-')]
    n_valid = len(list(filter(lambda x: valid(x, True), range(start, stop + 1))))
    return n_valid


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    #run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
