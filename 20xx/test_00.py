from os.path import isfile
import aoc_utils
import os
import re
import unittest


test_file = os.path.basename(__file__)
test_rx = re.compile(r'test_(\d+)\.py')
test_match = test_rx.match(test_file)
test_num = test_match.group(1)
file_rx = re.compile('^%s_.*\.py' % test_num)
files = list(filter(lambda x: isfile(x) and file_rx.match(x), os.listdir()))
if len(files) > 1:
    raise Exception('Only 1 file expected per challenge')
package_file = files[0]
pack = __import__(package_file[:-3])
expected = None
try:
    expected = aoc_utils.get_input('data/%s.ans' % test_num)
except FileNotFoundError:
    print('No test conditions for test %s' % test_num)
test_in = aoc_utils.get_input('data/%s_test.txt' % test_num)
main_in = aoc_utils.get_input('data/%s.txt' % test_num)


def get_output(result):
    if isinstance(result, list) or isinstance(result, tuple):
        return result[0]
    return result

def run_test(function, input, expected, index):
    if expected == None:
        print('Warning: no input for %s' % test_num)
    else:
        actual = function(input)
        assert(str(get_output(actual))) == expected[index]


class TestClass(unittest.TestCase):
    def test_part1_example(self):
        run_test(pack.part1, test_in, expected, 0)


    def test_part2_example(self):
        run_test(pack.part2, test_in, expected, 1)


    def test_part1_main(self):
        run_test(pack.part1, main_in, expected, 2)


    def test_part2_main(self):
        run_test(pack.part2, main_in, expected, 3)
