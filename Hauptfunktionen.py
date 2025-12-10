import random
from Konstanten import DATEI, RICHTIG, FALSCH, ENCODING, WEITER_JA, WEITER_NEIN

# ========= Datei laden =========
# Lindi Teil 1
def lade_karten():
    karten_liste = []
    try:
        with open(DATEI, "r", encoding=ENCODING) as f:
            for zeile in f:
                zeile = zeile.rstrip("\n")
                if zeile == "":
                    continue

                try:
                    teile = zeile.split("|")
                    if len(teile) != 5:
                        print(f"WARNUNG: Zeile ignoriert (erwarte 5 Teile, habe {len(teile)}): {zeile[:30]}...")
                        continue

                    frage, antwort, tags_str, richtig, falsch = teile

                    # 1. Prüfen, ob Zähler int sind
                    richtig_int = int(richtig)
                    falsch_int = int(falsch)
                    
                    tags = tags_str.split(";") if tags_str else []

                    karten_liste.append({
                        "frage": frage,
                        "antwort": antwort,
                        "tags": tags,
                        "richtig": richtig_int,
                        "falsch": falsch_int
                    })

                except ValueError:
                    # Fängt Fehler ab, wenn int(richtig) oder int(falsch) fehlschlägt und überspringt kaputte
                    # Zeile in der TXT Datei
                    print(f"FEHLER: Zeile ignoriert (ungültige Zähler): {zeile[:20]}...")
                    continue # Geht zur nächsten Zeile

    except FileNotFoundError:
        print(f"INFO: Datei '{DATEI}' nicht gefunden. Starte mit leerer Liste.")
    except IOError as e:
        # Fängt allgemeine Lese-/Schreibfehler ab
        print(f"SCHWERER FEHLER beim Lesen der Datei: {e}")

    return karten_liste


# ========= Speichern =========
#David Teil 1
def speichere_karten(karten_liste):
    try:
        with open(DATEI, "w", encoding=ENCODING) as f:
            for karte in karten_liste:
                tags_str = ";".join(karte["tags"]) if karte["tags"] else ""  # Tags mit ;

                zeile = "|".join([
                    karte["frage"],
                    karte["antwort"],
                    tags_str,
                    str(karte["richtig"]),
                    str(karte["falsch"])
                ])
                f.write(zeile + "\n")

    except IOError as e:
        print(f"FEHLER: Konnte Datei '{DATEI}' nicht speichern: {e}")



# ========= Eingaben =========
def eingabe_nicht_leer(prompt_text):
    text = input(prompt_text).strip()
    while text == "":
        print("Eingabe darf nicht leer sein.")
        text = input(prompt_text).strip()
    return text


# ========= Anzeige =========
#Lindi Teil 2
def zeige_karten(karten_liste, tag_filter=None):
    print("\n--- Karteikarten ---")
    ausgabe = 0
    for index, karte in enumerate(karten_liste, start=1):
        if tag_filter and tag_filter not in karte["tags"]:
            continue

        ausgabe += 1
        tags = ", ".join(karte["tags"]) if karte["tags"] else "-"

        print(f"{index:>3}. {karte['frage']}  [Tags: {tags}]  "
              f"Richtig: {karte['richtig']}  Falsch: {karte['falsch']}")

    if ausgabe == 0:
        print("(keine passenden Karten)")

#Carl Teil 1
def wähle_index(karten_liste):
    if not karten_liste:
        print("Keine Karten vorhanden.")
        return None

    while True:  # Eingabe solange wiederholen, bis gültig
        eingabe = input("Nummer der Karte (0=Abbrechen): ").strip()

        try:
            nummer = int(eingabe)
        except ValueError:
            print("Ungültige Eingabe. Bitte eine Zahl eingeben.")
            continue

        if nummer == 0:
            return None
        
        if 1 <= nummer <= len(karten_liste):
            return nummer - 1
        else:
            print(f"Ungültiger Bereich. Bitte eine Zahl zwischen 1 und {len(karten_liste)} wählen.")

def wähle_tag(karten_liste):
    # Alle Tags einsammeln
    alle_tags = sorted({tag for karte in karten_liste for tag in karte["tags"]})

    if not alle_tags:
        print("Keine Tags vorhanden – es werden alle Karten verwendet.")
        return ""

    print("\nVerfügbare Tags:")
    for i, tag in enumerate(alle_tags, start=1):
        print(f" {i}) {tag}")

    auswahl = input("Tag wählen (Nummer oder Name, Enter = alle): ").strip()

    # Enter für alle
    if auswahl == "":
        return ""

    # Zahl eingegeben?
    if auswahl.isdigit():
        nummer = int(auswahl)
        if 1 <= nummer <= len(alle_tags):
            return alle_tags[nummer - 1]
        else:
            print("Ungültige Nummer – es werden alle Karten verwendet.")
            return ""

    # sonst: direkt den eingegebenen Text als Tag verwenden
    return auswahl

# ========= Lernmodus =========
# auch Carl
def frage_bewertung():
    while True:
        bewertung = input("Richtig? (r/f/Enter skip): ").strip().lower()
        if bewertung in {RICHTIG, FALSCH, ""}:
            # Prüft, ob die Eingabe eine der erlaubten Optionen ist: richtig, falsch oder leer (skip)
            # (Set-Literal-Notation)
            return bewertung
        print("Ungültige Eingabe! Bitte 'r' für richtig, 'f' für falsch oder Enter drücken.")

