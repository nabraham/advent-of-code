import aoc_utils
import re
import matplotlib.pyplot as plt
import numpy as np

line_rx = re.compile('^position=<(.*),(.*)> velocity=<(.*),(.*)>$')

class Star:
    def __init__(self,x,y,vx,vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy


    def update(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy


class Sky:
    def __init__(self, stars):
        self.stars = stars


    def update(self):
        list(map(lambda x: x.update(), self.stars))


    def bounds(self):
        return [min(self.stars, key=lambda s: s.x).x,
                max(self.stars, key=lambda s: s.x).x,
                min(self.stars, key=lambda s: s.y).y,
                max(self.stars, key=lambda s: s.y).y]


    def area(self):
        b = self.bounds()
        return (b[1] - b[0]) * (b[3] - b[2])


    def draw(self):
        if self.area() < 4000000:
            b = self.bounds()
            mat = np.zeros((b[3] - b[2] + 1, b[1] - b[0] + 1), dtype=int)
            for s in self.stars:
                mat[(s.y - b[2], s.x - b[0])] = 1
            return mat
        return None


def display_capture(c, index, title):
    plt.subplot(index)
    plt.imshow(c, cmap='Greys',  interpolation='nearest')
    plt.title(title)


def part1(lines):
    stars = []
    for line in lines:
        match = line_rx.match(line)
        stars.append(Star(*map(int, match.groups())))

    sky = Sky(stars)
    prev_area = None
    area = sky.area()
    captures = []

    while prev_area is None or area < prev_area:
        prev_area = area
        sky.update()
        area = sky.area()
        captures.append(sky.draw())

    return captures[-2], len(captures) - 1


def run(filename):
    lines = aoc_utils.get_input(filename)
    return part1(lines)


if __name__ == '__main__':
    t, ti = run(aoc_utils.puzzle_test())
    m, mi = run(aoc_utils.puzzle_main())
    display_capture(t, 211, 'time = %d' % ti)
    display_capture(m, 212, 'time = %d' % mi)
    plt.show()
