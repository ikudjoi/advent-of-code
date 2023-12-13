def lines_to_cols(lines):
    cols = []
    for j in range(len(lines[0])):
        col = "".join([l[j] for l in lines])
        cols.append(col)
    return cols


def mirror_value(lines, expected_diff=0):
    hv = mirror_value_horizontal(lines, expected_diff=expected_diff)
    if hv > 0:
        return 100*hv

    cols = lines_to_cols(lines)
    vv = mirror_value_horizontal(cols, expected_diff=expected_diff)
    if vv == 0:
        raise ValueError("Could not find symmetry!")
    return vv


def differing_char_count(line1, line2):
    chrs1 = [c for c in line1]
    chrs2 = [c for c in line2]
    diff = sum([0 if c1 == c2 else 1 for c1, c2 in zip(chrs1, chrs2)])
    return diff


def mirror_value_horizontal(lines, expected_diff):
    prev_line = ""
    sym_line_candidates = []
    for i, line in enumerate(lines):
        if i > 0 and differing_char_count(line, prev_line) <= expected_diff:
            sym_line_candidates.append(i)
        prev_line = line

    if len(sym_line_candidates) == 0:
        return 0

    for c in sym_line_candidates:
        x, y = c-1, c
        total_diff = 0
        while True:
            if x < 0:
                if total_diff == expected_diff:
                    return c
                break
            if y >= len(lines):
                if total_diff == expected_diff:
                    return c
                break
            line_left = lines[x]
            line_right = lines[y]
            total_diff += differing_char_count(line_left, line_right)
            if total_diff > expected_diff:
                break
            x -= 1
            y += 1

    return 0


def main():
    with open("input.txt", "r") as f:
        contents = f.read()

    example_input = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

    # contents = example_input
    inputs = contents.split("\n\n")
    res = 0
    res2 = 0
    for i, input in enumerate(inputs):
        lines = input.splitlines()
        res += mirror_value(lines)
        res2 += mirror_value(lines, 1)

    print(res)
    print(res2)


if __name__ == "__main__":
    main()
