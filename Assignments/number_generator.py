def number_pattern(n):
    if type(n) is not int:
        return "Argument must be an integer value."

    if n < 1:
        return "Argument must be an integer greater than 0."

        result = ""

    nums = []

    for i in range(1, n + 1):
        nums.append(str(i))
    
    return " ".join(nums)