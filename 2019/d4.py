def passwordValid1(value):
    previousDigit = None
    pairFound = False
    while value > 0:
        digit = value % 10
        # print(f"value {value} digit {digit}")
        if digit == previousDigit:
            pairFound = True
        if previousDigit is not None and digit > previousDigit:
            return False
        previousDigit = digit

        # remove last digit from number (as integer) and continue
        value //= 10

    return pairFound

def passwordValid2(value):
    previousDigit = None
    pairNumber = None
    pairNumberFoundInvalid = False
    while value > 0:
        digit = value % 10
        # print(f"value {value} digit {digit}")
        
        # If a potential pair number was already found but yet another (third) is found, erase the found pair.
        if pairNumber is not None and digit == pairNumber:
            # print("found invalid")
            pairNumberFoundInvalid = True
        elif digit == previousDigit and (pairNumber is None or (pairNumberFoundInvalid and pairNumber != digit)):
            # print("new good pair found")
            pairNumber = digit
            pairNumberFoundInvalid = False
        if previousDigit is not None and digit > previousDigit:
            return False
        previousDigit = digit

        # remove last digit from number (as integer) and continue
        value //= 10

    return not pairNumberFoundInvalid and pairNumber is not None

minValue = 197487
maxValue = 673251
# minValue = 579999
# maxValue = 579999
validCount = 0

for value in range(minValue, maxValue + 1):
    if passwordValid2(value):
        print(f"{value} is valid")
        validCount += 1

print(validCount)