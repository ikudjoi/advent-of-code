from queue import PriorityQueue


with open("input.txt", "r") as f:
    contents = f.read()

example_input = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""


# contents = example_input
max_steps = 64

lines = contents.splitlines()
size = len(lines)
start = None
grid = []
for y, line in enumerate(lines):
    if not start and "S" in line:
        start = (y, line.index("S"))
        line = line.replace("S", ".")
    grid.append([c for c in line])


def neighbours(grid, coord):
    x, y = coord
    result = []

    for dir_ in (1, 0), (-1, 0), (0, 1), (0, -1):
        new_position = (x + dir_[0], y + dir_[1])
        a, b = new_position
        if not(0 <= a < len(grid) and 0 <= b < len(grid[0])):
            continue
        # Forbid moves onto rocks
        if grid[b][a] == "#":
            continue

        result.append(new_position)
    return result


# Dijkstra from (0, 0)
best_distance = {}
boundary = PriorityQueue()
boundary.put((0, start))


while not boundary.empty():
    # Find the boundary spot with the smallest distance
    # This is inefficient... should be using some sort of priority queue
    (value, key) = boundary.get()
    if key in best_distance:
        continue

    # Add it to best_distance
    best_distance[key] = value

    # Add all the boundary spots.
    for next_ in neighbours(grid, key):
        if next_ not in best_distance:
            dist = best_distance[key] + 1
            boundary.put((dist, next_))


print(len([k for k,v in best_distance.items() if v % 2 == 0 and v <= max_steps]))


def neighbours2(grid, coord):
    x, y = coord
    result = []

    for dir_ in (1, 0), (-1, 0), (0, 1), (0, -1):
        new_position = (x + dir_[0], y + dir_[1])
        a, b = new_position
        # Forbid moves onto rocks
        if grid[b%size][a%size] == "#":
            continue

        result.append(new_position)
    return result


def locations_by_distance(max_dist):
    # Dijkstra from (0, 0)
    best_distance2 = {}
    boundary2 = PriorityQueue()
    boundary2.put((0, start))

    while not boundary2.empty():
        # Find the boundary spot with the smallest distance
        # This is inefficient... should be using some sort of priority queue
        (value, key) = boundary2.get()
        if key in best_distance2:
            continue

        # Add it to best_distance
        best_distance2[key] = value

        # Add all the boundary spots.
        for next_ in neighbours2(grid, key):
            if next_ not in best_distance2:
                dist = best_distance2[key] + 1
                if dist <= max_dist:
                    boundary2.put((dist, next_))

    return len([k for k,v in best_distance2.items() if v % 2 == max_dist % 2])


"""
    In exactly 6 steps, he can still reach 16 garden plots.
    In exactly 10 steps, he can reach any of 50 garden plots.
    In exactly 50 steps, he can reach 1594 garden plots.
    In exactly 100 steps, he can reach 6536 garden plots.
    In exactly 500 steps, he can reach 167004 garden plots.
    In exactly 1000 steps, he can reach 668697 garden plots.
    In exactly 5000 steps, he can reach 16733044 garden plots.
"""
# 26501365

# locations_by_distance(6)     # 47     # 36 +
# locations_by_distance(10)    # 114
# locations_by_distance(50)    # 2340
# locations_by_distance(64)    # 3858
# locations_by_distance(100)   # 9288
# locations_by_distance(1000)  # 908142
# locations_by_distance(5000)


# for i in range(10):
#     md = int(math.pow(2, i))
#     locs = locations_by_distance(md)
#     print(f"locs: {locs}, area: {md*md}, diff: {locs - md*md}")


observations = []
for i in range(5):
    md = 131*i+65
    locs = locations_by_distance(md)
    observations.append(locs)
    print(f"dist: {md}, locs: {locs}, area: {md*md}")

"""
>>> y = [3943, 35126, 97407, 190786, 315263]
>>> x = [i for i in range(5)]
>>> np.polyfit(x, y, 2, full=True)
(array([15549., 15634.,  3943.]), array([6.66825999e-22]), 3, array([1.63437886, 0.55950035, 0.12555924]), 1.1102230246251565e-15)
>>> np.polyfit(x, y, 2)
"""