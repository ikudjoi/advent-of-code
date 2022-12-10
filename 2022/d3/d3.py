with open('input.txt', 'r') as f:
    contents = f.read()

example_input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

# contents = example_input
prio_sum = 0


def item_prio(input_char):
    ascii_num = ord(input_char)
    if input_char == input_char.lower():
        return ascii_num - 96
    else:
        return ascii_num - 64 + 26


for line in contents.splitlines():
    half = int(len(line)/2)
    comp1 = line[:half]
    comp1c = set([c for c in comp1])
    comp2 = line[half:]
    comp2c = set([c for c in comp2])

    match = list(comp1c.intersection(comp2c))[0]
    prio = item_prio(match)
    prio_sum += prio

print(prio_sum)

# part 2

comps = contents.splitlines()
prio_sum = 0
n = 3
chunks3 = list(comps[i:i+n] for i in range(0, len(comps), n))
for chunk in chunks3:
    sets = [set([c for c in line]) for line in chunk]
    match = list(sets[0].intersection(*sets[1:]))[0]
    prio = item_prio(match)
    prio_sum += prio

print(prio_sum)
