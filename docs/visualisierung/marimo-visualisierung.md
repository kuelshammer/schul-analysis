# Marimo Visualisierung mit Plotly und Altair

## Übersicht

Dieses Dokument beschreibt die Implementierung von interaktiven Visualisierungsmethoden für das Schul-Analysis Framework mit Fokus auf mathematisch korrekte Darstellung in Marimo-Notebooks.

## 🏆 Paketstrategie: Plotly für Mathematik, Altair für Statistik

### **Hauptvisualisierung: Plotly**

- **Vorteile**: Perfekte mathematische Korrektheit, Aspect Ratio Control, Schul-Konventionen
- **Interaktivität**: Zoom, pan, 3D-Rotation, volle Achsenkontrolle
- **Integration**: `mo.ui.plotly()` für exzellente Marimo-Integration
- **Educational**: Verzerrungsfreie Darstellung von Parabeln und Funktionen

### **Sekundärvisualisierung: Altair**

- **Vorteile**: Gut für statistische Diagramme, Data Selection
- **Einschränkung**: Kein Aspect Ratio Control, verzerrte mathematische Darstellung
- **Integration**: `mo.ui.altair_chart()` für gute Marimo-Integration
- **Use Case**: Statistische Analysen, nicht für präzise Mathematik

### **Vermeiden: Matplotlib**

- **Nachteile**: Nicht reaktiv, keine Aspect Ratio Kontrolle
- **Einsatz**: Nur für statische Exporte

## Methoden-Implementierung

### 1. Grundlegende Visualisierungsmethoden

```python
import marimo as mo
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class GanzrationaleFunktion:
    def zeige_funktion_plotly(self, x_range: tuple = (-10, 10), punkte: int = 200) -> mo.UI:
        """Zeigt interaktiven Funktionsgraph mit Plotly - MATHEMATISCH KORREKT"""
        x = np.linspace(x_range[0], x_range[1], punkte)
        y = [self.wert(xi) for xi in x]

        fig = px.line(
            x=x, y=y,
            title=f'Funktionsgraph: f(x) = {self.term()}',
            labels={'x': 'x', 'y': f'f(x) = {self.term()}'}
        )

        # 🔥 PERFECT MATHEMATICAL CONFIGURATION 🔥
        fig.update_layout(
            xaxis=dict(
                scaleanchor="y",     # 1:1 Aspect Ratio
                scaleratio=1,        # Keine Verzerrung!
                zeroline=True,       # Achse im Ursprung
                showgrid=True,       # Gitterlinien
                range=x_range,       # Dynamischer Bereich
                title='x'
            ),
            yaxis=dict(
                zeroline=True,
                showgrid=True,
                title=f'f(x) = {self.term()}'
            ),
            showlegend=False,
            width=600,
            height=400
        )

        return mo.ui.plotly(fig)

    def zeige_funktion_altair(self, x_range: tuple = (-10, 10), punkte: int = 200) -> mo.UI:
        """Zeigt interaktiven Funktionsgraph mit Altair - für statistische Zwecke"""
        # Daten generieren
        x = np.linspace(x_range[0], x_range[1], punkte)
        y = [self.wert(xi) for xi in x]

        # DataFrame für Altair erstellen
        df = pd.DataFrame({'x': x, 'y': y})

        # Altair Chart erstellen
        chart = alt.Chart(df).mark_line().encode(
            x=alt.X('x', title='x', scale=alt.Scale(domain=x_range)),
            y=alt.Y('y', title=f'f(x) = {self.term_latex()}'),
            tooltip=['x', 'y']
        ).properties(
            title=f'Funktionsgraph: f(x) = {self.term_latex()}',
            width=600,
            height=400
        ).interactive()

        return mo.ui.altair_chart(chart)
```

### 2. Nullstellen-Visualisierung

