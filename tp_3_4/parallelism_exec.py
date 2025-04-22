import os
import sys
from multiprocessing import Process, Pipe

def execute_commande(commande, args, retour_write):
    # Rediriger la sortie standard vers le tube
    os.dup2(retour_write, 1)
   
    os.close(retour_write)
    os.execl("/usr/bin/python3", "python3", commande, str(os.getpid()), *args)    # Exécuter la commande avec execl

def main():
    nb = 4  # nombre de processus à créer
    commandes = [
        ["boucles.py", "1", "5000000"],
        ["boucles.py", "3", "5000000"],
        ["boucles.py", "5", "5000000"],
        ["boucles.py", "10", "5000000"]
    ]
    
    processus = []
    tubes = []
    
    #in this section, the child computes the commands 
    #and sends a return to the parent. 
    # child -> write (compute) -> parent -> read 
    #  
    for i, cmd_args in enumerate(commandes):
        retour_read, retour_write = os.pipe() #creation des tubes de communication 
        pid = os.fork()
        
        if pid == 0:  
            os.close(retour_read)
            execute_commande(cmd_args[0], cmd_args[1:], retour_write) # Exécuter la commande

            sys.exit(1) # os._exit(1)

        else:
            os.close(retour_write)
            processus.append(pid)
            tubes.append(retour_read)
    
    # Récupérer les résultats
    retours_calcul = []
    
    for fd in tubes:
        resultat = os.read(fd, 1024).decode().strip()
        retours_calcul.append(resultat)
        os.close(fd)
    
    for pid in processus: #on attend le processus des enfants 
        os.waitpid(pid, 0)
        
    print("Résultats collectés:")
    for resultat in retours_calcul:
        print(resultat)

if __name__ == "__main__":
    main()