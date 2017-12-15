def generator(factor, maxx=2147483647):
    def next(prev):
        return (prev*factor) % maxx
    return next


def main(a, b, a_mult=-1, b_mult=-1, N=40000000, a_fact=16807, b_fact=48271):
    genA = generator(a_fact)
    genB = generator(b_fact)
    match = 0
    mask = (0xFF << 8) + 0xFF
    for i in range(N):
        a = genA(a)
        b = genB(b)
        if a_mult > 0:
            while a % a_mult != 0:
                a = genA(a)
            while b % b_mult != 0:
                b = genB(b)

        match += [0, 1][(mask & a) == (mask & b)]
    return match

if __name__ == '__main__':
    #example
    #print(main(65, 8921))
    #print(main(65,8921,4,8,2000))
    #print(main(65,8921,4,8,5000000))
   
    #PART 1
    #print(main(634,301))

    #PART 2
    print(main(634,301,4,8,5000000))


