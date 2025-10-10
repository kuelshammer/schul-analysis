"""
Erweiterte Fehlerklassen für das Schul-Analysis Framework.

Bietet spezifische Fehlerklassen für verschiedene Arten von mathematischen
und technischen Fehlern, die im Framework auftreten können.
"""

from typing import Any


class SchulAnalysisError(Exception):
    """Basisklasse für alle Schul-Analysis Fehler"""

    def __init__(
        self,
        message: str,
        *,
        user_message: str | None = None,
        context: dict[str, Any] | None = None,
        suggestion: str | None = None,
    ):
        """
        Args:
            message: Technische Fehlermeldung für Entwickler
            user_message: Schülerfreundliche Fehlermeldung
            context: Zusätzlicher Kontext zur Fehlerbehebung
            suggestion: Konkreter Lösungsvorschlag
        """
        super().__init__(message)
        self.user_message = user_message or message
        self.context = context or {}
        self.suggestion = suggestion

    def __str__(self) -> str:
        base_msg = super().__str__()
        if self.suggestion:
            return f"{base_msg}\n💡 Tipp: {self.suggestion}"
        return base_msg


# === Mathematische Fehler ===


class MathematischerDomainError(SchulAnalysisError):
    """Fehler bei mathematischen Domain-Verletzungen"""

    def __init__(self, message: str, domain: str = "", valid_range: str = ""):
        super().__init__(
            message,
            user_message=f"Diese Operation ist im mathematischen Bereich '{domain}' nicht erlaubt.",
            suggestion=f"Prüfe deine Eingabe. Gültiger Bereich: {valid_range}",
        )
        self.domain = domain
        self.valid_range = valid_range


class DivisionDurchNullError(MathematischerDomainError):
    """Spezifisch für Division durch Null"""

    def __init__(self, message: str = "Division durch Null"):
        super().__init__(message, domain="Division", valid_range="Nenner ≠ 0")
        self.user_message = "Du kannst nicht durch Null teilen! Prüfe den Nenner."


class UngueltigeFunktionError(MathematischerDomainError):
    """Fehler bei ungültigen Funktionsdefinitionen"""

    def __init__(self, function_type: str, problem: str):
        super().__init__(
            f"Ungültige {function_type}-Funktion: {problem}",
            domain="Funktionsdefinition",
            valid_range="Gültige mathematische Funktion",
        )


class ApproximationsError(SchulAnalysisError):
    """Fehler bei numerischen Approximationen"""

    def __init__(self, method: str, problem: str, precision: float = 1e-10):
        super().__init__(
            f"{method}-Approximation fehlgeschlagen: {problem}",
            user_message="Die numerische Berechnung konnte nicht mit der gewünschten Genauigkeit durchführt werden.",
            suggestion="Versuche eine einfachere Funktion oder prüfe die Eingabeparameter.",
        )
        self.method = method
        self.precision = precision


class KonvergenzError(ApproximationsError):
    """Spezifisch für Konvergenzprobleme"""

    def __init__(self, method: str, iterations: int):
        super().__init__(
            method,
            f"Keine Konvergenz nach {iterations} Iterationen",
            suggestion="Die Funktion konvergiert nicht. Prüfe, ob der Grenzwert existiert.",
        )
        self.iterations = iterations


# === Eingabe- und Syntaxfehler ===


class EingabeSyntaxError(SchulAnalysisError):
    """Fehler bei ungültiger Eingabesyntax"""

    def __init__(self, eingabe: str, expected_format: str):
        super().__init__(
            f"Ungültige Syntax: '{eingabe}'",
            user_message=f"Die Eingabe '{eingabe}' hat nicht das richtige Format.",
            suggestion=f"Erwartetes Format: {expected_format}",
        )
        self.eingabe = eingabe
        self.expected_format = expected_format


class UngueltigerAusdruckError(SchulAnalysisError):
    """Fehler bei ungültigen mathematischen Ausdrücken"""

    def __init__(self, ausdruck: str, grund: str):
        super().__init__(
            f"Ungültiger Ausdruck '{ausdruck}': {grund}",
            user_message=f"'{ausdruck}' ist kein gültiger mathematischer Ausdruck.",
            suggestion="Verwende gültige mathematische Notation (z.B. x^2+3x-2)",
        )


# === Sicherheitsfehler ===


class SicherheitsError(SchulAnalysisError):
    """Fehler bei Sicherheitsverletzungen"""

    def __init__(self, problem: str, ausdruck: str):
        super().__init__(
            f"Sicherheitsverletzung: {problem}",
            user_message="Dieser Ausdruck ist aus Sicherheitsgründen nicht erlaubt.",
            suggestion="Verwende nur mathematische Ausdrücke ohne gefährliche Befehle.",
        )
        self.problem = problem
        self.ausdruck = ausdruck


class KomplexitaetsError(SchulAnalysisError):
    """Fehler bei zu komplexen Berechnungen"""

    def __init__(self, operation: str, complexity: int, max_allowed: int):
        super().__init__(
            f"Operation '{operation}' zu komplex: {complexity} > {max_allowed}",
            user_message="Diese Berechnung ist zu komplex für das System.",
            suggestion="Vereinfache die Funktion oder teile sie in kleinere Schritte auf.",
        )
        self.operation = operation
        self.complexity = complexity
        self.max_allowed = max_allowed


