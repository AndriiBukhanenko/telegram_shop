def calculate_sum(a, b):
    if b < a:
        a, b = b, a
    sum =0
    for item in range(a, b + 1):
        sum = sum + item

    return sum

def calculate_sum(a, b):
    _sum = sum(range(min(a,b),max(a,b)+1))

    return _sum




print(calculate_sum(1, 5) ,15)
print(calculate_sum(3, 3) , 3)
print(calculate_sum(2, -7) )