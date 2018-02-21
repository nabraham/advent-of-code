import aoc_utils
import re
from pprint import pprint

def parse(marker):
    return re.match(r"\((\d+)x(\d+)\)", marker)


def get_next(s, n, groups):
    n_chars = int(groups[0])
    n_reps = int(groups[1])
    sub = s[n:n+n_chars]
    return n + n_chars, ''.join([sub]*n_reps)


def decompress(s):
    i = 0
    rez = ''
    while i < len(s):
        match = None
        if s[i] == '(':
            close_paren = s.find(')',i+1)
            if close_paren >= 0:
                marker = s[i:close_paren+1]
                match = parse(marker)
                if match != None:
                    next_i, r = get_next(s, close_paren+1, match.groups())
                    rez += r
                    i = next_i

        if match == None:
            rez += s[i]
            i += 1
    return rez


def part2(s):
    if len(s) == 0:
        return 0
    elif s[0] == '(':
        close_paren = s.find(')',1)
        if close_paren < 0:
            return len(s)
        else:
            marker = s[:close_paren+1]
            groups = parse(marker).groups()
            n_chars = int(groups[0])
            n_reps = int(groups[1])
            return n_reps * part2(s[close_paren+1:close_paren+1+n_chars]) + part2(s[(close_paren+1 + n_chars):])
    else:
        open_paren = s.find('(',1)
        if open_paren < 0:
            return len(s)
        else:
            return open_paren + part2(s[open_paren:])




def run(filename, debug=False):
    print('\n' + aoc_utils.file_header(filename))
    input = aoc_utils.get_input(filename)
    r = list(map(lambda x: (x, decompress(x), len(decompress(x)), part2(x)), input))
    if debug:
        pprint(r)
    else:
        print((r[0][0][:20], r[0][1][:20], r[0][2], r[0][3]))

if __name__ == '__main__':
    run(aoc_utils.puzzle_test(), True)
    run(aoc_utils.puzzle_main())
