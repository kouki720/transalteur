import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pipeline.schemas import RequeteTraduction
from src.pipeline.traducteur import traduire

# "React" est dans le glossaire → doit rester "React"
requete = RequeteTraduction(
    texte="J'ai développé une application React avec une API cloud.",
    langue_cible="en",
    langue_source="fr",
)
resultat = traduire(requete)
print("Traduction  :", resultat.traduction)
print("Termes vus  :", resultat.termes_glossaire)

# Témoin : sans terme du glossaire
requete2 = RequeteTraduction(
    texte="Le chat dort sur le canapé.",
    langue_cible="en",
    langue_source="fr",
)
resultat2 = traduire(requete2)
print("Témoin      :", resultat2.traduction)
print("Termes vus  :", resultat2.termes_glossaire)