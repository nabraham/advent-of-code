class Cell:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def clone(self):
        return Cell(self.x, self.y)

    def odd(self):
        return self.x % 2

    def even(self):
        return not self.odd()

    def move(self, d):
        if d not in 'n,s,ne,se,nw,sw':
            raise Exception('invalid direction')
        
        if 'n' == d or ('n' in d and self.odd()):
            self.y += 1
        elif 's' == d or ('s' in d and self.even()):
            self.y -= 1

        if 'e' in d:
            self.x += 1
        elif 'w' in d:
            self.x -= 1

    def equal(self, other):
        return self.x == other.x and self.y == other.y

    def distance(self, other):
        copy = self.clone()
        dist = 0
        while not copy.equal(other):
            dist += 1
            dx = other.x - copy.x
            dy = other.y - copy.y
            NS = 'ns'[dy < 0]
            EW = ['ew'[dx < 0], ''][dx == 0]
            copy.move(NS+EW)
        return dist


    def __repr__(self):
        return '(%d,%d)' % (self.x,self.y)

def main(movements):
    moves = movements.split(',')
    origin = Cell(0,0)
    c = Cell(0,0)
    distances = []
    for m in moves:
        c.move(m)
        distances.append(c.distance(origin))

    return distances[-1], max(distances)

if __name__ == '__main__':
    with open('data/11.txt') as f:
        line = f.readlines()[0].strip('\n')
        print(main(line))
