with open("input.txt", "r") as f:
    contents = f.read()

example_input = """3   4
4   3
2   5
1   3
3   9
3   3
"""
# contents = example_input

a, b = [], []
for line in contents.splitlines():
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