```python
def zeige_nullstellen_plotly(self, real: bool = True, x_range: tuple = (-10, 10)) -> mo.UI:
    """Zeigt Funktion mit interaktiven Nullstellen-Markierungen - MATHEMATISCH KORREKT"""
    # Hauptfunktion
    x = np.linspace(x_range[0], x_range[1], 300)
    y = [self.wert(xi) for xi in x]

    # Plotly Figure erstellen
    fig = go.Figure()

    # Hauptfunktion hinzufügen
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        name=f'f(x) = {self.term()}',
        line=dict(color='blue', width=2)
    ))

    # Nullstellen hinzufügen
    nullstellen = self.nullstellen(real)
    if nullstellen:
        ns_x = [ns for ns in nullstellen if x_range[0] <= ns <= x_range[1]]
        ns_y = [0] * len(ns_x)
        ns_labels = [f'Nullstelle: {ns:.2f}' for ns in ns_x]

        fig.add_trace(go.Scatter(
            x=ns_x, y=ns_y,
            mode='markers',
            name='Nullstellen',
            marker=dict(size=12, color='red', symbol='circle'),
            text=ns_labels,
            hovertemplate='%{text}<extra></extra>'
        ))

        title = f'Nullstellen von f(x) = {self.term()}'
    else:
        title = f'Keine reellen Nullstellen für f(x) = {self.term()}'

    # 🔥 PERFECT MATHEMATICAL CONFIGURATION 🔥
    fig.update_layout(
        title=title,
        xaxis=dict(
            scaleanchor="y",     # 1:1 Aspect Ratio
            scaleratio=1,        # Keine Verzerrung!
            zeroline=True,       # Achse im Ursprung
            showgrid=True,       # Gitterlinien
            range=x_range,
            title='x'
        ),
        yaxis=dict(
            zeroline=True,
            showgrid=True,
            title=f'f(x) = {self.term()}'
        ),
        showlegend=True,
        width=600,
        height=400
    )

    return mo.ui.plotly(fig)

def zeige_nullstellen_altair(self, real: bool = True, x_range: tuple = (-10, 10)) -> mo.UI:
    """Zeigt Funktion mit interaktiven Nullstellen-Markierungen - für statistische Zwecke"""
    # Hauptfunktion
    x = np.linspace(x_range[0], x_range[1], 300)
    y = [self.wert(xi) for xi in x]

    df = pd.DataFrame({'x': x, 'y': y})

    # Basis-Chart
    base = alt.Chart(df).mark_line().encode(
        x=alt.X('x', title='x', scale=alt.Scale(domain=x_range)),
        y=alt.Y('y', title=f'f(x) = {self.term_latex()}')
    )

    # Nullstellen hinzufügen
    nullstellen = self.nullstellen(real)
    if nullstellen:
        ns_data = pd.DataFrame({
            'x': nullstellen,
            'y': [0] * len(nullstellen),
            'label': [f'Nullstelle: {ns:.2f}' for ns in nullstellen]
        })

        ns_points = alt.Chart(ns_data).mark_circle(
            size=100, color='red', fill='red'
        ).encode(
            x='x', y='y',
            tooltip=['x', 'label']
        )

        chart = (base + ns_points).properties(
            title=f'Nullstellen von f(x) = {self.term_latex()}',
            width=600,
            height=400
        ).interactive()
    else:
        chart = base.properties(
            title=f'Keine reellen Nullstellen für f(x) = {self.term_latex()}',
            width=600,
            height=400
        ).interactive()

    return mo.ui.altair_chart(chart)
```

### 3. Ableitungsvergleich

