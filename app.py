import threading
import tkinter as tk
from tkinter import ttk, messagebox

from src.config import LANGUES_SUPPORTEES, LANGUE_DEFAUT, NOMS_LANGUES
from src.pipeline.schemas import RequeteTraduction
from src.pipeline.traducteur import traduire


def nom(code: str) -> str:
    return f"{NOMS_LANGUES.get(code, code)} ({code})"


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Traducteur - Étude")
        self.geometry("720x560")
        self.minsize(600, 480)

        style = ttk.Style(self)
        style.configure("TButton", padding=6)
        style.configure("TLabel", padding=2)

        # --- Barre de langues ---
        barre = ttk.Frame(self, padding=(10, 10, 10, 0))
        barre.pack(fill="x")

        ttk.Label(barre, text="Source :").pack(side="left")
        self.source = ttk.Combobox(
            barre,
            values=[nom(c) for c in LANGUES_SUPPORTEES],
            state="readonly",
            width=16,
        )
        self.source.set(nom("fr"))
        self.source.pack(side="left", padx=(4, 10))

        self.bouton_inverser = ttk.Button(barre, text="⇄", width=3, command=self.inverser)
        self.bouton_inverser.pack(side="left", padx=6)

        ttk.Label(barre, text="Cible :").pack(side="left")
        self.cible = ttk.Combobox(
            barre,
            values=[nom(c) for c in LANGUES_SUPPORTEES],
            state="readonly",
            width=16,
        )
        self.cible.set(nom(LANGUE_DEFAUT))
        self.cible.pack(side="left", padx=(4, 0))

        # --- Saisie ---
        cadre_saisie = ttk.LabelFrame(self, text="Texte à traduire", padding=8)
        cadre_saisie.pack(fill="both", expand=True, padx=10, pady=(10, 6))
        self.entree = tk.Text(cadre_saisie, height=6, wrap="word", font=("Segoe UI", 11))
        self.entree.pack(fill="both", expand=True)

        # --- Bouton traduire ---
        self.bouton = ttk.Button(self, text="Traduire", command=self.lancer)
        self.bouton.pack(pady=6)

        # --- Résultat ---
        cadre_resultat = ttk.LabelFrame(self, text="Traduction", padding=8)
        cadre_resultat.pack(fill="both", expand=True, padx=10, pady=(0, 6))
        self.resultat = tk.Text(
            cadre_resultat,
            height=6,
            wrap="word",
            font=("Segoe UI", 11),
            state="disabled",
        )
        self.resultat.pack(fill="both", expand=True)

        # --- Barre de statut ---
        self.statut = ttk.Label(self, text="Prêt.", foreground="gray", padding=(10, 4))
        self.statut.pack(fill="x", side="bottom")

    # --- Helpers ---
    def code(self, valeur: str) -> str:
        return valeur.rsplit("(", 1)[-1].rstrip(")")

    def inverser(self):
        src, cib = self.source.get(), self.cible.get()
        self.source.set(cib)
        self.cible.set(src)

    def lancer(self):
        texte = self.entree.get("1.0", "end").strip()
        if not texte:
            messagebox.showwarning("Vide", "Saisis un texte à traduire.")
            return
        self.bouton.config(state="disabled")
        self.statut.config(text="Traduction en cours...", foreground="orange")
        threading.Thread(
            target=self._traduire,
            args=(texte, self.code(self.source.get()), self.code(self.cible.get())),
            daemon=True,
        ).start()

    def _traduire(self, texte, source, cible):
        try:
            resultat = traduire(RequeteTraduction(
                texte=texte, langue_cible=cible, langue_source=source
            ))
            self.after(0, self._afficher, resultat)
        except Exception as e:
            self.after(0, self._erreur, str(e))

    def _afficher(self, resultat):
        self.resultat.config(state="normal")
        self.resultat.delete("1.0", "end")
        self.resultat.insert("1.0", resultat.traduction)
        self.resultat.config(state="disabled")
        if resultat.alertes:
            self.statut.config(text=" | ".join(resultat.alertes), foreground="orange")
        else:
            self.statut.config(text="Traduction terminée.", foreground="green")
        self.bouton.config(state="normal")

    def _erreur(self, message):
        self.statut.config(text="Erreur.", foreground="red")
        self.bouton.config(state="normal")
        messagebox.showerror("Erreur", message)


if __name__ == "__main__":
    Application().mainloop()