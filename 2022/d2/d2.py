with open('input.txt', 'r') as f:
    contents = f.read()

example_input = """A Y
B X
C Z
"""

# contents = example_input
win = 6
draw = 3
lose = 0
total_score = 0
for game in contents.splitlines():
    opponent_move = game[0]
    my_move = game[2]
    if my_move == 'X':  # rock
        shape_score = 1
    elif my_move == 'Y':  # paper
        shape_score = 2
    else:
        shape_score = 3

    if opponent_move == 'A': # rock
        if my_move == 'X': # rock
            result = draw
        elif my_move == 'Y': # paper
            result = win
        else:
            result = lose
    elif opponent_move == 'B': # paper
        if my_move == 'X': # rock
            result = lose
        elif my_move == 'Y': # paper
            result = draw
        else:
            result = win
    else: # scissors
        if my_move == 'X': # rock
            result = win
        elif my_move == 'Y': # paper
            result = lose
        else:
            result = draw

    total_score += shape_score + result

print(total_score)

# part 2

total_score = 0
for game in contents.splitlines():
    opponent_move = game[0]
    my_strategy = game[2]

    if my_strategy == 'X':
        result = lose
        if opponent_move == 'A': # rock
            shape_score = 3 # scissors
        elif opponent_move == 'B': # paper
            shape_score = 1 # paper
        else:
            shape_score = 2
    elif my_strategy == 'Y':
        result = draw
        if opponent_move == 'A': # rock
            shape_score = 1 # rock
        elif opponent_move == 'B': # paper
            shape_score = 2 # paper
        else:
            shape_score = 3
    else:
        result = win
        if opponent_move == 'A': # rock
            shape_score = 2 # paper
        elif opponent_move == 'B': # paper
            shape_score = 3 # scissors
        else:
            shape_score = 1

    total_score += shape_score + result

print(total_score)
