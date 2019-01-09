import aoc_utils
import re
from pprint import pprint
from collections import defaultdict

ids = defaultdict(int)


def get_id(team):
    global ids
    ids[team] += 1
    return '%s-%d' % (team, ids[team])


class System:
    def __init__(self, team, armies):
        self.team = team
        self.armies = armies

    def __repr__(self):
        s = '%s: %d armies' % (self.team, len(self.armies))
        return '\n'.join([s] + ['\t%s has %d units' % (a.id, len(a.units)) for a in self.armies])

    def alive(self):
        return len(self.armies) > 0

    def prune_dead(self):
        self.armies = list(filter(lambda x: x.alive, self.armies))

    def size(self):
        return sum(map(lambda x: len(x.units), self.armies))


class Army:
    def __init__(self, n_units, hit_points, attack_type, attack_damage, initiative, weaknesses, immunities, team):
        self.n_units = n_units
        self.hit_points = hit_points
        self.attack_type = attack_type
        self.attack_damage = attack_damage
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.team = team
        self.units = [hit_points] * n_units
        self.alive = True
        self.id = get_id(self.team)

    def __repr__(self):
        return '%s: EP(%d) U(%d) HP(%d) A(%s) AD(%d) INIT(%d) WK:%s IM:%s' % \
               (self.tid(), self.effective_power(), len(self.units), self.hit_points, self.attack_type,
                self.attack_damage, self.initiative, self.weaknesses, self.immunities)

    def tid(self):
        return self.id

    def damage_against(self, other, verbose=True):
        multiplier = 1
        if self.attack_type in other.immunities:
            multiplier = 0
        elif self.attack_type in other.weaknesses:
            multiplier = 2
        amnt = multiplier * self.effective_power()
        if verbose:
            pass
            # print('%s would deal %d against %s' % (self.tid(), amnt, other.tid()))
        return amnt

    def choose_target(self, system1, system2, existing_targets):
        opposition = system1 if system1.team != self.team else system2
        remaining_armies = list(filter(lambda x: x.id not in existing_targets, opposition.armies))
        zipped = map(lambda x: (x, self.damage_against(x)), remaining_armies)
        filtered = list(filter(lambda x: x[0].id not in existing_targets, zipped))

        if len(filtered) == 0:
            return None

        maxx = max(filtered, key=lambda x: x[1])[1]

        if maxx == 0:
            return None

        top = list(filter(lambda x: x[1] == maxx, filtered))
        if len(top) == 1:
            return top[0][0]

        maxx2 = max(top, key=lambda x: x[0].effective_power())[0].effective_power()
        top2 = list(filter(lambda x: x[0].effective_power() == maxx2, top))
        if len(top2) == 1:
            return top2[0][0]

        return max(top2, key=lambda x: x[0].initiative)[0]

    def attack(self, other_id, system1, system2):
        opposition = system1 if system1.team != self.team else system2
        target_army = list(filter(lambda x: x.id == other_id, opposition.armies))[0]
        target_army.receive_attack(self)

    def receive_attack(self, other):
        amount = other.damage_against(self, False)
        while amount >= self.hit_points and len(self.units) > 0:
            self.units.pop()
            amount -= self.hit_points
        if len(self.units) == 0:
            self.alive = False

    def effective_power(self):
        return len(self.units) * self.attack_damage


unit_rx = re.compile('(\\d+) units each with (\\d+) hit points')
attack_rx = re.compile('with an attack that does (\\d+) (.+) damage at initiative (\\d+)')


def parse_army(line, team, boost=0):
    hit_index = line.find('hit points') + len('hit points')
    with_index = line.find('with an attack')
    units, hp = list(unit_rx.match(line[:hit_index]).groups())
    attack_damage, attack_type, initiative = list(attack_rx.match(line[with_index:]).groups())
    weaknesses = []
    immunities = []
    if '(' in line:
        weak_str = re.split('[\\)\\(]', line)[1]
        parts = weak_str.split('; ')
        for p in parts:
            sub_parts = p.split(' to ')
            if sub_parts[0] == 'weak':
                weaknesses = sub_parts[1].split(', ')
            elif sub_parts[0] == 'immune':
                immunities = sub_parts[1].split(', ')
    return Army(int(units), int(hp), attack_type, int(attack_damage) + boost, int(initiative), weaknesses, immunities,
                team)


def parse_armies(lines, team, boost=0):
    return [parse_army(line, team, boost) for line in lines]


def parse(lines, immune_boost=0):
    whole = '\n'.join(lines)
    immune_str, infection_str = whole.split('\n\n')
    immune = parse_armies(immune_str.split('\n')[1:], 'immune', immune_boost)
    infection = parse_armies(infection_str.split('\n')[1:], 'infection')
    return System('immune', immune), System('infection', infection)


def fight(immune, infection, timeout=-1):
    count = 0
    while immune.alive() and infection.alive() and (timeout < 0 or count < timeout):
        target_order = sorted(immune.armies + infection.armies,
                              key=lambda x: -x.effective_power() - 0.001 * x.initiative)
        targets = dict()
        for army in target_order:
            t = army.choose_target(immune, infection, targets.values())
            if t is not None:
                targets[army.id] = t.id

        attack_order = sorted(immune.armies + infection.armies, key=lambda x: -x.initiative)
        for i, army in enumerate(attack_order):
            if army.alive and army.id in targets:
                army.attack(targets[army.id], immune, infection)
        immune.prune_dead()
        infection.prune_dead()
        count += 1
    return infection.size() + immune.size(), infection.size(), immune.size()


def part1(lines):
    immune, infection = parse(lines)
    return fight(immune, infection)


def part2(lines):
    infection_size = 0
    boost = 60
    rez = []
    while infection_size == 0:
        immune, infection = parse(lines, boost)
        total, infection_size, immune_size = fight(immune, infection, 10000)
        rez.append(immune_size)
        boost -= 1
    return rez[-2]


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    # run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
