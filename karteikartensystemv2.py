#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Einfaches Karteikarten-System (CLI)
Version für FHNW-Programmieren (Kapitel 2–7)
- Menü mit while-Schleife
- Funktionen
- Speichern in Datei
- Arbeiten mit Listen
"""

DATEI_NAME = "karten.txt"
TRENNER = "|||"


# =========================================================
# Hilfsfunktionen für Datei
# =========================================================
def lade_karten():
    """Liest alle Karten aus der Datei und gibt eine Liste von Dicts zurück."""
    karten = []
    try:
        with open(DATEI_NAME, "r", encoding="utf-8") as f:
            #was ist encoding beispielweise hier in dieser Zeile?
            for zeile in f:
                zeile = zeile.strip()
                if not zeile:
                    continue
                teile = zeile.split(TRENNER)
                if len(teile) != 4:
                    continue
                kid, frage, antwort, thema = teile
                karten.append({
                    "id": int(kid),
                    "frage": frage,
                    "antwort": antwort,
                    "thema": thema,
                })
    except FileNotFoundError:
        # Erste Ausführung – Datei existiert noch nicht
        pass
    return karten


def speichere_karten(karten):
    """Schreibt alle Karten in die Datei."""
    with open(DATEI_NAME, "w", encoding="utf-8") as f:
        for karte in karten:
            zeile = f"{karte['id']}{TRENNER}{karte['frage']}{TRENNER}{karte['antwort']}{TRENNER}{karte['thema']}\n"
            f.write(zeile)


def naechste_id(karten):
    """Ermittelt die nächste freie ID."""
    if not karten:
        return 1
    max_id = max(karte["id"] for karte in karten)
    return max_id + 1


def alle_themen(karten):
    """Gibt eine sortierte Liste aller Themen zurück."""
    themen = set()
    for k in karten:
        themen.add(k["thema"])
    return sorted(list(themen))


# =========================================================
# Funktionen für Use-Cases
# =========================================================
def karte_hinzufuegen(karten):
    print("\n--- Neue Karte anlegen ---")
    frage = input("Frage: ").strip()
    antwort = input("Antwort: ").strip()
    thema = input("Thema (leer = Allgemein): ").strip()
    if thema == "":
        thema = "Allgemein"
    neue_karte = {
        "id": naechste_id(karten),
        "frage": frage,
        "antwort": antwort,
        "thema": thema,
    }
    karten.append(neue_karte)
    speichere_karten(karten)
    print(f"Karte mit ID {neue_karte['id']} gespeichert.")


def themen_auswaehlen(karten):
    """Hilfsfunktion: Thema wählen oder * für alle."""
    themen = alle_themen(karten)
    if not themen:
        print("Es gibt noch keine Themen.")
        return None
    print("\nVerfügbare Themen:")
    for i, t in enumerate(themen, start=1):
        print(f"{i}) {t}")
    print("* ) alle Themen")
    wahl = input("Thema wählen: ").strip()
    if wahl == "*":
        return "*"
    if wahl.isdigit():
        nummer = int(wahl)
        if 1 <= nummer <= len(themen):
            return themen[nummer - 1]
    print("Ungültige Auswahl.")
    return None


def gefilterte_karten(karten, thema):
    if thema is None or thema == "*":
        return list(karten)
    return [k for k in karten if k["thema"] == thema]


def lernmodus(karten):
    print("\n=== Lernmodus ===")
    if not karten:
        print("Keine Karten vorhanden.")
        return
    thema = themen_auswaehlen(karten)
    if thema is None:
        return
    auswahl = gefilterte_karten(karten, thema)
    if not auswahl:
        print("Keine Karten zu diesem Thema.")
        return

    # einfache „durchklicken“-Variante
    for karte in auswahl:
        print(f"\nFrage (ID {karte['id']}, Thema: {karte['thema']}):")
        print(karte["frage"])
        input("Enter für Antwort...")
        print("Antwort:")
        print(karte["antwort"])
    print("\nLernmodus beendet.")


def quizmodus(karten):
    print("\n=== Prüfmodus ===")
    if not karten:
        print("Keine Karten vorhanden.")
        return
    thema = themen_auswaehlen(karten)
    if thema is None:
        return
    auswahl = gefilterte_karten(karten, thema)
    if not auswahl:
        print("Keine Karten zu diesem Thema.")
        return

    # Wir mischen nur mit der Standardbibliothek
    import random
    random.shuffle(auswahl)

    richtig = 0
    gesamt = len(auswahl)

    for karte in auswahl:
        print(f"\nFrage (ID {karte['id']}): {karte['frage']}")
        eingabe = input("Deine Antwort: ").strip().lower()
        loesung = karte["antwort"].strip().lower()
        if eingabe == loesung:
            print("✅ Richtig!")
            richtig += 1
        else:
            print(f"❌ Falsch. Richtig wäre: {karte['antwort']}")
    print(f"\nErgebnis: {richtig} von {gesamt} richtig.")


def karte_bearbeiten(karten):
    print("\n--- Karte bearbeiten ---")
    try:
        cid = int(input("ID der Karte: ").strip())
    except ValueError:
        print("Ungültige ID.")
        return
    # Karte suchen
    karte = None
    for k in karten:
        if k["id"] == cid:
            karte = k
            break
    if karte is None:
        print("Karte nicht gefunden.")
        return

    print(f"Aktuelle Frage: {karte['frage']}")
    neue_frage = input("Neue Frage (leer = unverändert): ").strip()
    print(f"Aktuelle Antwort: {karte['antwort']}")
    neue_antwort = input("Neue Antwort (leer = unverändert): ").strip()
    print(f"Aktuelles Thema: {karte['thema']}")
    neues_thema = input("Neues Thema (leer = unverändert): ").strip()

    if neue_frage != "":
        karte["frage"] = neue_frage
    if neue_antwort != "":
        karte["antwort"] = neue_antwort
    if neues_thema != "":
        karte["thema"] = neues_thema

    speichere_karten(karten)
    print("Karte aktualisiert.")


def karte_loeschen(karten):
    print("\n--- Karte löschen ---")
    try:
        cid = int(input("ID der Karte: ").strip())
    except ValueError:
        print("Ungültige ID.")
        return
    neue_liste = []
    geloescht = False
    for k in karten:
        if k["id"] == cid:
            geloescht = True
        else:
            neue_liste.append(k)
    if geloescht:
        speichere_karten(neue_liste)
        karten[:] = neue_liste  # Liste im Speicher auch aktualisieren
        print("Karte gelöscht.")
    else:
        print("Keine Karte mit dieser ID gefunden.")


def themen_verwalten(karten):
    print("\n--- Themen verwalten -")