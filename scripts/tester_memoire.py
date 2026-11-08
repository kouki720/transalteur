import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pipeline.schemas import RequeteTraduction
from src.pipeline.traducteur import traduire

# Phrase dans la mémoire → doit être réutilisée sans appel au modèle
r1 = traduire(RequeteTraduction(texte="Le chat dort sur le canapé.", langue_cible="en"))
print("Mémoire  :", r1.traduction)
print("Alertes  :", r1.alertes)

# Phrase absente → doit passer par le modèle
r2 = traduire(RequeteTraduction(texte="Le chien mange une pomme.", langue_cible="en"))
print("Modèle   :", r2.traduction)
print("Alertes  :", r2.alertes)