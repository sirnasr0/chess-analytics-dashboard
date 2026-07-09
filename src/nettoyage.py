import json
import pandas as pd
from datetime import datetime

PSEUDO = "theyluv_gns"

with open("data/raw/parties_brutes.json", "r", encoding="utf-8") as f:
    parties = json.load(f)

#Codes de résultat chess.com qui veulent dire match nul
RESULTATS_NULLE = {"agreed", "repetition", "stalemate",
                   "insufficient", "timevsinsufficient", "50move"}

#Traduction des codes bruts chess.com en libellés lisibles
METHODES = {
    "checkmated": "Échec et mat",
    "resigned": "Abandon",
    "timeout": "Temps écoulé",
    "abandoned": "Partie abandonnée",
    "agreed": "Accord mutuel",
    "repetition": "Répétition",
    "stalemate": "Pat",
    "insufficient": "Matériel insuffisant",
    "timevsinsufficient": "Temps (matériel insuffisant)"
}

def determiner_resultat_et_methode(partie, pseudo):
    """Détermine couleur, résultat et méthode à partir d'une partie brute."""
    if partie["white"]["username"].lower() == pseudo.lower():
        mes_infos = partie["white"]
        infos_adversaire = partie["black"]
        couleur = "Blancs"
    else:
        mes_infos = partie["black"]
        infos_adversaire = partie["white"]
        couleur = "Noirs"

    mon_code = mes_infos["result"]
    if mon_code == "win":
        resultat = "Victoire"
        methode_brute = infos_adversaire["result"]
    elif mon_code in RESULTATS_NULLE:
        resultat = "Nulle"
        methode_brute = mon_code
    else:
        resultat = "Défaite"
        methode_brute = mon_code

    methode = METHODES.get(methode_brute, methode_brute)
    return couleur, resultat, methode, mes_infos, infos_adversaire


def extraire_nom_ouverture(partie):
    """Extrait le nom lisible de l'ouverture depuis le champ eco."""
    if "eco" in partie:
        return partie["eco"].split("/")[-1].replace("-", " ")
    return "Inconnue"


lignes = []


for partie in parties:
    couleur, resultat, methode, mes_infos, infos_adversaire = determiner_resultat_et_methode(partie, PSEUDO)
    nom_ouverture = extraire_nom_ouverture(partie)

    lignes.append({
        "Date": datetime.fromtimestamp(partie["end_time"]),
        "Couleur": couleur,
        "Resultat": resultat,
        "Methode": methode,
        "Mon_elo": mes_infos["rating"],
        "Elo_adversaire": infos_adversaire["rating"],
        "Type_partie": partie["time_class"],
        "Ouverture": nom_ouverture,
    })

df = pd.DataFrame(lignes)

df["Annee"] = df["Date"].dt.year
df["Mois"] = df["Date"].dt.month
df["Jour_semaine"] = df["Date"].dt.day_name()
df["Heure"] = df["Date"].dt.hour

df["Diff_elo"] = df["Mon_elo"] - df["Elo_adversaire"]

df["Ouverture_principale"] = df["Ouverture"].apply(lambda x: " ".join(x.split()[:2]))

print(df.shape)
print(df.head())
print(df["Resultat"].unique())
print(df["Methode"].unique)

df.to_csv("data/processed/chess_data_clean.csv", index=False)
print("\nSauvegardé dans data/processed/chess_data_clean.csv")