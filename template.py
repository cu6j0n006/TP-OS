import os
import random
import time
import select

def executer(nb, taches):
    ordre_pipes = []
    retour_r, retour_w = os.pipe()

    enfants_pids = []

    # Création des enfants
    for i in range(nb):
        r, w = os.pipe()
        pid = os.fork()
        if pid == 0:
            # Enfant
            os.close(w)
            os.close(retour_r)
            ordre_fd = r
            retour_fd = retour_w
            identifiant = i + 1

            while True:
                data = os.read(ordre_fd, 1024)
                if not data:
                    break
                try:
                    cmd = int(data.decode().strip())
                    time.sleep(cmd)
                    os.write(retour_fd, f"{identifiant}\n".encode())
                except:
                    break
            os._exit(0)
        else:
            os.close(r)
            ordre_pipes.append(w)
            enfants_pids.append(pid)

    os.close(retour_w)
    disponibles = list(range(1, nb + 1))
    ordre_dict = {i + 1: ordre_pipes[i] for i in range(nb)}
    retour_fd = retour_r
    poll = select.poll()
    poll.register(retour_fd, select.POLLIN)

    remaining = list(taches)
    start_time = time.time()

    while remaining or disponibles != list(range(1, nb + 1)):
        while remaining and disponibles:
            cmd = remaining.pop(0)
            enfant_id = disponibles.pop(0)
            os.write(ordre_dict[enfant_id], f"{cmd}\n".encode())

        if not disponibles:
            events = poll.poll()
            for fd, event in events:
                if event & select.POLLIN:
                    msg = os.read(retour_fd, 1024).decode()
                    for ligne in msg.strip().splitlines():
                        enfant_id = int(ligne.strip())
                        disponibles.append(enfant_id)

    end_time = time.time()
    for w in ordre_pipes:
        os.close(w)
    os.close(retour_fd)
    for pid in enfants_pids:
        os.waitpid(pid, 0)

    return end_time - start_time


if __name__ == "__main__":
    nb_taches = 100
    taches = [random.randint(1, 10) for _ in range(nb_taches)]
    essais = [1, 2, 4, 8, 16, 32]

    print(f"\nDes tests sur {nb_taches} tâches (valeurs entre 1 et 10 secondes) :\n")
    for nb in essais:
        duree = executer(nb, taches)
        print(f"  - nb = {nb:<2} -> Temps total : {duree:.2f} secondes")
