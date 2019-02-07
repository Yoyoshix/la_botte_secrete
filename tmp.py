number = "1.1"
res = ""
try:
    res = round(float(number) ** 2, 10)
except ValueError as e:
    print("error :", e)
print(res)