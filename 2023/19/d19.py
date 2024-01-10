def part_accept(part, workflows):
    next_wf_name = "in"
    while True:
        if next_wf_name == "A":
            return True
        if next_wf_name == "R":
            return False
        wf = workflows[next_wf_name]

        for wf_step in wf:
            if ">" in wf_step:
                comp = lambda v, t: v > t
            elif "<" in wf_step:
                comp = lambda v, t: v < t
            else:
                next_wf_name = wf_step
                break

            k = wf_step[0]
            rest = wf_step[2:]
            threshold, dest = rest.split(":")
            threshold = int(threshold)
            res = comp(part[k], threshold)

            if res:
                next_wf_name = dest
                break


def inverse_cond(value):
    if "<" in value:
        p, v = value.split("<")
        return f"{p}>{int(v)-1}"
    elif ">" in value:
        p, v = value.split(">")
        return f"{p}<{int(v)+1}"
    else:
        raise ValueError("Unexpected!")


def is_plain_condition(value):
    if ":" in value:
        return False
    return ">" in value or "<" in value


def main():
    with open("input.txt", "r") as f:
        contents = f.read()

    example_input = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

    # contents = example_input
    workflows, input = contents.split("\n\n")
    workflows = [wf.split("{") for wf in workflows.splitlines()]
    workflows = {wf[0]: wf[1][:-1].split(",") for wf in workflows}
    parts = [{v.split("=")[0]: int(v.split("=")[1]) for v in p[1:-1].split(",")} for p in input.splitlines()]
    res = 0
    for part in parts:
        if part_accept(part, workflows):
            res += sum(part.values())
    print(res)


    # part 2

    wf = workflows["in"]
    expanded_workflows = [wf]
    fully_expanded_workflows = []
    expand = True
    while expand:
        expand = False
        next_iteration = []
        for wf in expanded_workflows:
            for i, wf_step in enumerate(wf):
                if is_plain_condition(wf_step):
                    continue

                if wf_step in ("R", "A"):
                    fully_expanded_workflows.append(wf)
                    break

                if ":" not in wf_step:
                    target_wf = workflows[wf_step]
                    merged_wf = wf[:i] + target_wf
                    next_iteration.append(merged_wf)
                    break

                expand = True
                cond, dest_step = wf_step.split(":")
                if dest_step in ("A", "R"):
                    merged_true_wf = wf[:i] + [cond] + [dest_step]
                else:
                    true_wf = workflows[dest_step]
                    merged_true_wf = wf[:i] + [cond] + true_wf
                next_iteration.append(merged_true_wf)
                inversed = inverse_cond(cond)
                on_false_step = wf[i]
                if on_false_step in ("A", "R"):
                    merged_false_wf = wf[:i] + [inversed] + [on_false_step]
                elif ":" in on_false_step:
                    merged_false_wf = wf[:i] + [inversed] + wf[i+1:]
                else:
                    false_wf = workflows[on_false_step]
                    merged_false_wf = wf[:i] + [inversed] + false_wf
                next_iteration.append(merged_false_wf)
                break

        expanded_workflows = next_iteration

    res = 0
    for wf in fully_expanded_workflows:
        if wf[-1] == "R":
            continue
        wf_values = 1
        for c in "xmas":
            conds = [co for co in wf[:-1] if co[0] == c]
            ltc = [co for co in conds if co[1] == "<"]
            lt = min([int(co[2:]) for co in ltc]) if len(ltc) > 0 else 4001
            gtc = [co for co in conds if co[1] == ">"]
            gt = max([int(co[2:]) for co in gtc]) if len(gtc) > 0 else 0
            allowed_values = lt - gt - 1
            wf_values *= allowed_values
        res += wf_values

    print(res)


if __name__ == "__main__":
    main()


dbg = """
s<1351:px,qqz

s<1351,a<2006:qkq,m>2090:A,rfg
s>1350,s>2770:qs,m<1801:hdj,R

s<1351,a<2006,x<1416:A,crn
s<1351,a>2005,m>2090:A,rfg
s>1350,s>2770,s>3448:A,lnx
s>1350,s<2771,m<1801:hdj,R

s<1351,a<2006,x<1416:A
s<1351,a<2006,x>1415,x>2662:A,R
s<1351,a>2005,m>2090:A
s<1351,a>2005,m<2091,s<537:gd,x>2440:R,A
s>1350,s>2770,s>3448:A
s>1350,s>2770,s<3449,m>1548:A,A
s>1350,s<2771,m<1801,m>838:A,pv
s>1350,s<2771,m>1800:R

s<1351,a<2006,x<1416:A
s<1351,a<2006,x>1415,x>2662:A
s<1351,a<2006,x>1415,x<2663:R
s<1351,a>2005,m>2090:A
s<1351,a>2005,m<2091,s<537,a>3333:R,R
s<1351,a>2005,m<2091,s>536,x>2440:R,A
s>1350,s>2770,s>3448:A
s>1350,s>2770,s<3449,m>1548:A
s>1350,s>2770,s<3449,m<1549:A
s>1350,s<2771,m<1801,m>838:A
s>1350,s<2771,m<1801,m<839,a>1716:R,A
s>1350,s<2771,m>1800:R


s<1351,a<2006,x<1416:A
s<1351,a<2006,x>1415,x>2662:A
s<1351,a<2006,x>1415,x<2663:R
s<1351,a>2005,m>2090:A
s<1351,a>2005,m<2091,s<537,a>3333:R
s<1351,a>2005,m<2091,s<537,a<3334:R
s<1351,a>2005,m<2091,s>536,x>2440:R
s<1351,a>2005,m<2091,s>536,x<2441:A
s>1350,s>2770,s>3448:A
s>1350,s>2770,s<3449,m>1548:A

s>1350,s>2770,s<3449,m<1549:A
s>1350,s<2771,m<1801,m>838:A
s>1350,s<2771,m<1801,m<839,a>1716:R
s>1350,s<2771,m<1801,m<839,a<1717:A
s>1350,s<2771,m>1800:R
"""