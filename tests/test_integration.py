import csv
from unittest.mock import patch

from src.pipeline.schemas import RequeteTraduction
from src.pipeline.traducteur import traduire
from src.tools import glossaire, memoire


def test_memoire_court_circuite_le_modele(tmp_path, monkeypatch):
    csv_memoire = tmp_path / "memoire.csv"
    csv_memoire.write_text(
        "texte_source,langue_source,langue_cible,traduction_validee\n"
        "Le chat dort.,fr,en,The cat is sleeping.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(memoire, "CHEMIN_MEMOIRE", csv_memoire)

    with patch("src.pipeline.traducteur.creer_client") as mock_client:
        resultat = traduire(RequeteTraduction(
            texte="Le chat dort.", langue_cible="en", langue_source="fr"
        ))
        mock_client.assert_not_called()

    assert resultat.traduction == "The cat is sleeping."
    assert "réutilisé depuis la mémoire" in resultat.alertes


def test_glossaire_injecte_dans_le_prompt(tmp_path, monkeypatch):
    csv_glossaire = tmp_path / "glossaire.csv"
    csv_glossaire.write_text(
        "terme_source,langue_source,langue_cible,traduction_imposee,type\n"
        "React,fr,en,React,impose\n",
        encoding="utf-8",
    )
    csv_memoire = tmp_path / "memoire_vide.csv"
    csv_memoire.write_text(
        "texte_source,langue_source,langue_cible,traduction_validee\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(glossaire, "CHEMIN_GLOSSAIRE", csv_glossaire)
    monkeypatch.setattr(memoire, "CHEMIN_MEMOIRE", csv_memoire)

    with patch("src.pipeline.traducteur.creer_client") as mock_client:
        mock_llm = mock_client.return_value
        mock_llm.invoke.return_value.content = "I built a React app."
        resultat = traduire(RequeteTraduction(
            texte="J'ai fait une app React.", langue_cible="en", langue_source="fr"
        ))
        prompt_envoye = mock_llm.invoke.call_args[0][0]

    assert "React" in prompt_envoye
    assert resultat.termes_glossaire == ["React"]


def test_traduction_memorisee_si_pas_alerte(tmp_path, monkeypatch):
    csv_glossaire = tmp_path / "glossaire_vide.csv"
    csv_glossaire.write_text(
        "terme_source,langue_source,langue_cible,traduction_imposee,type\n",
        encoding="utf-8",
    )
    csv_memoire = tmp_path / "memoire_vide.csv"
    csv_memoire.write_text(
        "texte_source,langue_source,langue_cible,traduction_validee\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(glossaire, "CHEMIN_GLOSSAIRE", csv_glossaire)
    monkeypatch.setattr(memoire, "CHEMIN_MEMOIRE", csv_memoire)

    with patch("src.pipeline.traducteur.creer_client") as mock_client:
        mock_client.return_value.invoke.return_value.content = "The dog eats an apple."
        traduire(RequeteTraduction(
            texte="Le chien mange une pomme.", langue_cible="en", langue_source="fr"
        ))

    lignes = list(csv.DictReader(csv_memoire.open(encoding="utf-8")))
    assert len(lignes) == 1
    assert lignes[0]["texte_source"] == "Le chien mange une pomme."


def test_verificateur_detecte_violation():
    from src.tools import verificateur
    entrees = [{"terme_source": "React", "traduction_imposee": "React", "type": "impose"}]
    alertes = verificateur.verifier("J'ai utilisé Réagir.", entrees)
    assert len(alertes) == 1
    assert "React" in alertes[0]