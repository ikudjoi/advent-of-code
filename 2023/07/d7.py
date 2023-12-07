import math

with open("input.txt", "r") as f:
    contents = f.read()

example_input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

# contents = example_input

cards = "A,K,Q,J,T,9,8,7,6,5,4,3,2"
card_values_part1 = {c: i for i, c in enumerate(cards.split(","))}


hands = contents.splitlines()
hands = {line.split(" ")[0]: int(line.split(" ")[1]) for line in hands}


def hand_type_value_part1(hand):
    card_counts = {c: hand.count(c) for c in hand}
    # Five of a kind
    if max(card_counts.values()) == 5:
        return 0
    # Four of a kind
    if max(card_counts.values()) == 4:
        return 1
    # Full house
    if len(card_counts) == 2:
        return 2
    if len(card_counts) == 3:
        # Three of a kind
        if max(card_counts.values()) == 3:
            return 3
        # Two pairs
        return 4
    # One pair
    if len(card_counts) == 4:
        return 5
    return 6


def hand_value(hand, cvs, hand_type_value_func):
    type_value = hand_type_value_func(hand)
    hand_value = type_value*10000000000
    for i, c in enumerate(hand):
        cv = cvs[c]
        hand_value += cv * int(math.pow(100, 4-i))

    return hand_value


def hand_value_part1(hand):
    return hand_value(hand, card_values_part1, hand_type_value_part1)


ordered_hands = sorted(hands.keys(), key=hand_value_part1)

res = 0
for i, h in enumerate(reversed(ordered_hands)):
    bid = hands[h]
    res += (i+1)*bid

print(res)


# part 2
cards = "A,K,Q,T,9,8,7,6,5,4,3,2,J"
card_values_part2 = {c: i for i, c in enumerate(cards.split(","))}


def hand_type_value_part2(hand):
    card_counts = {c: hand.count(c) for c in hand}
    joker_count = card_counts.pop("J", 0)
    if joker_count == 0:
        return hand_type_value_part1(hand)
    # Five of a kind
    if joker_count >= 4:
        return 0
    if joker_count == 3:
        # Five of a kind
        if len(card_counts) == 1:
            return 0
        # Four of kind
        return 1
    if joker_count == 2:
        # Five of a kind
        if len(card_counts) == 1:
            return 0
        # Four of a kind
        if len(card_counts) == 2:
            return 1
        # Three of a kind
        return 3

    # joker_count == 1
    # Five of a kind
    if len(card_counts) == 1:
        return 0
    if len(card_counts) == 2:
        # Four of a kind
        if max(card_counts.values()) == 3:
            return 1
        # Full house
        return 2
    # Three of a kind
    if len(card_counts) == 3:
        return 3
    # One pair
    return 5


def hand_value_part2(hand):
    return hand_value(hand, card_values_part2, hand_type_value_part2)


ordered_hands = sorted(hands.keys(), key=hand_value_part2)

res = 0
for i, h in enumerate(reversed(ordered_hands)):
    bid = hands[h]
    res += (i+1)*bid

print(res)
