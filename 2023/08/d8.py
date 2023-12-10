import math

with open("input.txt", "r") as f:
    contents = f.read()

example_input = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

example_input2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

# contents = example_input
# contents = example_input2

instr, coords = contents.split("\n\n")
coords = {l.split(" = ")[0]: l.split(" = ")[1] for l in coords.splitlines()}
coords = {k: v[1:-1].split(", ") for k, v in coords.items()}


def measure_steps(start_coord, end_condition):
    current_coord = start_coord
    cntr = 0
    while (True):
        for i in instr:
            cntr += 1
            alternatives = coords[current_coord]
            current_coord = alternatives[0] if i == "L" else alternatives[1]
            if end_condition(current_coord):
                return cntr, current_coord


print(measure_steps("AAA", lambda v: v == "ZZZ"))


# part 2
start_coords = [k for k in coords.keys() if k[-1] == "A"]
end_coords = [k for k in coords.keys() if k[-1] == "Z"]
a_to_z = {sc: measure_steps(sc, lambda v: v[-1] == "Z") for sc in start_coords}
z_to_z = {ec: measure_steps(ec, lambda v: v[-1] == "Z") for ec in end_coords}  # Loop!!!

a_to_z_combined = {sc: (dist_ec[0], z_to_z[dist_ec[1]][0]) for sc, dist_ec in a_to_z.items()}
steps_to_z = [i[1] for i in a_to_z_combined.values()]


print(math.lcm(*steps_to_z))
