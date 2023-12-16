def let_stones_fall_line(line_above, line_below):
    new_line_above = []
    new_line_below = []
    changed = False
    for i in range(len(line_above)):
        ca = line_above[i]
        cb = line_below[i]
        if ca == "." and cb == "O":
            new_line_above.append("O")
            new_line_below.append(".")
            changed = True
        else:
            new_line_above.append(ca)
            new_line_below.append(cb)

    if changed:
        return "".join(new_line_above), "".join(new_line_below), True
    return line_above, line_below, False


def let_stones_fall(lines):
    stones_moved = True
    while stones_moved:
        stones_moved = False
        next_iteration_lines = []
        line_above = lines[0]
        for line in lines[1:]:
            line_above, line_below, line_stones_moved = let_stones_fall_line(line_above, line)
            stones_moved = stones_moved or line_stones_moved
            next_iteration_lines.append(line_above)
            line_above = line_below
        next_iteration_lines.append(line_below)
        lines = next_iteration_lines

    return lines


def rotate_left(lines):
    cols = []
    for j in range(len(lines[0])):
        col = "".join([l[j] for l in reversed(lines)])
        cols.append(col)
    return cols


def cycle(lines):
    for i in range(4):
        lines = let_stones_fall(lines)
        lines = rotate_left(lines)

    return lines


def calc_weight(lines):
    res = 0
    for i, line in enumerate(reversed(lines)):
        count_stones = line.count("O")
        res += (i+1)*count_stones
    return res


def hsh(lines):
    return hash("".join(lines))


def main():
    with open("input.txt", "r") as f:
        contents = f.read()

    example_input = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

    # contents = example_input
    lines = contents.splitlines()
    final_lines = let_stones_fall(lines)
    print(calc_weight(final_lines))

    visited_hashes = {hsh(lines): 0}
    visited_lines = {}
    i = 1
    target_cycles = 1000000000
    while i <= target_cycles:
        lines = cycle(lines)
        h = hsh(lines)
        if h in visited_hashes.keys():
            prev_i = visited_hashes[h]
            cycle_len = i - prev_i
            mod_current_step = i % cycle_len
            mod_target = target_cycles % cycle_len
            diff_target_cycle = mod_current_step - mod_target
            if diff_target_cycle < 0:
                diff_target_cycle += cycle_len
            target_i = i - diff_target_cycle
            target_lines = visited_lines[target_i]
            break

        visited_hashes[h] = i
        visited_lines[i] = lines
        i += 1

    print(calc_weight(target_lines))


if __name__ == "__main__":
    main()
