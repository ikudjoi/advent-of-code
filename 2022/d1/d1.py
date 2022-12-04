with open('input.txt', 'r') as f:
    contents = f.read()

max_cal = 0
max_i = 0
batches = contents.split('\n\n')
for i, batch in enumerate(batches):
    cal_sum = sum([int(l) for l in batch.splitlines()])
    if cal_sum > max_cal:
        max_i = i
        max_cal = cal_sum

print(max_cal)

# part 2

cal_sums = [sum([int(l) for l in batch.splitlines()]) for batch in batches]
cal_sums = sorted(cal_sums)
print(cal_sums[-3:])
print(sum(cal_sums[-3:]))
