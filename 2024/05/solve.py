import itertools

from aocd import get_data

year, day = [int(v) for v in __file__.split("/")[-3:-1]]
input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

input = get_data(day=day, year=year)


class Puzzle():
    def __init__(self, input):
        ordering_s, pages_s = input.split("\n\n")
        ordering = [[int(v) for v in l.split("|")] for l in sorted(ordering_s.splitlines())]
        self.ordering = {k: {p[1] for p in v} for k, v in itertools.groupby(ordering, lambda v: v[0])}
        self.pages = [[int(v) for v in l.split(",")] for l in pages_s.splitlines()]
        self.not_ok_pages = []


    def pages_ok(self, pages):
        for cur_page_ix, cur_page in enumerate(pages):
            following_pages = pages[cur_page_ix + 1:]
            allowed_following_pages = self.ordering.get(cur_page, set())
            for following_page in following_pages:
                if not following_page in allowed_following_pages:
                    return False
        return True

    def part1(self):
        ok_pages = []
        for page in self.pages:
            if self.pages_ok(page):
                ok_pages.append(page)
            else:
                self.not_ok_pages.append(page)

        res = [p[int((len(p)-1)/2)] for p in ok_pages]
        res = sum(res)
        return res

    def fix_order_pages_once(self, pages):
        for cur_page_ix, cur_page in enumerate(pages):
            following_pages = pages[cur_page_ix + 1:]
            allowed_following_pages = self.ordering.get(cur_page, set())
            for following_page_ix, following_page in enumerate(following_pages):
                if not following_page in allowed_following_pages:
                    reordered_pages = pages[:cur_page_ix]
                    reordered_pages.append(following_page)
                    middle_untouched = pages[cur_page_ix + 1:][:following_page_ix]
                    reordered_pages.extend(middle_untouched)
                    reordered_pages.append(cur_page)
                    reordered_pages.extend(pages[cur_page_ix + 2 + following_page_ix:])
                    return reordered_pages

        return None

    def fix_order_pages(self, pages):
        cur_pages = pages.copy()
        while True:
            next_order = self.fix_order_pages_once(cur_pages)
            if not next_order:
                return cur_pages
            cur_pages = next_order

    def part2(self):
        middle_sum = 0
        for pages in self.not_ok_pages:
            reordered_pages = self.fix_order_pages(pages)
            middle_sum += reordered_pages[int((len(reordered_pages)-1)/2)]

        return middle_sum


p = Puzzle(input)
print(p.part1())
print(p.part2())
