from aocd import get_data

year, day = [int(v) for v in __file__.split("/")[-3:-1]]
input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

input = get_data(day=day, year=year)


def apply_op(v1, v2, op):
    if op == "+":
        return v1 + v2
    return v1*v2

def test_facs2(test_val, x, y, conc):
    if test_val == x*y or test_val == x+y:
        return True
    if not conc:
        return False

    return str(test_val) == str(x) + str(y)

def test_facs(test_val, facs, conc):
    if test_val <= 0:
        return False

    if len(facs) == 2:
        return test_facs2(test_val, *facs, conc)

    last_fac = facs[-1]
    d = test_val/last_fac
    reduced_facs = facs[:-1]

    last_is_plus_test_result = test_facs(test_val-last_fac, reduced_facs, conc)
    if last_is_plus_test_result:
        return True

    last_is_prod_test_result = (d == int(d)) and test_facs(int(d), reduced_facs, conc)
    if last_is_prod_test_result:
        return True

    if not conc:
        return False

    test_val_s = str(test_val)
    last_fac_s = str(last_fac)
    if not test_val_s.endswith(last_fac_s):
        return False

    reduced_test_val = int(test_val_s[:-len(last_fac_s)])
    last_is_conc_test_result = test_facs(reduced_test_val, reduced_facs, True)

    return last_is_conc_test_result


def calc_sum(eqs, conc):
    sum_test_vals = 0
    for i, line in enumerate(eqs):
        test_val, facs = line
        if (i+1)%10 == 0:
            print(f"line {i+1}")

        if test_facs(test_val, facs, conc):
            sum_test_vals += test_val

    return sum_test_vals


if __name__ == "__main__":
    eqs = []
    for line in input.splitlines():
        test_val, facs = line.split(": ", 1)
        facs = [int(f) for f in facs.split()]
        eqs.append((int(test_val), facs))

    print(calc_sum(eqs, False))
    print(calc_sum(eqs, True))
