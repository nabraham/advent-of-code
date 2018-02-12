import aoc_utils

ULDR = {'U': [-1,0], 'L': [0,-1], 'D': [1,0], 'R': [0,1]}

def move(pos, m):
    return [pos[0] + m[0], pos[1] + m[1]]


def valid(pos, pad):
    return pos[0] >= 0 and \
           pos[0] < len(pad) and \
           pos[1] >= 0 and \
           pos[1] < len(pad[pos[0]]) and \
           pad[pos[0]][pos[1]] != '.'


def run(filename, keypad, start):
    pad = keypad.split(',')
    print('\n' + aoc_utils.file_header(filename))
    input = aoc_utils.get_input(filename)
    pos = start
    code = list()
    for row in input:
        for char in row:
            step = move(pos, ULDR[char])
            if valid(step, pad):
                pos = step
        code.append(pad[pos[0]][pos[1]])
    print(''.join(map(str,code)))
        

if __name__ == '__main__':
    pad = '123,456,789'
    start = [1,1]
    run(aoc_utils.puzzle_test(), pad, start)
    run(aoc_utils.puzzle_main(), pad, start)

    pad = '..1..,.234.,56789,.abc.,..d..'
    start = [2,0]
    run(aoc_utils.puzzle_test(), pad, start)
    run(aoc_utils.puzzle_main(), pad, start)
