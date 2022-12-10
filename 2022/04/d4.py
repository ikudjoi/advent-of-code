with open('input.txt', 'r') as f:
    contents = f.read()

example_input = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

# contents = example_input
totally_included = 0
overlap = 0

for pair_line in contents.splitlines():
    elf1, elf2 = pair_line.split(',')
    range1 = [int(n) for n in elf1.split('-')]
    range2 = [int(n) for n in elf2.split('-')]

    if ((range1[0] >= range2[0] and range1[1] <= range2[1])
        or (range2[0] >= range1[0] and range2[1] <= range1[1])):
        totally_included += 1

    if range1[0] <= range2[1] and range2[0] <= range1[1]:
        overlap += 1

print(totally_included)

# part 2
print(overlap)