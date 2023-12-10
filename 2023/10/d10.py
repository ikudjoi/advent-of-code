from enum import Enum

with open("input.txt", "r") as f:
    contents = f.read()

example_input = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""

# contents = example_input

matrix = []
lines = contents.splitlines()
for i, line in enumerate(lines):
    y = len(lines) - 1 - i
    x = line.find("S")
    if x >= 0:
        rat = (x, y)
    matrix.append([c for c in line])


class Direction(Enum):
    UP = (0, 1)
    RIGHT = (1, 0)
    DOWN = (0, -1)
    LEFT = (-1, 0)


class Matrix:
    # ALLOWED_PIPES_TO = {
    #     Direction.UP:    set(["|", "L", "J"]),
    #     Direction.RIGHT: set(["-", "J", "7"]),
    #     Direction.DOWN:  set(["|", "F", "7"]),
    #     Direction.LEFT:  set(["-", "F", "L"]),
    # }

    def __init__(self, char_matrix, position):
        self.char_matrix = char_matrix
        self.start_position = position
        self.current_position = position
        self.distance = 0

    @property
    def pipe(self):
        x, y = self.current_position
        i = len(self.char_matrix) - 1 - y
        try:
            return self.char_matrix[i][x]
        except IndexError:
            return "."

    def new_direction(self, old_direction):
        pipe = self.pipe
        if old_direction == Direction.UP:
            if pipe == "|":
                return Direction.UP
            if pipe == "F":
                return Direction.RIGHT
            if pipe == "7":
                return Direction.LEFT
        if old_direction == Direction.RIGHT:
            if pipe == "-":
                return Direction.RIGHT
            if pipe == "J":
                return Direction.UP
            if pipe == "7":
                return Direction.DOWN
        if old_direction == Direction.DOWN:
            if pipe == "|":
                return Direction.DOWN
            if pipe == "J":
                return Direction.LEFT
            if pipe == "L":
                return Direction.RIGHT
        if old_direction == Direction.LEFT:
            if pipe == "-":
                return Direction.LEFT
            if pipe == "F":
                return Direction.DOWN
            if pipe == "L":
                return Direction.UP
        raise ValueError(f"Cannot traverse {old_direction} to pipe {pipe}")

    def traverse(self, start_direction):
        visited_pipes = [self.current_position]
        traversed_distance = 0
        direction = start_direction
        while True:
            # self.validate_step(direction)
            next_position = [sum(x) for x in zip(self.current_position, direction.value)]
            self.current_position = tuple(next_position)
            traversed_distance += 1
            if self.pipe == "S":
                break
            visited_pipes.append(self.current_position)
            direction = self.new_direction(direction)

        return traversed_distance, visited_pipes


m = Matrix(matrix, rat)
dist, pipes = m.traverse(Direction.UP)
print(int(dist/2))

area = 0
with open("output.txt", "wt") as f:
    for i, chars in enumerate(m.char_matrix):
        inside = False
        pipe_crossed_up = False
        pipe_crossed_down = False
        hilighted_pipe_chars = []
        y = len(m.char_matrix) - i - 1
        for x, c in enumerate(chars):
            coord = (x,y)
            if coord in pipes:
                hilighted_pipe_chars.append("O")
                if c in ("L", "J", "|", "S"):  # S is a J in my input
                    pipe_crossed_up = not pipe_crossed_up
                if c in ("F", "7", "|"):
                    pipe_crossed_down = not pipe_crossed_down
                if pipe_crossed_down and pipe_crossed_up:
                    inside = not inside
                    pipe_crossed_up = False
                    pipe_crossed_down = False
            else:
                if inside:
                    hilighted_pipe_chars.append("I")
                    area += 1
                else:
                    hilighted_pipe_chars.append(" ")
        if inside:
            raise ValueError(f"not consistent! y:{y}")

        f.write("".join(hilighted_pipe_chars) + "\n")

print(area)