import math
import matplotlib.pyplot as plt

def intersection_rayon_segment(ox, oy, dx, dy, ax, ay, bx, by):
    """
    Calcule l'intersection entre un rayon partant de (ox, oy) dirigé par (dx, dy)
    et un segment délimité par les points A(ax, ay) et B(bx, by).
    Utilise la résolution d'équations paramétriques et le déterminant (produit vectoriel 2D).
    """
   
    sx = bx - ax
    sy = by - ay
    
    
    det = dx * sy - dy * sx
    
  
    if abs(det) < 1e-8:
        return None
        
    
    t = ((ax - ox) * sy - (ay - oy) * sx) / det
    u = ((ax - ox) * dy - (ay - oy) * dx) / det
    
    
    if t > 0 and 0 <= u <= 1:
        ix = ox + t * dx
        iy = oy + t * dy
        return t, ix, iy 
        
    return None

def calculer_champ_vision(ox, oy, segments):
    """
    Génère le polygone de visibilité en lançant des rayons vers les extrémités des murs.
    """
    points_impact = []
    angles_a_tester = []
    
 
    for segment in segments:
        for point in [segment[0], segment[1]]:
            angle = math.atan2(point[1] - oy, point[0] - ox)
            
            angles_a_tester.extend([angle - 0.00001, angle, angle + 0.00001])
            
   
    angles_a_tester.sort()
    

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


murs = [

    ((0, 0), (12, 0)), ((12, 0), (12, 10)), ((12, 10), (0, 10)), ((0, 10), (0, 0)),
   
    ((2, 2), (10, 2)), ((10, 2), (10, 8)), ((10, 8), (2, 8)), ((2, 8), (2, 2)),
   
    ((6, 2), (6, 5)), 
   
    ((3, 4), (4, 4)), ((4, 4), (4, 5)), ((4, 5), (3, 5)), ((3, 5), (3, 4))
]


fig, ax = plt.subplots(figsize=(8, 6))

def actualiser_affichage(event):

    if event.xdata is None or event.ydata is None: 
        return
    
    ax.clear() 
    ax.set_title("Raycasting 2D - Bougez la souris pour explorer la carte !")
    ax.set_xlim(-1, 13)
    ax.set_ylim(-1, 11)
    ax.set_aspect('equal')
    
    
    for mur in murs:
        (x1, y1), (x2, y2) = mur
        ax.plot([x1, x2], [y1, y2], color='black', linewidth=3)
        
   
    visibilite = calculer_champ_vision(event.xdata, event.ydata, murs)
    if visibilite:
        visibilite.append(visibilite[0]) 
        vx = [p[0] for p in visibilite]
        vy = [p[1] for p in visibilite]
        ax.fill(vx, vy, color='yellow', alpha=0.5)
        
   
    ax.plot(event.xdata, event.ydata, 'ro', markersize=8)
    
   
    ax.set_xticks([])
    ax.set_yticks([])
    
    fig.canvas.draw_idle()


fig.canvas.mpl_connect('motion_notify_event', actualiser_affichage)


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
