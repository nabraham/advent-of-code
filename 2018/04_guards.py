from collections import defaultdict, namedtuple
from datetime import timedelta
from dateutil import parser
from pprint import pprint
import aoc_utils
import operator
import re

start_rx = re.compile('\[(.*)\] Guard #(\d+) begins shift')
falls_rx = re.compile('\[(.*)\] falls asleep')
wakes_rx = re.compile('\[(.*)\] wakes up')
Shift = namedtuple('Shift', ['guard', 'start', 'stop'])


def part1(lines):
    shifts = parse_log(lines)
    totals = calc_totals(shifts)
    max_guard = max(totals.items(), key=operator.itemgetter(1))[0]
    return max_guard * max_minute(shifts, max_guard)


def part2(lines):
    shifts = parse_log(lines)
    minutes = guard_to_minute_counts(shifts)
    max_minute = calc_max_minute(minutes)
    return max_minute[0] * max_minute[1][0]


# ( <guard>, ( <minute>, <count> ) )
def calc_max_minute(guard_to_minutes):
    max_per_guard = map(lambda x: (x[0], max(x[1].items(), key=operator.itemgetter(1))),
                        guard_to_minutes.items())
    return max(max_per_guard, key=lambda x: x[1][1])
    
    
# { <guard>: { <minute> : <count> } }
def guard_to_minute_counts(shifts):
    minutes = defaultdict(lambda: defaultdict(int))
    for s in shifts:
        curr = s.start
        while curr < s.stop:
            minutes[s.guard][curr.minute] += 1
            curr += timedelta(minutes=1)
    return minutes


def max_minute(shifts, guard):
    guard_shifts = filter(lambda x: x.guard == guard, shifts)
    minute_counts = guard_to_minute_counts(guard_shifts)
    return max(minute_counts[guard].items(), key=operator.itemgetter(1))[0]


# { <guard> : <total_minutes> }
def calc_totals(shifts):
    total = defaultdict(int)
    for s in shifts:
        delta = s.stop - s.start
        minutes = delta.seconds/60 - 1
        total[s.guard] += int(minutes)
    return total


def parse_log(lines):
    guard = -1
    falls = -1
    wakes = -1
    shifts = []

    for line in sorted(lines, key=lambda x: x[:17]):
        start_match = start_rx.match(line)
        falls_match = falls_rx.match(line)
        wakes_match = wakes_rx.match(line)
        if start_match:
            guard = int(start_match.group(2))
        elif falls_match:
            falls = parser.parse(falls_match.group(1))
        elif wakes_match:
            wakes = parser.parse(wakes_match.group(1))
            shifts.append(Shift(guard, falls, wakes))

    return shifts
            

def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
