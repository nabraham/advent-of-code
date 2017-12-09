import math
from collections import defaultdict

#17  16  15  14  13
#18   5   4   3  12
#19   6   1   2  11
#20   7   8   9  10
#21  22  23---> ...

#(25, 5.0, 5, 2.0, [23.0, 19.0, 15.0, 11.0])
#(26, 5.0990195135927845, 5, 2.0, [23.0, 19.0, 15.0, 11.0])

def part1(n):
    s = math.sqrt(n)
    f = math.ceil(s)
    if f % 2 == 0:
        f += 1
    rad = (f - 1) / 2
    poles = [f**2 - rad - i * (2*rad) for i in range(4)]
    pole_dist = [abs(n - p) for p in poles]

    return n,s,f,rad,poles,pole_dist,min(pole_dist) + rad

#147  142  133  122   59
#304    5    4    2   57
#330   10    1    1   54
#351   11   23   25   26
#362  747  806  880

def key(x,y):
    return '<%d,%d>' % (x, y)


def neighbor_sum(g,p):
    s = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            s += g[key(p.x+dx, p.y+dy)]
    return s


def calc_min_max(mmx, p):
    #[minx maxx miny maxy]
    if p.x < mmx[0]:
        mmx[0] = p.x
        return mmx
    elif p.x > mmx[1]:
        mmx[1] = p.x
        return mmx
    if p.y < mmx[2]:
        mmx[2] = p.y
        return mmx
    elif p.y > mmx[3]:
        mmx[3] = p.y
        return mmx
    else:
        return None


class Point:
    def __init__(self, x,y):
        self.x = x
        self.y = y

    def inc(self, v):
        self.x += v[0]
        self.y += v[1]

    def __repr__(self):
        return key(self.x, self.y)

def part2(n):
    p = Point(0,0)
    grid = defaultdict(int)
    grid[str(p)] = 1
    directions = [(1,0), (0,1), (-1,0), (0, -1)]
    di = 0
    min_max = [0, 0, 0, 0]
    while True:
        mmx = calc_min_max(min_max, p)
        if mmx != None:
            di = (di + 1) % 4
            min_max = mmx
        p.inc(directions[di])
        v = neighbor_sum(grid,p)
        grid[str(p)] = v
        if v > n:
            return p, v


if __name__=='__main__':
    import sys
    n = int(sys.argv[1])
    print(part1(n))
    print(part2(n))
