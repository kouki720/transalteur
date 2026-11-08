from src.config import MODEL_ID, TEMPERATURE, MAX_TOKENS
from src.llm.nvidia_client import creer_client
from src.pipeline.schemas import RequeteTraduction, ResultatTraduction
from src.tools import glossaire, memoire, verificateur

_PROMPT = """Traduis la phrase suivante en {langue_cible}.
Réponds uniquement avec la traduction, sans commentaire ni explication.
{bloc_glossaire}
Phrase : "{texte}"
"""


def traduire(requete: RequeteTraduction) -> ResultatTraduction:
    langue_source = requete.langue_source or "fr"

    # 1) Mémoire de traduction : si la phrase exacte a déjà été validée, on la réutilise
    deja = memoire.chercher(requete.texte, langue_source, requete.langue_cible)
    if deja is not None:
        return ResultatTraduction(
            traduction=deja,
            langue_source=langue_source,
            alertes=["réutilisé depuis la mémoire"],
        )

    # 2) Glossaire : on récupère les termes présents dans le texte
    entrees = glossaire.termes_pour(requete.texte, langue_source, requete.langue_cible)
    bloc = glossaire.bloc_prompt(entrees)

    # 3) Appel au modèle
    prompt = _PROMPT.format(
        langue_cible=requete.langue_cible,
        bloc_glossaire=bloc + "\n" if bloc else "",
        texte=requete.texte,
    )
    llm = creer_client(MODEL_ID, temperature=TEMPERATURE, max_tokens=MAX_TOKENS)
    reponse = llm.invoke(prompt)
    traduction = reponse.content.strip()

    # 4) Vérification de la sortie
    alertes = verificateur.verifier(traduction, entrees)

    # 5) Mémorisation uniquement si la traduction est fiable (glossaire respecté)
    if not alertes:
        memoire.ajouter(requete.texte, langue_source, requete.langue_cible, traduction)

    return ResultatTraduction(
        traduction=traduction,
        langue_source=langue_source,
        termes_glossaire=[e["terme_source"] for e in entrees],
        alertes=alertes,
    )