#definitive Abgabe Programmierprojekt Karteikartensystem
#Carl Klein, Ylllind Gashi, David Lienhardt

import random

# Datei, in der die Karteikarten gespeichert werden
DATEI = "karteikarten.txt"


# ------------------------------------------------------------
# Karteikarten aus der Datei laden
# ------------------------------------------------------------
def lade_karten():
    karten_liste = []

    try:
        with open(DATEI, "r") as f:
            for zeile in f:
                # Zeilenumbruch entfernen
                zeile = zeile.rstrip("\n")

                # Leere Zeilen überspringen
                if zeile == "":
                    continue

                # Zeile in Teile zerlegen (Trennzeichen: "|")
                teile = zeile.split("|")

                # Erwartet: frage | antwort | tags_str | richtig | falsch
                if len(teile) < 5:
                    # Ungültige Zeile überspringen
                    continue
#Tags sind wie Fächer, für den User zu unterteilen in welche Listen er die Karteikarten will
                frage = teile[0]
                antwort = teile[1]
                tags_str = teile[2]
                richtig = teile[3]
                falsch = teile[4]

                # Tags sind durch Semikolon getrennt
                if tags_str:
                    tags = tags_str.split(";")
                else:
                    tags = []

                # In ein einheitliches Dict umwandeln (dict =dictionary)
                eintrag = {
                    "frage": frage,
                    "antwort": antwort,
                    "tags": tags,
                    "richtig": int(richtig),
                    "falsch": int(falsch),
                }

                karten_liste.append(eintrag)

    except FileNotFoundError:
        # Wenn die Datei noch nicht existiert, einfach leere Liste zurückgeben
        pass

    return karten_liste


# ------------------------------------------------------------
# Karteikarten in die Datei schreiben
# ------------------------------------------------------------
def speichere_karten(karten_liste):
    with open(DATEI, "w") as f:
        for karte in karten_liste:
            # Tags wieder zu einem String zusammensetzen
            if karte["tags"]:
                tags_str = ";".join(karte["tags"])
            else:
                tags_str = ""

            # Alles durch "|" trennen und in einer Zeile speichern
            zeile = "|".join([
                karte["frage"],
                karte["antwort"],
                tags_str,
                str(karte["richtig"]),
                str(karte["falsch"]),
            ])
            f.write(zeile + "\n")


# ------------------------------------------------------------
# Benutzer-Eingabe, die nicht leer sein darf
# ------------------------------------------------------------
def eingabe_nicht_leer(prompt_text):
    text = input(prompt_text).strip()

    # So lange nachfragen, bis etwas drin steht
    while text == "":
        print("Eingabe darf nicht leer sein.")
        text = input(prompt_text).strip()

    return text


# ------------------------------------------------------------
# Alle Karten anzeigen (optional nach Tag filtern)
# -------------------------------------------------------------
def zeige_karten(karten_liste, tag_filter=None):
    print("\n--- Karteikarten ---")
    anzahl_ausgegeben = 0

    for index, karte in enumerate(karten_liste, start=1):
        # Wenn ein Filter gesetzt ist, nur passende Karten zeigen
        if tag_filter and (tag_filter not in karte["tags"]):
            continue

        anzahl_ausgegeben = anzahl_ausgegeben + 1

        if karte["tags"]:
            tags_anzeige = ", ".join(karte["tags"])
        else:
            tags_anzeige = "-"

        print(
            f"{index:>3}. {karte['frage']}   "
            f"[Tags: {tags_anzeige}]   "
            f"Richtig: {karte['richtig']}  Falsch: {karte['falsch']}"
        )

    if anzahl_ausgegeben == 0:
        print("(keine passenden Karten)")


# ------------------------------------------------------------
# Nutzer wählt eine Karten-Nummer           Bis hier ist der code allgemein und von allen zu verstehen
# ------------------------------------------------------------
def wähle_index(karten_liste):
    if not karten_liste:
        print("Keine Karten vorhanden.")
        return None

    try:
        eingabe = input("Nummer der Karte (oder 0 zum Abbrechen): ").strip()
        nummer = int(eingabe)

        if nummer == 0:
            return None

        if 1 <= nummer <= len(karten_liste):
            return nummer - 1

    except ValueError:
        # Wenn keine Zahl eingegeben wurde
        pass

    print("Ungültige Auswahl.")
    return None


