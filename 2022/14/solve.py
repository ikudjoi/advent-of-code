import math

with open('input.txt', 'r') as f:
    contents = f.read()

example_input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

# contents = example_input

rocks = set()
for line in contents.splitlines():
    points = line.split(' -> ')
    start = points[0]
    for next_point in points[1:]:
        s_x, s_y = [int(c) for c in start.split(',')]
        e_x, e_y = [int(c) for c in next_point.split(',')]
        if s_x == e_x:
            diff = e_y-s_y
            for i in range(abs(diff)+1):
                y = int(s_y+math.copysign(i, diff))
                rocks.add((s_x, y))
        elif s_y == e_y:
            diff = e_x-s_x
            for i in range(abs(diff)+1):
                x = int(s_x+math.copysign(i, diff))
                rocks.add((x, s_y))
        else:
            raise Exception("saatana")

        start = next_point


class PouringSand:
    def __init__(self, rocks):
        self.rocks = rocks
        self.min_rock_x = min([r[0] for r in rocks])
        self.min_rock_y = min([r[1] for r in rocks])
        self.max_rock_x = max([r[0] for r in rocks])
        self.max_rock_y = max([r[1] for r in rocks])
        self.sand_source = (500, 0)

    def print_state(self, sand):
        for y in range(self.max_rock_y + 2):  # include the source at y == 0
            for x in range(self.min_rock_x-1, self.max_rock_x+2):
                if (x, y) in self.rocks:
                    print('#', end='')
                elif (x, y) in sand:
                    print('o', end='')
                elif (x, y) == self.sand_source:
                    print('+', end='')
                else:
                    print('.', end='')
            print('')
        print('')

    def pour(self):
        settled_sand = set()
        s = self.sand_source
        while s[1] <= self.max_rock_y:                # down          # left down       # right down
            next_s_alternatives = [(s[0], s[1]+1), (s[0]-1, s[1]+1), (s[0]+1, s[1]+1)]
            flowing = False
            for next_s in next_s_alternatives:
                if next_s not in self.rocks and next_s not in settled_sand:
                    s = next_s
                    flowing = True
                    break

            if not flowing:

                settled_sand.add(s)
                if s == self.sand_source:
                    break

                # self.print_state(settled_sand)
                s = self.sand_source

        self.print_state(settled_sand)
        print(len(settled_sand))


p = PouringSand(rocks)
p.print_state(set())
p.pour()


# part 2

floor_y = p.max_rock_y + 2
for x in range(500-floor_y, 500+floor_y+1):
    rocks.add((x, floor_y))

p2 = PouringSand(rocks)
p2.print_state(set())
p2.pour()
