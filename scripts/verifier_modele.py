import sys
from pathlib import Path

# Permettre l'import de src.* depuis scripts/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.llm.nvidia_client import lister_modeles, creer_client


def main():
    modeles = lister_modeles()
    print(f"{len(modeles)} modèles disponibles.")
    for m in modeles[:15]:
        print(" -", m)

    modele = "nvidia/nemotron-3.5-super-vl-120b-a12b"  # à ajuster selon la liste ci-dessus
    if modele not in modeles:
        print(f"\nATTENTION : {modele} absent de la liste. Choisis un ID valide.")
        return

    llm = creer_client(modele)
    prompt = (
        "Traduis la phrase suivante en anglais. "
        "Réponds uniquement avec la traduction.\n\n"
        'Phrase : "Le chat dort sur le canapé."'
    )
    print("\nTest 1 :", llm.invoke(prompt).content)

    prompt2 = (
        "Traduis la phrase suivante en anglais. "
        "Réponds uniquement avec la traduction.\n\n"
        'Phrase : "Il a du pain sur la planche."'
    )
    print("Test 2 :", llm.invoke(prompt2).content)


if __name__ == "__main__":
    main()