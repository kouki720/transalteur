import csv
from src.config import CHEMIN_MEMOIRE

_ENTETES = ["texte_source", "langue_source", "langue_cible", "traduction_validee"]


def charger_memoire() -> list[dict]:
    if not CHEMIN_MEMOIRE.exists():
        return []
    with open(CHEMIN_MEMOIRE, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def chercher(texte: str, langue_source: str, langue_cible: str) -> str | None:
    """Retourne la traduction validée si la phrase exacte existe, sinon None."""
    texte_norm = texte.strip().lower()
    for e in charger_memoire():
        if (
            e["texte_source"].strip().lower() == texte_norm
            and e["langue_source"] == langue_source
            and e["langue_cible"] == langue_cible
        ):
            return e["traduction_validee"]
    return None


def ajouter(texte: str, langue_source: str, langue_cible: str, traduction: str) -> None:
    """Ajoute une traduction validée à la mémoire (crée le fichier si absent)."""
    if chercher(texte, langue_source, langue_cible) is not None:
        return  # déjà présente, on ne duplique pas

    nouveau = not CHEMIN_MEMOIRE.exists()
    with open(CHEMIN_MEMOIRE, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=_ENTETES)
        if nouveau:
            writer.writeheader()
        writer.writerow({
            "texte_source": texte.strip(),
            "langue_source": langue_source,
            "langue_cible": langue_cible,
            "traduction_validee": traduction.strip(),
        })