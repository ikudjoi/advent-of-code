def main():
    with open("input.txt", "r") as f:
        contents = f.read()
    boundaries = (200000000000000, 400000000000000)

    example_input = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

    contents = example_input
    boundaries = (7, 27)


if __name__ == "__main__":
    main()
