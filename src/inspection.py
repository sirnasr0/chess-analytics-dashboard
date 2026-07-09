import json

with open("data/raw/parties_brutes.json", "r", encoding="utf-8") as f:
    parties = json.load(f)


print(f"Nombre total de parties : {len(parties)}")
print("\nClés disponibles pour une partie:")
print(list(parties[0].keys()))

print("\nExemple d'une partie complète :")
print(json.dumps(parties[0], indent=2, ensure_ascii= False))