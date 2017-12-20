import re
import numpy as np

class Particle:
    def __init__(self, i, p, v, a):
        self.id = i
        self.position = p
        self.velocity = v
        self.acceleration = a

    def step(self):
        self.velocity += self.acceleration
        self.position += self.velocity

    def dist(self):
        return sum(abs(self.position))

    def __repr__(self):
        return '%d - %s' % (self.id, self.position)

def main(particles, N_SUCCESS=1000, N_FAIL=100000):
    MAXX = 2**31-1
    last_min = -1
    min_particle = -1
    same_count = 0
    sim_count = 0
    while True:
        sim_count += 1
        min_dist = MAXX
        for p in particles:
            p.step()
            if p.dist() < min_dist:
                min_dist = p.dist()
                min_particle = p.id

        if min_particle == last_min:
            same_count += 1
            if same_count == N_SUCCESS:
                return min_particle
        else:
            print('[%d] - New min: %d' % (sim_count, min_particle))
            last_min = min_particle
            same_count = 0

        if sim_count == N_FAIL:
            print('Failed after %d simulations' % N_FAIL)
            return -1

def run(filename):
    print('%s\n%s' % (filename, '-'*len(filename)))
    with open(filename) as f:
        particles = []
        for i, line in enumerate(f.readlines()):
            parts = re.split('[><]', line)
            p = np.array([int(x) for x in parts[1].split(',')])
            v = np.array([int(x) for x in parts[3].split(',')])
            a = np.array([int(x) for x in parts[5].split(',')])
            particles.append(Particle(i, p, v, a))
        print('\n'.join(map(str, particles[:5])))

if __name__ == '__main__':
    run('data/20.txt')
