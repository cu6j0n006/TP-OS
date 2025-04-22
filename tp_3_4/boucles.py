from sys import argv

id = argv[1]
n = int(argv[2])
longtemps = int(argv[3])

for i in range(n):
    for j in range(longtemps):
        pass

print(f"{id}: Fini {n} boucles")