# Industrial IoT - Automatisierungstechnik

## Inhaltsverzeichnis
- [Übersicht](#übersicht)
- [Installation](#installation)
- [Verwendung](#verwendung)
  - [database_storage.py](#database_storagepy)
  - [mqtt_client.py](#mqtt_clientpy)
  - [predict.py](#predictpy)
  - [serializer.py](#serializerpy)
  - [user_interface.py](#user_interfacepy)
- [Datendateien](#datendateien)
- [Benutzeroberfläche](#benutzeroberfläche)


## Übersicht
Dieses Projekt befasst sich mit der Automatisierung von Datenverarbeitungs- und Vorhersageprozessen. Es umfasst verschiedene Module, die Daten auslesen, formatieren, vorhersagen und über eine Benutzeroberfläche präsentieren.

### Komponenten:
- **Datenspeicherung**: Skript zum Speichern und Laden von Daten im JSON-Format.
- **MQTT-Kommunikation**: Skript zum Verbinden mit einem MQTT-Broker, Abonnieren von Themen und Veröffentlichen von Nachrichten.
- **Prädiktive Modellierung**: Skript zum Trainieren und Verwenden eines prädiktiven Modells.
- **Datenserialisierung**: Skript zur Serialisierung und Deserialisierung von Daten.
- **Benutzeroberfläche**: Skript zur Bereitstellung einer grafischen Benutzeroberfläche mit Tkinter.

Das Projekt ist modular aufgebaut und kann bei Bedarf leicht um zusätzliche Funktionen erweitert werden.

## Installation

1. **Repository klonen**:
    ```bash
    git clone https://github.com/J0n1lu5/automatisierung
    ```

2. **Verzeichnis wechseln**:
    ```bash
    cd automatisierung
    ```

3. **Abhängigkeiten installieren**:
    ```bash
    pip install -r requirements.txt
    ```

## Verwendung

### database_storage.py
Dieses Python-Modul bietet Methoden zum Speichern und Laden von Daten in einer JSON-Datei mit der Klasse `DatabaseStorage`.

#### Klasse: `DatabaseStorage`
- **Attribute**:
  - `file_path`: Pfad zur JSON-Datei, in der die Daten gespeichert werden.

- **Methoden**:
  - `save(data)`: Speichert die bereitgestellten Daten in der angegebenen JSON-Datei.
    ```python
    def save(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f)
    ```
  - `load()`: Lädt und gibt die Daten aus der JSON-Datei zurück.
    ```python
    def load(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)
    ```

### mqtt_client.py
Dieses Python-Modul ermöglicht die Verbindung zu einem MQTT-Broker, das Abonnieren von Themen und das Veröffentlichen von Nachrichten mit der Klasse `MQTTClient`.

#### Klasse: `MQTTClient`
- **Attribute**:
  - `broker`: Adresse des MQTT-Brokers.
  - `port`: Port des MQTT-Brokers.
  - `topic`: MQTT-Thema zum Veröffentlichen/Abonnieren.

- **Methoden**:
  - `connect()`: Verbindet sich mit dem MQTT-Broker.
    ```python
    def connect(self):
        self.client.connect(self.broker, self.port, 60)
    ```
  - `publish(payload)`: Veröffentlicht die angegebene Nutzlast im angegebenen Thema.
    ```python
    def publish(self, payload):
        self.client.publish(self.topic, payload)
    ```
  - `subscribe(on_message)`: Abonniert das angegebene Thema und verarbeitet eingehende Nachrichten mit der bereitgestellten `on_message`-Callback-Funktion.
    ```python
    def subscribe(self, on_message):
        self.client.subscribe(self.topic)
        self.client.on_message = on_message
        self.client.loop_start()
    ```

### predict.py
Dieses Python-Modul bietet Funktionen zum Trainieren und Verwenden eines prädiktiven Modells mit der Klasse `Predictor`.

#### Klasse: `Predictor`
- **Attribute**:
  - `model`: Machine-Learning-Modell (Standard ist `LinearRegression`).

- **Methoden**:
  - `train(X, y)`: Trainiert das Modell mit den bereitgestellten Merkmalen `X` und Zielwerten `y`.
    ```python
    def train(self, X, y):
        self.model.fit(X, y)
    ```
  - `predict(X)`: Sagt die Zielwerte für die angegebenen Merkmale `X` voraus.
    ```python
    def predict(self, X):
        return self.model.predict(X)
    ```

### serializer.py
Dieses Python-Modul bietet Methoden zur Serialisierung und Deserialisierung von JSON-Daten mit der Klasse `Serializer`.

#### Klasse: `Serializer`
- **Methoden**:
  - `serialize(data)`: Konvertiert die bereitgestellten Daten in einen JSON-String.
    ```python
    def serialize(self, data):
        return json.dumps(data)
    ```
  - `deserialize(data)`: Konvertiert den bereitgestellten JSON-String zurück in Daten.
    ```python
    def deserialize(self, data):
        return json.loads(data)
    ```

### user_interface.py
Dieses Python-Skript erstellt eine einfache grafische Benutzeroberfläche mit Tkinter.

#### Klasse: `UserInterface`
- **Attribute**:
  - `master`: Tkinter-Hauptfenster.

- **Methoden**:
  - `__init__(self, master)`: Initialisiert die GUI mit einem Label und Buttons.
    ```python
    def __init__(self, master):
        self.master = master
        master.title("Automatisierung")

        self.label = Label(master, text="Dies ist eine einfache GUI")
        self.label.pack()

        self.greet_button = Button(master, text="Grüßen", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Schließen", command=master.quit)
        self.close_button.pack()
    ```
  - `greet()`: Gibt eine Begrüßungsnachricht aus.
    ```python
    def greet(self):
        print("Hallo!")
    ```

## Datendateien
- `data.json`: Enthält JSON-Daten, die im Projekt verwendet werden.
- `formatted_data.csv`: Enthält formatierte Daten im CSV-Format.
- `formatted_data.json`: Enthält formatierte Daten im JSON-Format.
- `reg_123456-654321-112233.csv`: Enthält spezifische Datensätze im CSV-Format.
- `X.csv`: Enthält Merkmalsdaten im CSV-Format.

## Benutzeroberfläche

Über die Benutzeroberfläche können die folgenden Aktionen durchgeführt werden:

- **Start recording**: Startet die Aufzeichnung der Daten.
- **Compute Data**: Formatiert die Daten und bereitet sie für die Vorhersage vor.
- **Prediction**: Leitet zum Modul für die lineare Regression weiter.
- **Plot data**: Ermöglicht das Plotten der Daten.


