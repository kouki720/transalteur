import csv
from src.config import CHEMIN_GLOSSAIRE


def charger_glossaire() -> list[dict]:
    if not CHEMIN_GLOSSAIRE.exists():
        return []
    with open(CHEMIN_GLOSSAIRE, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def termes_pour(texte: str, langue_source: str, langue_cible: str) -> list[dict]:
    """Retourne les entrées du glossaire dont le terme_source apparaît dans le texte."""
    entrees = charger_glossaire()
    texte_bas = texte.lower()
    resultat = []
    for e in entrees:
        if e["langue_source"] != langue_source or e["langue_cible"] != langue_cible:
            continue
        if e["terme_source"].lower() in texte_bas:
            resultat.append(e)
    return resultat


def bloc_prompt(entrees: list[dict]) -> str:
    """Formate les entrées du glossaire en instructions pour le prompt."""
    if not entrees:
        return ""
    lignes = ["Respecte impérativement le glossaire suivant :"]
    for e in entrees:
        if e["type"] == "impose":
            lignes.append(f'- "{e["terme_source"]}" doit être traduit par "{e["traduction_imposee"]}"')
        else:
            lignes.append(f'- "{e["terme_source"]}" ne doit pas être traduit, garde-le tel quel')
    return "\n".join(lignes)