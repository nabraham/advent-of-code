import aoc_utils

class PortBridge:
    def __init__(self, h, t, f=False):
        self.head = h
        self.tail = t
        self.flipped = f


    def clone(self, flipped):
        return PortBridge(self.head, self.tail, flipped)


    def end(self):
        return [self.tail, self.head][self.flipped]


    def sum(self):
        return self.head + self.tail


    def __repr__(self):
        return '(%d:%d%s)' % (self.head, self.tail, ['','*'][self.flipped])


    def __hash__(self):
        return hash('%d,%d' % (self.head, self.tail))


    def __eq__(self,other):
        return self.head == other.head and self.tail == other.tail


def main(parts):
    all_set = set().union(parts)

    queue = [[PortBridge(0,0)]]
    all_paths = []
    while len(queue) > 0:
        keep_going = []
        for q in queue:
            tail = q[-1]
            available = all_set - set(q)
            new_queue = []
            for a in available:
                if tail.end() == a.head:
                    new_queue.append(q + [a])
                elif tail.end() == a.tail:
                    new_queue.append(q + [a.clone(True)])

            if len(new_queue) == 0:
                all_paths.append(q)
            else:
                keep_going += new_queue
        queue = keep_going
    return all_paths


def run(filename):
    print('\n' + aoc_utils.file_header(filename))
    input = [tuple(map(int,line.split('/'))) for line in aoc_utils.get_input(filename)]
    bridges = [PortBridge(i[0],i[1]) for i in input]
    all_paths = main(bridges)

    print('PART 1:', max(list(map(lambda p: sum([b.sum() for b in p]), all_paths))))

    sorted_paths = sorted(all_paths, key=lambda p: 100000*len(p) + sum([b.sum() for b in p]), reverse=True)
    print('PART 2:', sorted_paths[0], sum([b.sum() for b in sorted_paths[0]]))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
