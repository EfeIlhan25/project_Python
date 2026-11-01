# Calculateur de ligne de vue 2D (raycasting)

## Présentation du projet
Ce projet calcule le champ de vision d'un observateur placé au milieu de murs, en 2D. Inspiré de la vision dans les jeux vidéo (comme *Project Zomboid*), il produit un **polygone de visibilité** : l'ensemble des points que l'observateur voit. Le calcul du cœur est fait à la main, sans bibliothèque géométrique. `matplotlib` ne sert qu'à l'affichage et aux graphiques.

**Auteurs :** Efe Ilhan, Norik Kalachyan, Nizar Lamaaizi
**Module :** Mathématiques appliquées et calcul numérique (R1.07)

## Répartition du travail

**Travail commun (réalisé ensemble, à trois) :** choix du sujet, premier programme (intersection rayon/mur par le déterminant, polygone de visibilité, marge epsilon pour les rayons rasants), carte de test (maison avec cloison et table), affichage interactif à la souris.

**Approfondissement et finalisation (par personne) :**

- **Norik Kalachyan**
  - Piste 1 : étude de l'effet de epsilon (`mesure_epsilon.py`, « Résultat 1 »).
  - Reprise de l'affichage (`main.py`) : refus des positions de souris hors de la carte ou sur un mur.
  - Rédaction et relecture du README.
- **Efe Ilhan**
  - Piste 2 : comparaison avec la méthode à 360 rayons (`mesure_360.py`, « Résultat 2 »).
  - Suivi des tests automatiques (`test_vision.py`).
  - Relecture croisée de tout le code.
- **Nizar Lamaaizi**
  - Piste 3 : vérification en calcul exact et cas limites (`verification_exacte.py`, « Résultat 3 »).
  - Découpage du cœur du calcul en `vision.py` et `geometrie.py`.
  - Mise en ligne sur GitHub et envoi du courriel au professeur.

**Tests :** l'ensemble des tests (`test_vision.py` et les scripts de mesure) a été exécuté et vérifié par nous trois.

**TP :** chaque membre a ses solutions dans `tp/` (un dossier par personne).

## Structure du dépôt
```
tp/                      solutions des TP (un dossier par membre)
projet/
  main.py                affichage interactif (souris)
  vision.py              cœur du calcul : intersection, polygone de visibilité, méthode naïve
  geometrie.py           aire d'un polygone, point dans un polygone (reprises des TP)
  mesure_epsilon.py      piste 1
  mesure_360.py          piste 2
  verification_exacte.py piste 3
  test_vision.py         tests automatiques
  resultats/             tableaux (.csv) et graphiques (.png) produits par les scripts
```

## Comment lancer
Python 3 et `matplotlib` suffisent : `pip install matplotlib`. Depuis le dossier `projet/` :

| Commande | Effet |
|---|---|
| `python main.py` | ouvre la carte ; bouger la souris déplace l'observateur |
| `python mesure_epsilon.py` | étude de epsilon (tableau + graphique) |
| `python mesure_360.py` | comparaison avec 360 rayons (tableaux + graphique) |
| `python verification_exacte.py` | vérification en calcul exact |
| `python -m unittest test_vision -v` | lance les 16 tests |

**Ce qu'il faut observer avec `main.py` :** des murs noirs, l'observateur en rouge et sa zone visible en jaune, mise à jour en temps réel. Quand la souris est hors de la carte ou sur un mur, le point devient gris et aucune zone n'est dessinée.

## Notions du module mobilisées
- **Géométrie du plan et déterminant (TP6)** : l'intersection d'un rayon et d'un mur résout un système linéaire 2×2 par le déterminant (produit vectoriel 2D). L'aire (formule du lacet) et le test « point dans un polygone » reprennent le TP6.
- **Flottants (TP1)** : rayons rasants, tolérance sur le déterminant, comparaison au calcul exact avec `Fraction` (TP1 et TP4).
- **Mesure du coût (TP2)** : temps d'exécution selon la taille de la carte.

## Méthode
Pour chaque extrémité de mur, on lance trois rayons : un sur l'angle exact et deux décalés de ± epsilon (epsilon = 0,00001 rad). On garde pour chaque rayon l'impact le plus proche, puis on relie les impacts dans l'ordre des angles.

## Résultats
Les nombres ci-dessous viennent des scripts du dépôt (graines fixées). Les temps dépendent de la machine ; ceux du tableau 2b sont donnés à titre d'exemple.

### Résultat 1 — effet de epsilon (`mesure_epsilon.py`)
Erreur sur l'aire visible, par rapport à une référence par comptage de points (pas de 0,05, précision d'environ 0,2 %), sur 8 positions dont des positions alignées avec des sommets.

