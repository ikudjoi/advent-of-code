import math


with open('input.txt', 'r') as f:
    contents = f.read()

example_input = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

# contents = example_input


class Monkey:
    def __init__(self, input):
        i_lines = input.splitlines()
        self.number = int(i_lines[0][7:-1])
        self.items = [int(i) for i in i_lines[1][18:].split(', ')]
        self.operation = i_lines[2][19:]
        self.divisible_by = int(i_lines[3][21:])
        self.true_target_monkey = int(i_lines[4][29:])
        self.false_target_monkey = int(i_lines[5][30:])
        self.inspections = 0
        self.input = input

    def inspect(self):
        for old in self.items:
            self.inspections += 1
            new = eval(self.operation)
            worry_value = math.floor(new / 3)
            div_rest = worry_value % self.divisible_by
            if div_rest == 0:
                yield self.true_target_monkey, worry_value
            else:
                yield self.false_target_monkey, worry_value

        self.items.clear()


monkeys = contents.split('\n\n')
monkeys = [Monkey(i) for i in monkeys]


for round in range(20):
    for monkey in monkeys:
        for target_monkey, worry_value in monkey.inspect():
            monkeys[target_monkey].items.append(worry_value)
    pass


max_monkey_inspections = sorted([m.inspections for m in monkeys])[-2:]
print(max_monkey_inspections[0] * max_monkey_inspections[1])
