import math
from functools import reduce


def knot(values, index, length):
    half = math.floor(length/2)
    for h in range(half):
        i = (index + h) % len(values)
        j = (index + length - h - 1) % len(values)
        tmp = int(values[i])
        values[i] = int(values[j])
        values[j] = tmp
    return values


def main(values, lengths, iters=1, verbose=False):
    i = 0
    skip_size = 0
    for n in range(iters):
        if verbose:
            print('%d - %s' % (n, values[:10]))
        for length in lengths:
            values = knot(values, i, length)
            i = (i + length + skip_size) % len(values)
            skip_size += 1
    return values


if __name__ == '__main__':
    with open('data/10.txt') as f:
        line = f.readlines()[0]

        #PART 1
        lengths = [int(x) for x in line.split(',')]
        values = main(list(range(256)), lengths)
        print(values[0] * values[1])

        #PART 2
        lengths2 = [ord(c) for c in line.strip('\n')] + [17, 31, 73, 47, 23]
        values2 = main(list(range(256)), lengths2, 64)
        blocks = [values2[16*b:16*(b+1)] for b in range(16)]
        chars = [hex(reduce(lambda x,y: x ^ y, b))[2:] for b in blocks]
        print(''.join(chars))
