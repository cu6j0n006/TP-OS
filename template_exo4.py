import os
import math
import select
import sys

def sommeFromPrecision(d):
    return int(5 * (10 ** d))

def executer(nb, N):
    step = N // nb
    reste = N % nb
    enfants_pids = []
    retour_fds = []
    total = 0.0

    for i in range(nb):
        N1 = i * step
        N2 = (i + 1) * step if i != nb - 1 else N  # pour dernier bloc
        retour_r, retour_w = os.pipe()
        pid = os.fork()

        if pid == 0:
            os.dup2(retour_w, 1)  # stdout → pipe
            os.close(retour_r)
            os.execlp("python3", "python3", "calcul.py", str(N1), str(N2))
            os._exit(1)
        else:
            os.close(retour_w)
            retour_fds.append(retour_r)
            enfants_pids.append(pid)

    poll = select.poll()
    for fd in retour_fds:
        poll.register(fd, select.POLLIN)

    lu = 0
    while lu < nb:
        events = poll.poll()
        for fd, event in events:
            if event & select.POLLIN:
                data = os.read(fd, 1024).decode()
                if data:
                    total += float(data.strip())
                os.close(fd)
                poll.unregister(fd)
                lu += 1

    for pid in enfants_pids:
        os.waitpid(pid, 0)

    return 4 * total  # Leibniz donne pi/4

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <nb> <precision>")
        sys.exit(1)

    nb = int(sys.argv[1])
    precision = int(sys.argv[2])
    N = sommeFromPrecision(precision)

    print(f"Calcul de π avec {nb} processus et précision {precision} décimales.")
    pi_approx = executer(nb, N)
    print(f"Résultat : {pi_approx:.{precision}f}")
