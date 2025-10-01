"""
Analyse von SymPy-Faktorisierungen zur Generierung menschlich verständlicher Lösungswege.
"""

import sympy as sp
from typing import List, Tuple, Dict, Any
from src.schul_analysis.ganzrationale import GanzrationaleFunktion


def analysiere_sympy_loesung(funktion: GanzrationaleFunktion) -> Dict[str, Any]:
    """
    Analysiert SymPy's Lösung und extrahiert menschlich nachvollziehbare Muster.
    """
    term = funktion.term_sympy
    grad = len(funktion.koeffizienten) - 1

    analyse = {
        "grad": grad,
        "term": term,
        "sympy_factor": None,
        "sympy_roots": None,
        "muster": [],
        "loesungswege": [],
        "empfohlener_weg": None,
    }

    # 1. SymPy's Faktorisierung und Nullstellen abfragen
    try:
        analyse["sympy_factor"] = sp.factor(term)
        analyse["sympy_roots"] = sp.roots(term)
    except:
        pass

    # 2. Muster erkennen
    muster = []

    # Muster 1: Differenz von Quadraten
    if _ist_differenz_von_quadraten(term):
        muster.append("differenz_von_quadraten")

    # Muster 2: Perfekte Potenzen
    if _ist_perfekte_potenz(analyse["sympy_factor"]):
        muster.append("perfekte_potenz")

    # Muster 3: Symmetrische Nullstellen
    if _ist_symmetrisch(analyse["sympy_roots"]):
        muster.append("symmetrisch")

    # Muster 4: Rationale Nullstellen
    if _hat_rationale_nullstellen(analyse["sympy_roots"]):
        muster.append("rationale_nullstellen")

    # Muster 5: Linearfaktoren
    if _ist_linearfaktorisiert(analyse["sympy_factor"]):
        muster.append("linearfaktoren")

    analyse["muster"] = muster

    # 3. Lösungswege generieren
    wege = []

    if "differenz_von_quadraten" in muster:
        wege.append(_generiere_differenz_quadrate_weg(term, analyse))

    if "rationale_nullstellen" in muster:
        wege.append(_generiere_rationale_nullstellen_weg(funktion, analyse))

    if "perfekte_potenz" in muster:
        wege.append(_generiere_perfekte_potenz_weg(term, analyse))

    if "linearfaktoren" in muster:
        wege.append(_generiere_linearfaktoren_weg(term, analyse))

    analyse["loesungswege"] = wege

    # 4. Empfohlener Weg auswählen
    analyse["empfohlener_weg"] = _waehle_empfohlenen_weg(wege, muster)

    return analyse


def _ist_differenz_von_quadraten(term: sp.Basic) -> bool:
    """Prüft, ob der Term eine Differenz von Quadraten ist."""
    if term.is_polynomial():
        # Versuche, Term als a² - b² zu erkennen
        try:
            faktorisiert = sp.factor(term)
            if isinstance(faktorisiert, sp.Mul):
                faktoren = sp.Mul.make_args(faktorisiert)
                if len(faktoren) == 2:
                    f1, f2 = faktoren
                    if (
                        f1.is_Add
                        and len(f1.args) == 2
                        and f2.is_Add
                        and len(f2.args) == 2
                    ):
                        # Prüfe ob (a+b)(a-b) Form
                        return True
        except:
            pass
    return False


def _ist_perfekte_potenz(faktorisiert: sp.Basic) -> bool:
    """Prüft, ob es sich um eine perfekte Potenz handelt."""
    if isinstance(faktorisiert, sp.Pow):
        return True
    return False


def _ist_symmetrisch(roots: dict) -> bool:
    """Prüft, ob Nullstellen symmetrisch sind."""
    if not roots:
        return False

    nullstellen = list(roots.keys())
    # Prüfe ob für jede Nullstelle a auch -a existiert
    for nullstelle in nullstellen:
        if -nullstelle not in nullstellen:
            return False
    return True


def _hat_rationale_nullstellen(roots: dict) -> bool:
    """Prüft, ob rationale Nullstellen vorhanden sind."""
    if not roots:
        return False

    for nullstelle in roots.keys():
        if nullstelle.is_rational:
            return True
    return False


