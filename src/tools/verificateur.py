def verifier(traduction: str, entrees_glossaire: list[dict]) -> list[str]:
    """Retourne une liste d'alertes si le glossaire n'est pas respecté."""
    alertes = []
    for e in entrees_glossaire:
        if e["type"] == "impose":
            attendu = e["traduction_imposee"]
            if attendu.lower() not in traduction.lower():
                alertes.append(
                    f'glossaire non respecté : "{e["terme_source"]}" '
                    f'aurait dû donner "{attendu}"'
                )
    return alertes