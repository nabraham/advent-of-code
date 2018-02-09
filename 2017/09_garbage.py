import aoc_utils

def main(line, verbose=False):
    ignore_next = False
    in_carrot = False
    depth = 0
    score = 0
    carrot_score = 0
    if verbose:
        print('\n',line)
    for c in list(line):
        if in_carrot:
            if ignore_next:
                ignore_next = False
            elif c == '!':
                ignore_next = True
            elif c == '>':
                in_carrot = False
            else:
                carrot_score += 1
        else:
            if c == '<':
                in_carrot = True
            elif c == '{':
                depth += 1
            elif c == '}':
                score += depth
                depth -= 1
        if verbose:
            print('carrot: %s, ignore: %s, depth: %d, score: %d, carrot_score: %d' % (in_carrot, ignore_next, depth, score, carrot_score))
    return score, carrot_score


def test():
    main('{{{},{},{{}}}}', True)
    main('{<a>,<a>,<a>,<a>}', True)
    main('{{<!>},{<!>},{<!>},{<a>}}', True)


def regular():
    print(main(aoc_utils.get_input()[0]))


if __name__ == '__main__':
    test()
    regular()