# ------------------------------------------------------------
# Lernmodus: nacheinander Fragen zeigen                         carl Start
# ------------------------------------------------------------
def lernen(karten_liste):
    if not karten_liste:
        print("Noch keine Karten vorhanden.")
        return

    # Optional nur Karten mit bestimmtem Tag üben
    tag = input("Nur Karten mit Tag üben (Enter = alle): ").strip()

    # Reihenfolge mischen
    reihenfolge = list(range(len(karten_liste)))
    random.shuffle(reihenfolge)

    geuebt = 0

    for idx in reihenfolge:
        karte = karten_liste[idx]

        # Tag-Filter anwenden
        if tag and (tag not in karte["tags"]):
            continue

        # Frage anzeigen
        print("\nFrage:\n" + karte["frage"])
        input("\n[Enter] für die Antwort...")

        # Antwort anzeigen
        print("\nAntwort:\n" + karte["antwort"])

        # Bewertung abfragen
        bewertung = input(
            "\nWar deine Antwort richtig? (r/f/Enter=überspringen): "
        ).strip().lower()

        if bewertung == "r":
            karte["richtig"] = karte["richtig"] + 1
        elif bewertung == "f":
            karte["falsch"] = karte["falsch"] + 1

        geuebt = geuebt + 1

        # Weiter machen?
        weiter = input("Weiter? (Enter = ja, q = beenden): ").strip().lower()
        if weiter == "q":
            break

    if geuebt == 0:
        print("Keine passende Karte geübt.")

    # Fortschritt speichern
    speichere_karten(karten_liste)


# ------------------------------------------------------------
# Prüfungsmodus: feste Anzahl Fragen, Punkte zählen
# ------------------------------------------------------------
def prüfungsmodus(karten_liste):
    if not karten_liste:
        print("Noch keine Karten vorhanden.")
        return

    tag = input("Nur Karten mit Tag prüfen (Enter = alle): ").strip()

    # Passende Karten herausfiltern
    passende = []
    for eintrag in karten_liste:
        if (not tag) or (tag in eintrag["tags"]):
            passende.append(eintrag)

    if not passende:
        print("Keine passenden Karten gefunden.")
        return

    # Anzahl Fragen erfragen
    try:
        eingabe = input(f"Wieviele Fragen? (1–{len(passende)}): ").strip()
        anzahl = int(eingabe)
    except ValueError:
        # Fallback: 10 oder maximal so viele wie vorhanden
        anzahl = min(10, len(passende))
        print(f"Ungültige Zahl, nehme {anzahl}.")

    # Grenzen einhalten
    if anzahl < 1:
        anzahl = 1
    if anzahl > len(passende):
        anzahl = len(passende)

    # Reihenfolge mischen und die gewünschte Anzahl nehmen
    random.shuffle(passende)
    fragen = passende[:anzahl]

    punkte = 0
    print("\n--- Prüfungsmodus ---")

    for i, karte in enumerate(fragen, start=1):
        print(f"\nFrage {i}/{anzahl}:\n{karte['frage']}")

        nutzer_antwort = input("\nDeine Antwort: ").strip().lower()
        richtige_antwort = karte["antwort"].strip().lower()

        if nutzer_antwort == richtige_antwort:
            print(" Richtig!")
            punkte = punkte + 1
            karte["richtig"] = karte["richtig"] + 1
        else:
            print(" Falsch.")
            print("Richtig:", karte["antwort"])
            karte["falsch"] = karte["falsch"] + 1

    # Ergebnis anzeigen
    print("\n--- Ergebnis ---")
    prozent = int(punkte * 100 / anzahl)
    print(f"Punkte: {punkte}/{anzahl}  |  Quote: {prozent}%")

    # Fortschritt speichern
    speichere_karten(karten_liste)
#---------------------------------------------Carl Ende

