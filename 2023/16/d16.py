from enum import Enum


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


def traverse_one_step(coord, direction):
    return tuple([sum(x) for x in zip(coord, direction.value)])


def traverse_beam(mmap, start_coord, direction):
    map_size = len(mmap)
    coords = [(start_coord, direction)]
    visited_coords = set()
    visited_coord_directions = set()
    advanced = True
    while advanced:
        advanced = False
        next_coords = []
        for c, d in coords:
            if min(c) < 0:
                continue
            if max(c) >= map_size:
                continue
            v_name = f"{c[0]},{c[1]},{d.name}"
            if v_name in visited_coord_directions:
                continue
            else:
                visited_coord_directions.add(v_name)
                advanced = True
            if c not in visited_coords:
                yield c
                visited_coords.add(c)

            chr = mmap[c[1]][c[0]]
            if d == Direction.RIGHT:
                if chr == "/":
                    d = Direction.UP
                    nc = traverse_one_step(c, d)
                    next_coords.append((nc, d))
                    continue
                if chr == "\\":
                    d = Direction.DOWN
                    nc = traverse_one_step(c, d)
                    next_coords.append((nc, d))
                    continue
                if chr in ("-", "."):
                    nc = traverse_one_step(c, d)
                    next_coords.append((nc, d))
                    continue
                if chr == "|":
                    for adir in (Direction.UP, Direction.DOWN):
                        nc = traverse_one_step(c, adir)
                        next_coords.append((nc, adir))
                    continue
            if d == Direction.UP:
                if chr == "/":
                    d = Direction.RIGHT
                    nc = traverse_one_step(c, d)
                    next_coords.append((nc, d))
                    continue
                if chr == "\\":
                    d = Direction.LEFT
                    nc = traverse_one_step(c, d)
                    next_coords.append((nc, d))
                    continue
                if chr in ("|", "."):
                    nc = traverse_one_step(c, d)
                    next_coords.append((nc, d))
                    continue
                if chr == "-":
                    for adir in (Direction.LEFT, Direction.RIGHT):
                        nc = traverse_one_step(c, adir)
                        next_coords.append((nc, adir))
                    continue
            if d == Direction.LEFT:
                if chr == "/":
                    d = Direction.DOWN
                    nc = traverse_one_step(c, d)
                    next_coords.append((nc, d))
                    continue
                if chr == "\\":
                    d = Direction.UP
                    nc = traverse_one_step(c, d)
                    next_coords.append((nc, d))
                    continue
                if chr in ("-", "."):
                    nc = traverse_one_step(c, d)
                    next_coords.append((nc, d))
                    continue
                if chr == "|":
                    for adir in (Direction.UP, Direction.DOWN):
                        nc = traverse_one_step(c, adir)
                        next_coords.append((nc, adir))
                    continue
            if d == Direction.DOWN:
                if chr == "/":
                    d = Direction.LEFT
                    nc = traverse_one_step(c, d)
                    next_coords.append((nc, d))
                    continue
                if chr == "\\":
                    d = Direction.RIGHT
                    nc = traverse_one_step(c, d)
                    next_coords.append((nc, d))
                    continue
                if chr in ("|", "."):
                    nc = traverse_one_step(c, d)
                    next_coords.append((nc, d))
                    continue
                if chr == "-":
                    for adir in (Direction.LEFT, Direction.RIGHT):
                        nc = traverse_one_step(c, adir)
                        next_coords.append((nc, adir))
                    continue
        coords = next_coords

def print_map(mmap, visited_coords):
    with open("output.txt", "wt") as f:
        for y, line in enumerate(mmap):
            res_line = []
            for x, c in enumerate(line):
                coord = (x,y)
                if coord in visited_coords:
                    res_line.append("#")
                else:
                    res_line.append(".")
            f.write("".join(res_line))
            f.write("\n")


def main():
    with open("input.txt", "r") as f:
        contents = f.read().rstrip()

    example_input = """.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....
"""
    # contents = example_input
    mirror_map = contents.splitlines()
    res = list(traverse_beam(mirror_map, (0,0), Direction.RIGHT))
    print_map(mirror_map, res)
    print(len(res))


    # part 2
    map_size = len(mirror_map)
    max_energized = 0
    for x in range(map_size):
        print(f"x={x}")
        energized_down = len(list(traverse_beam(mirror_map, (x,0), Direction.DOWN)))
        energized_up = len(list(traverse_beam(mirror_map, (x,map_size-1), Direction.UP)))
        max_energized = max(max_energized, energized_down, energized_up)
    for y in range(map_size):
        print(f"y={y}")
        energized_right = len(list(traverse_beam(mirror_map, (0,y), Direction.RIGHT)))
        energized_left = len(list(traverse_beam(mirror_map, (map_size-1,y), Direction.LEFT)))
        max_energized = max(max_energized, energized_right, energized_left)
    print(max_energized)


if __name__ == "__main__":
    main()
