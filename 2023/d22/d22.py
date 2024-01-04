import itertools


class Brick:
    def __init__(self, x1, x2):
        self.x1 = [int(d) for d in x1.split(",")]
        self.x2 = [int(d) for d in x2.split(",")]
        self.locations = list(self.get_locations())
        self.supported_by_bricks = []
        self.supports_bricks = []

    @property
    def min_z(self):
        return min(self.x1[2], self.x2[2])

    @property
    def max_z(self):
        return max(self.x1[2], self.x2[2])

    def get_locations(self):
        yield self.x1.copy()

        for j in range(3):
            if self.x1[j] != self.x2[j]:
                next_coord = self.x1.copy()
                dir = 1 if self.x1[j] < self.x2[j] else -1
                while True:
                    next_coord[j] += dir
                    yield next_coord
                    if next_coord == self.x2:
                        break

                    next_coord = next_coord.copy()

    def let_fall(self, steps=1):
        self.x1[2] -= steps
        self.x2[2] -= steps
        for l in self.locations:
            l[2] -= steps

    def supported_by(self, other_brick):
        for o_loc in other_brick.locations:
            for t_loc in self.locations:
                if o_loc[0] == t_loc[0] and o_loc[1] == t_loc[1] and o_loc[2] + 1 == t_loc[2]:
                    return True
        return False

    def __str__(self):
        res = []
        for i in range(3):
            if self.x1[i] == self.x2[i]:
                res.append(str(self.x1[i]))
            else:
                res.append(f"{self.x1[i]}..{self.x2[i]}")
        return ",".join(res)

    def __repr__(self):
        return f"<Brick {self.__str__()}>"

    def __lt__(self, other):
        if other.min_z > self.min_z:
            return True


def count_bricks_would_fall(brick):
    return len(bricks_that_would_get_removed(brick)) - 1


def bricks_that_would_get_removed(brick):
    removed_bricks = set([brick])
    more_bricks_removed = True
    while more_bricks_removed:
        more_bricks_removed = False
        for desc_brick in walk_descendant_bricks(brick):
            if desc_brick not in removed_bricks and all([sp in removed_bricks for sp in desc_brick.supported_by_bricks]):
                removed_bricks.add(desc_brick)
                more_bricks_removed = True

    return removed_bricks


def walk_descendant_bricks(brick):
    yielded = set()
    for supported_brick in brick.supports_bricks:
        for desc_brick in walk_descendant_bricks(supported_brick):
            if not desc_brick in yielded:
                yielded.add(desc_brick)
                yield desc_brick
    yield brick


def main():
    with open("input.txt", "r") as f:
        contents = f.read()

    example_input = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""

    example_input2 = """0,0,1~0,0,2
1,0,1~2,0,1
1,0,2~1,0,2
0,0,3~1,0,3"""

    example_input3 = """0,0,1~0,5,1
0,6,1~0,9,1
0,0,2~0,0,2
0,3,2~0,8,2"""

    # contents = example_input
    lines = contents.splitlines()
    bricks = []
    for line in lines:
        x1, x2 = line.split("~")
        brick = Brick(x1, x2)
        bricks.append(brick)
    bricks = sorted(bricks)

    bricks_fell = True
    while bricks_fell:
        bricks_fell = False
        bricks_by_min_z = sorted(bricks, key=lambda x: x.min_z)
        bricks_by_min_z = {k: list(v) for k, v in itertools.groupby(bricks_by_min_z, key=lambda x: x.min_z)}
        bricks_by_max_z = sorted(bricks, key=lambda x: x.max_z)
        bricks_by_max_z = {k: list(v) for k, v in itertools.groupby(bricks_by_max_z, key=lambda x: x.max_z)}
        for z, bricks_on_level in bricks_by_min_z.items():
            for b in bricks_on_level:
                b.supported_by_bricks = []
                b.supports_bricks = []

            if z == 1:
                continue
            for brick in bricks_on_level:
                possibly_supported_by = bricks_by_max_z.get(z-1, [])
                supported_by_other_brick = False
                for ob in possibly_supported_by:
                    if brick.supported_by(ob):
                        brick.supported_by_bricks.append(ob)
                        ob.supports_bricks.append(brick)
                        supported_by_other_brick = True
                if not supported_by_other_brick:
                    brick.let_fall(1)
                    bricks_fell = True

    supported_by_single_brick = [b for b in bricks if len(b.supported_by_bricks) == 1]
    can_be_disintegrated = set()
    for brick in bricks:
        brick_can_be_disintegrated = not any([sb for sb in brick.supports_bricks if sb in supported_by_single_brick])
        if brick_can_be_disintegrated:
            can_be_disintegrated.add(brick)

    print(len(can_be_disintegrated))

    # part 2 awfully slow
    part2_bricks = set(bricks) - can_be_disintegrated
    total_would_fall = 0
    fall_count_for_brick = 0
    print(f"Total bricks to process: {len(part2_bricks)}")
    for i, brick in enumerate(part2_bricks):
        print(f"{i}: Processing brick {brick} and previous brick made {fall_count_for_brick} to fall")
        fall_count_for_brick = count_bricks_would_fall(brick)
        total_would_fall += fall_count_for_brick

    print(total_would_fall)


if __name__ == "__main__":
    main()
