"""Piste 3 : vérifier le code en calcul exact (Fraction) et traiter les cas limites.

Lancer :  python verification_exacte.py
Idée (TP4 étape 8, TP6 étape 2) : un flottant est un rationnel exact (Fraction(0.1) le montre).
On peut donc refaire les tests d'orientation SANS aucun arrondi et voir quand la version
flottante se trompe.
"""
import random
from fractions import Fraction

from geometrie import _orientation
from vision import LIMITES, calculer_champ_vision, distance_point_segment, murs, observateur_valide


def orientation_exacte(p, q, r):
    """Signe exact de l'orientation (1, -1 ou 0) pour des coordonnées flottantes."""
    p, q, r = [(Fraction(x), Fraction(y)) for x, y in (p, q, r)]
    d = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (d > 0) - (d < 0)


def orientation_flottante(p, q, r):
    d = _orientation(p, q, r)
    return (d > 0) - (d < 0)


# ---------- 1. Quand la version flottante de l'orientation se trompe ----------
random.seed(0)
total, zero_flottant, signe_inverse = 200_000, 0, 0
for _ in range(total):
    a = (random.uniform(-10, 10), random.uniform(-10, 10))
    d = (random.uniform(-1, 1), random.uniform(-1, 1))
    t1, t2 = random.uniform(0, 5), random.uniform(5, 10)
    b = (a[0] + t1 * d[0], a[1] + t1 * d[1])     # b et c quasi alignés avec a,
    c = (a[0] + t2 * d[0], a[1] + t2 * d[1])     # aux arrondis près
    f, e = orientation_flottante(a, b, c), orientation_exacte(a, b, c)
    if f != e:
        if f == 0:
            zero_flottant += 1       # le flottant dit « alignés », l'exact dit « pas tout à fait »
        else:
            signe_inverse += 1       # le flottant se trompe de côté
print(f"1. Triplets presque alignés ({total}) : le signe flottant diffère du signe exact "
      f"dans {zero_flottant + signe_inverse} cas ({(zero_flottant + signe_inverse) / total * 100:.2f} %)")
print(f"   dont le flottant répond « alignés » (0) : {zero_flottant}")
print(f"   dont le flottant se trompe de côté (+1 / -1 inversés) : {signe_inverse}")

# ---------- 2. Les points du polygone sont-ils vraiment visibles (test exact) ? ----------
def segment_coupe_strictement(o, p, mur):
    a, b = mur
    s1 = orientation_exacte(o, p, a) * orientation_exacte(o, p, b)
    s2 = orientation_exacte(a, b, o) * orientation_exacte(a, b, p)
    return s1 < 0 and s2 < 0


def violations(observateur):
    """Nombre de sommets P du polygone tels qu'un mur coupe strictement [observateur, P].
    On ignore le mur sur lequel P est posé (P vient d'une intersection calculée en flottant)."""
    nb = 0
    for p in calculer_champ_vision(observateur[0], observateur[1], murs):
        for mur in murs:
            if distance_point_segment(p[0], p[1], *mur[0], *mur[1]) < 1e-6:
                continue
            if segment_coupe_strictement(observateur, p, mur):
                nb += 1
                break
    return nb


OBSERVATEURS = [(5, 5), (5, 4), (2.5, 4.5), (7, 2.5), (9, 5), (3.5, 1), (1.3, 7.7), (8.2, 6.1), (11, 9), (1, 1)]
print("2. Sommets du polygone invalides (test exact) par position de l'observateur :")
for o in OBSERVATEURS:
    print(f"   {str(o):>12} : {violations(o)} / {len(calculer_champ_vision(o[0], o[1], murs))} sommets")

# ---------- 3. Cas limites : observateur hors carte, sur un mur ----------
print("3. Observateurs invalides (refusés par observateur_valide) :")
for o in [(-0.5, 5), (12.5, 5), (6, 3), (0, 5), (5, 5), (3.5, 4.5)]:
    print(f"   {str(o):>12} : {'valide' if observateur_valide(o[0], o[1], murs, LIMITES) else 'REFUSÉ'}")
