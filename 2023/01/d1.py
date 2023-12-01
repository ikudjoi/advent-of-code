import re

with open("input.txt", "r") as f:
    contents = f.read()

sum = 0
for line in contents.splitlines():
    parsed_line = re.sub("\D", "", line)
    d = int(parsed_line[0] + parsed_line[-1])
    sum += d

print(sum)

# part 2

sum = 0
spat = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
spatm = {s: str(i+1) for i, s in enumerate(spat)}
dpatm = {str(i+1): str(i+1) for i in range(9)}
patm = dict(spatm, **dpatm)

for line in contents.splitlines():
    min_indices = {}
    max_indices = {}
    for to_replace, replacement in patm.items():
        try:
            i = line.index(to_replace)
            min_indices[i] = replacement
            ri = line.rindex(to_replace)
            max_indices[ri] = replacement
        except ValueError:
            continue
    mi = min(min_indices)
    miv = min_indices[mi]
    ma = max(max_indices)
    mav = max_indices[ma]
    v = int(miv+mav)
    sum += v

print(sum)