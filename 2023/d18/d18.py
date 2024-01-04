import itertools


def move(location, dir, steps):
    if dir == "R":
        return location[0] + steps, location[1]
    elif dir == "L":
        return location[0] - steps, location[1]
    elif dir == "U":
        return location[0], location[1] - steps
    elif dir == "D":
        return location[0], location[1] + steps


def process_instructions(dir_steps, draw_files):
    start = (0, 0)

    digged_trenches = [start]
    current_location = start
    if dir_steps[0][0] == "R" and dir_steps[-1][0] == "U":
        start_edge = "F"
    elif dir_steps[0][0] == "L" and dir_steps[-1][0] == "U":
        start_edge = "7"
    else:
        raise ValueError("Not expected start edge type!")

    pipe_map = {start: start_edge}  # same kind of edge both in example & actual input
    prev_dir = None
    for ins in dir_steps:
        dir, steps = ins
        if dir in ("U", "D"):
            pipe = "|"
        else:
            pipe = "-"

        if prev_dir:
            if prev_dir == "R" and dir == "D":
                pipe_map[current_location] = "7"
            elif prev_dir == "R" and dir == "U":
                pipe_map[current_location] = "J"
            elif prev_dir == "U" and dir == "L":
                pipe_map[current_location] = "7"
            elif prev_dir == "U" and dir == "R":
                pipe_map[current_location] = "F"
            elif prev_dir == "L" and dir == "U":
                pipe_map[current_location] = "L"
            elif prev_dir == "L" and dir == "D":
                pipe_map[current_location] = "F"
            elif prev_dir == "D" and dir == "L":
                pipe_map[current_location] = "J"
            elif prev_dir == "D" and dir == "R":
                pipe_map[current_location] = "L"

        if draw_files:
            for i in range(steps):
                current_location = move(current_location, dir, 1)
                digged_trenches.append(current_location)
                if i < steps-1:
                    pipe_map[current_location] = pipe
        else:
            current_location = move(current_location, dir, steps)

        prev_dir = dir

    if draw_files:
        max_x = max([v[0] for v in pipe_map.keys()])
        min_x = min([v[0] for v in pipe_map.keys()])
        max_y = max([v[1] for v in pipe_map.keys()])
        min_y = min([v[1] for v in pipe_map.keys()])

        with open("output_trench.txt", "wt") as ft, open("output_pipes.txt", "wt") as fp:
            for y in range(min_y, max_y + 1):
                line_t = []
                line_p = []
                for x in range(min_x, max_x+1):
                    if (x, y) in digged_trenches:
                        line_t.append("#")
                    else:
                        line_t.append(".")

                    p = pipe_map.get((x,y), ".")
                    line_p.append(p)

                ft.write("".join(line_t))
                ft.write("\n")
                fp.write("".join(line_p))
                fp.write("\n")

    area = 0
    pipe_edges = {k: v for k, v in pipe_map.items() if v not in ("-", "|")}

    current_vertical_trenches = []
    previous_y = None

    edges_by_y = itertools.groupby(sorted(pipe_edges.items(), key=lambda x: x[0][1]), key=lambda x: x[0][1])
    for y, edges in edges_by_y:
        vertical_trenches_below = []
        edges_by_x = {edge[0][0]: edge[1] for edge in sorted(edges)}
        edges_and_trenches = set(edges_by_x.keys())
        edges_and_trenches.update(current_vertical_trenches)

        inside = False
        pipe_crossed_up = False
        pipe_crossed_down = False

        slice_start = None
        slice_width = 0
        for x in sorted(edges_and_trenches):
            c = edges_by_x.get(x, "|")
            if c in ("L", "J", "|"):
                pipe_crossed_up = not pipe_crossed_up
            if c in ("F", "7", "|"):
                pipe_crossed_down = not pipe_crossed_down
                vertical_trenches_below.append(x)

            if not inside and c in ("F", "L"):
                slice_start = x

            if pipe_crossed_down and pipe_crossed_up:
                inside = not inside
                pipe_crossed_up = False
                pipe_crossed_down = False

            if not inside and c in ("J", "7"):
                slice_width += (1+x-slice_start)
                slice_start = None
            if c == "|":
                if slice_start is None:
                    slice_start = x
                else:
                    slice_width += (1+x-slice_start)
                    slice_start = None

        if inside:
            raise ValueError(f"not consistent! y:{y}")
        area += slice_width
        if previous_y is not None and previous_y < y - 1:
            slice_starts = current_vertical_trenches[0::2]
            slice_ends = current_vertical_trenches[1::2]
            slice_width = 0
            for slice in zip(slice_starts, slice_ends):
                slice_width = 1+slice[1]-slice[0]
                slice_height = y-previous_y-1
                area_addition = slice_width*slice_height
                area += area_addition
        previous_y = y
        current_vertical_trenches = vertical_trenches_below
    return area


def main():
    with open("input.txt", "r") as f:
        contents = f.read()

    example_input = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

    # contents = example_input
    ins = [l.split(" ") for l in contents.splitlines()]
    part1_ins = [(l[0], int(l[1])) for l in ins]
    area = process_instructions(part1_ins, False)
    print(area)

    part2_ins = []
    for inp in ins:
        hx = inp[2][2:-2]
        steps = int(hx, 16)
        dir_num = int(inp[2][-2:-1])
        if dir_num == 0:
            dir = "R"
        elif dir_num == 1:
            dir = "D"
        elif dir_num == 2:
            dir = "L"
        elif dir_num == 3:
            dir = "U"
        part2_ins.append((dir, steps))

    area = process_instructions(part2_ins, False)
    print(area)


if __name__ == "__main__":
    main()
