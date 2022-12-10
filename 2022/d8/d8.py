with open('input.txt', 'r') as f:
    contents = f.read()

example_input = """30373
25512
65332
33549
35390
"""

# contents = example_input
grid = [[int(c) for c in line] for line in contents.splitlines()]
grid_size = len(grid)
visible_trees = set()
hidden_trees = set()


def loop_tree_grid():
    for y in range(grid_size):
        for x in range(grid_size):
            tree_height = grid[y][x]
            trees_to_north = [h[x] for h in grid[:y]]
            trees_to_north.reverse()
            trees_to_east = grid[y][x + 1:]
            trees_to_south = [h[x] for h in grid[y + 1:]]
            trees_to_west = grid[y][:x]
            trees_to_west.reverse()
            yield x, y, tree_height, trees_to_north, trees_to_east, trees_to_south, trees_to_west


for x, y, tree_height, trees_to_north, trees_to_east, trees_to_south, trees_to_west in loop_tree_grid():
    if not trees_to_west or not trees_to_east or not trees_to_north or not trees_to_south:
        visible_trees.add((x, y))
        continue

    max_west = max(trees_to_west)
    if max_west < tree_height:
        visible_trees.add((x, y))
        continue

    max_east = max(trees_to_east)
    if max_east < tree_height:
        visible_trees.add((x, y))
        continue

    max_north = max(trees_to_north)
    if max_north < tree_height:
        visible_trees.add((x, y))
        continue

    max_south = max(trees_to_south)
    if max_south < tree_height:
        visible_trees.add((x, y))
        continue

    hidden_trees.add((x, y))


print(len(visible_trees))


# part 2

scenic_scores = {}


def scenic_score_one_dim(origin_tree_height, trees_in_front):
    scenic_score = 0
    for tree in trees_in_front:
        scenic_score += 1
        if tree >= origin_tree_height:
            break

    return scenic_score


for x, y, tree_height, trees_to_north, trees_to_east, trees_to_south, trees_to_west in loop_tree_grid():
    if not trees_to_west or not trees_to_east or not trees_to_north or not trees_to_south:
        # Trees on the edge have zero scenic score
        continue

    north_score = scenic_score_one_dim(tree_height, trees_to_north)
    east_score = scenic_score_one_dim(tree_height, trees_to_east)
    south_score = scenic_score_one_dim(tree_height, trees_to_south)
    west_score = scenic_score_one_dim(tree_height, trees_to_west)
    scenic_score = north_score * east_score * south_score * west_score
    scenic_scores[(x, y)] = scenic_score


print(max(scenic_scores.values()))