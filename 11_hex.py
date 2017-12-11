# Use a tilted coordinate system
# 0,0
# 
#       1,0
# 
# 0,1         2,0
# 
#       1,1          3,0
# 
# 0,2         2,1          4,0  
# 
#       1,2          3,1        5,0
# 
# 0,3          2,2         4,1  
# 
#  N: y-1                  
# SE: x+1,
# NE: x+1,y-1

class Cell:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


    def move(self, d):
        if d not in 'n,s,ne,se,nw,sw':
            raise Exception('invalid direction')

        if d in ['n','ne']:
            self.y -=1
        elif d in ['s', 'sw']:
            self.y += 1

        if 'w' in d:
            self.x -= 1
        elif 'e' in d:
            self.x += 1


    def distance(self, other_x=0, other_y=0):
        dx = other_x - self.x
        dy = other_y - self.y
        if dx * dy > 0:
            return abs(dx + dy)
        else:
            return max(abs(dx), abs(dy))


    def __repr__(self):
        return '(%d,%d)' % (self.x,self.y)


def main(movements):
    moves = movements.split(',')
    c = Cell()
    distances = []
    for m in moves:
        c.move(m)
        distances.append(c.distance())
    return c, distances[-1], max(distances)


if __name__ == '__main__':
    with open('data/11.txt') as f:
        line = f.readlines()[0].strip('\n')
        print(main(line))
