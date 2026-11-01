"""Piste 2 : notre méthode (rayons vers les sommets) contre la méthode naïve (N rayons réguliers).

Lancer :  python mesure_360.py
Sorties : tableaux affichés, resultats/temps_vs_murs.csv, resultats/temps_vs_murs.png
Trois questions :
  A. Sur une carte à fente étroite et lointaine, que voit la méthode naïve ?
  B. Combien de rayons faut-il à la méthode naïve pour retrouver la fente ?
  C. Comment les temps évoluent-ils quand le nombre de murs augmente ?
"""
import csv
import math
import os
import random
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from geometrie import aire, dedans
from vision import calculer_champ_vision, calculer_champ_vision_naif

DOSSIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultats")
os.makedirs(DOSSIER, exist_ok=True)

# ---------- A et B : une carte où 360 rayons ratent une fente ----------
# Salle de 100 x 100, cloison verticale en x = 60 percée d'une fente de 0,52 de large.
# L'observateur est en (10, 40) ; la fente est centrée sur la direction 3,5 degrés,
# donc entre les rayons à 3 et à 4 degrés de la méthode naïve.
OBS = (10, 40)
centre = OBS[1] + 50 * math.tan(math.radians(3.5))
demi = 0.26
carte_fente = [
    ((0, 0), (100, 0)), ((100, 0), (100, 100)), ((100, 100), (0, 100)), ((0, 100), (0, 0)),
    ((60, 0), (60, centre - demi)),
    ((60, centre + demi), (60, 100)),
]
SONDE = (95, OBS[1] + 85 * math.tan(math.radians(3.5)))   # point derrière la fente, dans son faisceau

print(f"Fente centrée en y = {centre:.3f}, largeur {2 * demi}. Point sonde derrière la fente : "
      f"({SONDE[0]}, {SONDE[1]:.2f})")
poly = calculer_champ_vision(OBS[0], OBS[1], carte_fente)
print(f"\nNotre méthode : {len(poly)} points, aire {aire(poly):.1f}, sonde vue : {dedans(SONDE, poly)}")
print("\nMéthode naïve (nombre de rayons -> aire, sonde vue ?)")
for nb in (90, 180, 360, 720, 1440, 3600):
    p = calculer_champ_vision_naif(OBS[0], OBS[1], carte_fente, nb)
    print(f"  {nb:>5} rayons : aire {aire(p):9.1f}   sonde vue : {dedans(SONDE, p)}")

# ---------- C : temps selon le nombre de murs ----------
def carte_aleatoire(n, graine=1):
    """Carte de n murs courts répartis au hasard dans un carré 100 x 100, plus les 4 bords."""
    r = random.Random(graine)
    murs = [((0, 0), (100, 0)), ((100, 0), (100, 100)), ((100, 100), (0, 100)), ((0, 100), (0, 0))]
    for _ in range(n):
        x, y = r.uniform(5, 95), r.uniform(5, 95)
        a = r.uniform(0, 2 * math.pi)
        l = r.uniform(3, 10)
        murs.append(((x, y), (x + l * math.cos(a), y + l * math.sin(a))))
    return murs


def temps(fonction, repetitions=5):
    meilleur = float("inf")
    for _ in range(repetitions):
        debut = time.perf_counter()
        fonction()
        meilleur = min(meilleur, time.perf_counter() - debut)
    return meilleur * 1000


print("\nTemps par appel (ms), meilleur de 5 essais")
print(f"{'murs':>6} {'notre méthode':>15} {'naïf 360':>10} {'rapport':>9}")
lignes = []
for n in (4, 10, 20, 40, 60, 80, 120, 200):
    murs = carte_aleatoire(n)
    t_nous = temps(lambda: calculer_champ_vision(50.3, 50.7, murs))
    t_naif = temps(lambda: calculer_champ_vision_naif(50.3, 50.7, murs, 360))
    lignes.append((len(murs), t_nous, t_naif))
    print(f"{len(murs):>6} {t_nous:>15.2f} {t_naif:>10.2f} {t_naif / t_nous:>8.1f}x")

with open(os.path.join(DOSSIER, "temps_vs_murs.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["murs", "temps_notre_methode_ms", "temps_naif360_ms"])
    w.writerows(lignes)

plt.figure(figsize=(7, 4))
plt.plot([l[0] for l in lignes], [l[1] for l in lignes], "o-", label="notre méthode (6 rayons par mur)")
plt.plot([l[0] for l in lignes], [l[2] for l in lignes], "s-", label="naïf (360 rayons)")
plt.xlabel("nombre de murs")
plt.ylabel("temps par appel (ms)")
plt.title("Temps de calcul selon le nombre de murs")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(DOSSIER, "temps_vs_murs.png"), dpi=120)
print("fichiers écrits dans", DOSSIER)
