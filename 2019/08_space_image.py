import aoc_utils
from functools import reduce
from pprint import pprint

# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def part1(lines, cols, rows):
    data = [int(x) for x in list(lines[0])]
    layers = chunks(data, cols * rows)
    layer = min(layers, key=lambda x: x.count(0))
    return layer.count(1) * layer.count(2)


def part2(lines, cols, rows):
    data = [int(x) for x in list(lines[0])]
    layers = list(chunks(data, cols * rows))
    out = []
    for i in range(cols*rows):
        pixels_i = map(lambda x: x[i], layers)
        out_pix = reduce(lambda x,y: y if x == 2 else x, pixels_i)
        out.append(out_pix if out_pix < 2 else 0)
    picture = list(chunks(out, cols))
    WHITE=u'\u2588'
    return '\n'.join([''.join([WHITE if c == 1 else ' ' for c in row]) for row in picture])
            


def run(filename, cols, rows):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines, cols, rows))
    print(part2(lines, cols, rows))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test(), 3 , 2)
    run(aoc_utils.puzzle_main(), 25, 6)
