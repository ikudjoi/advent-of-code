with open('input.txt', 'r') as f:
    contents = f.read()

example_input = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

# contents = example_input

initial, moves = contents.split('\n\n')
initial_rows = initial.splitlines()
stack_nums = [n for n in initial_rows[-1].split(' ') if n]
num_stacks = len(stack_nums)

stacks = []
for stack_num in range(num_stacks):
    stack = []
    stacks.append(stack)
    for pos in range(len(initial_rows) - 1):
        input_row = initial_rows[-2-pos]
        idx = 1 + 4*stack_num
        if idx >= len(input_row):
            continue

        c = input_row[idx]
        if c == ' ':
            break

        stack.append(c)

orig_stacks = stacks.copy()

# print(stacks)
for move in moves.splitlines():
    p1, p2 = move.split(' from ')
    num_crates = int(p1[5:])
    s_from, s_to = [int(i)-1 for i in p2.split(' to ')]

    stack_from = stacks[s_from]
    stack_to = stacks[s_to]
    crates_to_move = stack_from[-num_crates:]
    crates_to_move.reverse()
    stack_from = stack_from[:-num_crates]
    stack_to = stack_to + crates_to_move
    stacks[s_from] = stack_from
    stacks[s_to] = stack_to

result = ''.join([s[-1] for s in stacks])
print(result)

# part 2

stacks = orig_stacks

# print(stacks)
for move in moves.splitlines():
    p1, p2 = move.split(' from ')
    num_crates = int(p1[5:])
    s_from, s_to = [int(i)-1 for i in p2.split(' to ')]

    stack_from = stacks[s_from]
    stack_to = stacks[s_to]
    crates_to_move = stack_from[-num_crates:]
    stack_from = stack_from[:-num_crates]
    stack_to = stack_to + crates_to_move
    stacks[s_from] = stack_from
    stacks[s_to] = stack_to

result = ''.join([s[-1] for s in stacks])
print(result)