```python
def zeige_ableitung_plotly(self, ordnung: int = 1, x_range: tuple = (-10, 10)) -> mo.UI:
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
        rows=2, cols=1,
        subplot_titles=[f'f(x) = {self.term()}', f"f^{ordnung}(x) = {ableitung.term()}"],
        vertical_spacing=0.1
    )

    # Originalfunktion
    fig.add_trace(
        go.Scatter(x=x, y=y_orig, mode='lines', name='f(x)', line=dict(color='blue')),
        row=1, col=1
    )

    # Ableitung
    fig.add_trace(
        go.Scatter(x=x, y=y_abl, mode='lines', name=f'f^{ordnung}(x)', line=dict(color='red')),
        row=2, col=1
    )

    # 🔥 PERFECT MATHEMATICAL CONFIGURATION 🔥
    fig.update_layout(
        title=f'Funktion vs. {ordnung}. Ableitung',
        height=600,
        showlegend=False,
        xaxis=dict(
            scaleanchor="y",     # 1:1 Aspect Ratio
            scaleratio=1,        # Keine Verzerrung!
            zeroline=True,
            showgrid=True,
            range=x_range,
            title='x'
        ),
        xaxis2=dict(
            scaleanchor="y2",    # 1:1 Aspect Ratio für zweite Achse
            scaleratio=1,
            zeroline=True,
            showgrid=True,
            range=x_range,
            title='x'
        ),
        yaxis=dict(
            zeroline=True,
            showgrid=True,
            title='f(x)'
        ),
        yaxis2=dict(
            zeroline=True,
            showgrid=True,
            title=f'f^{ordnung}(x)'
        )
    )

    return mo.ui.plotly(fig)

def zeige_ableitung_altair(self, ordnung: int = 1, x_range: tuple = (-10, 10)) -> mo.UI:
    """Zeigt Funktion und Ableitung im Vergleich - für statistische Zwecke"""
    # Daten generieren
    x = np.linspace(x_range[0], x_range[1], 300)

    # Originalfunktion
    y_orig = [self.wert(xi) for xi in x]

    # Ableitung
    ableitung = self.ableitung(ordnung)
    y_abl = [ableitung.wert(xi) for xi in x]

    # DataFrame für Altair
    df = pd.DataFrame({
        'x': x,
        'f(x)': y_orig,
        f'f^({ordnung})(x)': y_abl
    })

    # Melt für facetten
    df_melted = df.melt('x', var_name='Funktion', value_name='y')

    # Chart mit Facetten
    chart = alt.Chart(df_melted).mark_line().encode(
        x=alt.X('x', title='x', scale=alt.Scale(domain=x_range)),
        y=alt.Y('y', title='y'),
        color='Funktion',
        tooltip=['x', 'Funktion', 'y']
    ).properties(
        title=f'Funktion vs. {ordnung}. Ableitung',
        width=300,
        height=300
    ).facet(
        column='Funktion'
    ).resolve_scale(y='independent')

    return mo.ui.altair_chart(chart)
```

### 4. Extremstellen-Visualisierung

```python
def zeige_extremstellen_altair(self, x_range: tuple = (-10, 10)) -> mo.UI:
    """Zeigt Funktion mit interaktiven Extremstellen-Markierungen"""
    # Daten generieren
    x = np.linspace(x_range[0], x_range[1], 300)
    y = [self.wert(xi) for xi in x]

    df = pd.DataFrame({'x': x, 'y': y})

    # Basis-Chart
    base = alt.Chart(df).mark_line().encode(
        x=alt.X('x', title='x', scale=alt.Scale(domain=x_range)),
        y=alt.Y('y', title=f'f(x) = {self.term_latex()}')
    )

    # Extremstellen hinzufügen
    extremstellen = self.extremstellen()
    if extremstellen:
        ext_data = pd.DataFrame({
            'x': [ext[0] for ext in extremstellen],
            'y': [self.wert(ext[0]) for ext in extremstellen],
            'art': [ext[1] for ext in extremstellen],
            'color': ['red' if ext[1] == 'Maximum' else 'blue' for ext in extremstellen]
        })

        ext_points = alt.Chart(ext_data).mark_circle(
            size=120, fill='red'
        ).encode(
            x='x', y='y',
            color=alt.Color('art', scale=alt.Scale(domain=['Maximum', 'Minimum'], range=['red', 'blue'])),
            tooltip=['x', 'art', 'y']
        )

        chart = (base + ext_points).properties(
            title=f'Extremstellen von f(x) = {self.term_latex()}',
            width=600,
            height=400
        ).interactive()
    else:
        chart = base.properties(
            title=f'Keine Extremstellen für f(x) = {self.term_latex()}',
            width=600,
            height=400
        ).interactive()

    return mo.ui.altair_chart(chart)
```

### 5. Reaktive Parameter-Steuerung

