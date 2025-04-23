# calcul.py
from sys import argv

N1 = int(argv[1])
N2 = int(argv[2])
somme = 0.0

for k in range(N1, N2):
    somme += ((-1) ** k) / (2 * k + 1)

print(somme)
