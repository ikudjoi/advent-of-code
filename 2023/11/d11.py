import itertools

with open("input.txt", "r") as f:
    contents = f.read()

example_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

# contents = example_input
galaxies = []
lines = contents.splitlines()
empty_x = set(range(len(lines[0])))
empty_y = set()
for y, line in enumerate(lines):
    line_chars = {x: c for x, c in enumerate(line)}
    row_galaxies = [(x, y) for x, c in line_chars.items() if c == "#"]
    galaxies += row_galaxies
    empty_cells = set([x for x, c in line_chars.items() if c == "."])
    empty_x = empty_x.intersection(empty_cells)
    if not row_galaxies:
        empty_y.add(y)


total_distance = 0
pairs = 0
for g1, g2 in itertools.combinations(galaxies, 2):
    pairs += 1
    minimums = [min(v) for v in zip(g1, g2)]
    maximums = [max(v) for v in zip(g1, g2)]
    relevant_empty_x = [x for x in empty_x if minimums[0] < x < maximums[0]]
    relevant_empty_y = [y for y in empty_y if minimums[1] < y < maximums[1]]
    naive_g_euklid_dist = sum([vmax-vmin for vmin, vmax in zip(minimums, maximums)])
    g_dist = naive_g_euklid_dist + 999999*len(relevant_empty_x) + 999999*len(relevant_empty_y)
    total_distance += g_dist

print(total_distance)
