from aocd import get_data

input = get_data(day=2, year=2024)

example = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

example2 = """48 46 47 49 51 54 56
1 1 2 3 4 5
1 2 3 4 5 5
5 1 2 3 4 5
1 4 3 2 1
1 6 7 8 9
1 2 3 4 3
9 8 7 6 7
7 10 8 10 11
29 28 27 25 26 25 22 20 
"""

# input = example2


def report_safe(vals):
    prev_val = vals[0]
    asc = None
    for v in vals[1:]:
        if not (1 <= abs(prev_val - v) <= 3):
            return False

        v_asc = (v - prev_val) > 0
        prev_val = v
        if asc is None:
            asc = v_asc
            continue

        if v_asc != asc:
            return False

    return True


def damp(vals, problem_ix):
    alt_vals = vals.copy()
    del alt_vals[problem_ix]
    if report_safe(alt_vals):
        return True

    alt_vals = vals.copy()
    del alt_vals[problem_ix - 1]
    return report_safe(alt_vals)


def report_safe2(vals):
    # Check if removing first item helps
    if report_safe(vals[1:]):
        return True

    prev_val = vals[0]
    asc = None
    for ix, v in enumerate(vals[1:]):
        if not (1 <= abs(prev_val - v) <= 3):
            return damp(vals, ix+1)

        v_asc = (v - prev_val) > 0
        prev_val = v
        if asc is None:
            asc = v_asc
            continue

        if v_asc != asc:
            return damp(vals, ix+1)

    return True


def report_safe3(vals):
    # Check if removing first item helps
    if report_safe(vals[1:]):
        return True

    skipped = False
    prev_val = vals[0]
    asc = None
    for ix, v in enumerate(vals[1:]):
        if not (1 <= abs(prev_val - v) <= 3):
            if skipped:
                return False
            skipped = True
            continue

        v_asc = (v - prev_val) > 0
        if asc is None:
            asc = v_asc
            prev_val = v
            continue

        if v_asc != asc:
            if skipped:
                return False

            skipped = True
            continue

        prev_val = v

    return True


num_safe = 0
num_safe2 = 0
for line in input.splitlines():
    vals = [int(i) for i in line.split()]
    if report_safe(vals):
        num_safe += 1
    if report_safe2(vals):
        num_safe2 += 1

print(num_safe)
print(num_safe2)
