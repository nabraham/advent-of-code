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

    def hash(self):
        return '%s' % self.position

    def __repr__(self):
        return '%d - %s %s %s' % (self.id, self.position, self.velocity, self.acceleration)


def part2(particles, N_SUCCESS=50, N_FAIL=100000):
    no_collision_count = 0
    sim_count = 0
    while sim_count < N_FAIL:
        sim_count += 1
        collisions = set()
        seen = set()

        for p in particles:
            p.step()
            if p.hash() in seen:
                collisions.add(p.hash())
            seen.add(p.hash())

        if len(collisions) > 0:
            particles = list(filter(lambda p: p.hash() not in collisions, particles))
            print('%d - New particle list size: %d' % (sim_count, len(particles)))
            no_collision_count = 0
        else:
            no_collision_count += 1
        
        if no_collision_count == N_SUCCESS:
            return len(particles)

    print('Failed after %d simulations' % N_FAIL)
    return -1


def part1(particles, N_SUCCESS=500, N_FAIL=100000):
    MAXX = 2**31-1
    last_min = -1
    min_particle = -1
    same_count = 0
    sim_count = 0
    while sim_count < N_FAIL:
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
            print('%d - New min: %d' % (sim_count, min_particle))
            last_min = min_particle
            same_count = 0

    print('Failed after %d simulations' % N_FAIL)
    return -1

def create_particles(lines):
    particles = []
    for i, line in enumerate(lines):
        parts = re.split('[><]', line)
        p = np.array([int(x) for x in parts[1].split(',')])
        v = np.array([int(x) for x in parts[3].split(',')])
        a = np.array([int(x) for x in parts[5].split(',')])
        particles.append(Particle(i, p, v, a))
    return particles


def run(filename):
    print('%s\n%s' % (filename, '-'*len(filename)))
    with open(filename) as f:
        lines = f.readlines()
        print(part1(create_particles(lines)))
        print(part2(create_particles(lines)))

if __name__ == '__main__':
    run('data/20.txt')
