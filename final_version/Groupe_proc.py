import os
import time
import random

NB_ENFANTS = 4
NB_TACHES = 20

def boucle_enfant(pipe_lecture, retour_ecriture, identifiant):
    while True:
        commande = os.read(pipe_lecture, 10).decode().strip()
        if commande == "quit":
            break
        print(f"[Enfant {identifiant}] Reçu : {commande}, dodo {commande} sec")
        time.sleep(int(commande))
        os.write(retour_ecriture, f"{identifiant}\n".encode())

def distribuer_les_commandes(pipes_ordre, pipe_retour, nb_taches):
    enfants_disponibles = list(range(len(pipes_ordre)))
    taches = []
    for i in range(nb_taches):
        taches.append(random.randint(1, 5))

    while taches or len(enfants_disponibles) < len(pipes_ordre):
        while taches and enfants_disponibles:
            enfant = enfants_disponibles.pop(0)
            commande = f"{taches.pop(0)}\n"
            os.write(pipes_ordre[enfant][1], commande.encode())
            print(f"[Parent] Envoi à enfant {enfant} : {commande.strip()} sec")

        if not enfants_disponibles:
            msg = os.read(pipe_retour, 10).decode().strip()
            if msg.isdigit():
                print(f"[Parent] Enfant {msg} est libre")
                enfants_disponibles.append(int(msg))

    for i, w in enumerate(pipes_ordre): #on envoit "quit"
        os.write(w[1], b"quit\n")
        print(f"[Parent] Quit envoyé à enfant {i}")

def main():
    ordre = []
    retour = os.pipe()

    # Création des pipes et des enfants
    for i in range(NB_ENFANTS):
        ordre.append(os.pipe())

    for i in range(NB_ENFANTS):
        pid = os.fork()
        if pid == 0:
            for j in range(NB_ENFANTS):
                if j != i:
                    os.close(ordre[j][0])
                    os.close(ordre[j][1])
            os.close(ordre[i][1])
            os.close(retour[0])
            boucle_enfant(ordre[i][0], retour[1], i)
            os._exit(0)
    for i in range(NB_ENFANTS): # Parent
        os.close(ordre[i][0])
    os.close(retour[1])

    debut = time.time()
    distribuer_les_commandes(ordre, retour[0], NB_TACHES)
    fin = time.time()
    print(f"\nTemps total : {round(fin - debut, 2)} secondes")

if __name__ == "__main__":
    main()
