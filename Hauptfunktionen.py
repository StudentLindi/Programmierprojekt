
#Carl Anfang Teil 1

# Lernmodus: nacheinander Fragen zeigen                                                             carl Start

def lernen(karten_liste):
    if not karten_liste:
        print("Noch keine Karten vorhanden.")
        return

    # Optional nur Karten mit bestimmtem Tag üben, Strip ignoriert input leerzeichen
    tag = input("Nur Karten mit Tag üben (Enter = alle): ").strip()

    # Reihenfolge mischen, WIESO LIST?
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
        #.strip(): Alle Leerzeichen werden am Anfang und Ende der Benutzereingabe entfernt
        #.lower(): Die Eingabe des Users wird in Kleinbuchstaben umgewandelt

    if geuebt == 0:
        print("Keine passende Karte geübt.")

    # Fortschritt speichern
    speichere_karten(karten_liste)


# Prüfungsmodus: feste Anzahl Fragen, Punkte zählen (CARL TEIL)    

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
        # Fallback: 10 oder maximal so viele wie vorhanden, warum min. 10?
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
            print("Richtig!")
            punkte = punkte + 1
            karte["richtig"] = karte["richtig"] + 1
        else:
            print("Falsch.")
            print("Richtig:", karte["antwort"])
            karte["falsch"] = karte["falsch"] + 1

    # Ergebnis anzeigen
    print("\n--- Ergebnis ---")
    prozent = int(punkte * 100 / anzahl)
    print(f"Punkte: {punkte}/{anzahl}  |  Quote: {prozent}%")

    # Fortschritt speichern
    speichere_karten(karten_liste)
#---------------------------------------------Carl Ende


# Eine Karte bearbeiten                       David start

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
    neu = input( f"Frage [{karte['frage']}]: ").strip()
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


# Eine Karte löschen

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

# Neue Karte hinzufügen                         Lindi Start               

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


# Hauptmenü   in der eigenen Datei erstellen und Import   
# #lern und prüfmodus zusammensnehmen
#                                                           Wieder Allgemein

