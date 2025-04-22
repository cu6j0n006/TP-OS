### 1. Comprendre l’objectif

Avant de coder, assure-toi de bien comprendre le fonctionnement global :

- Tu as un **processus parent** qui crée plusieurs **processus enfants**.
- Le parent a une **liste de commandes** (ici, des entiers qui indiquent combien de secondes "d'attente" chaque commande représente).
- Les **enfants reçoivent une commande**, dorment pendant la durée indiquée, puis **signalent au parent qu’ils sont libres**.
- Le parent gère les enfants disponibles et attribue les commandes au fur et à mesure.

---

### 2. Définir la communication (pipes)

Tu as deux sens de communication :

- **Parent → Enfant i** : un tube `ordre[i]` pour chaque enfant (écrire des commandes).
- **Enfants → Parent** : un seul tube `retour`, partagé par tous les enfants, où chacun écrit quand il a fini.

Donc :

- Chaque enfant a un tube d’entrée personnel (pour recevoir des ordres).
- Tous les enfants partagent un tube de sortie commun (pour indiquer qu’ils ont terminé).

---

### 3. Création des processus enfants

- Le parent crée `nb` enfants avec un `fork` (ou autre méthode selon le langage).
- Chaque enfant entre dans une boucle infinie où il attend une commande sur son tube d’entrée.
- Lorsqu’il reçoit une commande, il :
  1. la lit,
  2. attend pendant `n` secondes,
  3. écrit son identifiant dans le tube `retour`.

---

### 4. Le parent gère la distribution

- Le parent a une **liste de tâches** (par exemple, 100 entiers entre 1 et 10).
- Il maintient aussi une **liste des enfants disponibles**.
- Tant qu’il y a des tâches :
  1. Il vérifie s’il a un enfant disponible.
  2. Il envoie une commande à cet enfant.
  3. Si aucun enfant n’est libre, il **attend un message sur le tube `retour`** indiquant qu’un enfant a fini.
  4. Il remet alors cet enfant dans la liste des disponibles.

---

### 5. Fin de traitement

- Quand toutes les tâches sont terminées, le parent :
  1. Envoie une commande spéciale (`"quit"`) à chaque enfant pour les arrêter.
  2. Attend que tous les enfants terminent et se ferment proprement.

---

### 6. Tester les performances

- Tu choisis une valeur de `nb` (nombre de processus enfants).
- Tu observes combien de temps prend l’exécution avec différentes valeurs de `nb`.
- Cela te permet de déterminer la meilleure valeur pour ta machine (celle qui exécute les tâches le plus rapidement sans trop créer de surcharge).

---

### 🛠️ Astuces supplémentaires

- Utilise bien les **fermetures de tubes** (très important) pour éviter les blocages.
- Gère proprement les conversions (par exemple, si tu envoies un entier sous forme de texte, assure-toi que l’enfant sait le lire correctement).
- Tu peux aussi logguer les actions (qui fait quoi, quand) pour t’assurer que la logique est bien respectée.
