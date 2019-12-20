with open('input1.txt') as f:
    content = f.readlines()

def calculateFuel(values):
    result = [v/3 for v in values]
    result = [v-2 for v in result]
    result = [max(0, v) for v in result]
    return result

values = [int(v) for v in content]
values = calculateFuel(values)
totalFuel = sum(values)
print(totalFuel)

while True:
    values = calculateFuel(values)
    addedFuel = sum(values)
    if (addedFuel == 0):
        break

    totalFuel += addedFuel

print(totalFuel)