def _ist_linearfaktorisiert(faktorisiert: sp.Basic) -> bool:
    """Prüft, ob vollständig in Linearfaktoren zerlegt."""
    if isinstance(faktorisiert, sp.Mul):
        faktoren = sp.Mul.make_args(faktorisiert)
        for faktor in faktoren:
            if not (
                faktor.is_Add
                and len(faktor.args) == 2
                and any(
                    arg == faktor.variables[0]
                    for arg in faktor.args
                    if hasattr(arg, "variables")
                )
            ):
                return False
        return True
    return False


def _generiere_differenz_quadrate_weg(term: sp.Basic, analyse: dict) -> dict:
    """Generiert Lösungsweg für Differenz von Quadraten."""
    return {
        "name": "Differenz von Quadraten",
        "strategie": "a² - b² = (a+b)(a-b)",
        "schwierigkeit": "einfach",
        "schritte": [
            "Erkenne die Form a² - b²",
            "Wende die Formel (a+b)(a-b) an",
            "Setze jeden Faktor gleich null",
        ],
    }


def _generiere_rationale_nullstellen_weg(
    funktion: GanzrationaleFunktion, analyse: dict
) -> dict:
    """Generiert Lösungsweg mit Rational Root Theorem."""
    return {
        "name": "Rational Root Theorem",
        "strategie": "p/q mit p|a₀, q|aₙ",
        "schwierigkeit": "mittel",
        "schritte": [
            "Finde Teiler des absoluten Glieds a₀",
            "Finde Teiler des Leitkoeffizienten aₙ",
            "Teste mögliche rationale Nullstellen p/q",
            "Spalte gefundene Linearfaktoren ab",
        ],
    }


def _generiere_perfekte_potenz_weg(term: sp.Basic, analyse: dict) -> dict:
    """Generiert Lösungsweg für perfekte Potenzen."""
    return {
        "name": "Perfekte Potenz",
        "strategie": "(x-a)ⁿ = 0 ⇒ x = a",
        "schwierigkeit": "einfach",
        "schritte": [
            "Erkenne die Form (x-a)ⁿ",
            "Die Nullstelle ist x = a mit Vielfachheit n",
        ],
    }


def _generiere_linearfaktoren_weg(term: sp.Basic, analyse: dict) -> dict:
    """Generiert Lösungsweg für Linearfaktoren."""
    return {
        "name": "Linearfaktoren",
        "strategie": "Produkt gleich null setzen",
        "schwierigkeit": "einfach",
        "schritte": [
            "Setze jeden Linearfaktor gleich null",
            "Löse die einfachen Gleichungen",
        ],
    }


def _waehle_empfohlenen_weg(wege: List[dict], muster: List[str]) -> str:
    """Wählt den empfohlenen Lösungswege basierend auf Schwierigkeit."""
    # Priorität: einfach → mittel → komplex
    schwierigkeit_prio = {"einfach": 1, "mittel": 2, "komplex": 3}

    if not wege:
        return "Allgemeine Lösung mit SymPy"

    # Wähle den einfachsten Weg
    einfachster = min(wege, key=lambda w: schwierigkeit_prio.get(w["schwierigkeit"], 3))
    return einfachster["name"]


if __name__ == "__main__":
    # Teste die Analyse
    test_cases = [
        "x^3-6x^2+11x-6",  # (x-1)(x-2)(x-3)
        "x^4-5x^2+4",  # (x²-1)(x²-4) - symmetrisch
        "x^2-4",  # Differenz von Quadraten
        "(x-2)^3",  # Perfekte Potenz
    ]

    for case in test_cases:
        print(f"\n=== {case} ===")
        f = GanzrationaleFunktion(case)
        analyse = analysiere_sympy_loesung(f)

        print(f"Muster: {analyse['muster']}")
        print(f"Empfohlener Weg: {analyse['empfohlener_weg']}")

        for weg in analyse["loesungswege"]:
            print(f"- {weg['name']} ({weg['schwierigkeit']})")
            print(f"  Strategie: {weg['strategie']}")
