import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pipeline.schemas import RequeteTraduction
from src.pipeline.traducteur import traduire

# Cas normal : glossaire respecté → aucune alerte
r1 = traduire(RequeteTraduction(
    texte="J'ai développé une application React avec une API cloud.",
    langue_cible="en",
    langue_source="fr",
))
print("Normal   :", r1.traduction)
print("Alertes  :", r1.alertes)

# Cas forcé : on simule une sortie qui viole le glossaire
from src.tools import verificateur
entrees = [{"terme_source": "React", "traduction_imposee": "React", "type": "impose"}]
alertes = verificateur.verifier("J'ai utilisé Réagir pour ce projet.", entrees)
print("Forcé    :", alertes)