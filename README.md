#  Calculateur de Ligne de Vue 2D (Raycasting Algorithmique)

##  Présentation du projet
Ce projet implémente un moteur de calcul de champ de vision (Ligne de Vue / Raycasting) en 2D. Inspiré des mécaniques de vision de jeux vidéo (comme *Project Zomboid*), l'algorithme calcule dynamiquement la zone visible par un observateur au milieu d'obstacles (murs), générant un polygone de visibilité.

**Auteurs :** Efe Ilhan et Norik Kalachyan
**Module :** Mathématiques appliquées et calcul numérique

##  Structure du dépôt
* `tp/` : Contient l'ensemble des solutions aux exercices de TP réalisés pendant le semestre.
* `projet/` : Contient le code source de ce projet personnel.

##  Comment lancer le projet
1. Assurez-vous d'avoir un environnement Python 3 fonctionnel.
2. Installez la bibliothèque d'affichage (si ce n'est pas déjà fait) : 
   `pip install matplotlib`
3. Exécutez le script principal depuis le dossier `projet/` : 
   `python main.py` *(si votre fichier porte un autre nom, remplacez main.py)*
4. **Ce qu'il faut observer :** Le programme affiche une carte 2D avec des murs noirs, la position du joueur en rouge, et le cône de vision calculé en jaune. Déplacez la souris sur la fenêtre pour voir le champ de vision se mettre à jour en temps réel.

##  Notions mathématiques mobilisées
Conformément aux attentes du module, ce projet n'utilise aucune bibliothèque géométrique externe pour le cœur du calcul (tout est fait à la main).
* **Géométrie vectorielle et systèmes linéaires :** Le calcul de l'intersection entre un rayon de vision (demi-droite) et un obstacle (segment) se fait via la mise en équation paramétrique des deux éléments.
* **Calcul matriciel (Déterminant) :** Utilisation du produit vectoriel 2D pour vérifier si le rayon et le mur sont parallèles, et pour résoudre le système.
* **Arithmétique des flottants :** Résolution des erreurs de précision machine lors des calculs d'angles rasants.

##  Analyse critique et profondeur d'exploitation

**1. La limite de précision des nombres flottants (L'astuce de l'Epsilon)**
Le défi principal de cet algorithme concerne la norme IEEE 754 des flottants. Lorsqu'un rayon frappe exactement l'extrémité d'un segment, les approximations d'arrondis rendent le résultat instable : le programme hésite et ne sait pas si le rayon traverse le mur ou est bloqué. 
Pour stabiliser l'algorithme, nous avons implémenté une marge d'erreur infinitésimale (epsilon = 0.00001). Au lieu de lancer un seul rayon par sommet, le programme en lance trois : sur l'angle exact, légèrement à gauche (angle - epsilon), et légèrement à droite (angle + epsilon). Cela force mathématiquement le rayon décalé à "passer derrière" l'obstacle, générant une ombre correcte sans artefact visuel.

**2. Optimisation géométrique vs Méthode naïve**
La première approche envisagée (naïve) consistait à lancer 360 rayons autour de l'observateur (un par degré). Outre son inefficacité, elle causait des "trous" dans le champ de vision sur les murs éloignés à cause de l'écartement des rayons. L'implémentation finale est purement géométrique : l'algorithme repère les extrémités des murs et ne lance des rayons **que** vers ces points précis, garantissant une précision parfaite et une complexité réduite.

##  Utilisation de l'Intelligence Artificielle
Dans le respect des consignes d'évaluation, nous déclarons avoir utilisé un assistant IA comme aide technique.
* **Ce que l'IA a généré :** L'assistant a été utilisé pour nous proposer l'idée initiale, nous expliquer la méthode de résolution du système paramétrique (calcul de t et u via le déterminant), et fournir le squelette de base pour l'affichage avec matplotlib.
* **Ce que nous avons réalisé, vérifié et analysé nous-mêmes :** 
  * **L'analyse du problème des flottants :** Nous avons modifié le code pour tester l'algorithme sans la marge d'erreur (epsilon). Nous avons pu constater visuellement l'apparition d'artefacts (des rayons qui traversent les coins des murs). Cela nous a permis de vérifier par nous-mêmes comment la machine gère les arrondis (IEEE 754) et pourquoi le décalage mathématique des rayons était obligatoire pour obtenir un ombrage solide.
  * **Implémentation de l'interactivité en temps réel :** Nous avons restructuré la fin du code pour intégrer la gestion d'événements de `matplotlib` (`motion_notify_event`). Nous avons créé une fonction de rafraîchissement qui recalcule le système d'équations paramétriques à chaque mouvement de la souris, transformant un simple graphique statique en un véritable prototype de mécanique de jeu.
  * **Création d'une topologie de test complexe (Level Design) :** Nous avons remplacé les murs de base par un plan structuré simulant un intérieur de bâtiment (murs extérieurs, cloison, obstacle central type table). Cela nous a permis de vérifier que l'algorithme gère correctement les occlusions multiples (quand un mur en cache un autre situé derrière lui).
  * La reprise complète et la correction des TP présents dans le dossier `tp/`.
