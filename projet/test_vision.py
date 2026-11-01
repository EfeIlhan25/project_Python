"""Tests automatiques. Lancer :  python -m unittest test_vision -v"""
import math
import unittest

from geometrie import aire, aire_reference, dedans
from vision import (LIMITES, calculer_champ_vision, calculer_champ_vision_naif,
                    distance_point_segment, intersection_rayon_segment, murs,
                    observateur_valide)

PIECE = [((0, 0), (10, 0)), ((10, 0), (10, 10)), ((10, 10), (0, 10)), ((0, 10), (0, 0))]


class TestIntersection(unittest.TestCase):
    def test_mur_perpendiculaire(self):
        t, x, y = intersection_rayon_segment(0, 0, 1, 0, 5, -1, 5, 1)
        self.assertAlmostEqual(t, 5)
        self.assertAlmostEqual(x, 5)
        self.assertAlmostEqual(y, 0)

    def test_mur_parallele(self):
        self.assertIsNone(intersection_rayon_segment(0, 0, 1, 0, 0, 1, 5, 1))

    def test_mur_derriere_l_observateur(self):
        self.assertIsNone(intersection_rayon_segment(0, 0, 1, 0, -5, -1, -5, 1))

    def test_mur_trop_court(self):
        self.assertIsNone(intersection_rayon_segment(0, 0, 1, 0, 5, 1, 5, 2))


class TestChampDeVision(unittest.TestCase):
    def test_piece_vide(self):
        for o in [(5, 5), (1, 1), (9.5, 0.5)]:
            self.assertAlmostEqual(aire(calculer_champ_vision(o[0], o[1], PIECE)), 100, places=2)

    def test_observateur_dans_la_table(self):
        self.assertAlmostEqual(aire(calculer_champ_vision(3.5, 4.5, murs)), 1.0, places=2)

    def test_carte_de_la_maison_contre_la_reference(self):
        o = (5, 4)
        ref = aire_reference(o, murs, LIMITES, pas=0.1)
        a = aire(calculer_champ_vision(o[0], o[1], murs))
        self.assertLess(abs(a - ref) / ref, 0.01)

    def test_sans_epsilon_le_resultat_est_faux(self):
        o = (5, 4)                                    # aligné avec des sommets de la table
        ref = aire_reference(o, murs, LIMITES, pas=0.1)
        sans = aire(calculer_champ_vision(o[0], o[1], murs, epsilon=0))
        avec = aire(calculer_champ_vision(o[0], o[1], murs))
        self.assertGreater(abs(sans - ref) / ref, 0.10)
        self.assertLess(abs(avec - ref) / ref, 0.01)

    def test_naif_proche_de_la_methode_geometrique_sur_une_piece(self):
        a1 = aire(calculer_champ_vision(5, 5, PIECE))
        a2 = aire(calculer_champ_vision_naif(5, 5, PIECE, 360))
        self.assertLess(abs(a1 - a2) / a1, 0.01)


class TestFenteEtroite(unittest.TestCase):
    def setUp(self):
        self.obs = (10, 40)
        centre = self.obs[1] + 50 * math.tan(math.radians(3.5))
        self.carte = [
            ((0, 0), (100, 0)), ((100, 0), (100, 100)), ((100, 100), (0, 100)), ((0, 100), (0, 0)),
            ((60, 0), (60, centre - 0.26)), ((60, centre + 0.26), (60, 100)),
        ]
        self.sonde = (95, self.obs[1] + 85 * math.tan(math.radians(3.5)))

    def test_notre_methode_voit_derriere_la_fente(self):
        p = calculer_champ_vision(self.obs[0], self.obs[1], self.carte)
        self.assertTrue(dedans(self.sonde, p))

    def test_360_rayons_ratent_la_fente(self):
        p = calculer_champ_vision_naif(self.obs[0], self.obs[1], self.carte, 360)
        self.assertFalse(dedans(self.sonde, p))

    def test_1440_rayons_la_retrouvent(self):
        p = calculer_champ_vision_naif(self.obs[0], self.obs[1], self.carte, 1440)
        self.assertTrue(dedans(self.sonde, p))


class TestObservateurValide(unittest.TestCase):
    def test_cas(self):
        self.assertTrue(observateur_valide(5, 5, murs, LIMITES))
        self.assertTrue(observateur_valide(3.5, 4.5, murs, LIMITES))   # dans la table : valide
        self.assertFalse(observateur_valide(-0.5, 5, murs, LIMITES))   # hors carte
        self.assertFalse(observateur_valide(12.5, 5, murs, LIMITES))
        self.assertFalse(observateur_valide(6, 3, murs, LIMITES))      # sur un mur
        self.assertFalse(observateur_valide(0, 5, murs, LIMITES))      # sur le bord

    def test_distance_point_segment(self):
        self.assertAlmostEqual(distance_point_segment(5, 3, 0, 0, 10, 0), 3)
        self.assertAlmostEqual(distance_point_segment(-3, 4, 0, 0, 10, 0), 5)   # au-delà de l'extrémité
        self.assertAlmostEqual(distance_point_segment(1, 1, 2, 2, 2, 2), math.sqrt(2))   # mur réduit à un point


class TestGeometrie(unittest.TestCase):
    def test_aire(self):
        self.assertEqual(aire([(0, 0), (1, 0), (1, 1), (0, 1)]), 1.0)
        self.assertEqual(aire([(0, 0), (4, 0), (0, 3)]), 6.0)

    def test_dedans(self):
        carre = [(0, 0), (2, 0), (2, 2), (0, 2)]
        self.assertTrue(dedans((1, 1), carre))
        self.assertFalse(dedans((3, 1), carre))


if __name__ == "__main__":
    unittest.main(verbosity=2)
