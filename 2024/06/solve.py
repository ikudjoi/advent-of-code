from enum import Enum

from aocd import get_data

year, day = [int(v) for v in __file__.split("/")[-3:-1]]
input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

input = get_data(day=day, year=year)


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


class Grid:
    def __init__(self, input):
        obstacles = set()
        for y, line in enumerate(input.splitlines()):
            for x, c in enumerate(line):
                if c == "^":
                    self.guard_x = x
                    self.guard_y = y
                if c == "#":
                    obstacles.add((x, y))

        self.obstacles = obstacles
        self.size_x = x
        self.size_y = y
        self.guard_dir = Direction.UP

    def in_range(self, x, y):
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    @staticmethod
    def apply_step(x, y, dir: Direction):
        return x + dir.value[0], y + dir.value[1]

    @staticmethod
    def turn(dir):
        if dir == Direction.UP:
            return Direction.RIGHT
        if dir == Direction.RIGHT:
            return Direction.DOWN
        if dir == Direction.DOWN:
            return Direction.LEFT
        return Direction.UP

    def guard_walk(self, obstacles=None):
        gx = self.guard_x
        gy = self.guard_y
        n = 0
        obstacles = obstacles or self.obstacles
        visited = {(gx, gy): {self.guard_dir: 0}}
        gdir = self.guard_dir
        while self.in_range(gx, gy):
            gnx, gny = self.apply_step(gx, gy, gdir)
            while (gnx, gny) in obstacles:
                gdir = self.turn(gdir)
                gnx, gny = self.apply_step(gx, gy, gdir)

            n += 1
            gx, gy = gnx, gny
            prev_visits = visited.get((gx, gy))
            if not prev_visits:
                visited[(gx, gy)] = {gdir: n}
            else:
                if gdir in prev_visits:
                    # Loop found!
                    return True, visited
                prev_visits[gdir] = n

        self.visited = visited
        return False, visited

    def gen_loops(self, visited):
        loops = 0
        for additional_obstacle_loc in visited:
            obstacles = self.obstacles.copy()
            obstacles.add(additional_obstacle_loc)
            loop, visited = self.guard_walk(obstacles)
            if loop:
                loops += 1

            continue
        return loops


g = Grid(input)
_, visited = g.guard_walk()
print(len(visited))
# Remove first guard location from the dict
(k := next(iter(visited)), visited.pop(k))
print(g.gen_loops(visited))
