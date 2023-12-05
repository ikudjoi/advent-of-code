with open("input.txt", "r") as f:
    contents = f.read()

example_input = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

# contents = example_input

paragraphs = contents.split("\n\n")
current_values = [int(s) for s in paragraphs[0][7:].split(" ")]
value_type = "seed"


class Map:
    def __init__(self, configuration):
        self.configuration = configuration
        conf_lines = configuration.splitlines()
        dir = conf_lines[0][:-5].split("-to-")
        self.source, self.target = dir
        mappings = [[int(v) for v in l.split(" ")] for l in conf_lines[1:]]
        # Convert to start-end-offset mapping
        self.mappings = [(s, s+l, d-s) for d, s, l in mappings]

    def map_ranges(self, rngs):
        input_ranges = rngs
        for r_start, r_end, offset in self.mappings:
            modified_ranges = []
            for start, end in input_ranges:
                if end <= r_start:
                    modified_ranges.append((start, end))
                    continue
                if start >= r_end:
                    modified_ranges.append((start, end))
                    continue
                if start < r_start:
                    modified_ranges.append((start, r_start))
                    start = r_start
                if end > r_end:
                    modified_ranges.append((r_end, end))
                    end = r_end

                modified_range_start = max(start, r_start) + offset
                modified_range_end = min(end, r_end) + offset
                yield modified_range_start, modified_range_end

            input_ranges = modified_ranges
        for r in input_ranges:
            yield r

    def map_value(self, src_value):
        for r_start, r_end, offset in self.mappings:
            if r_start <= src_value <= r_end:
                return src_value + offset

        return src_value

    def map(self, src_values):
        return [self.map_value(v) for v in src_values]


maps = [Map(p) for p in paragraphs[1:]]
maps = {m.source: m for m in maps}


def map_to_location(mps, input_value):
    value_type = "seed"
    current_value = input_value
    while value_type != "location":
        map = mps[value_type]
        current_value = map.map_value(current_value)
        value_type = map.target
    return current_value


locations = [map_to_location(maps, s) for s in current_values]
print(min(locations))


# part 2

value_type = "seed"
seed_range_input = [int(s) for s in paragraphs[0][7:].split(" ")]
min_location = None
seed_range_starts = seed_range_input[0::2]
seed_range_lengths = seed_range_input[1::2]

# Range ends are exclusive
ranges = [(rs, rs+rl) for rs, rl in zip(seed_range_starts, seed_range_lengths)]
value_type = "seed"
while value_type != "location":
    map = maps[value_type]
    next_ranges = []
    value_type = map.target
    for cr in map.map_ranges(ranges):
        next_ranges.append(cr)
    ranges = next_ranges

print(min([s for s,e in ranges]))
