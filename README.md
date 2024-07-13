# Industrial Iot

## Intro
Dieses Projekt befasst sich mit der Automatisierung von Datenverarbeitungs- und Vorhersageprozessen. Es umfasst verschiedene Module, die Daten auslesen, formatieren, vorhersagen und über eine Benutzeroberfläche präsentieren.

## Installation
1. Klonen Sie dieses Repository:

    ```bash
    git clone https://github.com/J0n1lu5/automatisierung
    ```

2. Wechseln Sie in das Verzeichnis:

    ```bash
    cd automatisierung
    ```

3. Installieren Sie die erforderlichen Pakete:

    ```bash
    pip install -r requirements.txt
    ```

4. Starten sie Streamlit um die Benutzeroberfläche zu starten:

    ```bashs
    python userinterface.py
    ```
## Benutzeroberfläche

Über die Benutzeroberfläche können die folgenden Aktionen durchgeführt werden:

- **Start recording**: Startet die Aufzeichnung der Daten.
- **Compute Data**: Formatiert die Daten und bereitet sie für die Vorhersage vor.
- **Prediction**: Leitet zum Modul für die lineare Regression weiter.
- **Plot data**: Ermöglicht das Plotten der Daten.