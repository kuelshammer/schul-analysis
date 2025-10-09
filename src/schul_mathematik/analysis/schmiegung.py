"""
Schmiegkurven-Module für das Schul-Analysis Framework

Dieses Modul enthält Funktionen zur Erzeugung und Analyse von Schmiegkurven,
die durch Punkte mit optionalen Tangenten- oder Normalenbedingungen definiert sind.
"""

from .funktion import Funktion
from .schmiegkurven import Schmiegkurve


# Import Graph from parent module (it's still in __init__.py)
def _get_graph_function():
    """Helper to import Graph function from parent module"""
    from . import Graph

    return Graph


# ====================
# Schmiegkurven-Funktionen
# ====================


def Schmiegparabel(punkt1, punkt2, punkt3, tangente1=None, tangente3=None):
    """Erzeugt eine Schmiegparabel durch 3 Punkte mit optionalen Tangenten

    Args:
        punkt1, punkt2, punkt3: Drei (x, y) Punkte durch die die Parabel verläuft
        tangente1: Optionale Tangentensteigung an punkt1
        tangente3: Optionale Tangentensteigung an punkt3

    Returns:
        Schmiegkurve: Schmiegparabel als Schmiegkurven-Objekt

    Beispiele:
        >>> # Parabel durch drei Punkte
        >>> p1, p2, p3 = (0, 1), (1, 4), (2, 9)  # auf y = x² + 1
        >>> parabel = Schmiegparabel(p1, p2, p3)
        >>> print(parabel.term)

        >>> # Parabel mit Tangentenbedingungen
        >>> parabel_mit_t = Schmiegparabel((0, 0), (1, 1), (2, 0), tangente1=0)
        >>> print(parabel_mit_t.term)
    """
    return Schmiegkurve.schmiegparabel(punkt1, punkt2, punkt3, tangente1, tangente3)


def Schmiegkegel(punkte, tangenten=None, grad=3):
    """Erzeugt einen Schmiegkegel (kubisches Polynom) durch bis zu 4 Punkte

    Args:
        punkte: Liste von (x, y) Punkten (maximal 4)
        tangenten: Optionale Liste von Tangentensteigungen
        grad: Grad des Polynoms (Standard 3)

    Returns:
        Schmiegkurve: Schmiegkegel als Schmiegkurven-Objekt

    Beispiele:
        >>> # Kubische Kurve durch 4 Punkte
        >>> punkte = [(0, 0), (1, 1), (2, 8), (3, 27)]
        >>> kegel = Schmiegkegel(punkte)
        >>> print(kegel.term)

        >>> # Mit Tangentenbedingung
        >>> kegel_mit_t = Schmiegkegel([(0, 0), (2, 4)], tangenten=[1])
        >>> print(kegel_mit_t.term)
    """
    return Schmiegkurve.schmiegkegel(punkte, tangenten, grad)


def Schmieggerade(punkt, tangente):
    """Erzeugt eine Schmieggerade durch einen Punkt mit gegebener Tangente

    Args:
        punkt: (x, y) Punkt durch den die Gerade verläuft
        tangente: Steigung der Geraden

    Returns:
        Schmiegkurve: Schmieggerade als Schmiegkurven-Objekt

    Beispiele:
        >>> # Gerade durch (0, 0) mit Steigung 2
        >>> gerade = Schmieggerade((0, 0), 2)
        >>> print(gerade.term)  # Erwartet: 2x
    """
    return Schmiegkurve.schmieggerade(punkt, tangente)


