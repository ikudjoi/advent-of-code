def hsh(value):
    res = 0
    for c in value:
        av = ord(c)
        res += av
        res *= 17
        res %= 256
    return res

def main():
    with open("input.txt", "r") as f:
        contents = f.read().rstrip()

    # example_input = "HASH"
    example_input = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    # contents = example_input
    steps = contents.split(",")
    res = 0
    for step in steps:
        current_value = hsh(step)
        res += current_value
    print(res)

    # part 2
    boxes = {}
    for step in steps:
        if step[-1] == "-":
            label = step[:-1]
            focal_len = None
        else:
            label, focal_len = step.split("=")
            focal_len = int(focal_len)
        box = hsh(label)
        box_arr = boxes.get(box, [])
        new_arr_ver = []
        already_existed = False
        new_itm = (label, focal_len)
        for itm in box_arr:
            i_label, i_focal_len = itm
            if i_label == label:
                already_existed = True
                if not focal_len:
                    continue
                else:
                    new_arr_ver.append(new_itm)
            else:
                new_arr_ver.append((i_label, i_focal_len))
        if not already_existed and focal_len:
            new_arr_ver.append(new_itm)

        boxes[box] = new_arr_ver

    res = 0
    for box_num, box_arr in boxes.items():
        for slot_num, lens in enumerate(box_arr):
            lens_value = (box_num+1)*(slot_num+1)*(lens[1])
            res += lens_value

    print(res)


if __name__ == "__main__":
    main()
