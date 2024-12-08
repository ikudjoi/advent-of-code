from aocd import get_data
import itertools
import math

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

input2 = """T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........
"""

# input = input2
input = get_data(day=day, year=year)


class Grid:
    def __init__(self, input):
        antennas = {}
        for y, line in enumerate(input.splitlines()):
            for x, c in enumerate(line):
                if c == ".":
                    continue

                a_coll = antennas.get(c, set())
                if not a_coll:
                    antennas[c] = a_coll
                a_coll.add((x, y))

        self.antennas = antennas
        self.size_x = x+1
        self.size_y = y+1

    def in_range(self, x, y):
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def find_antinodes1(self):
        antinode_locations = set()
        for a_type, a_coll in self.antennas.items():
            for a_pair in itertools.combinations(a_coll, 2):
                aa, ab = a_pair
                xd = ab[0] - aa[0]
                yd = ab[1] - aa[1]
                an1 = (aa[0]-xd, aa[1]-yd)
                an2 = (ab[0]+xd, ab[1]+yd)
                for an in [an1, an2]:
                    if self.in_range(*an) and an not in antinode_locations:
                        antinode_locations.add(an)
        return antinode_locations

    def find_antinodes2(self):
        antinode_locations = set()
        for a_type, a_coll in self.antennas.items():
            for a_pair in itertools.combinations(a_coll, 2):
                aa, ab = a_pair
                xd = ab[0] - aa[0]
                yd = ab[1] - aa[1]
                d_gcd = math.gcd(abs(xd), abs(yd))
                xd_lcm = xd / d_gcd
                yd_lcm = yd / d_gcd

                for dir in [1, -1]:
                    an = aa
                    while self.in_range(*an):
                        if an not in antinode_locations:
                            antinode_locations.add(an)
                        nx = an[0] + xd_lcm * dir
                        ny = an[1] + yd_lcm * dir
                        an = (nx, ny)

        return antinode_locations

g = Grid(input)
print(len(g.find_antinodes1()))
print(len(g.find_antinodes2()))
