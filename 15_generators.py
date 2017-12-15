def generator(factor, modulus=-1, maxx=2147483647):
    def next(prev):
        nxt = (prev*factor) % maxx
        if modulus > 0:
            while nxt % modulus != 0:
                nxt = (nxt * factor) % maxx
        return nxt
    return next


def main(a, b, a_mod=-1, b_mod=-1, N=40000000, a_fact=16807, b_fact=48271):
    genA = generator(a_fact, a_mod)
    genB = generator(b_fact, b_mod)
    match = 0
    mask = (0xFF << 8) + 0xFF
    for i in range(N):
        a = genA(a)
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
