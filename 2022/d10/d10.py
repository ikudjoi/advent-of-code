with open('input.txt', 'r') as f:
    contents = f.read()

example_input = """noop
addx 3
addx -5"""

with open('ex_input2.txt', 'r') as f:
    example_input2 = f.read()

# contents = example_input2
instructions = contents.splitlines()


def prev_control_cycle(cycles):
    if cycles < 20:
        return 0

    mod_prev_control = (cycles - 20) % 40
    return cycles - mod_prev_control


prev_control_cycle(21)

X = 1
cycles = 0
signal_strengths = []
for instruction in instructions:
    prev_cycles = cycles
    prev_X = X
    if instruction == 'noop':
        cycles += 1

    elif instruction.startswith('addx'):
        x_diff = int(instruction[5:])
        X += x_diff
        cycles += 2

    pcc = prev_control_cycle(cycles)
    if pcc > prev_control_cycle(prev_cycles):
        signal_strength = prev_X * pcc
        signal_strengths.append(signal_strength)

print(sum(signal_strengths))


# part 2

X = 1
cycles = 0
output = []

for instruction in instructions:
    prev_cycles = cycles
    prev_X = X
    double_cycles = instruction.startswith('addx')
    if instruction == 'noop':
        cycles += 1
        print_cycles = [prev_cycles%40]

    elif double_cycles:
        x_diff = int(instruction[5:])
        X += x_diff
        cycles += 2
        print_cycles = [prev_cycles%40, (prev_cycles+1)%40]

    for print_cycle in print_cycles:
        if abs(print_cycle - prev_X) <= 1:
            output.append('#')
        else:
            output.append('.')

foo = len(output)
for line in range(int(len(output)/40)):
    chars = output[line*40:(line+1)*40]
    print(''.join(chars))

