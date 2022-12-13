import collections.abc

with open('input.txt', 'r') as f:
    contents = f.read()

example_input = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

# contents = example_input

inputs = contents.split('\n\n')
refined_input = {}
for i, inp in enumerate(inputs):
    num = i+1
    item1, item2 = inp.splitlines()
    left = eval(item1)
    right = eval(item2)
    refined_input[num] = (left, right)


def is_in_right_order(left, right):
    if not isinstance(left, collections.abc.Sequence):
        if not isinstance(right, collections.abc.Sequence):
            if left < right:
                return True
            if left > right:
                return False
            return None

        left = [left]

    if isinstance(left, collections.abc.Sequence) and not isinstance(right, collections.abc.Sequence):
        right = [right]

    min_len = min(len(left), len(right))
    for i in range(min_len):
        l = left[i]
        r = right[i]
        iiro = is_in_right_order(l, r)
        if iiro is not None:
            return iiro

    if len(left) > min_len:
        return False

    if len(right) > min_len:
        return True

    return None


right_order_num_sum = 0
for num, pair in refined_input.items():
    left, right = pair
    res = is_in_right_order(left, right)

    if res or res is None:
        right_order_num_sum += num

print(right_order_num_sum)

# part 2

# Was trying to use Python3 native sorts but ended up in a problem
# that later proved not to be related to the sort itself
# before realizing that I ended up implementing this sort of my own...

all_packets = [eval(l) for l in contents.splitlines() if l]
first_div = [[2]]
second_div = [[6]]
all_packets.append(first_div)
all_packets.append(second_div)

current_sort_iteration = all_packets
performed_sort = True

while performed_sort:
    next_sort_iteration = []
    for_next_comp = None
    performed_sort = False
    for i in range(len(current_sort_iteration)-1):
        left = for_next_comp or current_sort_iteration[i]
        right = current_sort_iteration[i+1]
        res = is_in_right_order(left, right)
        if res is None or res:
            next_sort_iteration.append(left)
            for_next_comp = right
        else:
            performed_sort = True
            next_sort_iteration.append(right)
            for_next_comp = left
    next_sort_iteration.append(for_next_comp)
    current_sort_iteration = next_sort_iteration


d1n = next_sort_iteration.index(first_div)+1
d2n = next_sort_iteration.index(second_div)+1

print(d1n * d2n)

