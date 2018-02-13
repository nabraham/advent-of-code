import aoc_utils
import re

def pals(s, w=4):
    palindromes = []
    if len(s) >= w:
        for i in range(len(s)-w+1):
            sw = s[i:i+w]
            if sw == sw[::-1] and sw[0] != sw[1]:
                palindromes.append(sw)
    return palindromes


def valid_tls(s):
    parts = re.split('[\[\]]', s)
    outside = [parts[p] for p in range(0,len(parts),2)]
    inside = [parts[p] for p in range(1,len(parts),2)]
    return any(map(lambda x: len(pals(x)) > 0, outside)) and not any(map(lambda x: len(pals(x)) > 0, inside))


def flatten(lst):
    return [x for y in lst for x in y]


def inv(abba):
    a = abba[0]
    b = abba[1]
    return abba.replace(a,'.').replace(b,a).replace('.',b)


def valid_ssl(s):
    parts = re.split('[\[\]]', s)
    outside = [parts[p] for p in range(0,len(parts),2)]
    inside = [parts[p] for p in range(1,len(parts),2)]
    abas = set(flatten(list(map(lambda x: pals(x,3), outside))))
    babs = flatten(list(map(lambda x: pals(x,3), inside)))
    babs_inv = set(map(inv, babs))
    return len(abas.intersection(babs_inv)) > 0


def main(input, validator):
    valids = list(map(lambda x: (x, validator(x)), input))
    print(len(list(filter(lambda x:x[1], valids))))


def run(filename):
    print('\n' + aoc_utils.file_header(filename))
    input = aoc_utils.get_input(filename)
    main(input, valid_tls)
    main(input, valid_ssl)


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
