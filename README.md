README – Karteikartensystem

Programmierprojekt von Carl Klein, Yllind Gashi & David Lienhardt

Projektbeschreibung

Dieses Projekt ist ein Karteikartensystem, mit dem Nutzer eigene Lernkarten erstellen, bearbeiten und lernen können.
Das Programm läuft in der Konsole und speichert alle Karteikarten dauerhaft in einer Textdatei (karteikarten.txt).

Es gibt verschiedene Modi wie Lernen, Prüfungsmodus und Verwaltung der Karteikarten.
Alle Eingaben erfolgen über die Tastatur.

Funktionen
1. Lernen

Karteikarten werden zufällig angezeigt

Optional: Lernen nach Tag (z. B. “Mathe”, “Geschichte”)

Nutzer gibt an, ob die Frage richtig oder falsch beantwortet wurde

Statistiken werden gespeichert

2. Prüfungsmodus

Nutzer wählt die Anzahl der Fragen

Fragen werden zufällig ausgewählt

Richtig/falsch wird automatisch geprüft

Am Ende gibt es Punkte & Prozentwertung

3. Karteikarten verwalten

Hinzufügen neuer Karten

Bearbeiten bestehender Karten

Löschen von Karten

Jede Karte hat:

Frage

Antwort

beliebig viele Tags

Zähler für richtige & falsche Antworten

Installation & Voraussetzungen

Keinerlei externe Bibliotheken nötig.
Du benötigst:

Python 3 (getestet auf Version 3.10+)

Ausführung

Starte das Programm in einer Konsole:

python main.py


oder, falls Windows:

python3 main.py

Dateistruktur
projektordner/
│
├── main.py                # Hauptprogramm
├── karteikarten.txt       # Speicherung aller Karten
└── README.md              # Projektdokumentation

 Speicherformat der Karteikarten

Jede Zeile in karteikarten.txt entspricht einer Karte und folgt diesem Schema:

Frage | Antwort | Tag1;Tag2 | Anzahl_richtig | Anzahl_falsch


Beispiel:

Was ist die Hauptstadt von Frankreich?|Paris|Geo;Europa|3|1

 Beispielablauf im Menü
=== Karteisystem by Carl, Yllind & David ===
1) Lernen
2) Prüfungsmodus
3) Karteikarte bearbeiten
4) Karteikarte löschen
5) Karte hinzufügen
0) Beenden

 Mitwirkende

Carl Klein – Lern– & Prüfungsmodus

David Lienhardt – Bearbeiten & Löschen

Yllind Gashi – Hinzufügen neuer Karten

Alle – Allgemeine Struktur, Menüführung, Kommentare

Besonderheiten des Projekts

Nutzerfreundliches, simples Menü

Tags zur Kategorisierung

Speicherung von Lernfortschritt

Zufällige Reihenfolge der Fragen

Robuste Fehlerbehandlung bei Eingaben


exportieren.

Welche Datei hättet ihr gerne?
