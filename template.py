import os
import sys
import select

nb = 3  # nombre de processus enfants
taches = ["python3 script1.py", "python3 script2.py", "python3 script3.py", "python3 script4.py"]

ordre_pipes = []  # tubes parent -> enfants
retour_r, retour_w = os.pipe()  # tube enfants -> parent

# Création des tubes et des processus enfants
for i in range(nb):
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        # Enfant
        os.close(w)  # ferme le bout d’écriture
        os.close(retour_r)  # l’enfant n’a pas besoin de lire sur retour
        ordre_fd = r
        retour_fd = retour_w
        identifiant = str(i + 1)

        while True:
            commande = os.read(ordre_fd, 1024).decode()
            if not commande:
                break  # tube fermé
            args = commande.strip().split()
            # Exécute la commande reçue (remplace le processus)
            try:
                os.execvp(args[0], args)
            except Exception as e:
                os.write(retour_fd, f"ERREUR {identifiant}\n".encode())
                os._exit(1)
    else:
        # Parent
        os.close(r)  # ferme le bout de lecture
        ordre_pipes.append(w)

# Le parent continue ici
os.close(retour_w)  # le parent n’écrit pas dans retour
disponibles = list(range(1, nb + 1))  # file des enfants disponibles
ordre_dict = {i + 1: ordre_pipes[i] for i in range(nb)}  # id -> pipe

# Écoute non-bloquante sur retour
retour_fd = retour_r
poll = select.poll()
poll.register(retour_fd, select.POLLIN)

while taches or disponibles != list(range(1, nb + 1)):
    # Attribuer les tâches disponibles
    while taches and disponibles:
        cmd = taches.pop(0)
        enfant_id = disponibles.pop(0)
        os.write(ordre_dict[enfant_id], (cmd + "\n").encode())

    # Attendre qu’un enfant se libère si aucun n’est disponible
    if not disponibles:
        events = poll.poll()
        for fd, event in events:
            if event & select.POLLIN:
                msg = os.read(retour_fd, 1024).decode()
                for ligne in msg.strip().splitlines():
                    if ligne.startswith("ERREUR"):
                        enfant_id = int(ligne.split()[1])
                    else:
                        enfant_id = int(ligne.strip())
                    disponibles.append(enfant_id)
