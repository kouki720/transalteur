import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pipeline.schemas import RequeteTraduction
from src.pipeline.traducteur import traduire

requete = RequeteTraduction(texte="Le chat dort sur le canapé.", langue_cible="en")
resultat = traduire(requete)
print("Traduction :", resultat.traduction)