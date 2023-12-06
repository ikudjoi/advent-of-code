import math

with open("input.txt", "r") as f:
    contents = f.read()

example_input = """Time:      7  15   30
Distance:  9  40  200
"""

# contents = example_input
parsed_lines = [l.split(" ") for l in contents.splitlines()]
times, record_distances = [[int(i) for i in l if i.isdigit()] for l in parsed_lines]


def num_faster_solutions(time_available, record_distance):
    sqrt_term = math.sqrt(time_available*time_available-4*record_distance)
    solution_1 = (time_available-sqrt_term)/2
    solution_1 = int(solution_1+1 if int(solution_1) == solution_1 else math.ceil(solution_1))
    solution_2 = (time_available+sqrt_term)/2
    solution_2 = int(solution_2-1 if int(solution_2) == solution_2 else math.floor(solution_2))
    return solution_2 - solution_1 + 1


res = 1
for t, rd in zip(times, record_distances):
    ns = num_faster_solutions(t, rd)
    res *= ns

print(res)

# part 2
total_time = int("".join([str(t) for t in times]))
total_record_distance = int("".join([str(d) for d in record_distances]))
print(num_faster_solutions(total_time, total_record_distance))
