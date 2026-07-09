import requests
import json
import time

PSEUDO = "theyluv_gns"


def recuperer_liste_archives(pseudo):
    url = f"https://api.chess.com/pub/player/theyluv_gns/games/archives"
    reponse = requests.get(url, headers={"User-Agent": "Projet perso - analyse stats"})
    reponse.raise_for_status()
    return reponse.json()["archives"]

def recuperer_parties_dun_mois(url_archive):
    reponse = requests.get(url_archive, headers={"User-Agent" : "Projet perso - analyse stats"})
    reponse.raise_for_status()
    return reponse.json()["games"]

def recuperer_toutes_les_parties(pseudo):
    archives = recuperer_liste_archives(pseudo)
    print(f"{len(archives)} mois d'archives trouvés pour {pseudo}")

    toutes_les_parties = []

    for i, url_archive in enumerate(archives):
        parties_du_mois = recuperer_parties_dun_mois(url_archive)
        toutes_les_parties.extend(parties_du_mois)
        print(f"  [{i+1}/{len(archives)}] {url_archive.split('/')[-2]}-{url_archive.split('/')[-1]} : {len(parties_du_mois)} parties")
        time.sleep(0.2)
    
    return toutes_les_parties


if __name__ == "__main__":
    parties = recuperer_toutes_les_parties(PSEUDO)
    print(f"\nTotal : {len(parties)} parties récupérées")

    with open("data/raw/parties_brutes.json", "w", encoding="utf-8") as f:
        json.dump(parties, f, ensure_ascii=False, indent=2)
    
    print("Sauvegardé dans data/raw/parties_brutes.json")