import math

with open("input.txt", "r") as f:
    contents = f.read()

example_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

# contents = example_input

cards = {line.split(": ")[0]: line.split(": ")[1] for line in contents.splitlines()}
cards = {k.split(" ")[-1]: v.split(" | ") for k, v in cards.items()}
cards = {int(k): [[int(v) for v in s.split(" ") if v] for s in v] for k, v in cards.items()}
res = 0
for n, card in cards.items():
    win_cards, my_cards = card
    # win_cards = set(win_cards)
    my_cards = set(my_cards)
    m = my_cards.intersection(win_cards)
    card_score = int(math.pow(2, len(m) - 1))
    res += card_score

print(res)


# part 2
number_cards = {k: 1 for k in cards}
for n, card in cards.items():
    win_cards, my_cards = card
    # win_cards = set(win_cards)
    my_cards = set(my_cards)
    m = my_cards.intersection(win_cards)
    num_this_card = number_cards[n]
    for i in range(n+1, n+1+len(m)):
        number_cards[i] += num_this_card

print(sum(number_cards.values()))
