from functools import cache

from aocd import get_data

year, day = [int(v) for v in __file__.split("/")[-3:-1]]
input = "125 17"


input = get_data(day=day, year=year)


stones = [int(s) for s in input.split()]


@cache
def blink_stone_once(v):
    if v == 0:
        return [1]

    vs = str(v)
    lvs = len(vs)
    if lvs % 2 == 0:
        hlvs = int(lvs/2)
        v1 = int(vs[:hlvs])
        v2 = int(vs[hlvs:])
        return [v1, v2]

    return [v*2024]


@cache
def stone_count_blink_n(v, n):
    if n == 1:
        return len(blink_stone_once(v))

    child_stones = blink_stone_once(v)
    res = 0
    for cs in child_stones:
        res += stone_count_blink_n(cs, n-1)

    return res


# part 1
r1 = 0
for s in stones:
    r1 += stone_count_blink_n(s, 25)
print(r1)

# part 2
r2 = 0
for s in stones:
    r2 += stone_count_blink_n(s, 75)
print(r2)
