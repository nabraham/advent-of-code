from collections import Counter

def valid(line):
    c = Counter(line.split(' '))
    return max(c.values()) == 1


def valid_ana(line):
    parts = list(map(lambda x: ''.join(sorted(list(x))), line.split(' ')))
    c = Counter(parts)
    return max(c.values()) == 1


def solve(lines):
    return [
        len(list(filter(valid, lines))), 
        len(list(filter(valid_ana, lines)))
    ]


if __name__ == '__main__':
    with open('data/04.txt') as f:
        print(solve([line.strip('\n') for line in f.readlines()]))
