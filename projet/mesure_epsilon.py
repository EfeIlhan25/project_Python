"""Piste 1 : effet de epsilon sur la précision du polygone de visibilité.

Lancer :  python mesure_epsilon.py
Sorties : tableau affiché, resultats/epsilon.csv, resultats/epsilon.png
"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from geometrie import aire, aire_reference
from vision import LIMITES, calculer_champ_vision, murs

DOSSIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultats")
os.makedirs(DOSSIER, exist_ok=True)

# positions alignées avec des sommets (cas rasants) et positions quelconques
OBSERVATEURS = [(5, 5), (5, 4), (2.5, 4.5), (7, 2.5), (9, 5), (3.5, 1), (1.3, 7.7), (8.2, 6.1)]
EPSILONS = [0, 1e-12, 1e-9, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]

references = {o: aire_reference(o, murs, LIMITES) for o in OBSERVATEURS}

lignes = []
for eps in EPSILONS:
    erreurs = []
    for o in OBSERVATEURS:
        a = aire(calculer_champ_vision(o[0], o[1], murs, epsilon=eps))
        erreurs.append(abs(a - references[o]) / references[o] * 100)
    lignes.append((eps, sum(erreurs) / len(erreurs), max(erreurs)))

print(f"{'epsilon':>10} {'erreur moyenne':>16} {'erreur max':>12}")
for eps, moy, mx in lignes:
    print(f"{eps:>10g} {moy:>14.2f} % {mx:>10.2f} %")

with open(os.path.join(DOSSIER, "epsilon.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["epsilon", "erreur_moyenne_pct", "erreur_max_pct"])
    w.writerows(lignes)

xs = [e if e > 0 else 1e-15 for e, _, _ in lignes]   # epsilon = 0 tracé à 1e-15 (échelle log)
plt.figure(figsize=(7, 4))
plt.loglog(xs, [m for _, m, _ in lignes], "o-", label="erreur moyenne")
plt.loglog(xs, [x for _, _, x in lignes], "s--", label="erreur maximale")
plt.xlabel("epsilon (radians)   [le point le plus à gauche est epsilon = 0]")
plt.ylabel("erreur sur l'aire visible (%)")
plt.title("Effet de epsilon sur la précision")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(DOSSIER, "epsilon.png"), dpi=120)
print("fichiers écrits dans", DOSSIER)