# === Visualisierungsfehler ===


class VisualisierungsError(SchulAnalysisError):
    """Fehler bei der Erstellung von Visualisierungen"""

    def __init__(self, plot_type: str, problem: str):
        super().__init__(
            f"{plot_type}-Visualisierung fehlgeschlagen: {problem}",
            user_message="Das Diagramm konnte nicht erstellt werden.",
            suggestion="Prüfe die Funktionseingabe und versuche einen kleineren Wertebereich.",
        )
        self.plot_type = plot_type


class DarstellungsError(SchulAnalysisError):
    """Fehler bei der Darstellung von Funktionen"""

    def __init__(self, function_type: str, problem: str):
        super().__init__(
            f"Darstellungsfehler bei {function_type}: {problem}",
            user_message="Die Funktion kann in diesem Bereich nicht korrekt dargestellt werden.",
            suggestion="Wähle einen anderen Wertebereich oder prüfe auf Polstellen.",
        )


# === Konfigurationsfehler ===


class KonfigurationsError(SchulAnalysisError):
    """Fehler bei der Konfiguration"""

    def __init__(self, parameter: str, value: Any, expected_type: type):
        super().__init__(
            f"Ungültige Konfiguration: {parameter}={value} (erwartet: {expected_type.__name__})",
            user_message="Die Einstellung ist ungültig.",
            suggestion=f"Der Parameter '{parameter}' muss vom Typ {expected_type.__name__} sein.",
        )
        self.parameter = parameter
        self.value = value
        self.expected_type = expected_type


# === Nullstellen-Berechnungsfehler ===


class NullstellenBerechnungsFehler(SchulAnalysisError):
    """Basisklasse für Fehler bei der Nullstellenberechnung"""

    def __init__(self, message: str, funktion: str = "", ursache: str = ""):
        super().__init__(
            message,
            user_message=f"Fehler bei der Berechnung der Nullstellen von f(x) = {funktion}",
            suggestion=ursache
            or "Prüfe die Funktionseingabe und verwende gültige mathematische Ausdrücke.",
        )
        self.funktion = funktion
        self.ursache = ursache


class PolynomLoesungsFehler(NullstellenBerechnungsFehler):
    """Fehler bei der Lösung von Polynom-Gleichungen"""

    def __init__(self, polynom: str, grad: int, ursache: str = ""):
        super().__init__(
            f"Polynom-Lösung fehlgeschlagen: {polynom} (Grad {grad})",
            funktion=polynom,
            ursache=ursache
            or "Das Polynom könnte keine analytische Lösung haben oder zu komplex sein.",
        )
        self.polynom = polynom
        self.grad = grad


class GleichungsLoesungsFehler(NullstellenBerechnungsFehler):
    """Fehler bei der Lösung allgemeiner Gleichungen"""

    def __init__(self, gleichung: str, ursache: str = ""):
        super().__init__(
            f"Gleichung konnte nicht gelöst werden: {gleichung}",
            funktion=gleichung,
            ursache=ursache
            or "Die Gleichung ist zu komplex oder hat keine geschlossene Lösung.",
        )
        self.gleichung = gleichung


class TrigonometrischeLoesungsFehler(NullstellenBerechnungsFehler):
    """Fehler bei der Lösung trigonometrischer Gleichungen"""

    def __init__(self, gleichung: str, ursache: str = ""):
        super().__init__(
            f"Trigonometrische Gleichung konnte nicht gelöst werden: {gleichung}",
            funktion=gleichung,
            ursache=ursache
            or "Die trigonometrische Gleichung hat keine einfache Lösung.",
        )
        self.gleichung = gleichung


class ApproximationsFehler(NullstellenBerechnungsFehler):
    """Fehler bei numerischer Approximation von Nullstellen"""

    def __init__(self, funktion: str, ursache: str = ""):
        super().__init__(
            f"Numerische Approximation fehlgeschlagen: {funktion}",
            funktion=funktion,
            ursache=ursache
            or "Die Funktion hat keine numerisch approximierbaren Nullstellen.",
        )
        self.funktion = funktion


# === Utility-Funktionen ===


def handle_schul_analysis_error(error: Exception) -> str:
    """
    Wandelt jede Exception in eine benutzerfreundliche Fehlermeldung um

    Args:
        error: Die aufgetretene Exception

    Returns:
        Benutzerfreundliche Fehlermeldung
    """
    if isinstance(error, SchulAnalysisError):
        return error.user_message
    elif isinstance(error, ZeroDivisionError):
        return "Division durch Null ist nicht erlaubt!"
    elif isinstance(error, ValueError):
        return f"Ungültiger Wert: {str(error)}"
    elif isinstance(error, TypeError):
        return f"Typfehler: {str(error)}"
    else:
        return f"Ein unerwarteter Fehler ist aufgetreten: {str(error)}"
