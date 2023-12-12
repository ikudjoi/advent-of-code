from functools import cache


def validate(row, counts, replacements):
    replacements_copy = list(replacements)
    counts_copy = counts.copy()

    current_expected_count_hashes = counts_copy.pop(0)
    current_counted_hashes = 0
    for c in row:
        if c == "?":
            c = replacements_copy.pop(0)
        if c == "#":
            current_counted_hashes += 1
            continue

        # Continue counting if not even started yet
        if current_counted_hashes == 0:
            continue

        # c == "."
        if current_counted_hashes > current_expected_count_hashes:
            return False
        if 0 < current_counted_hashes < current_expected_count_hashes:
            return False

        current_expected_count_hashes = counts_copy.pop(0) if counts_copy else 0
        current_counted_hashes = 0

    return current_expected_count_hashes == current_counted_hashes


def permutate(hash_count, dot_count):
    if hash_count == 0:
        yield "." * dot_count
    elif dot_count == 0:
        yield "#" * hash_count
    else:
        for v in permutate(hash_count - 1, dot_count):
            yield "#" + v
        for v in permutate(hash_count, dot_count - 1):
            yield "." + v


@cache
def num_arrangements(row, counts):
    if len(counts) == 0:
        if "#" in row:
            return 0
        return 1

    total_arrangements = 0
    min_length_row = sum(counts) + len(counts) - 1
    if len(row) < min_length_row:
        return 0

    current_expected_count = counts[0]
    damaged_group_ok_here = all([c in ("#", "?") for c in row[:current_expected_count]])
    if damaged_group_ok_here:
        if len(row) == current_expected_count:
            return 1

        if row[current_expected_count] in (".", "?"):
            rest_row = row[current_expected_count+1:]
            rest_counts = counts[1:]
            total_arrangements = num_arrangements(rest_row, rest_counts)

    if row[0] == "#":
        return total_arrangements

    rest_row = row[1:]
    return total_arrangements + num_arrangements(rest_row, counts)


def main():
    with open("input.txt", "r") as f:
        contents = f.read()

    example_input = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

    # contents = example_input
    res = 0
    lines = contents.splitlines()
    rows = {i: (x.split(" ")[0], [int(v) for v in x.split(" ")[1].split(",")])
            for i, x in enumerate(lines)}
    for n, row_counts in rows.items():
        row, counts = row_counts
        counts *= 5
        counts = tuple(counts)
        fiverow = "?".join([row for i in range(5)])
        num_arrgm = num_arrangements(fiverow, counts)
        print(f"{n} {num_arrgm}")

        # total_unknown = len([c for c in row if c == "?"])
        # total_hash = len([c for c in row if c == "#"])
        # expected_hashes = sum(counts)
        # missing_hashes = expected_hashes - total_hash
        # permuted = permutate(missing_hashes, total_unknown - missing_hashes)
        # valid_permutations = [v for v in permuted if validate(row, counts, v)]
        # if num_arrgm != len(valid_permutations):
        #     raise ValueError("")
        res += num_arrgm

    print(res)


if __name__ == "__main__":
    main()


    # row = '??????#.?#????'
    # counts = [2,2,4]
    # narg = num_arrangements('#.?#????', [4])
    # narg = num_arrangements('???#.?#????', [2,4])
    # narg = num_arrangements('??????#.?#????', counts)
    # foo = list(permutate(6, 5))
    # res = []
    # for f in foo:
    #     if not validate(row, counts, f):
    #         continue
    #     repl = [c for c in f]
    #     bar = []
    #     for c in row:
    #         if c == "?":
    #             c = repl.pop(0)
    #         bar.append(c)
    #     res.append("".join(bar))
