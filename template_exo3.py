import os
import select
import time
import random

def executer(nb, lignes_commandes):
    ordre_pipes = []
    retour_pipes = []  # Liste des pipes (r) pour stdout des enfants
    enfants_pids = []
    retours_calcul = []

    for i in range(nb):
        ordre_r, ordre_w = os.pipe()
        retour_r, retour_w = os.pipe()
        pid = os.fork()

        if pid == 0:
            # Enfant
            os.dup2(retour_w, 1)  # redirige stdout vers retour_w
            for fd in [ordre_w, retour_r, retour_w]:
                os.close(fd)  # on garde uniquement ordre_r et stdout

            id_str = str(i + 1)
            ligne = os.read(ordre_r, 1024).decode().strip()
            if ligne:
                cmd = ligne.split()
                os.execlp("python3", "python3", cmd[0], id_str, *cmd[1:])
            os._exit(1)
        else:
            os.close(ordre_r)
            os.close(retour_w)
            ordre_pipes.append(ordre_w)
            retour_pipes.append(retour_r)
            enfants_pids.append(pid)

    # Envoyer les commandes aux enfants
    for i, cmd in enumerate(lignes_commandes):
        os.write(ordre_pipes[i], (cmd + "\n").encode())
        os.close(ordre_pipes[i])  # fermeture côté parent après écriture

    # Lecture non-bloquante des retours
    poll = select.poll()
    for retour_fd in retour_pipes:
        poll.register(retour_fd, select.POLLIN)

    finished = 0
    while finished < nb:
        events = poll.poll()
        for fd, event in events:
            if event & select.POLLIN:
                data = os.read(fd, 1024).decode()
                if data:
                    retours_calcul.extend(data.strip().splitlines())
            finished += 1
            poll.unregister(fd)
            os.close(fd)

    for pid in enfants_pids:
        os.waitpid(pid, 0)

    return retours_calcul


if __name__ == "__main__":
    # Préparation des lignes de commande
    nb_lignes = 20
    commandes = [
        f"boucles.py {random.randint(1, 10)} 5000000"
        for _ in range(nb_lignes)
    ]

    essais = [1, 2, 4, 8, 16]
    print("\nDes tests avec boucles.py (5000000 tours)\n")
    for nb in essais:
        lignes = commandes[:nb]  # on envoie autant de commandes que de processus
        t0 = time.time()
        resultats = executer(nb, lignes)
        t1 = time.time()
        print(f"  - nb = {nb:<2} → Temps : {t1 - t0:.2f}s | Résultats: {resultats}")