# ------------------------------------------------------------
# Eine Karte bearbeiten                       David start
# ------------------------------------------------------------
def bearbeiten(karten_liste):
    if not karten_liste:
        print("Noch keine Karten vorhanden.")
        return

    zeige_karten(karten_liste)
    idx = wähle_index(karten_liste)

    if idx is None:
        return

    karte = karten_liste[idx]

    print("\nLeere Eingabe = Feld behalten, '-' = Feld leeren.")

    # Frage bearbeiten
    neu = input(f"Frage [{karte['frage']}]: ").strip()
    if neu == "-":
        karte["frage"] = ""
    elif neu != "":
        karte["frage"] = neu

    # Antwort bearbeiten
    neu = input(f"Antwort [{karte['antwort']}]: ").strip()
    if neu == "-":
        karte["antwort"] = ""
    elif neu != "":
        karte["antwort"] = neu

    # Tags bearbeiten (Semikolon-getrennt)
    alte_tags = ";".join(karte["tags"])
    neu = input(f"Tags (Semikolon-getrennt) [{alte_tags}]: ").strip()
    if neu == "-":
        karte["tags"] = []
    elif neu != "":
        # Leerzeichen um einzelne Tags entfernen
        neue_tags = []
        for t in neu.split(";"):
            t = t.strip()
            if t:
                neue_tags.append(t)
        karte["tags"] = neue_tags

    speichere_karten(karten_liste)
    print("Änderungen gespeichert.")


# ------------------------------------------------------------
# Eine Karte löschen
# ------------------------------------------------------------
def löschen(karten_liste):
    if not karten_liste:
        print("Noch keine Karten vorhanden.")
        return

    zeige_karten(karten_liste)
    idx = wähle_index(karten_liste)

    if idx is None:
        return

    sicher = input("Wirklich löschen? (j/N): ").strip().lower()
    if sicher == "j":
        del karten_liste[idx]
        speichere_karten(karten_liste)
        print("Karte gelöscht.")
    else:
        print("Abgebrochen.")
#-----------------------------------------------David Ende

# ------------------------------------------------------------
# Neue Karte hinzufügen                         Lindi Start               
# ------------------------------------------------------------
def hinzufügen(karten_liste):
    # Frage und Antwort dürfen nicht leer sein
    frage = eingabe_nicht_leer("Frage: ")
    antwort = eingabe_nicht_leer("Antwort: ")

    # Tags optional
    tags_eingabe = input("Tags (Semikolon-getrennt, optional): ").strip()

    if tags_eingabe:
        tags = []
        for t in tags_eingabe.split(";"):
            t = t.strip()
            if t:
                tags.append(t)
    else:
        tags = []

    # Neue Karte anlegen
    neue_karte = {
        "frage": frage,
        "antwort": antwort,
        "tags": tags,
        "richtig": 0,
        "falsch": 0,
    }
    karten_liste.append(neue_karte)

    # Speichern
    speichere_karten(karten_liste)
    print("Karte hinzugefügt.")

#------------------------------------------------Lindi Ende
# ------------------------------------------------------------
# Hauptmenü                                      Wieder Allgemein
# ------------------------------------------------------------
def menü():
    karten_liste = lade_karten()

    while True:
        print("\n=== Karteisystem by Carl, Yllind & David ===")
        print("1) Lernen")
        print("2) Prüfungsmodus")
        print("3) Karteikarte bearbeiten")
        print("4) Karteikarte löschen")
        print("5) Karte hinzufügen")
        print("0) Beenden")

        wahl = input("Auswahl: ").strip()

        if wahl == "1":
            lernen(karten_liste)
        elif wahl == "2":
            prüfungsmodus(karten_liste)
        elif wahl == "3":
            bearbeiten(karten_liste)
        elif wahl == "4":
            löschen(karten_liste)
        elif wahl == "5":
            hinzufügen(karten_liste)
        elif wahl == "0":
            print("Tschüss!")
            break
        else:
            print("Ungültige Auswahl.")


# Programm starten
if __name__ == "__main__":
    menü()
