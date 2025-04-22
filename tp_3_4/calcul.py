import sys

def somme_leibniz(N1, N2):
    """Calcule la somme partielle de Leibniz de N1 (inclus) à N2 (non inclus)."""
    somme = 0.0
    for n in range(N1, N2):
        terme = 1.0 / (2 * n + 1)
        if n % 2 == 0:
            somme += terme
        else:
            somme -= terme
    return somme

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: python3 {sys.argv[0]} id N1 N2")
        sys.exit(1)
    
    id = sys.argv[1]
    N1 = int(sys.argv[2])
    N2 = int(sys.argv[3])
    
    resultat = somme_leibniz(N1, N2)
    print(f"{id}: {resultat}")