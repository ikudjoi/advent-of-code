with open("input.txt", "r") as f:
    contents = f.read()

example_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

# contents = example_input


# line = "10 6 0 -9 -17 -3 94 430 1384 3829 9653 22684 50245 105711 212793 413161 781189 1454703 2702133 5071680 9721774"
res = 0
res2 = 0
for line in contents.splitlines():
    all_vals = [[int(v) for v in line.split(" ")]]
    vals = all_vals[-1]
    while True:
        next_vals = [y-x for x, y in zip(vals[:-1], vals[1:])]
        if len(set(next_vals)) == 1:
            final_val = next_vals[0]
            break
        all_vals.append(next_vals)
        vals = next_vals

    increment = final_val
    for vals in reversed(all_vals):
        extrapolated = vals[-1] + increment
        vals.append(extrapolated)
        increment = extrapolated

    increment = final_val
    for vals in reversed(all_vals):
        extrapolated = vals[0] - increment
        vals.insert(0, extrapolated)
        increment = extrapolated

    res += all_vals[0][-1]
    res2 += all_vals[0][0]

print(res)
print(res2)




# for line in contents.splitlines():
#     inp = {x: int(v) for x, v in enumerate(line.split(" "))}
#     x = [v for v in inp.keys()]
#     y = [v for v in inp.values()]
#     deg = 0
#     while True:
#         fit_result = np.polyfit(x, y, deg=deg, full=True)
#         coeffs, residual = fit_result[:2]
#         if abs(residual) < 0.000001:
#             f = np.poly1d(coeffs)
#             break
#         deg += 1
#
#     coeffs = [int(round(c, 0)) for c in coeffs]
#     next_val = 0
#     x = len(inp)
#     next_val = f(x)
#     next_val = int(round(next_val, 0))
#
#     res += next_val
#
#
# print(res)
# # 1782867737