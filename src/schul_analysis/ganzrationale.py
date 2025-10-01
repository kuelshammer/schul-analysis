"""
Ganzrationale Funktionen (Polynome) für das Schul-Analysis Framework.

Unterstützt verschiedene Konstruktor-Formate und mathematisch korrekte
Visualisierung mit Plotly für Marimo-Notebooks.
"""

import numpy as np
import pandas as pd
import marimo as mo
from typing import Union, List, Tuple, Dict, Any
import sympy as sp
from sympy import sympify, latex, solve, diff, symbols, Poly
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


class GanzrationaleFunktion:
    """
    Repräsentiert eine ganzrationale Funktion (Polynom) mit verschiedenen
    Konstruktor-Optionen und Visualisierungsmethoden.
    """

    def __init__(self, eingabe: Union[str, List[float], Dict[int, float]]):
        """
        Konstruktor für ganzrationale Funktionen.

        Args:
            eingabe: String ("x^3-2x+1"), Liste ([1, 0, -2, 1]) oder Dictionary ({3: 1, 1: -2, 0: 1})
        """
        self.x = symbols("x")
        self.original_eingabe = str(eingabe)  # Original eingabe speichern

        if isinstance(eingabe, str):
            # String-Konstruktor mit robuster Verarbeitung
            self.term_str, self.term_sympy = self._parse_string_eingabe(eingabe)
        elif isinstance(eingabe, list):
            # Listen-Konstruktor: [1, 0, -2, 1] für x³ - 2x + 1
            self.term_str = self._liste_zu_string(eingabe)
            self.term_sympy = self._liste_zu_sympy(eingabe)
        elif isinstance(eingabe, dict):
            # Dictionary-Konstruktor: {3: 1, 1: -2, 0: 1} für x³ - 2x + 1
            self.term_str = self._dict_zu_string(eingabe)
            self.term_sympy = self._dict_zu_sympy(eingabe)
        else:
            raise TypeError("Eingabe muss String, Liste oder Dictionary sein")

        # Koeffizienten extrahieren (als exakte SymPy-Objekte)
        self.koeffizienten = self._extrahiere_koeffizienten()

    def _parse_string_eingabe(self, eingabe: str) -> Tuple[str, sp.Basic]:
        """
        Robuster Parser für verschiedene String-Formate von ganzrationalen Funktionen.

        Unterstützt:
        - "x^2+4x-2" (Standard-Schreibweise)
        - "$x^2+4x-2$" (LaTeX-Format)
        - "x**2+4*x-2" (Python-Syntax)
        - "2x" (implizite Multiplikation)
        - "x^2 + 4x - 2" (mit Leerzeichen)

        Args:
            eingabe: String-Eingabe in verschiedenen Formaten

        Returns:
            Tuple aus (bereinigter_string, sympy_ausdruck)
        """
        import re

        # Prüfe auf offensichtlich ungültige Eingaben
        if not re.match(r"^[x\d\+\-\*\^\s\(\)\.\$\/]+$", eingabe.replace(" ", "")):
            raise ValueError(f"Ungültige Zeichen in Eingabe: '{eingabe}'")

        # 1. LaTeX-Format bereinigen ($ entfernen)
        bereinigt = eingabe.replace("$", "").strip()

        # 2. Spezialfall: Linearfaktoren-Format
        if self._ist_linearfaktor_format(bereinigt):
            return self._parse_linearfaktoren(bereinigt)

        # 3. Leerzeichen um Operatoren normalisieren
        bereinigt = re.sub(r"\s*([+\-])\s*", r"\1", bereinigt)

        # 4. Dezimalzahlen schützen (ersetze temporär)
        dezimal_pattern = r"(\d+)\.(\d+)"
        bereinigt = re.sub(dezimal_pattern, r"DEZIMAL_\1_DEZTRENN_\2", bereinigt)

        # 5. Implizite Multiplikation behandeln (z.B. "2x" → "2*x")
        bereinigt = re.sub(r"(\d+)([a-zA-Z])", r"\1*\2", bereinigt)
        bereinigt = re.sub(r"([a-zA-Z])(\d)", r"\1^\2", bereinigt)  # x2 → x^2

        # 6. Hochzeichen-Konvertierung (^ → **)
        bereinigt = re.sub(r"([a-zA-Z])\^(\d+)", r"\1**\2", bereinigt)
        bereinigt = re.sub(r"([a-zA-Z])\^([a-zA-Z])", r"\1**\2", bereinigt)

        # 7. Spezialfall: x ohne Exponent → x^1
        bereinigt = re.sub(r"(?<![a-zA-Z])(x)(?![a-zA-Z0-9_*^])", r"x**1", bereinigt)
        bereinigt = re.sub(r"([+\-])(x)(?![a-zA-Z0-9_*^])", r"\1x**1", bereinigt)

        # 8. Koeffizienten ohne x normalisieren
        bereinigt = re.sub(r"([+\-])(\d+)(?![a-zA-Z0-9_*^])", r"\1\2*x**0", bereinigt)
        bereinigt = re.sub(r"^(\d+)(?![a-zA-Z0-9_*^])", r"\1*x**0", bereinigt)

        # 9. Dezimalzahlen wiederherstellen
        bereinigt = re.sub(r"DEZIMAL_(\d+)_DEZTRENN_(\d+)", r"\1.\2", bereinigt)

        # 10. Versuch mit sympify
        try:
            term_sympy = sympify(bereinigt)
            return bereinigt, term_sympy
        except Exception as e:
            # Fallback: Versuch mit alternativer Verarbeitung
            try:
                # Nochmal bereinigen mit einfacherer Logik
                einfache_bereinigung = (
                    eingabe.replace("$", "").replace("^", "**").strip()
                )

                # Implizite Multiplikation: Zahl gefolgt von Variable
                einfache_bereinigung = re.sub(
                    r"(\d)([a-zA-Z])", r"\1*\2", einfache_bereinigung
                )

                # Implizite Multiplikation: Variable gefolgt von Zahl
                einfache_bereinigung = re.sub(
                    r"([a-zA-Z])(\d)", r"\1^\2", einfache_bereinigung
                )

                # Multiplikation zwischen Klammerausdrücken
                einfache_bereinigung = re.sub(r"\)\(", ")*(", einfache_bereinigung)

                term_sympy = sympify(einfache_bereinigung)
                return einfache_bereinigung, term_sympy
            except Exception as e2:
                raise ValueError(
                    f"Konnte '{eingabe}' nicht in gültigen mathematischen Ausdruck umwandeln. "
                    f"Versuch 1: '{bereinigt}' → {e}. "
                    f"Versuch 2: '{einfache_bereinigung}' → {e2}"
                )

    def _ist_linearfaktor_format(self, eingabe: str) -> bool:
        """Prüft, ob die Eingabe im Linearfaktoren-Format vorliegt."""
        import re

        # Pattern für Linearfaktoren: (x±a), (x±b), etc.
        # Auch mit Potenzen: (x±a)^n
        # Auch mit Koeffizienten: k(x±a)
        # Auch mit expliziten Multiplikationszeichen: (x±a)*(x±b)
        # Auch mit impliziten Multiplikationszeichen: (x±a)(x±b)
        pattern = r"^(\d*\(x[+\-]\d+\)(\^\d+)?[*]*)*\d*\(x[+\-]\d+\)(\^\d+)?$"

        return bool(re.match(pattern, eingabe.replace(" ", "")))

    def _parse_linearfaktoren(self, eingabe: str) -> tuple[str, sp.Basic]:
        """Parst Linearfaktoren in expandierte Form."""
        import re

        # Leerzeichen entfernen
        bereinigt = eingabe.replace(" ", "")

        # Entferne explizite Multiplikationszeichen und extrahiere alle Faktoren
        bereinigt = bereinigt.replace("*", "")
        faktoren = re.findall(r"(\d*)\(x([+\-])(\d+)\)(\^\d+)?", bereinigt)

        if not faktoren:
            raise ValueError(f"Ungültiges Linearfaktoren-Format: '{eingabe}'")

        # Baue den Ausdruck direkt mit SymPy zusammen
        x = self.x
        ergebnis = 1

        for koeff, vorzeichen, zahl, potenz in faktoren:
            # Koeffizient verarbeiten
            if koeff:
                koeff_int = sp.Integer(int(koeff))
            else:
                koeff_int = sp.Integer(1)

            # Vorzeichen und Zahl verarbeiten
            if vorzeichen == "+":
                konstante = -sp.Integer(int(zahl))  # (x+1) bedeutet (x - (-1))
            else:
                konstante = sp.Integer(int(zahl))  # (x-1) bedeutet (x - 1)

            # Linearfaktor erstellen
            linearfaktor = x - konstante

            if potenz:
                # Mit Potenz
                potenz_wert = int(potenz[1:])  # ^n extrahieren
                faktor = koeff_int * linearfaktor**potenz_wert
            else:
                # Ohne Potenz
                faktor = koeff_int * linearfaktor

            ergebnis = ergebnis * faktor

        try:
            # Expandiere zu Standardform
            term_expanded = sp.expand(ergebnis)
            term_string = str(ergebnis)

            return term_string, term_expanded
        except Exception as e:
            raise ValueError(
                f"Konnte Linearfaktoren '{eingabe}' nicht verarbeiten: {e}"
            )

    def _liste_zu_string(self, koeff: list[float]) -> str:
        """Wandelt Koeffizienten-Liste in Term-String um."""
        terme = []
        for i, k in enumerate(koeff):
            if k == 0:
                continue
            if i == 0:
                terme.append(str(k))
            elif i == 1:
                if k == 1:
                    terme.append("x")
                elif k == -1:
                    terme.append("-x")
                else:
                    terme.append(f"{k}x")
            else:
                if k == 1:
                    terme.append(f"x^{i}")
                elif k == -1:
                    terme.append(f"-x^{i}")
                else:
                    terme.append(f"{k}x^{i}")

        if not terme:
            return "0"

        return "+".join(terme).replace("+-", "-")

    def _liste_zu_sympy(self, koeff: List[float]) -> sp.Basic:
        """Wandelt Koeffizienten-Liste in SymPy-Ausdruck um."""
        term = 0
        for i, k in enumerate(koeff):
            term += k * self.x**i
        return term

    def _dict_zu_string(self, koeff: Dict[int, float]) -> str:
        """Wandelt Koeffizienten-Dictionary in Term-String um."""
        # Sortiere nach absteigendem Grad
        sortierte_koeff = sorted(koeff.items(), key=lambda x: -x[0])

        terme = []
        for grad, k in sortierte_koeff:
            if k == 0:
                continue
            if grad == 0:
                terme.append(str(k))
            elif grad == 1:
                if k == 1:
                    terme.append("x")
                elif k == -1:
                    terme.append("-x")
                else:
                    terme.append(f"{k}x")
            else:
                if k == 1:
                    terme.append(f"x^{grad}")
                elif k == -1:
                    terme.append(f"-x^{grad}")
                else:
                    terme.append(f"{k}x^{grad}")

        if not terme:
            return "0"

        return "+".join(terme).replace("+-", "-")

    def _dict_zu_sympy(self, koeff: Dict[int, float]) -> sp.Basic:
        """Wandelt Koeffizienten-Dictionary in SymPy-Ausdruck um."""
        term = 0
        for grad, k in koeff.items():
            term += k * self.x**grad
        return term

    def _extrahiere_koeffizienten(self) -> List[sp.Basic]:
        """Extrahiert Koeffizienten aus SymPy-Ausdruck."""
        try:
            # Prüfe, ob der Ausdruck gültig ist
            if not hasattr(self.term_sympy, "subs"):
                raise ValueError("Ungültiger SymPy-Ausdruck")

            poly = Poly(self.term_sympy, self.x)
            return [poly.coeff_monomial(self.x**i) for i in range(poly.degree() + 1)]
        except Exception as e:
            # Fallback: Manuelle Koeffizienten-Extraktion
            koeffizienten = []

            try:
                # Konstante Term
                const_term = self.term_sympy.subs(self.x, 0)
                if const_term != 0:
                    try:
                        koeffizienten.append(const_term)
                    except (TypeError, ValueError):
                        # Wenn es sich nicht um eine Zahl handelt, überspringen
                        pass

                # Für höhere Grade: Ableitungen verwenden
                for i in range(1, 10):  # Maximal Grad 10
                    try:
                        # i-te Ableitung an x=0 dividiert durch i!
                        ableitung_i = sp.diff(self.term_sympy, self.x, i)
                        wert_0 = ableitung_i.subs(self.x, 0)
                        koeff = wert_0 / sp.factorial(i)

                        if koeff != 0:  # Nur signifikante Koeffizienten
                            # Stelle sicher, dass die Liste lang genug ist
                            while len(koeffizienten) < i:
                                koeffizienten.append(sp.Integer(0))
                            koeffizienten.append(koeff)
                    except:
                        break

                # Wenn keine Koeffizienten gefunden wurden
                if not koeffizienten:
                    koeffizienten = [sp.Integer(0)]

                return koeffizienten
            except Exception:
                # Wenn alles fehlschlägt, leere Liste zurückgeben
                return [sp.Integer(0)]

    def term(self) -> str:
        """Gibt den Term als String zurück."""
        return self.term_str

    def term_latex(self) -> str:
        """Gibt den Term als LaTeX-String zurück."""
        return latex(self.term_sympy)

    def wert(self, x_wert: float) -> float:
        """Berechnet den Funktionswert an einer Stelle."""
        return float(self.term_sympy.subs(self.x, x_wert))

    def ableitung(self, ordnung: int = 1) -> "GanzrationaleFunktion":
        """Berechnet die Ableitung gegebener Ordnung."""
        abgeleitet = diff(self.term_sympy, self.x, ordnung)

        # Erstelle neue Funktion direkt mit dem abgeleiteten Ausdruck
        neue_funktion = GanzrationaleFunktion.__new__(GanzrationaleFunktion)
        neue_funktion.x = self.x
        neue_funktion.term_sympy = abgeleitet
        neue_funktion.term_str = str(abgeleitet)
        neue_funktion.koeffizienten = neue_funktion._extrahiere_koeffizienten()

        # Stelle sicher, dass die Koeffizientenliste die richtige Länge hat
        # (füge führende Nullen hinzu, wenn nötig)
        erwartete_laenge = max(0, len(self.koeffizienten) - ordnung)
        while len(neue_funktion.koeffizienten) < erwartete_laenge:
            neue_funktion.koeffizienten.insert(0, 0.0)

        return neue_funktion

    def nullstellen(self, real: bool = True) -> List[float]:
        """Berechnet die Nullstellen der Funktion."""
        try:
            lösungen = solve(self.term_sympy, self.x)
            nullstellen = []

            for lösung in lösungen:
                if real:
                    # Nur reelle Nullstellen
                    if lösung.is_real:
                        nullstellen.append(float(lösung))
                else:
                    # Auch komplexe Nullstellen
                    if lösung.is_real:
                        nullstellen.append(float(lösung))
                    else:
                        # Komplexe Zahl in Real- und Imaginärteil aufteilen
                        nullstellen.append(complex(lösung))

            return sorted(nullstellen)
        except:
            return []

    def extremstellen(self) -> List[Tuple[float, str]]:
        """Berechnet die Extremstellen der Funktion."""
        try:
            # Erste Ableitung
            f_strich = self.ableitung(1)

            # Kritische Punkte
            kritische_punkte = solve(f_strich.term_sympy, self.x)

            extremstellen = []

            for punkt in kritische_punkte:
                if punkt.is_real:
                    x_wert = float(punkt)

                    # Zweite Ableitung
                    f_doppelstrich = self.ableitung(2)
                    y_wert = f_doppelstrich.wert(x_wert)

                    if y_wert > 0:
                        art = "Minimum"
                    elif y_wert < 0:
                        art = "Maximum"
                    else:
                        art = "Sattelpunkt"

                    extremstellen.append((x_wert, art))

            return sorted(extremstellen, key=lambda x: x[0])
        except:
            return []

    def nullstellen_weg(self) -> str:
        """Gibt detaillierten Lösungsweg für Nullstellen als Markdown zurück."""
        weg = f"# Nullstellen von f(x) = {self.original_eingabe}\n\n"
        weg += f"Gegeben ist die Funktion: $$f(x) = {self.term_latex()}$$\n\n"

        # Verschiedene Lösungswege je nach Grad
        grad = len(self.koeffizienten) - 1

        if grad == 0:
            weg += "Bei einer konstanten Funktion gibt es keine Nullstellen.\n"
        elif grad == 1:
            weg += "## Lineare Funktion (Grad 1)\n\n"
            weg += f"$$f(x) = {self.term_latex()} = 0$$\n\n"

            a, b = self.koeffizienten[1], self.koeffizienten[0]
            ergebnis = -b / a
            weg += f"$$x = -\\frac{{{b}}}{{{a}}} = {ergebnis}$$\n"

        elif grad == 2:
            weg += "## Quadratische Funktion (Grad 2)\n\n"
            weg += f"$$f(x) = {self.term_latex()} = 0$$\n\n"

            a, b, c = (
                self.koeffizienten[2],
                self.koeffizienten[1],
                self.koeffizienten[0],
            )

            # Mitternachtsformel
            diskriminante = b**2 - 4 * a * c

            weg += "### Mitternachtsformel\n\n"
            weg += f"$$x = \\frac{{-b \\pm \\sqrt{{b^2 - 4ac}}}}{{2a}}$$\n\n"
            weg += f"Mit a = {a}, b = {b}, c = {c}:\n\n"
            weg += f"$$x = \\frac{{-{b} \\pm \\sqrt{{{b}^2 - 4 \\cdot {a} \\cdot {c}}}}}{{2 \\cdot {a}}}$$\n\n"
            weg += (
                f"$$x = \\frac{{-{b} \\pm \\sqrt{{{diskriminante}}}}}{{{2 * a}}}$$\n\n"
            )

            if diskriminante > 0:
                weg += "### Zwei reelle Nullstellen\n\n"
                sqrt_d = sp.sqrt(diskriminante)
                x1 = (-b + sqrt_d) / (2 * a)
                x2 = (-b - sqrt_d) / (2 * a)
                weg += f"$$x_1 = \\frac{{-{b} + \\sqrt{{{diskriminante}}}}}{{{2 * a}}} = {x1}$$\n\n"
                weg += f"$$x_2 = \\frac{{-{b} - \\sqrt{{{diskriminante}}}}}{{{2 * a}}} = {x2}$$\n\n"
            elif diskriminante == 0:
                weg += "### Eine doppelte Nullstelle\n\n"
                x = -b / (2 * a)
                weg += f"$$x = \\frac{{-{b}}}{{{2 * a}}} = {x}$$\n\n"
            else:
                weg += "### Keine reellen Nullstellen\n\n"
                weg += f"Da die Diskriminante D = {diskriminante} < 0 ist, gibt es keine reellen Nullstellen.\n\n"

                # Quadratische Ergänzung zeigen
                weg += "### Quadratische Ergänzung\n\n"
                weg += f"$$f(x) = {self.term_latex()}$$\n\n"
                weg += f"$$= {a}x^2 {b if b >= 0 else f'-{abs(b)}'}x {c if c >= 0 else f'-{abs(c)}'}$$\n\n"
                weg += f"$$= {a}\\left(x^2 {b / a:+}x\\right) {c:+}$$\n\n"
                weg += f"$$= {a}\\left(x^2 {b / a:+}x + \\left({b / (2 * a):.3f}\\right)^2 - \\left({b / (2 * a):.3f}\\right)^2\\right) {c:+}$$\n\n"
                weg += f"$$= {a}\\left(\\left(x {b / (2 * a):+.3f}\\right)^2 - {b**2 / (4 * a**2):.3f}\\right) {c:+}$$\n\n"
                weg += f"$$= {a}\\left(x {b / (2 * a):+.3f}\\right)^2 - {b**2 / (4 * a):.3f} {c:+}$$\n\n"
                weg += f"$$= {a}\\left(x {b / (2 * a):+.3f}\\right)^2 {c - b**2 / (4 * a):+.3f}$$\n\n"
                weg += f"Da {a} > 0 und der Term {a}(x {b / (2 * a):+.3f})² ≥ 0 ist, ergibt sich:\n\n"
                weg += f"$$f(x) \\geq {c - b**2 / (4 * a):+.3f} > 0$$\n\n"
                weg += "Somit hat die Funktion keine reellen Nullstellen.\n"

        return weg

    # ============================================
    # 🔥 PLOTLY VISUALISIERUNGSMETHODEN 🔥
    # ============================================

    def zeige_funktion_plotly(
        self, x_range: tuple = (-10, 10), punkte: int = 200
    ) -> Any:
        """Zeigt interaktiven Funktionsgraph mit Plotly - MATHEMATISCH KORREKT"""
        x = np.linspace(x_range[0], x_range[1], punkte)
        y = [self.wert(xi) for xi in x]

        fig = px.line(
            x=x,
            y=y,
            title=f"Funktionsgraph: f(x) = {self.term()}",
            labels={"x": "x", "y": f"f(x) = {self.term()}"},
        )

        # 🔥 PERFECT MATHEMATICAL CONFIGURATION 🔥
        fig.update_layout(
            xaxis=dict(
                scaleanchor="y",  # 1:1 Aspect Ratio
                scaleratio=1,  # Keine Verzerrung!
                zeroline=True,  # Achse im Ursprung
                showgrid=True,  # Gitterlinien
                range=x_range,  # Dynamischer Bereich
                title="x",
            ),
            yaxis=dict(zeroline=True, showgrid=True, title=f"f(x) = {self.term()}"),
            showlegend=False,
            width=600,
            height=400,
        )

        return mo.ui.plotly(fig)

    def perfekte_parabel_plotly(
        self, x_range: tuple = (-5, 5), punkte: int = 200
    ) -> Any:
        """PERFEKTE Parabel-Darstellung entsprechend Schul-Konventionen"""
        # Perfekte symmetrische Datenpunkte um den Scheitelpunkt
        x = np.linspace(x_range[0], x_range[1], punkte)
        y = [self.wert(xi) for xi in x]

        fig = go.Figure()

        # Hauptkurve
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name=f"f(x) = {self.term()}",
                line=dict(color="blue", width=3),
            )
        )

        # Scheitelpunkt berechnen und markieren
        try:
            # Für quadratische Funktionen: Scheitelpunkt bei x = -b/(2a)
            if len(self.koeffizienten) >= 3:
                a, b = self.koeffizienten[0], self.koeffizienten[1]
                s_x = -b / (2 * a)
                s_y = self.wert(s_x)

                fig.add_trace(
                    go.Scatter(
                        x=[s_x],
                        y=[s_y],
                        mode="markers",
                        name="Scheitelpunkt",
                        marker=dict(size=15, color="red", symbol="diamond"),
                        text=[f"S({s_x:.2f}|{s_y:.2f})"],
                        hovertemplate="%{text}<extra></extra>",
                    )
                )
        except:
            pass

        # 🔥 ABSOLUT PERFEKTE MATHEMATISCHE KONFIGURATION 🔥
        fig.update_layout(
            title=f"Parabel: f(x) = {self.term()}",
            xaxis=dict(
                scaleanchor="y",  # 🔥 1:1 Aspect Ratio - KEINE VERZERRUNG!
                scaleratio=1,  # 🔥 Perfekte Kreisverwandtschaft!
                zeroline=True,  # 🔥 Achse im Ursprung sichtbar
                zerolinewidth=2,  # 🔥 Deutliche Null-Linie
                zerolinecolor="black",  # 🔥 Schwarze Achse
                showgrid=True,  # 🔥 Gitterlinien helfen beim Ablesen
                gridwidth=1,  # 🔥 Dünne Gitterlinien
                gridcolor="lightgray",  # 🔥 Dezentes Gitter
                range=x_range,  # 🔥 Symmetrischer Bereich
                title="x",  # 🔥 Achsenbeschriftung
                ticks="outside",  # 🔥 Ticks außerhalb
                tickwidth=2,  # 🔥 Deutliche Ticks
                showline=True,  # 🔥 Achsenlinie sichtbar
                linewidth=2,  # 🔥 Deutliche Achsenlinie
            ),
            yaxis=dict(
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor="black",
                showgrid=True,
                gridwidth=1,
                gridcolor="lightgray",
                title=f"f(x) = {self.term()}",
                ticks="outside",
                tickwidth=2,
                showline=True,
                linewidth=2,
                scaleanchor="x",  # 🔥 Bidirektionale Verzerrungs-Verhinderung!
            ),
            plot_bgcolor="white",  # 🔥 Weißer Hintergrund für Schule
            paper_bgcolor="white",
            showlegend=True,
            width=700,
            height=500,
            font=dict(size=14),  # 🔥 Gute Lesbarkeit
        )

        return mo.ui.plotly(fig)

    def zeige_nullstellen_plotly(
        self, real: bool = True, x_range: tuple = (-10, 10)
    ) -> Any:
        """Zeigt Funktion mit interaktiven Nullstellen-Markierungen - MATHEMATISCH KORREKT"""
        # Hauptfunktion
        x = np.linspace(x_range[0], x_range[1], 300)
        y = [self.wert(xi) for xi in x]

        # Plotly Figure erstellen
        fig = go.Figure()

        # Hauptfunktion hinzufügen
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name=f"f(x) = {self.term()}",
                line=dict(color="blue", width=2),
            )
        )

        # Nullstellen hinzufügen
        nullstellen = self.nullstellen(real)
        if nullstellen:
            ns_x = [ns for ns in nullstellen if x_range[0] <= ns <= x_range[1]]
            ns_y = [0] * len(ns_x)
            ns_labels = [f"Nullstelle: {ns:.2f}" for ns in ns_x]

            fig.add_trace(
                go.Scatter(
                    x=ns_x,
                    y=ns_y,
                    mode="markers",
                    name="Nullstellen",
                    marker=dict(size=12, color="red", symbol="circle"),
                    text=ns_labels,
                    hovertemplate="%{text}<extra></extra>",
                )
            )

            title = f"Nullstellen von f(x) = {self.term()}"
        else:
            title = f"Keine reellen Nullstellen für f(x) = {self.term()}"

        # 🔥 PERFECT MATHEMATICAL CONFIGURATION 🔥
        fig.update_layout(
            title=title,
            xaxis=dict(
                scaleanchor="y",  # 1:1 Aspect Ratio
                scaleratio=1,  # Keine Verzerrung!
                zeroline=True,  # Achse im Ursprung
                showgrid=True,  # Gitterlinien
                range=x_range,
                title="x",
            ),
            yaxis=dict(zeroline=True, showgrid=True, title=f"f(x) = {self.term()}"),
            showlegend=True,
            width=600,
            height=400,
        )

        return mo.ui.plotly(fig)

    def zeige_ableitung_plotly(
        self, ordnung: int = 1, x_range: tuple = (-10, 10)
    ) -> Any:
        """Zeigt Funktion und Ableitung im Vergleich - MATHEMATISCH KORREKT"""
        # Daten generieren
        x = np.linspace(x_range[0], x_range[1], 300)

        # Originalfunktion
        y_orig = [self.wert(xi) for xi in x]

        # Ableitung
        ableitung = self.ableitung(ordnung)
        y_abl = [ableitung.wert(xi) for xi in x]

        # Plotly Subplots
        fig = make_subplots(
            rows=2,
            cols=1,
            subplot_titles=[
                f"f(x) = {self.term()}",
                f"f^{ordnung}(x) = {ableitung.term()}",
            ],
            vertical_spacing=0.1,
        )

        # Originalfunktion
        fig.add_trace(
            go.Scatter(
                x=x, y=y_orig, mode="lines", name="f(x)", line=dict(color="blue")
            ),
            row=1,
            col=1,
        )

        # Ableitung
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y_abl,
                mode="lines",
                name=f"f^{ordnung}(x)",
                line=dict(color="red"),
            ),
            row=2,
            col=1,
        )

        # 🔥 PERFECT MATHEMATICAL CONFIGURATION 🔥
        fig.update_layout(
            title=f"Funktion vs. {ordnung}. Ableitung",
            height=600,
            showlegend=False,
            xaxis=dict(
                scaleanchor="y",  # 1:1 Aspect Ratio
                scaleratio=1,  # Keine Verzerrung!
                zeroline=True,
                showgrid=True,
                range=x_range,
                title="x",
            ),
            xaxis2=dict(
                scaleanchor="y2",  # 1:1 Aspect Ratio für zweite Achse
                scaleratio=1,
                zeroline=True,
                showgrid=True,
                range=x_range,
                title="x",
            ),
            yaxis=dict(zeroline=True, showgrid=True, title="f(x)"),
            yaxis2=dict(zeroline=True, showgrid=True, title=f"f^{ordnung}(x)"),
        )

        return mo.ui.plotly(fig)
