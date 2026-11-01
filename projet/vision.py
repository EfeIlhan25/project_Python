import math

EPSILON = 0.00001


def intersection_rayon_segment(ox, oy, dx, dy, ax, ay, bx, by):
    """Intersection du rayon (origine (ox, oy), direction (dx, dy)) avec le segment [AB].

    On résout O + t*d = A + u*(B - A) avec le déterminant (produit vectoriel 2D).
    Renvoie (t, x, y) ou None s'il n'y a pas d'intersection.
    """
    sx = bx - ax
    sy = by - ay

    det = dx * sy - dy * sx
    if abs(det) < 1e-8:          # rayon parallèle au mur
        return None

    t = ((ax - ox) * sy - (ay - oy) * sx) / det
    u = ((ax - ox) * dy - (ay - oy) * dx) / det

    if t > 0 and 0 <= u <= 1:    # devant l'observateur et sur le segment
        return t, ox + t * dx, oy + t * dy
    return None


def impact_le_plus_proche(ox, oy, angle, segments):
    dx, dy = math.cos(angle), math.sin(angle)
    meilleur, distance_min = None, float("inf")
    for (ax, ay), (bx, by) in segments:
        resultat = intersection_rayon_segment(ox, oy, dx, dy, ax, ay, bx, by)
        if resultat and resultat[0] < distance_min:
            distance_min = resultat[0]
            meilleur = (resultat[1], resultat[2])
    return meilleur


def calculer_champ_vision(ox, oy, segments, epsilon=EPSILON):
    """Polygone de visibilité : un rayon vers chaque extrémité de mur, plus deux
    rayons décalés de +/- epsilon (en radians) pour passer de part et d'autre du coin."""
    angles = []
    for segment in segments:
        for (px, py) in segment:
            angle = math.atan2(py - oy, px - ox)
            angles.extend([angle - epsilon, angle, angle + epsilon])
    angles.sort()

    points = []
    for angle in angles:
        impact = impact_le_plus_proche(ox, oy, angle, segments)
        if impact:
            points.append(impact)
    return points


def calculer_champ_vision_naif(ox, oy, segments, nb_rayons=360):
    """Méthode naïve : nb_rayons rayons régulièrement répartis autour de l'observateur."""
    points = []
    for i in range(nb_rayons):
        angle = -math.pi + 2 * math.pi * i / nb_rayons
        impact = impact_le_plus_proche(ox, oy, angle, segments)
        if impact:
            points.append(impact)
    return points


def distance_point_segment(px, py, ax, ay, bx, by):
    sx, sy = bx - ax, by - ay
    longueur2 = sx * sx + sy * sy
    if longueur2 == 0:
        return math.hypot(px - ax, py - ay)
    u = max(0.0, min(1.0, ((px - ax) * sx + (py - ay) * sy) / longueur2))
    return math.hypot(px - (ax + u * sx), py - (ay + u * sy))


def observateur_valide(ox, oy, segments, limites, tolerance=1e-6):
    """Faux si l'observateur est hors de la carte ou posé sur un mur."""
    xmin, xmax, ymin, ymax = limites
    if not (xmin < ox < xmax and ymin < oy < ymax):
        return False
    for (ax, ay), (bx, by) in segments:
        if distance_point_segment(ox, oy, ax, ay, bx, by) < tolerance:
            return False
    return True


LIMITES = (0, 12, 0, 10)

murs = [
    ((0, 0), (12, 0)), ((12, 0), (12, 10)), ((12, 10), (0, 10)), ((0, 10), (0, 0)),
    ((2, 2), (10, 2)), ((10, 2), (10, 8)), ((10, 8), (2, 8)), ((2, 8), (2, 2)),
    ((6, 2), (6, 5)),
    ((3, 4), (4, 4)), ((4, 4), (4, 5)), ((4, 5), (3, 5)), ((3, 5), (3, 4)),
]
