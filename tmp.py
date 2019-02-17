def test(line, reverse):
    length = len(line)
    for idx in range(length*reverse-reverse, length*(-reverse+1)-reverse, (-reverse)*2+1):
        print(line[idx])

input = "abcdef"
test(input, False)
print("---")
test(input, True)
