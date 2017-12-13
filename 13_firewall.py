def hit(scanner, delay=0):
    return (scanner[0]+delay) % (2*(scanner[1]-1)) == 0


def part1(scanners):
    hits = filter(hit, scanners)
    score = sum(map(lambda s: s[0]*s[1], hits))
    return score


# iterating over part 1 took too long; need to short circuit failing attempts
def part2(scanners):
    delay = 0
    failing = True
    while failing:
        failing = False
        for scanner in scanners:
            if hit(scanner, delay):
                failing = True
                delay += 1
                break
    return delay


def parse_line(line):
    return [int(x) for x in line.strip('\n').split(':')]


def run_file(filename, verbose=False):
    print('\n%s\n%s' % (filename, '-'*len(filename)))
    with open(filename) as f:
        firewall = list(map(parse_line, f.readlines()))
        print('Score:', part1(firewall))
        print('Delay:', part2(firewall))


if __name__ == '__main__':
    run_file('data/13_test.txt', True)
    run_file('data/13.txt')
