"""
Step-by-Step Calculation Debugger für das Schul-Analysis Framework.

Dieses Modul bietet pädagogische Schritt-für-Schritt Anzeigen von mathematischen
Berechnungen für den Unterricht. Schüler können so den Lösungsweg nachvollziehen.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import sympy as sp
from sympy import latex, simplify

from .config import SchulAnalysisConfig
from .sympy_types import T_Expr


class DetailGrad(Enum):
    """Detailgrad für die Debug-Ausgabe."""

    MINIMAL = "minimal"
    NORMAL = "normal"
    PÄDAGOGISCH = "pädagogisch"
    AUSFÜHRLICH = "ausführlich"


class BerechnungsTyp(Enum):
    """Typen von Berechnungen für die Debug-Anzeige."""

    ABLEITUNG = "ableitung"
    INTEGRATION = "integration"
    NULLSTELLEN = "nullstellen"
    EXTREMA = "extrema"
    WENDEPUNKTE = "wendepunkte"
    VEREINFACHUNG = "vereinfachung"
    AUSWERTUNG = "auswertung"
    FUNKTIONEN_ANALYSE = "funktionen_analyse"


@dataclass
class BerechnungsSchritt:
    """Ein einzelner Berechnungsschritt mit Erklärung."""

    schritt_nummer: int
    titel: str
    beschreibung: str
    formel_vorher: Optional[str] = None
    formel_nachher: Optional[str] = None
    erklärung: str = ""
    mathematische_regeln: List[str] = field(default_factory=list)
    tipps: List[str] = field(default_factory=list)
    lernziele: List[str] = field(default_factory=list)

    def formatiere_latex(self) -> str:
        """Formatiert den Schritt als LaTeX für bessere Darstellung."""
        latex_parts = [f"\\textbf{{Schritt {self.schritt_nummer}: {self.titel}}}\n"]

        if self.beschreibung:
            latex_parts.append(f"\\textit{{{self.beschreibung}}}\n")

        if self.formel_vorher:
            latex_parts.append(f"\\text{{Vorher: }} {self.formel_vorher}")

        if self.formel_nachher:
            latex_parts.append(f"\\text{{Nachher: }} {self.formel_nachher}")

        if self.erklärung:
            latex_parts.append(f"\\text{{Erklärung: }} {self.erklärung}")

        if self.mathematische_regeln:
            latex_parts.append("\\text{Angewendete Regeln:}")
            for regel in self.mathematische_regeln:
                latex_parts.append(f"\\item {regel}")

        return "\n".join(latex_parts)


class BerechnungsStrategie(ABC):
    """Abstrakte Basisklasse für Berechnungsstrategien."""

    @abstractmethod
    def kann_anwenden(self, funktion: T_Expr, kontext: Dict[str, Any]) -> bool:
        """Prüft, ob diese Strategie angewendet werden kann."""
        pass

    @abstractmethod
    def wende_an(
        self, funktion: T_Expr, kontext: Dict[str, Any]
    ) -> List[BerechnungsSchritt]:
        """Wendet die Strategie an und gibt Schritte zurück."""
        pass


class AbleitungsStrategie(BerechnungsStrategie):
    """Strategie für die Ableitungsberechnung."""

    def kann_anwenden(self, funktion: T_Expr, kontext: Dict[str, Any]) -> bool:
        """Kann auf differenzierbare Funktionen angewendet werden."""
        return kontext.get("operation") == "ableitung"

    def wende_an(
        self, funktion: T_Expr, kontext: Dict[str, Any]
    ) -> List[BerechnungsSchritt]:
        """Führt die Ableitung Schritt für Schritt durch."""
        schritte = []
        ordnung = kontext.get("ordnung", 1)
        variable = kontext.get("variable", sp.Symbol("x"))

        # Schritt 1: Grundregel identifizieren
        schritt1 = BerechnungsSchritt(
            schritt_nummer=1,
            titel="Grundregel identifizieren",
            beschreibung=f"Wir berechnen die {ordnung}. Ableitung der Funktion",
            formel_vorher=latex(funktion),
            erklärung=f"Die {ordnung}. Ableitung zeigt die Änderungsrate der Funktion",
            mathematische_regeln=["Ableitungsregeln", "Potenzregel", "Kettenregel"],
        )
        schritte.append(schritt1)

        # Schritt 2: Terme analysieren
        if funktion.is_Add:
            schritt2 = BerechnungsSchritt(
                schritt_nummer=2,
                titel="Summenregel anwenden",
                beschreibung="Die Funktion ist eine Summe, daher werden die Terme einzeln abgeleitet",
                formel_vorher=latex(funktion),
                erklärung="Summenregel: (f + g)' = f' + g'",
                mathematische_regeln=["Summenregel"],
                tipps=["Leite jeden Term einzeln ab", "Addiere dann die Ergebnisse"],
            )
            schritte.append(schritt2)

        # Schritt 3: Einzelne Terme ableiten
        if hasattr(funktion, "args"):
            for i, term in enumerate(funktion.args, 1):
                abgeleiteter_term = sp.diff(term, variable, ordnung)
                schritt_term = BerechnungsSchritt(
                    schritt_nummer=len(schritte) + 1,
                    titel=f"Term {i} ableiten",
                    beschreibung=f"Ableitung von {latex(term)}",
                    formel_vorher=latex(term),
                    formel_nachher=latex(abgeleiteter_term),
                    erklärung=self._erkläre_ableitung(term, variable, ordnung),
                    mathematische_regeln=self._identifiziere_regel(term),
                )
                schritte.append(schritt_term)

        # Schritt 4: Ergebnis zusammenfassen
        ergebnis = sp.diff(funktion, variable, ordnung)
        schritt_final = BerechnungsSchritt(
            schritt_nummer=len(schritte) + 1,
            titel="Ergebnis zusammenfassen",
            beschreibung=f"Die {ordnung}. Ableitung ist:",
            formel_nachher=latex(ergebnis),
            erklärung="Alle abgeleiteten Terme werden zusammengefasst",
            tipps=[
                "Vereinfache das Ergebnis wenn möglich",
                "Prüfe mit der Ausgangsfunktion",
            ],
        )
        schritte.append(schritt_final)

        return schritte

    def _erkläre_ableitung(
        self, term: sp.Expr, variable: sp.Symbol, ordnung: int
    ) -> str:
        """Erklärt die Ableitung eines Terms."""
        if term.is_Mul:
            if len(term.args) == 2 and term.args[0].is_number:
                return f"Konstante {term.args[0]} bleibt erhalten, Variable wird abgeleitet"

        if term.is_Pow:
            if term.args[1].is_number:
                return f"Potenzregel: x^n wird zu n·x^(n-1)"

        return f"Standard-Ableitungsregeln anwenden"

    def _identifiziere_regel(self, term: sp.Expr) -> List[str]:
        """Identifiziert die angewendeten Ableitungsregeln."""
        regeln = []

        if term.is_Add:
            regeln.append("Summenregel")
        elif term.is_Mul:
            regeln.append("Produktregel")
        elif term.is_Pow:
            regeln.append("Potenzregel")
        else:
            regeln.append("Grundregeln")

        return regeln


class VereinfachungsStrategie(BerechnungsStrategie):
    """Strategie für die Vereinfachung von Ausdrücken."""

    def kann_anwenden(self, funktion: T_Expr, kontext: Dict[str, Any]) -> bool:
        """Kann auf Vereinfachungsoperationen angewendet werden."""
        return kontext.get("operation") == "vereinfachung"

    def wende_an(
        self, funktion: T_Expr, kontext: Dict[str, Any]
    ) -> List[BerechnungsSchritt]:
        """Führt die Vereinfachung Schritt für Schritt durch."""
        schritte = []

        # Schritt 1: Ausgangssituation
        schritt1 = BerechnungsSchritt(
            schritt_nummer=1,
            titel="Ausgangsausdruck analysieren",
            beschreibung="Wir vereinfachen den gegebenen Ausdruck Schritt für Schritt",
            formel_vorher=latex(funktion),
            erklärung="Ziel: Einfachste mögliche Form des Ausdrucks finden",
            lernziele=["Vereinfachungstechniken", "Äquivalente Umformungen"],
        )
        schritte.append(schritt1)

        # Schritt 2: Terme zusammenfassen
        if funktion.is_Add:
            vereinfacht = simplify(funktion)
            schritt2 = BerechnungsSchritt(
                schritt_nummer=2,
                titel="Gleiche Terme zusammenfassen",
                beschreibung="Addiere/Subtrahiere gleiche Terme",
                formel_vorher=latex(funktion),
                formel_nachher=latex(vereinfacht),
                erklärung="Gleiche Terme werden durch Addition/Subtraktion zusammengefasst",
                mathematische_regeln=["Zusammenfassen gleicher Terme"],
                tipps=[
                    "Achte auf die Vorzeichen",
                    "Prüfe ob Terme wirklich gleich sind",
                ],
            )
            schritte.append(schritt2)

        # Schritt 3: Ausklammern wenn möglich
        if hasattr(funktion, "args") and len(funktion.args) > 1:
            # Suche gemeinsame Faktoren
            gemeinsamer_faktor = self._finde_gemeinsamen_faktor(funktion)
            if gemeinsamer_faktor and gemeinsamer_faktor != 1:
                schritt3 = BerechnungsSchritt(
                    schritt_nummer=len(schritte) + 1,
                    titel="Gemeinsamen Faktor ausklammern",
                    beschreibung=f"Der gemeinsame Faktor {latex(gemeinsamer_faktor)} wird ausgeklammert",
                    formel_vorher=latex(funktion),
                    formel_nachher=latex(sp.factor(funktion)),
                    erklärung="Ausklammern macht den Ausdruck übersichtlicher",
                    mathematische_regeln=["Distributivgesetz"],
                    tipps=["Suche nach gemeinsamen Faktoren in allen Termen"],
                )
                schritte.append(schritt3)

        # Schritt 4: Ergebnis prüfen
        ergebnis = simplify(funktion)
        schritt_final = BerechnungsSchritt(
            schritt_nummer=len(schritte) + 1,
            titel="Vereinfachtes Ergebnis",
            beschreibung="Der vereinfachte Ausdruck lautet:",
            formel_nachher=latex(ergebnis),
            erklärung="Der Ausdruck ist jetzt in seiner einfachsten Form",
            lernziele=["Vereinfachung erfolgreich durchgeführt"],
        )
        schritte.append(schritt_final)

        return schritte

    def _finde_gemeinsamen_faktor(self, ausdruck: sp.Expr) -> Optional[sp.Expr]:
        """Findet einen gemeinsamen Faktor in einem Ausdruck."""
        if not ausdruck.is_Add:
            return None

        # Sammle alle Faktoren aller Terme
        alle_faktoren = []
        for term in ausdruck.args:
            if term.is_Mul:
                alle_faktoren.extend(term.args)
            else:
                alle_faktoren.append(term)

        # Finde gemeinsame Faktoren
        gemeinsame = set(alle_faktoren)
        for faktor in alle_faktoren:
            if alle_faktoren.count(faktor) == len(ausdruck.args):
                gemeinsame.add(faktor)

        # Gebe den ersten gemeinsamen Faktor zurück
        if gemeinsame:
            return next(iter(gemeinsame))
        return None


class DebugSession:
    """
    Sitzung für das Debuggen von Berechnungen mit pädagogischer Ausgabe.
    """

    def __init__(
        self, name: str, funktion: sp.Expr, detailgrad: DetailGrad = DetailGrad.NORMAL
    ):
        self.name = name
        self.funktion = funktion
        self.detailgrad = detailgrad
        self.schritte: List[BerechnungsSchritt] = []
        self.strategien: List[BerechnungsStrategie] = [
            AbleitungsStrategie(),
            VereinfachungsStrategie(),
        ]

    def berechne_mit_schritten(
        self, berechnungs_typ: BerechnungsTyp, **kwargs
    ) -> List[BerechnungsSchritt]:
        """
        Führt eine Berechnung mit Schritt-für-Schritt-Anzeige durch.

        Args:
            berechnungs_typ: Typ der Berechnung
            **kwargs: Zusätzliche Parameter für die Berechnung

        Returns:
            Liste der Berechnungsschritte
        """
        # Finde passende Strategie
        strategie = None
        for s in self.strategien:
            kontext = {"operation": berechnungs_typ.value, **kwargs}
            if s.kann_anwenden(self.funktion, kontext):
                strategie = s
                break

        if not strategie:
            raise ValueError(f"Keine Strategie für {berechnungs_typ} gefunden")

        # Führe Berechnung durch
        self.schritte = strategie.wende_an(self.funktion, kontext)

        # Filtere nach Detailgrad
        if self.detailgrad == DetailGrad.MINIMAL:
            # Nur wichtigste Schritte
            self.schritte = [
                s for s in self.schritte if s.schritt_nummer in [1, len(self.schritte)]
            ]
        elif self.detailgrad == DetailGrad.PÄDAGOGISCH:
            # Füge zusätzliche Erklärungen hinzu
            self._erweitere_pädagogisch()

        return self.schritte

    def _erweitere_pädagogisch(self):
        """Erweitert die Schritte um pädagogische Elemente."""
        for schritt in self.schritte:
            # Füge Lernziele hinzu
            if not schritt.lernziele:
                schritt.lernziele = [
                    "Mathematische Regeln verstehen",
                    "Systematisches Vorgehen lernen",
                    "Ergebnisse kritisch prüfen",
                ]

            # Füge zusätzliche Tipps hinzu
            if not schritt.tipps:
                schritt.tipps = [
                    "Schreibe jeden Schritt deutlich auf",
                    "Prüfe jeden Schritt sorgfältig",
                    "Vergleiche mit bekannten Beispielen",
                ]

    def formatiere_ausgabe(self, format_typ: str = "text") -> str:
        """
        Formatiert die Ausgabe der Berechnungsschritte.

        Args:
            format_typ: "text", "latex", oder "html"

        Returns:
            Formatierte Ausgabe
        """
        if format_typ == "latex":
            return self._formatiere_latex()
        elif format_typ == "html":
            return self._formatiere_html()
        else:
            return self._formatiere_text()

    def _formatiere_text(self) -> str:
        """Formatiert die Ausgabe als Text."""
        zeilen = [f"=== {self.name} ==="]
        zeilen.append(f"Funktion: {self.funktion}")
        zeilen.append(f"Detailgrad: {self.detailgrad.value}")
        zeilen.append("")

        for schritt in self.schritte:
            zeilen.append(f"Schritt {schritt.schritt_nummer}: {schritt.titel}")
            zeilen.append(f"  {schritt.beschreibung}")

            if schritt.formel_vorher:
                zeilen.append(f"  Vorher: {schritt.formel_vorher}")
            if schritt.formel_nachher:
                zeilen.append(f"  Nachher: {schritt.formel_nachher}")

            if schritt.erklärung:
                zeilen.append(f"  Erklärung: {schritt.erklärung}")

            if schritt.mathematische_regeln:
                zeilen.append(f"  Regeln: {', '.join(schritt.mathematische_regeln)}")

            zeilen.append("")

        return "\n".join(zeilen)

    def _formatiere_latex(self) -> str:
        """Formatiert die Ausgabe als LaTeX."""
        zeilen = [
            "\\section*{" + self.name + "}",
            f"Funktion: ${latex(self.funktion)}$",
            f"Detailgrad: {self.detailgrad.value}",
            "",
        ]

        for schritt in self.schritte:
            zeilen.append(schritt.formatiere_latex())
            zeilen.append("")

        return "\n".join(zeilen)

    def _formatiere_html(self) -> str:
        """Formatiert die Ausgabe als HTML."""
        html = [
            f"<h2>{self.name}</h2>",
            f"<p><strong>Funktion:</strong> {self.funktion}</p>",
            f"<p><strong>Detailgrad:</strong> {self.detailgrad.value}</p>",
            "<ol>",
        ]

        for schritt in self.schritte:
            html.append(f"""
            <li>
                <h3>{schritt.titel}</h3>
                <p>{schritt.beschreibung}</p>
                {f"<p><strong>Vorher:</strong> {schritt.formel_vorher}</p>" if schritt.formel_vorher else ""}
                {f"<p><strong>Nachher:</strong> {schritt.formel_nachher}</p>" if schritt.formel_nachher else ""}
                {f"<p><strong>Erklärung:</strong> {schritt.erklärung}</p>" if schritt.erklärung else ""}
                {f"<p><strong>Regeln:</strong> {', '.join(schritt.mathematische_regeln)}</p>" if schritt.mathematische_regeln else ""}
            </li>
            """)

        html.append("</ol>")
        return "\n".join(html)


# Convenience-Funktionen
def debug_ableitung(
    funktion: sp.Expr, ordnung: int = 1, detailgrad: DetailGrad = DetailGrad.NORMAL
) -> DebugSession:
    """
    Debuggt eine Ableitungsberechnung Schritt für Schritt.

    Args:
        funktion: Die abzuleitende Funktion
        ordnung: Ordnung der Ableitung
        detailgrad: Detailgrad der Ausgabe

    Returns:
        DebugSession mit allen Schritten
    """
    session = DebugSession(f"Ableitung {ordnung}. Ordnung", funktion, detailgrad)
    session.berechne_mit_schritten(BerechnungsTyp.ABLEITUNG, ordnung=ordnung)
    return session


def debug_vereinfachung(
    funktion: sp.Expr, detailgrad: DetailGrad = DetailGrad.NORMAL
) -> DebugSession:
    """
    Debuggt eine Vereinfachung Schritt für Schritt.

    Args:
        funktion: Der zu vereinfachende Ausdruck
        detailgrad: Detailgrad der Ausgabe

    Returns:
        DebugSession mit allen Schritten
    """
    session = DebugSession("Vereinfachung", funktion, detailgrad)
    session.berechne_mit_schritten(BerechnungsTyp.VEREINFACHUNG)
    return session


def debug_nullstellen(
    funktion: sp.Expr, detailgrad: DetailGrad = DetailGrad.NORMAL
) -> DebugSession:
    """
    Debuggt eine Nullstellenberechnung Schritt für Schritt.

    Args:
        funktion: Die zu analysierende Funktion
        detailgrad: Detailgrad der Ausgabe

    Returns:
        DebugSession mit allen Schritten
    """
    session = DebugSession("Nullstellenberechnung", funktion, detailgrad)
    session.berechne_mit_schritten(BerechnungsTyp.NULLSTELLEN)
    return session
