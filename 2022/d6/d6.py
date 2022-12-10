with open('input.txt', 'r') as f:
    contents = f.read()

# example_input = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
# example_input = "bvwbjplbgvbhsrlpgdmjqwftvncz"
# example_input = "nppdvjthqldpwncqszvftbrmjlhg"
# example_input = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
# example_input = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
example_input = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"

# contents = example_input


def find_marker(marker_length):
    buffered_chars = []
    for idx, c in enumerate(contents.strip()):
        if len(buffered_chars) < marker_length:
            buffered_chars.append(c)
            continue

        if len(set(buffered_chars)) < marker_length:
            buffered_chars = buffered_chars[1:]
            buffered_chars.append(c)
            continue

        return idx


print(find_marker(4))

# part 2
# I was lucky to guess how part 2 would extend the problem and
# made the marker length fully dynamic in the first place :)

print(find_marker(14))