import matplotlib.pyplot as plt

from vision import LIMITES, calculer_champ_vision, murs, observateur_valide

# ==========================================
# GESTION DE L'AFFICHAGE ET DE L'INTERACTIVITÉ
# ==========================================
fig, ax = plt.subplots(figsize=(8, 6))


def dessiner_carte(titre):
    """Efface la figure et redessine la carte (axes, murs, titre)."""
    ax.clear()
    ax.set_title(titre)
    ax.set_xlim(-1, 13)
    ax.set_ylim(-1, 11)
    ax.set_aspect('equal')
    for (x1, y1), (x2, y2) in murs:
        ax.plot([x1, x2], [y1, y2], color='black', linewidth=3)
    # Masquer les axes numériques pour un rendu plus "jeu vidéo"
    ax.set_xticks([])
    ax.set_yticks([])


def actualiser_affichage(event):
    # Si la souris sort de la fenêtre, on ignore l'événement
    if event.xdata is None or event.ydata is None:
        return

    # Un observateur hors de la carte ou posé sur un mur n'a pas de champ de vision utile
    if not observateur_valide(event.xdata, event.ydata, murs, LIMITES):
        dessiner_carte("Position invalide (hors de la carte ou sur un mur)")
        ax.plot(event.xdata, event.ydata, 'o', color='gray', markersize=8)
        fig.canvas.draw_idle()
        return

    dessiner_carte("Raycasting 2D - Bougez la souris pour explorer la carte !")

    # Calculer et dessiner la zone de visibilité
    visibilite = calculer_champ_vision(event.xdata, event.ydata, murs)
    if visibilite:
        visibilite.append(visibilite[0])  # Fermer le polygone géométrique
        vx = [p[0] for p in visibilite]
        vy = [p[1] for p in visibilite]
        ax.fill(vx, vy, color='yellow', alpha=0.5)

    # Dessiner le joueur (la position de la souris)
    ax.plot(event.xdata, event.ydata, 'ro', markersize=8)
    fig.canvas.draw_idle()


def main():
    # Connecter le mouvement de la souris à la fonction de rafraîchissement
    fig.canvas.mpl_connect('motion_notify_event', actualiser_affichage)
    # Affichage du tout premier écran (avant de bouger la souris)
    dessiner_carte("Raycasting 2D - Placez la souris sur la fenêtre !")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
