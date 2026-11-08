from dataclasses import dataclass, field


@dataclass
class RequeteTraduction:
    texte: str
    langue_cible: str
    langue_source: str | None = None


@dataclass
class ResultatTraduction:
    traduction: str
    langue_source: str | None = None
    termes_glossaire: list[str] = field(default_factory=list)
    alertes: list[str] = field(default_factory=list)