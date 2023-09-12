a = ["1", "2", "3", "4", "5"]

for a in filter(lambda x: int(x) > 3, a):
    print(a)
