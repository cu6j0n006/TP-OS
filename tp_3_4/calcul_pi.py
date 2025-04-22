import os
import sys
import math

def sommeFromPrecision(decimal):
    """
    Renvoie le nombre de termes nécessaires pour obtenir une précision de 'decimal' décimales.
    
    Pour une série alternée comme celle de Leibniz, la majoration de l'erreur
    est donnée par le premier terme non inclus dans la somme.
    
    Pour la formule de Leibniz: π/4 = 1 - 1/3 + 1/5 - 1/7 + ...
    Si on s'arrête à N termes, l'erreur est majorée par 1/(2*N+1)
    
    Pour obtenir 'decimal' décimales, il faut que 1/(2*N+1) < 10^(-decimal)
    Donc 2*N+1 > 10^decimal
    N > (10^decimal - 1)/2
    """
    return math.ceil((10**decimal - 1) / 2)

def execute_calcul(id, N1, N2, retour_write):
    # Rediriger la sortie standard vers le tube
    os.dup2(retour_write, 1)
    
    # Fermer le descripteur de fichier pour le tube en écriture
    os.close(retour_write)
    
    # Exécuter la commande calcul.py avec les paramètres
    os.execl("/usr/bin/python3", "python3", "calcul.py", str(id), str(N1), str(N2))

def main():
    # Vérifier les arguments
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} <nb_processus> <precision>")
        sys.exit(1)
    
    nb = int(sys.argv[1])  # Nombre de processus parallèles
    precision = int(sys.argv[2])  # Précision souhaitée en décimales
    
    # Calculer le nombre de termes nécessaires
    N = sommeFromPrecision(precision)
    print(f"Pour obtenir {precision} décimales précises, il faut calculer {N} termes.")
    
    # Calculer la taille de chaque bloc
    bloc_size = N // nb
    if N % nb != 0:
        bloc_size += 1
    
    processus = []
    tubes = []
    
    # Créer les processus pour calculer en parallèle
    for i in range(nb):
        N1 = i * bloc_size
        N2 = min((i + 1) * bloc_size, N)
        
        if N1 >= N2:
            break
        
        # Créer un tube pour la communication
        retour_read, retour_write = os.pipe()
        
        # Créer un processus enfant
        pid = os.fork()
        
        if pid == 0:  # Processus enfant
            # Fermer l'extrémité de lecture dans l'enfant
            os.close(retour_read)
            
            # Exécuter le calcul
            execute_calcul(i, N1, N2, retour_write)
            
            # Ne devrait jamais arriver si execl a réussi
            sys.exit(1)
        else:  # Processus parent
            # Fermer l'extrémité d'écriture dans le parent
            os.close(retour_write)
            
            # Stocker les informations sur le processus et le tube
            processus.append(pid)
            tubes.append(retour_read)
    
    # Récupérer les résultats
    somme_totale = 0.0
    
    for fd in tubes:
        # Lire les données du tube
        resultat = os.read(fd, 1024).decode().strip()
        
        # Extraire la valeur numérique
        id, valeur = resultat.split(': ')
        somme_totale += float(valeur)
        
        # Fermer le descripteur de fichier
        os.close(fd)
    
    # Attendre la fin des processus enfants
    for pid in processus:
        os.waitpid(pid, 0)
    
    # Multiplier par 4 pour obtenir Pi
    pi = 4.0 * somme_totale
    
    print(f"Valeur de π calculée: {pi}")
    print(f"Valeur de π (math.pi): {math.pi}")
    print(f"Différence: {abs(pi - math.pi)}")

if __name__ == "__main__":
    main()