# Neu gemacht von Carl um Lernmodus sauberer zu halten
# Eigene Funktion für Bewertung und Weitermachen und IF ELIF entfernt 
def frage_weitermachen():
    while True:
        wahl = input("Weiter? (Enter = ja / q = Nein): ").strip().lower()
        if wahl in WEITER_JA:
            return True
        if wahl in WEITER_NEIN:
            return False
        print("Fehler: Bitte nur Enter (für Ja) oder 'q' (für Nein) eingeben.")

# auch Carl
def lernen(karten_liste):
    if not karten_liste:
        print("Noch keine Karten vorhanden.")
        return

    tag = wähle_tag(karten_liste)
    reihenfolge = list(range(len(karten_liste)))
    random.shuffle(reihenfolge)

    geuebt = 0

    for idx in reihenfolge:
        karte = karten_liste[idx]

        if tag and tag not in karte["tags"]:
            continue

        print("\nFrage:", karte["frage"])
        input("[Enter für Antwort]")
        print("Antwort:", karte["antwort"])

        bewertung = frage_bewertung()

        if bewertung == RICHTIG:
            karte["richtig"] += 1
        elif bewertung == FALSCH:
            karte["falsch"] += 1

        geuebt += 1

        if not frage_weitermachen():
            break

    if geuebt == 0:
        print("Keine passende Karte geübt.")

    speichere_karten(karten_liste)
    return geuebt

# ========= Prüfungsmodus =========
#Carl
def prüfungsmodus(karten_liste):
    if not karten_liste:
        print("Keine Karten vorhanden.")
        return

    tag = wähle_tag(karten_liste)
    passende = [k for k in karten_liste if not tag or tag in k["tags"]]

    if not passende:
        print("Keine passenden Karten.")
        return

    try:
        # Versuch, die Eingabe in eine Zahl umzuwandeln
        anzahl = int(input(f"Wieviele Fragen? (1–{len(passende)}): "))
    except ValueError: # Nur abfangen, wenn int() fehlschlägt
        # Fallback auf Standardwert bei ungültiger Eingabe
        anzahl = min(10, len(passende))
        print(f"Ungültige Eingabe (keine Zahl) – nehme {anzahl} Fragen.")

    anzahl = max(1, min(anzahl, len(passende)))

    random.shuffle(passende)
    fragen = passende[:anzahl]

    punkte = 0
    for i, karte in enumerate(fragen, 1):
        print(f"\nFrage {i}/{anzahl}:\n{karte['frage']}")
        user = input("Antwort: ").lower().strip()

        if user == karte["antwort"].lower().strip():
            print("Richtig")
            punkte += 1
            karte["richtig"] += 1
        else:
            print("Falsch – richtig wäre:", karte["antwort"])
            karte["falsch"] += 1

    print(f"\nErgebnis: {punkte}/{anzahl} Punkte "
          f"({int(punkte / anzahl * 100)}%)")

    speichere_karten(karten_liste)


# ========= Bearbeiten =========
#David Teil 2
def bearbeiten(karten_liste):
    zeige_karten(karten_liste)
    idx = wähle_index(karten_liste)
    if idx is None:
        return

    karte = karten_liste[idx]

    neu = input(f"Frage ({karte['frage']}): ").strip()
    if neu:
        karte["frage"] = neu

    neu = input(f"Antwort ({karte['antwort']}): ").strip()
    if neu:
        karte["antwort"] = neu

    tags = input("Neue Tags (; getrennt / leer für keine Änderung): ").strip()
    if tags:
        karte["tags"] = [t.strip() for t in tags.split(";")]

    speichere_karten(karten_liste)
    print("Karte gespeichert")

# ========= Löschen ========= (David)
def löschen(karten_liste):
    if not karten_liste:
        print("Keine Karten zum Löschen vorhanden.")
        return
        
    zeige_karten(karten_liste)
    
    # Nutzer wählt Index der zu löschenden Karte
    idx = wähle_index(karten_liste)
    if idx is None:
        return

    karte_zu_löschen = karten_liste[idx]
    
    # Sicherheitsabfrage
    sicher = input(f"Soll die Karte '{karte_zu_löschen['frage']}' WIRKLICH gelöscht werden? (j/n): ").strip().lower()

    if sicher == 'j':
        del karten_liste[idx]  # Karte aus der Liste entfernen
        speichere_karten(karten_liste)
        print("Karte erfolgreich gelöscht und gespeichert.")
    else:
        print("Löschvorgang abgebrochen.")


# ========= Hinzufügen =========
# Lindi Teil 3
def hinzufügen(karten_liste):
    frage = eingabe_nicht_leer("Frage: ")
    antwort = eingabe_nicht_leer("Antwort: ")
    tags = input("Tags (; getrennt): ").strip()

    neue_karte = {
        "frage": frage,
        "antwort": antwort,
        "tags": [t.strip() for t in tags.split(";")] if tags else [],
        "richtig": 0,
        "falsch": 0
    }
    karten_liste.append(neue_karte)
    speichere_karten(karten_liste)
    print("Karte hinzugefügt")
