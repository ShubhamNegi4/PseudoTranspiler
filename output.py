print("ENTER A NUMBER:")
x = input()
if x.isdigit():
    x = int(x)
    divisors = 0
    i = 2
    while ((i * i) <= x):
        if ((x % i) == 0):
            divisors = (divisors + 1)
        i = (i + 1)
    if (divisors == 0):
        print("PRIME")
    else:
        print("NOT PRIME")
else:
    print("NUMBER NOT ENTERED")