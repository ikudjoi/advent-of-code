from aocd import get_data

year, day = [int(v) for v in __file__.split("/")[-3:-1]]
input = get_data(day=day, year=year)
example = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
# input = example


class Grid:
    def __init__(self, input):
        g = []
        for line in input.splitlines():
            g.append([c for c in line])

        self.grid = g
        self.size_x = len(g[0])
        self.size_y = len(g)

    def in_range(self, x, y):
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def is_xmas(self, x, y, xd, yd):
        expected_letters = "MAS"
        cx, cy = x, y
        for letter in expected_letters:
            cx += xd
            cy += yd
            if not self.in_range(cx, cy):
                return False

            if self.grid[cy][cx] != letter:
                return False

        return True

    def count_xmas(self):
        cnt_xmas = 0
        for y, line in enumerate(self.grid):
            for x, c in enumerate(line):
                if c != "X":
                    continue

                for xdir in range(-1, 2):
                    for ydir in range(-1, 2):
                        if xdir == 0 and ydir == 0:
                            continue
                        if self.is_xmas(x, y, xdir, ydir):
                            cnt_xmas += 1
        return cnt_xmas


    def is_xmas2(self, x, y):
        for xd, yd in [[1, 1], [-1, 1]]:
            collected_letters = []
            for r in [1, -1]:
                cx = x + xd * r
                cy = y + yd * r
                if not self.in_range(cx, cy):
                    return False

                collected_letters.append(self.grid[cy][cx])

            sm = "".join(sorted(collected_letters))
            if not sm == "MS":
                return False

        return True

    def count_xmas2(self):
        cnt_xmas = 0
        for y, line in enumerate(self.grid):
            for x, c in enumerate(line):
                if c != "A":
                    continue
                if self.is_xmas2(x, y):
                    cnt_xmas += 1

        return cnt_xmas

g = Grid(input)
print(g.count_xmas())
print(g.count_xmas2())
