import os
import sys
import math

def sommeFromPrecision(decimal):
    return math.ceil((10**decimal - 1) / 2)

def execute_calcul(id, N1, N2, retour_write):
    os.dup2(retour_write, 1)  # Rediriger la sortie standard vers le tube
    os.close(retour_write)
    os.execl("/usr/bin/python3", "python3", "calcul.py", str(id), str(N1), str(N2))

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} <nb_processus> <precision>")
        sys.exit(1)
    
    nb = int(sys.argv[1])  # Nombre de processus parallèles
    precision = int(sys.argv[2])  # Précision souhaitée en décimales

    N = sommeFromPrecision(precision)
    print(f"Pour obtenir {precision} décimales précises, il faut calculer {N} termes.")

    bloc_size = N // nb
    if N % nb != 0:
        bloc_size += 1
    
    processus = []
    tubes = []
    
    for i in range(nb):
        N1 = i * bloc_size
        N2 = min((i + 1) * bloc_size, N)
        
        if N1 >= N2:
            break
        
        retour_read, retour_write = os.pipe()
        
        pid = os.fork()
        
        if pid == 0:  
            os.close(retour_read)            
            execute_calcul(i, N1, N2, retour_write)
            
            sys.exit(1) #sauf erreur de execl

        else: 
            os.close(retour_write)
            processus.append(pid)
            tubes.append(retour_read)
    
    somme_totale = 0.0
    
    for fd in tubes:
        resultat = os.read(fd, 1024).decode().strip()
        id, valeur = resultat.split(': ')
        somme_totale += float(valeur)

        os.close(fd)
    
    for pid in processus:# Attendre la fin des processus enfants
        os.waitpid(pid, 0)
    
    
    pi = 4.0 * somme_totale # Multiplier par 4 pour obtenir Pi
    
    print(f"Valeur de pi calculée: {pi:.{precision}f}")
    print(f"Valeur de pi (math.pi): {math.pi}")
    print(f"Différence: {abs(pi - math.pi)}")

if __name__ == "__main__":
    main()