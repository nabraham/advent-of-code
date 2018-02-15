import aoc_utils
import numpy as np
import re

class Screen:
    pixels = None

    def __init__(self, m=6, n=50):
        self.pixels = np.matrix([[0] * n] * m)


    def __repr__(self):
        return '\n'.join([''.join(map(lambda x: '.#'[x], r.tolist()[0])) for r in self.pixels]) + '\n'


    def rect(self, a, b):
        for i in range(b):
            for j in range(a):
                self.pixels[i,j] = 1


    def rotate(self, rowcol, index, amnt):
        if rowcol == 'row':
            r = self.pixels[index,:]
            rolled = np.roll(r, amnt, axis=1)
            self.pixels[index,:] = rolled
        elif rowcol == 'column':
            c = self.pixels[:,index]
            rolled = np.roll(c, amnt, axis=0)
            self.pixels[:,index] = rolled
        else:
            raise Exception('bad rotation: ' + rowcol)


def process_command(screen, cmd):
    if 'rect' in cmd:
        parts = re.split('[x ]', cmd)
        screen.rect(int(parts[1]), int(parts[2]))
    elif 'rotate' in cmd:
        parts = re.split('[= ]', cmd)
        screen.rotate(parts[1], int(parts[3]), int(parts[5]))
    else:
        raise Exception('bad command: ' + cmd)


def run(filename):
    print('\n' + aoc_utils.file_header(filename))
    input = aoc_utils.get_input(filename)
    s = Screen()
    for i, cmd in enumerate(input):
        process_command(s, cmd)
    print(np.sum(s.pixels))
    print(s)
    

if __name__ == '__main__':
    run(aoc_utils.puzzle_main())
