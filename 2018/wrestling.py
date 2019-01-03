from z3 import And, Distinct, If, Int, Not, Solver, Sum
from string import ascii_uppercase

team_range = list(range(10))
A, B, C, D, E, F, G, H, I, J = team_range
# Forbidden matchups
FORBIDDEN = [(A,E), (B,C), (D,I), (F,J), (G, H)]
# Specific Byes (0-indexed)
SPECIFIC_BYES = [(G,3), (H,3), (J,4)]
# Specific matchups
SPECIFIC_MATCHUPS = [(C,F,0)]

# Tensor of matches (10 rounds x 4 matches x 2 teams)
X = [[[Int('x_%d_%d_%d' % (r, i, j)) for j in range(2)] for i in range(4)] for r in range(10)]

# Teams are 1-10
number_c = [And(0 <= X[r][i][j], X[r][i][j] < 10) for r in range(10) for i in range(4) for j in range(2)]

# Lowest number team is first -- useful for forbidden matchups
ordered_c = [(X[r][i][0] < X[r][i][1]) for r in range(10) for i in range(4)]

# Team plays once per round
round_c = [Distinct([X[r][i][j] for i in range(4) for j in range(2)]) for r in range(10)]

# Teams that cannot play each other
forbidden_c = [Not(And(X[r][i][0] == f[0], X[r][i][1] == f[1])) for r in range(10) for i in range(4) for f in FORBIDDEN]

# Play 8 of 9 teams (no repeats)
repeat_c = Distinct([(10 * X[r][i][0] + X[r][i][1]) for r in range(10) for i in range(4)])

# Each team has two byes (appears in 8 rounds)
byes_c = [8 == Sum([If(X[r][i][j] == t, 1, 0) for r in range(10) for i in range(4) for j in range(2)]) for t in team_range]

# 1+ bye on saturday (r=4...9)
sat_c = [6 > Sum([If(X[r][i][j] == t, 1, 0) for r in range(4,10) for i in range(4) for j in range(2)]) for t in team_range]

# Specific byes
spec_byes_c = [Not(X[r][i][j] == team) for team, r in SPECIFIC_BYES for i in range(4) for j in range(2)]

# Specific matchups
spec_match_c = [1 == Sum([If(And(X[r][i][0] == t1, X[r][i][1] == t2), 1, 0) for i in range(4)]) for t1, t2, r in SPECIFIC_MATCHUPS]

wrestling_c = number_c + ordered_c + round_c + forbidden_c + [repeat_c] + byes_c + sat_c + spec_byes_c + spec_match_c
s = Solver()
s.add(wrestling_c)
s.check()
m = s.model()

for r in range(10):
    print('\nround =', r+1)
    for i in range(4):
        print(ascii_uppercase[int(str(m.evaluate(X[r][i][0])))], ascii_uppercase[int(str(m.evaluate(X[r][i][1])))])
