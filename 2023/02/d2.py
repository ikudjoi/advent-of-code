with open("input.txt", "r") as f:
    contents = f.read()

example_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

# contents = example_input

max_cubes = {"red": 12, "green": 13, "blue": 14}


def enough_cubes(cube_set):
    for c, n in max_cubes.items():
        v = cube_set.get(c, 0)
        if v > n:
            return False
    return True


def parse_cube_set(inp_str):
    return {cs.split(" ")[-1]: int(cs.split(" ")[0]) for cs in inp_str.split(", ")}


lines = contents.splitlines()
res = 0
games = {l.split(": ")[0]: l.split(": ")[-1] for l in lines}
for id, g in games.items():
    sets = g.split("; ")
    enough = True
    max_required_cubes = {}
    for s in sets:
        cube_set = parse_cube_set(s)
        if not enough_cubes(cube_set):
            enough = False
            break

    if not enough:
        continue

    print(id)
    n = int(id.split(" ")[-1])
    res += n

print(res)


# part 2
import math

def max_cube_sets(set1, set2):
    return {k: max(set1.get(k, 0), set2.get(k, 0)) for k in set(set1).union(set2)}


res = 0
for id, g in games.items():
    sets = g.split("; ")
    enough = True
    max_required_cubes = {}
    for s in sets:
        cube_set = parse_cube_set(s)
        max_required_cubes = max_cube_sets(max_required_cubes, cube_set)

    res += math.prod(max_required_cubes.values())

print(res)
