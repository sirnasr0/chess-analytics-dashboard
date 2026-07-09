import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from nettoyage import determiner_resultat_et_methode, extraire_nom_ouverture


def test_victoire_en_blanc_par_abandon():
    partie = {
        "white": {"username": "theyluv_gns", "result": "win", "rating": 1000},
        "black": {"username": "Adversaire", "result": "resigned", "rating": 950},
    }
    couleur,resultat,methode,mes_infos,infos_adversaire = determiner_resultat_et_methode(partie, "theyluv_gns")

    assert couleur == "Blancs"
    assert resultat == "Victoire"
    assert methode == "Abandon"
    assert mes_infos["rating"] == 1000
    assert infos_adversaire["rating"] == 950


def test_defaite_en_noir_par_echec_et_mat():
    partie = {
        "white": {"username": "Adversaire", "result": "win", "rating": 1200},
        "black": {"username": "theyluv_gns", "result": "checkmated", "rating": 1100},
    }
    couleur,resultat,methode,mes_infos,infos_adversaire = determiner_resultat_et_methode(partie, "theyluv_gns")

    assert couleur == "Noirs"
    assert resultat == "Défaite"
    assert methode == "Échec et mat"

def test_nulle_par_repetition():
    partie = {
        "white": {"username": "theyluv_gns", "result": "repetition", "rating": 1000},
        "black": {"username": "Adversaire", "result": "repetition", "rating": 1000},
    }
    couleur, resultat, methode, mes_infos, infos_adversaire = determiner_resultat_et_methode(partie, "theyluv_gns")

    assert resultat == "Nulle"
    assert methode == "Répétition"


def test_pseudo_insensible_a_la_casse():
    partie = {
        "white": {"username": "theyluv_gns", "result": "win", "rating": 1000},
        "black": {"username": "Adversaire", "result": "resigned", "rating": 950},
    }
    couleur, resultat, methode, mes_infos, infos_adversaire = determiner_resultat_et_methode(partie, "theyluv_gns")

    assert couleur == "Blancs"


def test_extraire_nom_ouverture_avec_eco():
    partie = {"eco": "https://www.chess.com/openings/Sicilian-Defense-Smith-Morra-Gambit"}
    assert extraire_nom_ouverture(partie) == "Sicilian Defense Smith Morra Gambit"


def test_extraire_nom_ouverture_sans_eco():
    partie = {}
    assert extraire_nom_ouverture(partie) == "Inconnue"
