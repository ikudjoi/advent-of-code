from aocd import get_data

year, day = [int(v) for v in __file__.split("/")[-3:-1]]
input = get_data(day=day, year=year)


example = """3   4
4   3
2   5
1   3
3   9
3   3
"""
# input = example

a, b = [], []
for line in input.splitlines():
    av, bv = [v for v in line.split(" ") if v]
    a.append(int(av))
    b.append(int(bv))

aso = sorted(a)
bso = sorted(b)

dist = 0
for p in zip(aso, bso):
    av, bv = p
    dist += abs(av - bv)

print(dist)

# part 2

from collections import Counter

bc = Counter(bso)
sim = 0
for av in a:
    sim += av * bc.get(av, 0)

print(sim)
