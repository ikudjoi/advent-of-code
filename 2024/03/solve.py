from aocd import get_data
import re


year, day = [int(v) for v in __file__.split("/")[-3:-1]]
input = get_data(day=day, year=year)
example = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
# input = example

pat = re.compile(r"mul\(\d{1,3},\d{1,3}\)")

def calc_prod(val):
    matches = pat.findall(val)
    prod = 0
    for m in matches:
        a, b = [int(v) for v in m[4:-1].split(",")]
        prod += a * b
    return prod


# part1
print(calc_prod(input))

# part2

example2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
# input = example2

split_by_do = input.split("do()")
filtered = [v.split("don't()", 1)[0] for v in split_by_do]
print(calc_prod("|".join(filtered)))
