with open('input.txt', 'r') as f:
    contents = f.read()

example_input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

# contents = example_input


topo_grid = [[c for c in line] for line in contents.splitlines()]
topo_hash = {}
for y, row in enumerate(topo_grid):
    for x, c in enumerate(row):
        coord = (x, y)
        if c == 'S':
            start = coord
            topo_hash[coord] = 1
        elif c == 'E':
            end = coord
            topo_hash[coord] = 26
        else:
            topo_hash[coord] = ord(c) - 96


vertices = {}
for y in range(len(topo_grid)):
    for x in range(len(topo_grid[0])):
        edge_from = (x, y)
        height_from = topo_hash[edge_from]
        for edge_to in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            if edge_to not in topo_hash:
                continue

            height_to = topo_hash[edge_to]
            if height_to > height_from + 1:
                continue

            if edge_from not in vertices:
                vertices[edge_from] = [edge_to]
            else:
                vertices[edge_from].append(edge_to)


visited = set()
visited.add(start)
current_layer = [start]
distances = {start: 0}
distance = 0

while current_layer:
    next_layer = []
    distance += 1
    for step_from in current_layer:
        for step_to in vertices[step_from]:
            if step_to in visited:
                continue

            next_layer.append(step_to)
            visited.add(step_to)
            distances[step_to] = distance

    current_layer = next_layer


print(distances[end])


# part 2

reverse_vertices = {}
for step_from, steps_to in vertices.items():
    for step_to in steps_to:
        if step_to not in reverse_vertices:
            reverse_vertices[step_to] = [step_from]
        else:
            reverse_vertices[step_to].append(step_from)


visited = set()
visited.add(end)
current_layer = [end]
distance = 0


while current_layer:
    next_layer = []
    distance += 1
    for step_from in current_layer:
        for step_to in reverse_vertices[step_from]:
            if step_to in visited:
                continue

            next_layer.append(step_to)
            visited.add(step_to)

            if topo_hash[step_to] == 1:
                print(distance)
                break

    current_layer = next_layer
