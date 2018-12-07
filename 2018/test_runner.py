import os
import re
from os.path import isfile
import aoc_utils

file_rx = re.compile('\d{2}_.*\.py')

def test_main(mask=None):
    files = sorted(list(filter(lambda x: isfile(x) and file_rx.match(x), os.listdir())))
    if mask != None:
        files = list(filter(lambda x: mask.match(x), files))
    for f in files:
        pack = __import__(f[:-3])
        number = f[:2]
        expected = None
        try:
            expected = aoc_utils.get_input('data/%s.ans' % number)
            print(aoc_utils.file_header(f))
            if len(expected) >= 2:
                run_test(pack, 'data/%s_test.txt' % number, expected[:2], 'test')
            if len(expected) >= 4:
                run_test(pack, 'data/%s.txt' % number, expected[2:4], 'main')
        except FileNotFoundError:
            print('No expected for for %s' % number)


def get_output(result):
    if isinstance(result, list) or isinstance(result, tuple):
        return result[0]
    return result


def run_test(pack, filename, expected, msg):
    try:
        test_input = aoc_utils.get_input(filename)
        if pack.part1:
            actual = pack.part1(test_input)
            assert(str(get_output(actual)) == expected[0]), actual
            print('%s: part1 succeeded' % msg)
        if pack.part2:
            actual = pack.part2(test_input)
            assert(str(get_output(actual)) == expected[1]), actual
            print('%s: part2 succeeded' % msg)
    except FileNotFoundError:
        print('No test input for %s' % filename)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        mask = re.compile('.*%s.*' % sys.argv[1])
    test_main(mask)
