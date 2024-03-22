H = ["001", "010", "011", "100", "101", "110", "111"]
w = "1101011"
print("Syndrome: ")

def multi(a, b):
    if (a == "0") | (b == "0"):
        return "0"
    else:
        return "1"

def add(a):
    sum = "0"
    for i in a:
        if sum == i:
            sum = "0"
        else:
            sum = "1"
    return sum

for i in H:
    result1 = ""
    result2 = ""
    result3 = ""
    element1 = i[0]
    element2 = i[1]
    element3 = i[2]
    print(element1, element2, element3, sep="")
    for k in w:
        result1 += multi(k, element1)
        result2 += multi(k, element2)
        result3 += multi(k, element3)
    print(result1, result2, result3)

print(add(result1), add(result2), add(result3), sep="")