```python
def interaktive_funktion_altair(self) -> mo.UI:
    """Vollständig interaktive Funktion mit Parameter-Slidern"""
    # Sliders für Koeffizienten
    a_slider = mo.ui.slider(-5, 5, value=self.koeffizienten[0], step=0.1, label="a")
    b_slider = mo.ui.slider(-5, 5, value=self.koeffizienten[1] if len(self.koeffizienten) > 1 else 0, step=0.1, label="b")
    c_slider = mo.ui.slider(-5, 5, value=self.koeffizienten[2] if len(self.koeffizienten) > 2 else 0, step=0.1, label="c")

    # Bereichsauswahl
    x_min = mo.ui.slider(-20, 0, value=-10, step=1, label="x_min")
    x_max = mo.ui.slider(0, 20, value=10, step=1, label="x_max")

    @mo.cell
    def funktion_mit_parametern():
        # Neue Funktion mit Slider-Werten erstellen
        if len(self.koeffizienten) >= 3:
            neue_funktion = GanzrationaleFunktion([a_slider.value, b_slider.value, c_slider.value])
        elif len(self.koeffizienten) == 2:
            neue_funktion = GanzrationaleFunktion([a_slider.value, b_slider.value])
        else:
            neue_funktion = GanzrationaleFunktion([a_slider.value])

        # Visualisierung
        return neue_funktion.zeige_funktion_altair(x_range=(x_min.value, x_max.value))

    return mo.vstack([
        mo.md("## Interaktive Funktionsanalyse"),
        mo.hstack([a_slider, b_slider, c_slider]),
        mo.hstack([x_min, x_max]),
        funktion_mit_parametern
    ])
```

## Marimo-Integration Features

### Data Selection

Altair-Charts unterstützen **Data Selection** - wenn Schüler Punkte anklicken, werden die entsprechenden Daten gefiltert:

```python
def interaktive_nullstellen_suche(self):
    """Schüler können Punkte anklicken, um Koordinaten zu sehen"""
    x = np.linspace(-10, 10, 100)
    y = [self.wert(xi) for xi in x]

    df = pd.DataFrame({'x': x, 'y': y})

    chart = alt.Chart(df).mark_line().encode(
        x='x', y='y'
    ).add_params(
        alt.selection_point()
    )

    # Zeigt ausgewählte Punkte an
    @mo.cell
    def show_selection():
        selected_points = chart.value
        if selected_points is not None and len(selected_points) > 0:
            return mo.md(f**Ausgewählte Punkte: {selected_points}**)
        return mo.md("Klicke auf den Graphen, um Punkte auszuwählen")

    return mo.vstack([chart, show_selection])
```

## Educational Use Cases

### 1. Parameter-Experimente

Schüler können mit Slidern experimentieren und sofort sehen, wie sich Koeffizienten auf den Graphen auswirken.

### 2. Nullstellen-Suche

Interaktive Suche nach Nullstellen durch Zoomen und Data Selection.

### 3. Ableitungsanalyse

Vergleich von Funktion und Ableitung mit unabhängigen y-Achsen.

### 4. Kurvendiskussion

Kombinierte Darstellung aller wichtigen Eigenschaften einer Funktion.

### 🔥 PERFECT PARABOLIC REPRESENTATION WITH PLOTLY 🔥

