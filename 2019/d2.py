def runMachine(values, replacement1, replacement2):
    values = values.copy()
    currentIndex = 0
    # replacements
    values[1] = replacement1
    values[2] = replacement2
    opCode = values[currentIndex]

    while opCode != 99:
        # print(values)
        currentIndex+=1
        aValue = values[values[currentIndex]]
        currentIndex+=1
        bValue = values[values[currentIndex]]
        currentIndex+=1
        resultLocation = values[currentIndex]
        
        if (opCode == 1):
            result = aValue + bValue
        elif (opCode == 2):
            result = aValue * bValue
        else:
            raise Exception('perkele')

        # print(f"{aValue} {bValue} {result}")
        values[resultLocation] = result
        currentIndex+=1
        opCode = values[currentIndex]

    return values[0]


with open('input2.txt') as f:
    content = f.readline().strip()

values = [int(v) for v in content.split(',')]

print(runMachine(values, 12, 2))

for noun in range(0,99):
    for verb in range(0,99):
        if (runMachine(values, noun, verb) == 19690720):
            print(100 * noun + verb)
            break






