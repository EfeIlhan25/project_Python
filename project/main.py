import math
import matplotlib.pyplot as plt

def intersection_rayon_segment(ox, oy, dx, dy, ax, ay, bx, by):
    """
    Calcule l'intersection entre un rayon partant de (ox, oy) dirigé par (dx, dy)
    et un segment délimité par les points A(ax, ay) et B(bx, by).
    Utilise la résolution d'équations paramétriques et le déterminant (produit vectoriel 2D).
    """
    # Vecteur du segment AB
    sx = bx - ax
    sy = by - ay
    
    # Déterminant (produit vectoriel)
    det = dx * sy - dy * sx
    
    # Si le déterminant est 0 (ou très proche), le rayon et le mur sont parallèles
    if abs(det) < 1e-8:
        return None
        
    # Calcul des paramètres t (pour le rayon) et u (pour le segment)
    t = ((ax - ox) * sy - (ay - oy) * sx) / det
    u = ((ax - ox) * dy - (ay - oy) * dx) / det
    
    # Il y a intersection SI :
    # t > 0 (l'intersection est devant l'observateur, pas derrière)
    # 0 <= u <= 1 (l'intersection se trouve bien sur le segment de mur, pas dans son prolongement)
    if t > 0 and 0 <= u <= 1:
        ix = ox + t * dx
        iy = oy + t * dy
        return t, ix, iy # Retourne la distance (t) et les coordonnées de l'impact
        
    return None

def calculer_champ_vision(ox, oy, segments):
    """
    Génère le polygone de visibilité en lançant des rayons vers les extrémités des murs.
    """
    points_impact = []
    angles_a_tester = []
    
    # 1. On repère tous les angles vers les extrémités des murs
    for segment in segments:
        for point in [segment[0], segment[1]]:
            angle = math.atan2(point[1] - oy, point[0] - ox)
            # L'ASTUCE DES FLOTTANTS : On tire un rayon pile sur le point, 
            # un rayon légèrement à gauche, et un légèrement à droite.
            angles_a_tester.extend([angle - 0.00001, angle, angle + 0.00001])
            
    # 2. On trie les angles pour construire un polygone cohérent
    angles_a_tester.sort()
    
    # 3. Pour chaque angle, on lance un rayon et on garde l'impact le plus proche
    for angle in angles_a_tester:
        dx = math.cos(angle)
        dy = math.sin(angle)
        
        impact_le_plus_proche = None
        distance_min = float('inf')
        
        for segment in segments:
            (ax, ay), (bx, by) = segment
            resultat = intersection_rayon_segment(ox, oy, dx, dy, ax, ay, bx, by)
            
            if resultat:
                dist, ix, iy = resultat
                if dist < distance_min:
                    distance_min = dist
                    impact_le_plus_proche = (ix, iy)
                    
        if impact_le_plus_proche:
            points_impact.append(impact_le_plus_proche)
            
    return points_impact

# ==========================================
# CARTE ET TOPOLOGIE (LEVEL DESIGN)
# ==========================================
# Une petite maison avec une chambre, un couloir et une porte ouverte
murs = [
    # Murs extérieurs de la carte (limites du monde)
    ((0, 0), (12, 0)), ((12, 0), (12, 10)), ((12, 10), (0, 10)), ((0, 10), (0, 0)),
    # Murs extérieurs de la maison
    ((2, 2), (10, 2)), ((10, 2), (10, 8)), ((10, 8), (2, 8)), ((2, 8), (2, 2)),
    # Mur intérieur (séparation de pièce)
    ((6, 2), (6, 5)), 
    # Un obstacle au milieu de la pièce (ex: une table rectangulaire)
    ((3, 4), (4, 4)), ((4, 4), (4, 5)), ((4, 5), (3, 5)), ((3, 5), (3, 4))
]

# ==========================================
# GESTION DE L'AFFICHAGE ET DE L'INTERACTIVITÉ
# ==========================================
fig, ax = plt.subplots(figsize=(8, 6))

def actualiser_affichage(event):
    # Si la souris sort de la fenêtre, on ignore l'événement
    if event.xdata is None or event.ydata is None: 
        return
    
    ax.clear() # On efface l'image précédente
    ax.set_title("Raycasting 2D - Bougez la souris pour explorer la carte !")
    ax.set_xlim(-1, 13)
    ax.set_ylim(-1, 11)
    ax.set_aspect('equal')
    
    # 1. Dessiner les murs
    for mur in murs:
        (x1, y1), (x2, y2) = mur
        ax.plot([x1, x2], [y1, y2], color='black', linewidth=3)
        
    # 2. Calculer et dessiner la zone de visibilité
    visibilite = calculer_champ_vision(event.xdata, event.ydata, murs)
    if visibilite:
        visibilite.append(visibilite[0]) # Fermer le polygone géométrique
        vx = [p[0] for p in visibilite]
        vy = [p[1] for p in visibilite]
        ax.fill(vx, vy, color='yellow', alpha=0.5)
        
    # 3. Dessiner le joueur (la position de la souris)
    ax.plot(event.xdata, event.ydata, 'ro', markersize=8)
    
    # Masquer les axes numériques pour un rendu plus "jeu vidéo"
    ax.set_xticks([])
    ax.set_yticks([])
    
    fig.canvas.draw_idle()

# Connecter le mouvement de la souris à la fonction de rafraîchissement
fig.canvas.mpl_connect('motion_notify_event', actualiser_affichage)

# Affichage du tout premier écran (avant de bouger la souris)
ax.set_title("Raycasting 2D - Placez la souris sur la fenêtre !")
ax.set_xlim(-1, 13)
ax.set_ylim(-1, 11)
ax.set_aspect('equal')
for mur in murs:
    (x1, y1), (x2, y2) = mur
    ax.plot([x1, x2], [y1, y2], color='black', linewidth=3)
ax.set_xticks([])
ax.set_yticks([])

plt.tight_layout()
plt.show()