| epsilon (rad) | erreur moyenne | erreur maximale |
|---|---|---|
| 0 | 24,45 % | 72,14 % |
| 1e-12 | 0,22 % | 0,64 % |
| 1e-9 à 1e-5 | 0,22 % | 0,64 % |
| 1e-4 | 0,22 % | 0,65 % |
| 1e-3 | 0,26 % | 0,67 % |
| 1e-2 | 0,63 % | 1,74 % |
| 1e-1 | 3,83 % | 11,77 % |

**Interprétation.** Sans epsilon le résultat est faux, car un rayon pile sur un coin touche les deux murs qui s'y rejoignent et ne « passe » d'aucun côté. Dès qu'epsilon est strictement positif, le résultat est stable sur un très large intervalle (de 1e-12 à 1e-4). Quand epsilon devient grand, les rayons décalés visent à côté du coin et l'erreur remonte.

### Résultat 2 — notre méthode contre 360 rayons (`mesure_360.py`)
**2a. Précision.** Sur la carte de la maison, les 360 rayons sont aussi précis que notre méthode (écarts d'environ 1 %). Il faut une carte particulière pour les mettre en défaut : une salle de 100×100 avec une cloison percée d'une fente de 0,52 de large, vue à 50 unités.

| Méthode | Voit un point derrière la fente ? |
|---|---|
| Notre méthode | oui |
| Naïve, 90, 180 ou 360 rayons | non |
| Naïve, 720 rayons ou plus | oui |

Les « trous » de la méthode naïve existent donc, mais seulement pour des détails plus fins que l'écart entre rayons.

**2b. Temps.** Exemple de résultat (varie selon la machine) :

| Murs | Notre méthode (ms) | Naïf 360 (ms) |
|---|---|---|
| 8 | 0,26 | 1,92 |
| 24 | 1,87 | 4,50 |
| 64 | 11,48 | 10,68 |
| 124 | 24,45 | 11,88 |
| 204 | 65,04 | 19,26 |

**Interprétation.** Notre méthode lance 6 rayons par mur et teste chacun contre tous les murs : son coût croît comme le carré du nombre de murs. La méthode naïve lance un nombre fixe de rayons : son coût croît seulement avec le nombre de murs. Notre méthode est plus rapide sur de petites cartes (jusqu'à environ 60 murs ici) et plus lente au-delà. Elle n'est donc pas « de complexité réduite » en général.

### Résultat 3 — calcul exact et cas limites (`verification_exacte.py`)
- Sur 200 000 triplets de points presque alignés, le signe de l'orientation calculé en flottants diffère du signe exact (calculé avec `Fraction`) dans environ 14 % des cas. Dans presque tous ces cas, le flottant répond « alignés » (0) alors que l'exact trouve un petit écart ; il se trompe de côté seulement 12 fois sur 200 000.
- Pour 10 positions de l'observateur, aucun sommet du polygone n'est invalidé par le test exact (aucun mur ne coupe le segment observateur → sommet).

## Limites connues
- epsilon est fixe, en radians : un écart en radians correspond à un décalage d'autant plus grand que le mur est loin.
- Le coût est quadratique en nombre de murs (voir Résultat 2b) ; au-delà d'environ 60 murs, la méthode naïve est plus rapide.
- Un observateur hors de la carte ou posé sur un mur est refusé (`observateur_valide`) ; sans ce test, la zone visible n'avait pas de sens.
- La maison de la carte est fermée : l'extérieur n'est jamais visible depuis l'intérieur.
- Le déterminant est comparé à une tolérance absolue (1e-8) pour détecter le parallélisme.

## Utilisation de l'intelligence artificielle
Nous déclarons avoir utilisé un assistant IA.
- **Ce que l'IA a fait :** proposer l'idée initiale, expliquer la résolution du système paramétrique (t et u par le déterminant) et le squelette d'affichage `matplotlib` ; puis, pour l'approfondissement, proposer le découpage du code en fichiers, les scripts de mesure, les tests et la rédaction d'une première version de ce README.
- **Ce que nous avons fait nous-mêmes :**
  - **Test sans epsilon :** nous avons modifié le code pour retirer la marge epsilon et constaté l'apparition d'artefacts (des rayons qui traversent les coins des murs), ce qui nous a montré pourquoi le décalage des rayons est nécessaire.
  - **Interactivité :** nous avons intégré la gestion d'événements de `matplotlib` (`motion_notify_event`) pour recalculer le champ de vision à chaque mouvement de la souris.
  - **Carte de test :** nous avons construit un plan simulant un intérieur (murs extérieurs, cloison, table) pour vérifier les occlusions multiples.
  - **Exécution et vérification :** nous avons exécuté nous-mêmes tous les scripts et tous les tests.
  - **TP :** reprise et correction des TP présents dans le dossier `tp/`.
- Nous avons relu l'ensemble du code.
