from pprint import pprint


def increment(firewall):
    for layer in firewall:
        firewall[layer][1] += firewall[layer][2]
        if (firewall[layer][1] + 1) == firewall[layer][0] or firewall[layer][1] == 0:
            firewall[layer][2] *= -1


def print_firewall(fw, score, verbose=False):
    if verbose:
        print('Score:', score)
        pprint(fw)
        print()


def part1(firewall, size, verbose=False):
    score = 0
    for i in range(size+1):
        if i in firewall and firewall[i][1] == 0:
            score += i * firewall[i][0]
        increment(firewall)
        print_firewall(firewall, score, verbose)
    return score

def part2(firewall):
    scanners = sorted([(s, firewall[s][0]) for s in firewall], key=lambda x: x[0])
    delay = 0
    failing = True
    while failing:
        failing = False
        for scanner in scanners:
            if (scanner[0] + delay) % (2 * (scanner[1]-1)) == 0:
                failing = True
                delay += 1
                break
    return delay


def run_file(filename, verbose=False):
    print('\n%s\n%s' % (filename, '-'*len(filename)))
    firewall = {}
    with open(filename) as f:
        for line in f.readlines():
            parts = [int(x) for x in line.strip('\n').split(':')]
            size = parts[0]
            firewall[parts[0]] = [parts[1], 0, 1]  #depth, scanner index, direction

        #PART 1
        print('Score:', part1(firewall, size, verbose))

        #PART 2
        print('Delay:', part2(firewall))


if __name__ == '__main__':
    run_file('data/13_test.txt', True)
    run_file('data/13.txt')
