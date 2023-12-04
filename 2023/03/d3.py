with open("input.txt", "r") as f:
    contents = f.read()

example_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

# contents = example_input


def num_ranges(line):
    res = []
    parsing_num = False
    start = None
    for x, c in enumerate(line):
        if parsing_num:
            parsing_num = c.isdigit()
            if not parsing_num:
                end = x-1
                res.append((start, end))
        else:
            parsing_num = c.isdigit()
            if parsing_num:
                start = x
    if parsing_num:
        res.append((start, x))
    return res


lines = contents.splitlines()


def is_engine_part(ls, y, x1, x2):
    u_min, u_max = y-1, y+1
    v_min, v_max = x1-1, x2+1
    for u in range(u_min, u_max+1):
        for v in range(v_min, v_max+1):
            # Skip inside
            if u not in (u_min, u_max) and v not in (v_min, v_max):
                continue

            # I'm relying on IndexError too by Python has special handling for neg indices
            if u < 0 or v < 0:
                continue

            try:
                c = ls[u][v]
            except IndexError:
                continue
            if c != ".":
                return True

    return False


res = 0
for y, line in enumerate(lines):
    nrs = num_ranges(line)
    for nr in nrs:
        s, e = nr
        v = int(line[s:e+1])
        if is_engine_part(lines, y, s, e):
            res += v

print(res)

# part 2


def star_locations(ls, y, x1, x2):
    u_min, u_max = y-1, y+1
    v_min, v_max = x1-1, x2+1
    res = []
    for u in range(u_min, u_max+1):
        for v in range(v_min, v_max+1):
            # Skip inside
            if u not in (u_min, u_max) and v not in (v_min, v_max):
                continue

            # I'm relying on IndexError too by Python has special handling for neg indices
            if u < 0 or v < 0:
                continue

            try:
                c = ls[u][v]
            except IndexError:
                continue
            if c == "*":
                res.append((u,v))

    return res


star_values = {}
for y, line in enumerate(lines):
    nrs = num_ranges(line)
    for nr in nrs:
        s, e = nr
        v = int(line[s:e+1])
        stars = star_locations(lines, y, s, e)
        for star in stars:
            adjacent_values = star_values.pop(star, [])
            adjacent_values.append((v, s, y))
            star_values[star] = adjacent_values

filtered_parts = {k: v for k, v in star_values.items() if len(v) == 2}
res = 0
for star, pair in filtered_parts.items():
    part1, part2 = pair
    res += part1[0]*part2[0]

print(res)