```python
def perfekte_parabel_plotly(self, x_range: tuple = (-5, 5), punkte: int = 200) -> mo.UI:
    """PERFEKTE Parabel-Darstellung entsprechend Schul-Konventionen"""
    # Perfekte symmetrische Datenpunkte um den Scheitelpunkt
    x = np.linspace(x_range[0], x_range[1], punkte)
    y = [self.wert(xi) for xi in x]

    fig = go.Figure()

    # Hauptkurve
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        name=f'f(x) = {self.term()}',
        line=dict(color='blue', width=3)
    ))

    # Scheitelpunkt berechnen und markieren
    try:
        # Für quadratische Funktionen: Scheitelpunkt bei x = -b/(2a)
        if len(self.koeffizienten) >= 3:
            a, b = self.koeffizienten[0], self.koeffizienten[1]
            s_x = -b / (2 * a)
            s_y = self.wert(s_x)

            fig.add_trace(go.Scatter(
                x=[s_x], y=[s_y],
                mode='markers',
                name='Scheitelpunkt',
                marker=dict(size=15, color='red', symbol='diamond'),
                text=[f'S({s_x:.2f}|{s_y:.2f})'],
                hovertemplate='%{text}<extra></extra>'
            ))
    except:
        pass

    # 🔥 ABSOLUT PERFEKTE MATHEMATISCHE KONFIGURATION 🔥
    fig.update_layout(
        title=f'Parabel: f(x) = {self.term()}',
        xaxis=dict(
            scaleanchor="y",        # 🔥 1:1 Aspect Ratio - KEINE VERZERRUNG!
            scaleratio=1,           # 🔥 Perfekte Kreisverwandtschaft!
            zeroline=True,          # 🔥 Achse im Ursprung sichtbar
            zerolinewidth=2,        # 🔥 Deutliche Null-Linie
            zerolinecolor='black',  # 🔥 Schwarze Achse
            showgrid=True,          # 🔥 Gitterlinien helfen beim Ablesen
            gridwidth=1,            # 🔥 Dünne Gitterlinien
            gridcolor='lightgray',  # 🔥 Dezentes Gitter
            range=x_range,          # 🔥 Symmetrischer Bereich
            title='x',             # 🔥 Achsenbeschriftung
            ticks='outside',        # 🔥 Ticks außerhalb
            tickwidth=2,           # 🔥 Deutliche Ticks
            showline=True,         # 🔥 Achsenlinie sichtbar
            linewidth=2            # 🔥 Deutliche Achsenlinie
        ),
        yaxis=dict(
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='black',
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            title=f'f(x) = {self.term()}',
            ticks='outside',
            tickwidth=2,
            showline=True,
            linewidth=2,
            scaleanchor="x"        # 🔥 Bidirektionale Verzerrungs-Verhinderung!
        ),
        plot_bgcolor='white',      # 🔥 Weißer Hintergrund für Schule
        paper_bgcolor='white',
        showlegend=True,
        width=700,
        height=500,
        font=dict(size=14)        # 🔥 Gute Lesbarkeit
    )

    return mo.ui.plotly(fig)
```

### 🔥 BEISPIEL: PARABEL f(x) = x² - 4x + 3

```python
# Perfekte Darstellung der Parabel f(x) = x² - 4x + 3
f = GanzrationaleFunktion([1, -4, 3])
parabel_chart = f.perfekte_parabel_plotly(x_range=(-2, 6))

# Ergebnis:
# - Perfekte 1:1 Darstellung (keine Verzerrung!)
# - Scheitelpunkt S(2|-1) korrekt markiert
# - Nullstellen bei x=1 und x=3 exakt ablesbar
# - Achsenkreuz deutlich sichtbar
# - Gitter für präzises Ablesen
```

## Warum Plotly für Schul-Mathematik UNERLÄSSLICH ist:

1. **🔥 Aspect Ratio Control**: `scaleanchor="y", scaleratio=1` verhindert Verzerrung
2. **🔥 Mathematical Accuracy**: Parabeln sehen aus wie Parabeln, nicht wie Ellipsen
3. **🔥 Educational Standards**: Entspricht den Konventionen aus Schulbüchern
4. **🔥 Interactive Learning**: Schüler können zoomen ohne mathematische Korrektheit zu verlieren
5. **🔥 Professional Output**: Drucker- und präsentationsreife Grafiken

## 🚫 Altair für Mathematik - Problematische Einschränkungen:

- **Kein Aspect Ratio Control**: Parabeln werden immer verzerrt dargestellt
- **Keine Achsen im Ursprung**: Schwer ablesbar für Schüler
- **Statistischer Fokus**: Optimal für Data Science, schlecht für Mathematik
- **Verzerrte Geometrie**: Kreise werden zu Ellipsen, Winkel sind nicht korrekt

## Performance-Tipps

1. **Datenmenge**: Plotly funktioniert auch mit > 50.000 Datenpunkten problemlos
2. **Reaktive Updates**: Plotly-Charts sind sehr performant in Marimo
3. **Chart-Komplexität**: Plotly unterstützt komplexe mathematische Visualisierungen
4. **Memory Management**: Plotly ist sehr speichereffizient für interaktive Graphen
