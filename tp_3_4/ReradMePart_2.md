## **3. Groupe de processus avec `exec()`**

### Objectif :

Exécuter dynamiquement des scripts Python via `os.execl()` dans les processus enfants, et récupérer leurs sorties via un pipe.

### Étapes à suivre :

#### 1. Modifier le code des enfants :

- Chaque **enfant** ne va plus faire `time.sleep()`, mais va :
  - Rediriger sa sortie standard (`stdout`) vers le tube `retour`.
  - Lancer un script externe avec `os.execl("python3", "python3", "commande.py", id, arg1, arg2)`.

#### 2. Redirection de la sortie :

- Avant de faire `os.execl()`, dans l’enfant :
  - Fermer `stdout` (`os.close(1)`) puis dupliquer l’extrémité écriture du pipe `retour` sur `stdout` (`os.dup2(retour_w, 1)`).
  - Cela garantit que les `print()` du script `commande.py` arrivent dans le parent.

#### 3. Le parent :

- Lit la sortie standard de tous les enfants via le tube `retour`.
- Stocke les résultats (`id: résultat`) dans une liste `retours_calcul`.

#### 4. Test avec `boucles.py` :

- Ce script fait des boucles lourdes sans calcul réel (simule une charge CPU).
- Lance-le avec des arguments variables (`n` de 1 à 10, `longtemps` = 5_000_000).
- Observe :
  - Le **temps total d'exécution**.
  - L’évolution de la **concurrence** : plus d’enfants = plus de parallélisme, mais aussi plus de surcharge.

---

## **4. Calcul de Pi (Formule de Leibniz)**

### Rappel de la formule :

\[
\pi = 4 \sum\_{k=0}^{\infty} \frac{(-1)^k}{2k + 1}
\]

### 🛠 Étapes à suivre :

#### 1. Écrire `calcul.py` :

- Le script prend deux entiers N1 et N2.
- Il calcule et affiche la **somme partielle** entre ces bornes.

#### 2. Estimer les bornes pour une précision :

- Utilise l’inégalité d’erreur : pour garantir `10^-d` de précision, il faut aller jusqu’à \( k \approx 10^d \).
- Écrire une fonction `sommeFromPrecision(d)` qui retourne ce `k`.

#### 3. Intégrer dans le parent :

- Calcule `N = sommeFromPrecision(précision)`.
- Découpe l’intervalle `[0, N]` en `nb` tranches.
- Envoie chaque tranche à un processus enfant qui exécute `calcul.py N1 N2`.
- Le parent **additionne tous les résultats partiels** reçus.
- Multiplie par 4 pour obtenir une estimation de π.

---

## Tests et résultats attendus :

| Précision demandée | Approx. valeur de N | Temps avec 2, 4, 8 enfants |
| ------------------ | ------------------- | -------------------------- |
| 6 décimales        | ~1_000_000          | Rapide                     |
| 8 décimales        | ~100_000_000        | Plus lent                  |
| 12 décimales       | ~10^12 (énorme)     | Très long ou impossible    |

Tu remarqueras que :

- La parallélisation devient utile à partir de grosses valeurs de `N`.
- Il y a une **limite physique liée aux cœurs de ton CPU**.
- Le **meilleur `nb`** est proche du **nombre de cœurs logiques** de ta machine (à tester empiriquement).