def HermiteInterpolation(punkte, werte, ableitungen):
    """Erzeugt eine Schmiegkurve mittels Hermite-Interpolation

    Args:
        punkte: Liste der Stützstellen x_i
        werte: Liste der Funktionswerte f(x_i)
        ableitungen: Liste der Ableitungswerte f'(x_i)

    Returns:
        Schmiegkurve: Hermite-Interpolationspolynom

    Beispiele:
        >>> # Hermite-Interpolation mit Werten und Ableitungen
        >>> x_vals = [0, 1]
        >>> y_vals = [0, 1]
        >>> y_derivs = [0, 0]
        >>> hermite = HermiteInterpolation(x_vals, y_vals, y_derivs)
        >>> print(hermite.term)
    """
    return Schmiegkurve.hermite_interpolation(punkte, werte, ableitungen)


def SchmiegkurveAllgemein(punkte, tangenten=None, normalen=None, grad=None):
    """Erzeugt eine allgemeine Schmiegkurve mit beliebigen Bedingungen

    Args:
        punkte: Liste von (x, y) Punkten
        tangenten: Optionale Liste von Tangentensteigungen
        normalen: Optionale Liste von Normalensteigungen
        grad: Gewünschter Grad des Polynoms

    Returns:
        Schmiegkurve: Allgemeine Schmiegkurve

    Beispiele:
        >>> # Allgemeine Schmiegkurve durch 2 Punkte mit Normalen
        >>> kurve = SchmiegkurveAllgemein(
        ...     [(0, 0), (2, 4)],
        ...     normalen=[-1, -0.5]  # Senkrechte zu y = x und y = 0.5x
        ... )
        >>> print(kurve.term)
    """
    return Schmiegkurve(punkte, tangenten, normalen, grad)


# ====================
# Parametrische Funktionen
# ====================


def Graph_parametrisiert(parametrische_funktion, **parameter_werte):
    """Erzeugt mehrere Graphen für eine parametrische Funktion mit verschiedenen Parameterwerten

    Args:
        parametrische_funktion: ParametrischeFunktion-Objekt
        **parameter_werte: Dictionary mit Parameter-Namen und Wertelisten
                         z.B. a=[-2, -1, 0, 1, 2] für Parameter 'a'

    Returns:
        plotly.graph_objects.Figure: Plotly-Figur mit allen Funktionen

    Beispiele:
        >>> # Parametrische Funktion f_a(x) = a*x^2 + x
        >>> x = Variable("x")
        >>> a = Parameter("a")
        >>> f_param = ParametrischeFunktion([a, 1, 0], [x])  # a*x^2 + x

        # Erzeuge Graphen für verschiedene a-Werte
        >>> fig = Graph_parametrisiert(f_param, a=[-2, -1, 0, 1, 2])

        # Mit Marimo anzeigen:
        >>> mo.ui.plotly(fig)
    """
    if not isinstance(parametrische_funktion, Funktion):
        raise TypeError("Erste Argument muss eine Funktion sein")

    if not parameter_werte:
        raise ValueError("Mindestens ein Parameter mit Werten muss angegeben werden")

    # Sammle alle konkreten Funktionen
    konkrete_funktionen = []

    for param_name, werte in parameter_werte.items():
        for _i, wert in enumerate(werte):
            # Erzeuge konkrete Funktion mit diesem Parameterwert
            konkrete_funktion = parametrische_funktion.mit_wert(**{param_name: wert})

            # Füge Parameter-Info zum Funktionsnamen hinzu
            if hasattr(konkrete_funktion, "_parameter_info"):
                konkrete_funktion._parameter_info = f"{param_name}={wert}"
            else:
                konkrete_funktion._parameter_info = f"{param_name}={wert}"

            konkrete_funktionen.append(konkrete_funktion)

    # Verwende die bestehende Graph-Funktion für mehrere Funktionen
    Graph = _get_graph_function()
    fig = Graph(*konkrete_funktionen)

    # Passe den Titel an, um die Parametrisierung zu zeigen
    param_info = ", ".join(
        [f"{k}=[{min(v)}, {max(v)}]" for k, v in parameter_werte.items()]
    )
    fig.update_layout(
        title=f"<b>{parametrische_funktion.term()}</b><br>Parameter: {param_info}"
    )

    return fig
