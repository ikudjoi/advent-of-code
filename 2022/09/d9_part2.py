with open('input.txt', 'r') as f:
    contents = f.read()

example_input = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


# contents = example_input
head = (0, 0)
tail = [(0, 0) for _ in range(9)]


def dist(h, t):
    return max(abs(h[0] - t[0]), abs(h[1] - t[1]))


def head_move(h, direction):
    if direction == 'U':
        return h[0], h[1]+1
    if direction == 'R':
        return h[0]+1, h[1]
    if direction == 'D':
        return h[0], h[1]-1
    if direction == 'L':
        return h[0]-1, h[1]


def one_step(n):
    if n == 0:
        return 0
    if n < 0:
        return -1
    return 1


def tail_follow(t, h):
    if dist(h, t) <= 1:
        return t

    x_diff = h[0] - t[0]
    y_diff = h[1] - t[1]
    return t[0] + one_step(x_diff), t[1] + one_step(y_diff)


tail_locations = set()
head_moves = [line.split(' ') for line in contents.splitlines()]
for direction, steps in head_moves:
    steps = int(steps)
    for n in range(steps):
        head = head_move(head, direction)
        leader = head
        new_tail = []
        for tail_knot in tail:
            new_tail_knot = tail_follow(tail_knot, leader)
            leader = new_tail_knot
            new_tail.append(new_tail_knot)
        tail_locations.add(new_tail[-1])
        tail = new_tail

print(len(tail_locations))