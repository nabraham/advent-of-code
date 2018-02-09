import aoc_utils
from pprint import pprint

def run(filename):
    print('\n' + aoc_utils.file_header(filename))
    input = aoc_utils.get_input(filename)
    pprint(input)

if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
