README File - Karteikartensystem (Carl,David,Yilllind)
1. Projektbeschreibung:

Dieses Programm ist ein Karteikartensystem, das zum Lernen und Abfragen von Wissen genutzt werden kann. Benutzer können Karteikarten erstellen, bearbeiten, löschen und entweder im Lernmodus oder im Prüfungsmodus üben. 
Der Lernfortschritt wird im Lernmodus dauerhaft gespeichert.

2. Vorraussetzungen und Start

Python Version: Python 3.10 oder höher

Benötigte Dateien im gleichen Ordner:

main.py (Menü / Startpunkt)

Hauptfunktionen.py

Konstanten.py

Start des Programms:
python main.py

3. Dateiformat

Die Karteikarten werden zeilenweise in folgendem Format gespeichert:
Frage|Antwort|tag1;tag2|richtig|falsch
Beispiel:
Was ist Python?|Programmiersprache|Informatik;Programmieren|3|1

=====================

4. Menü und Funktionen

1) Lernen: 

Lernmodus zum selbstständigen Üben

Optionales Filtern nach Themen (Tags)

Karten werden zufällig gemischt

Ablauf:

Frage anzeigen → Enter → Antwort anzeigen

Selbstbewertung:

r = richtig

f = falsch

Enter = überspringen

Lernstand (richtig/falsch) wird sofort gespeichert

Nach jeder Karte kann entschieden werden, ob weiter gelernt wird 

2) Prüfung:

Testmodus zur Wissensüberprüfung

Optionales Filtern nach Tags

Benutzer wählt Anzahl Fragen

Bei ungültiger Eingabe wird automatisch eine Standardanzahl gewählt

Ablauf:

Frage wird angezeigt

Antwort wird eingegeben

Exakter Vergleich (ohne Gross-/Kleinschreibung)

Bewertung:

Richtig = 1 Punkt

Falsch = 0 Punkte

Am Ende Ausgabe von Punktzahl und Prozentwert

Ergebnisse werden gespeichert
   
3) Karte bearbeiten

Anzeige aller Karten

Auswahl über Kartennummer

Bearbeitbar:

Frage

Antwort

Tags

Leere Eingaben lassen bestehende Werte unverändert

Änderungen werden dauerhaft gespeichert

4) Karte löschen

Anzeige aller Karten

Auswahl über Kartennummer

Sicherheitsabfrage vor dem Löschen

Karte wird endgültig entfernt und gespeichert

5) Neue Karte

Erstellung neuer Karteikarten

Pflichtfelder:

Frage

Antwort

Optionale Tags (durch ; getrennt)

Zähler für richtig/falsch starten bei 0

Karte wird sofort gespeichert
   
0) Beenden

Beendet das Programm sauber

Speichert alle Änderungen

Abbruch via Strg + C wird abgefangen

=====================
=====================

5. Eingaberegeln und Bedienung

Tags: Nummer, Name oder Enter für alle

Weiter im Lernmodus:

    Enter = weiter
    q = beenden

Antwortvergleich im Prüfungsmodus:
    
    Exakt (ohne Tippfehler-Toleranz)

6. Fehlerbehandlung

Ungültige Benutzereingaben werden abgefangen

Beschädigte Zeilen in der Textdatei werden übersprungen

Programm startet auch ohne vorhandene Kartendatei

7. Aufgabenteilung

Carl: Lernmodus, Prüfungsmodus, Tag-Auswahl, Hilfsfunktionen

David: Speichern, Löschen, Bearbeiten, Index-Auswahl

Yilllind: Laden der Karten, Anzeige, Eingabevalidierung
