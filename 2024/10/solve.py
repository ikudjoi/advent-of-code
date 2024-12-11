from enum import Enum
from queue import Queue

from aocd import get_data

year, day = [int(v) for v in __file__.split("/")[-3:-1]]
input = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


input = get_data(day=day, year=year)


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


class Grid:
    def __init__(self, input):
        grid = []
        trailheads = set()
        for y, line in enumerate(input.splitlines()):
            gl = []
            for x, v in enumerate(line):
                if v == ".":
                    iv = None
                else:
                    iv = int(v)
                gl.append(iv)
                if iv == 0:
                    trailheads.add((x, y))
            grid.append(gl)

        self.grid = grid
        self.trailheads = trailheads
        self.size_x = x+1
        self.size_y = y+1

    def in_range(self, x, y):
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def value(self, x, y):
        return self.grid[y][x]

    def neighbours(self, x, y):
        result = []

        expected_neighbor_value = self.value(x, y) + 1
        for dir in Direction:
            new_position = (x + dir.value[0], y + dir.value[1])
            if not self.in_range(*new_position):
                continue

            neighbour_value = self.grid[new_position[1]][new_position[0]]
            if neighbour_value != expected_neighbor_value:
                continue

            result.append(new_position)
        return result

    def find_trails(self):
        res1 = []
        res2 = []
        for trailhead in self.trailheads:
            trs1 = self.find_trail(*trailhead)
            res1.append(trs1)
            trs2 = self.find_all_trails(*trailhead)
            res2.append(trs2)
        return res1, res2

    def find_trail(self, x, y):
        visited = set()
        q = Queue()
        q.put((x,y))

        nines_reached = 0
        while not q.empty():
            pos = q.get()

            if pos in visited:
                continue

            # Add it to visited locations
            visited.add(pos)
            if self.value(*pos) == 9:
                nines_reached += 1

            # Add all the boundary spots.
            for next_pos in self.neighbours(*pos):
                if next_pos not in visited:
                    q.put(next_pos)

        # self.print_visited(visited)
        return nines_reached

    def find_all_trails(self, x, y):
        visited = {}
        q = Queue()
        q.put((x,y))

        nine_times_reached = 0
        while not q.empty():
            pos = q.get()

            if self.value(*pos) == 9:
                nine_times_reached += 1

            # Add all the boundary spots.
            for next_pos in self.neighbours(*pos):
                if next_pos not in visited:
                    q.put(next_pos)

        # self.print_visited(visited)
        return nine_times_reached

    def print_visited(self, visited):
        for y, line in enumerate(self.grid):
            for x, v in enumerate(line):
                if (x, y) in visited:
                    print(v, end="")
                else:
                    print(".", end="")
            print("")

g = Grid(input)
trs1, trs2 = g.find_trails()
print(sum(trs1), sum(trs2))
