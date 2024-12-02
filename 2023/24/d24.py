from typing import NamedTuple, Set
from types import SimpleNamespace
from enum import Enum


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


class State(SimpleNamespace):
    position: tuple
    dir: Direction
    dist: int = 0
    visited_intersections: Set[tuple] = set()


class Grid:
    def __init__(self, grid_str):
        lines = grid_str.splitlines()
        self.size = len(lines)
        self.start = State(position=(lines[0].index("."), 0), dir=Direction.DOWN)
        self.end_position = (lines[-1].index("."), self.size - 1)

        self.grid = []
        for line in lines:
            self.grid.append([c for c in line])

    @staticmethod
    def take_step(state: State, to_dir: Direction) -> State:
        new_pos = (state.position[0] + to_dir.value[0], state.position[1] + to_dir.value[1])
        return State(position=new_pos, dir=to_dir)

    def close_neighbours(self, state: State):
        x, y = state.position
        arrived_dir = state.dir

        tile = self.grid[y][x]
        forced_dir = None
        if tile == "^":
            forced_dir = Direction.UP
        elif tile == ">":
            forced_dir = Direction.RIGHT
        elif tile == "v":
            forced_dir = Direction.DOWN
        elif tile == "<":
            forced_dir = Direction.LEFT

        if forced_dir:
            # Forbidden to go up slope
            if arrived_dir.value[0] + forced_dir.value[0] == 0 and arrived_dir.value[1] + forced_dir.value[1] == 0:
                return []

            return [self.take_step(state, forced_dir)]

        result = []
        for next_dir in Direction:
            if arrived_dir.value[0] + next_dir.value[0] == 0 and arrived_dir.value[1] + next_dir.value[1] == 0:
                continue

            next_state_cand = self.take_step(state, next_dir)
            a, b = next_state_cand.position
            if not(0 <= a < len(self.grid) and 0 <= b < len(self.grid[0])):
                continue
            # Forbid moves onto rocks
            if self.grid[b][a] == "#":
                continue

            result.append(next_state_cand)

        return result

    def next_intersection(self, from_state: State = None):
        from_state = from_state or self.start
        state = from_state
        dist = 1
        prev_state = state
        # Take at least one step to get out from the original intersection
        state = self.take_step(state, state.dir)
        cns = self.close_neighbours(state)
        # Forbidden direction
        if len(cns) == 0:
            return None, [], False

        while len(cns) == 1:
            dist += 1
            prev_state = cns[0]
            cns = self.close_neighbours(prev_state)

        prev_state.dist = from_state.dist + dist
        prev_state.visited_intersections = from_state.visited_intersections.copy()
        dirs = [cn.dir for cn in cns]

        if len(cns) == 0:
            if prev_state.position == self.end_position:
                print(prev_state.dist)
                return prev_state, [], True

            return None, [], False

        # Returned to same intersection!
        if prev_state.position in prev_state.visited_intersections:
            return None, [], False

        prev_state.visited_intersections.add(prev_state.position)
        return prev_state, dirs, False

    def traverse_alternatives(self, from_state: State = None):
        from_state = from_state or self.start
        next_intersection, dirs, end_reached = self.next_intersection(from_state)
        for dir in dirs:
            new_from_state = next_intersection
            new_from_state.dir = dir
            for state in self.traverse_alternatives(new_from_state):
                yield state


def main():
    with open("input.txt", "r") as f:
        contents = f.read()

    example_input = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""

    # contents = example_input
    g = Grid(contents)

    # dist, intersection, next_states = g.next_intersection()
    [a for a in g.traverse_alternatives()]
    print("")


if __name__ == "__main__":
    main()
