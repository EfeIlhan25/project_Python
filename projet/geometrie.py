import random


def aire(polygone):
    """Aire d'un polygone par la formule du lacet (TP6)."""
    n = len(polygone)
    somme = 0.0
    for i in range(n):
        x1, y1 = polygone[i]
        x2, y2 = polygone[(i + 1) % n]
        somme += x1 * y2 - x2 * y1
    return abs(somme) / 2


def dedans(point, polygone):
    """Point dans un polygone par lancer de rayon (TP6)."""
    x, y = point
    n = len(polygone)
    interieur = False
    for i in range(n):
        x1, y1 = polygone[i]
        x2, y2 = polygone[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            x_croisement = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < x_croisement:
                interieur = not interieur
    return interieur


def _orientation(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def segments_se_coupent(a, b, c, d):
    """Vrai si [ab] et [cd] se croisent franchement (cas alignés ignorés)."""
    return (_orientation(a, b, c) * _orientation(a, b, d) < 0
            and _orientation(c, d, a) * _orientation(c, d, b) < 0)


def aire_reference(observateur, segments, limites, pas=0.05):
    """Aire visible par comptage de points d'une grille : un point est visible
    si aucun mur ne coupe le segment observateur -> point. Précision de l'ordre de 0,2 %."""
    xmin, xmax, ymin, ymax = limites
    nx, ny = int((xmax - xmin) / pas), int((ymax - ymin) / pas)
    visibles = 0
    for i in range(nx):
        for j in range(ny):
            p = (xmin + pas * (i + 0.5), ymin + pas * (j + 0.5))
            if not any(segments_se_coupent(observateur, p, s[0], s[1]) for s in segments):
                visibles += 1
    return visibles * pas * pas
