import aoc_utils
import re
from pprint import pprint

def parse(marker):
    return re.match(r"\((\d+)x(\d+)\)", marker)


def get_next(s, i, n, groups):
    n_chars = int(groups[0])
    n_reps = int(groups[1])
    sub = s[n+1:n+1+n_chars]
    return n + 1, ''.join([sub]*(n_reps-1))


def decompress(s):
    i = 0
    rez = ''
    while i < len(s):
        groups = None
        if s[i] == '(':
            close_paren = s.find(')',i+1)
            if close_paren >= 0:
                marker = s[i:close_paren+1]
                match = parse(marker)
                if match != None:
                    next_i, r = get_next(s, i, close_paren, match.groups())
                    rez += r
                    i = next_i

        if groups == None:
            rez += s[i]
            i += 1
    return rez


def run(filename):
    print('\n' + aoc_utils.file_header(filename))
    input = aoc_utils.get_input(filename)
    pprint(list(map(lambda x: len(decompress(x)), input)))

if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
