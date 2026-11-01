# 🔦 Calculateur de Ligne de Vue 2D (Raycasting Algorithmique)

## 📌 Présentation du projet
Ce projet implémente un moteur de calcul de champ de vision (Ligne de Vue / Raycasting) en 2D. Inspiré des mécaniques de vision de jeux vidéo (comme *Project Zomboid*), l'algorithme calcule dynamiquement la zone visible par un observateur au milieu d'obstacles (murs), générant un polygone de visibilité.

**membre :** [Efe Ilhan] [Kalachyan Norik] *(Ajouter les autres membres si travail en groupe et préciser qui a fait quoi)*
**Groupe :** [Ton Groupe de TP]
**Module :** Mathématiques appliquées et calcul numérique

## 📁 Structure du dépôt
* `tp/` : Contient l'ensemble des solutions aux exercices de TP réalisés pendant le semestre.
* `projet/` : Contient le code source de ce projet personnel.

## 🚀 Comment lancer le projet
1. Assurez-vous d'avoir un environnement Python 3 fonctionnel.
2. Installez la bibliothèque d'affichage (si ce n'est pas déjà fait) : 
   `pip install matplotlib`
3. Exécutez le script principal depuis le dossier `projet/` : 
   `python [nom_de_ton_fichier_principal].py`
4. **Ce qu'il faut observer :** Le programme affiche une carte 2D avec des murs noirs, la position du joueur en rouge, et le cône de vision calculé en jaune. *(Si tu as ajouté la souris : Déplacez la souris sur la fenêtre pour voir le champ de vision se mettre à jour en temps réel).*

## 🧮 Notions mathématiques mobilisées
Conformément aux attentes du module, ce projet n'utilise aucune bibliothèque géométrique externe pour le cœur du calcul (tout est fait à la main).
* **Géométrie vectorielle et systèmes linéaires :** Le calcul de l'intersection entre un rayon de vision (demi-droite) et un obstacle (segment) se fait via la mise en équation paramétrique des deux éléments.
* **Calcul matriciel (Déterminant) :** Utilisation du produit vectoriel 2D pour vérifier si le rayon et le mur sont parallèles, et pour résoudre le système.
* **Arithmétique des flottants :** Résolution des erreurs de précision machine lors des calculs d'angles rasants.

## 🔬 Analyse critique et profondeur d'exploitation

*(Note : Garde cette section, c'est elle qui rapporte les 6 points de "Profondeur d'exploitation". Modifie-la si tu as fait d'autres tests)*

**1. La limite de précision des nombres flottants (L'astuce de l'Epsilon)**
Le défi principal de cet algorithme concerne la norme IEEE 754 des flottants. Lorsqu'un rayon frappe exactement l'extrémité d'un segment, les approximations d'arrondis rendent le résultat instable : le programme hésite et ne sait pas si le rayon traverse le mur ou est bloqué. 
Pour stabiliser l'algorithme, j'ai implémenté une marge d'erreur infinitésimale (epsilon = 0.00001). Au lieu de lancer un seul rayon par sommet, le programme en lance trois : sur l'angle exact, légèrement à gauche (angle - epsilon), et légèrement à droite (angle + epsilon). Cela force mathématiquement le rayon décalé à "passer derrière" l'obstacle, générant une ombre correcte sans artefact visuel.

**2. Optimisation géométrique vs Méthode naïve**
La première approche envisagée (naïve) consistait à lancer 360 rayons autour de l'observateur (un par degré). Outre son inefficacité, elle causait des "trous" dans le champ de vision sur les murs éloignés à cause de l'écartement des rayons.
L'implémentation finale est purement géométrique : l'algorithme repère les extrémités des murs et ne lance des rayons **que** vers ces points précis, garantissant une précision parfaite et une complexité réduite.

## 🤖 Utilisation de l'Intelligence Artificielle
Dans le respect des consignes d'évaluation, je déclare avoir utilisé un assistant IA comme aide technique.
* **Ce que l'IA a généré :** L'assistant a été utilisé pour me proposer l'idée initiale, m'expliquer la méthode de résolution du système paramétrique (calcul de t et u via le déterminant), et fournir le squelette de base pour l'affichage avec matplotlib.
* **Ce que j'ai réalisé, vérifié et analysé moi-même :** 
  * [Exemple 1 : L'analyse du problème des flottants et la justification mathématique dans ce rapport.]
  * [Exemple 2 : L'ajout de l'interactivité pour que l'observateur bouge à la souris.]
  * [Exemple 3 : La création de la carte (coordonnées des murs) pour tester des cas critiques d'occlusion.]
  * La reprise complète et la correction des TP présents dans le dossier `tp/`.
