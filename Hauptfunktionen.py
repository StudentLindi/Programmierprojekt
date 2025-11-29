import random
from Konstanten import DATEI

# ========= Datei laden =========
def lade_karten():
    karten_liste = []
    try:
        with open(DATEI, "r", encoding="utf-8") as f:
            for zeile in f:
                zeile = zeile.rstrip("\n")
                if zeile == "":
                    continue

                teile = zeile.split("|")
                if len(teile) < 5:
                    continue

                frage = teile[0]
                antwort = teile[1]
                tags_str = teile[2]
                richtig = teile[3]
                falsch = teile[4]

                tags = tags_str.split(";") if tags_str else []

                eintrag = {
                    "frage": frage,
                    "antwort": antwort,
                    "tags": tags,
                    "richtig": int(richtig),
                    "falsch": int(falsch)
                }
                karten_liste.append(eintrag)

    except FileNotFoundError:
        pass

    return karten_liste


# ========= Speichern =========
def speichere_karten(karten_liste):
    with open(DATEI, "w", encoding="utf-8") as f:
        for karte in karten_liste:
            tags_str = ";".join(karte["tags"]) if karte["tags"] else ""
            zeile = "|".join([
                karte["frage"],
                karte["antwort"],
                tags_str,
                str(karte["richtig"]),
                str(karte["falsch"])
            ])
            f.write(zeile + "\n")


# ========= Eingaben =========
def eingabe_nicht_leer(prompt_text):
    text = input(prompt_text).strip()
    while text == "":
        print("Eingabe darf nicht leer sein.")
        text = input(prompt_text).strip()
    return text


# ========= Anzeige =========
def zeige_karten(karten_liste, tag_filter=None):
    print("\n--- Karteikarten ---")
    ausgabe = 0
    for index, karte in enumerate(karten_liste, start=1):
        if tag_filter and tag_filter not in karte["tags"]:
            continue
        ausgabe += 1
        tags = ", ".join(karte["tags"]) if karte["tags"] else "-"
        print(f"{index:>3}. {karte['frage']}   [Tags: {tags}]   Richtig: {karte['richtig']}  Falsch: {karte['falsch']}")
    if ausgabe == 0:
        print("(keine passenden Karten)")


def wähle_index(karten_liste):
    if not karten_liste:
        print("Keine Karten vorhanden.")
        return None
    try:
        nummer = int(input("Nummer der Karte (0=Abbrechen): ").strip())
        if nummer == 0:
            return None
        if 1 <= nummer <= len(karten_liste):
            return nummer - 1
    except:
        pass
    print("Ungültige Auswahl.")
    return None


# ========= Lernmodus =========
def lernen(karten_liste):
    if not karten_liste:
        print("Noch keine Karten vorhanden."); return

    tag = input("Nur Karten mit Tag üben (Enter = alle): ").strip()
    reihenfolge = list(range(len(karten_liste)))
    random.shuffle(reihenfolge)

    geübt = 0

    for idx in reihenfolge:
        karte = karten_liste[idx]
        if tag and tag not in karte["tags"]:
            continue

        print("\nFrage:\n" + karte["frage"])
        input("\n[Enter] für die Antwort...")
        print("\nAntwort:\n" + karte["antwort"])

        bewertung = input("\nRichtig? (r/f/Enter skip): ").strip().lower()
        if bewertung == RICHTIG:
            karte["richtig"] += 1
        elif bewertung == FALSCH:
            karte["falsch"] += 1

        geübt += 1
        if input("Weiter? (Enter = ja, q = stopp): ").strip().lower() == "q":
            break

    if geübt == 0: print("Keine passende Karte geübt.")
    speichere_karten(karten_liste)


# ========= Prüfungsmodus =========
def prüfungsmodus(karten_liste):
    if not karten_liste: print("Keine Karten."); return

    tag = input("Tagfilter (Enter = alle): ").strip()
    passende = [k for k in karten_liste if (not tag) or tag in k["tags"]]

    if not passende: print("Keine passenden Karten."); return

    try:
        anzahl = int(input(f"Wieviele Fragen (1-{len(passende)}): "))
    except:
        anzahl = min(10, len(passende))
        print(f"Ungültig, nehme {anzahl}.")
    
    anzahl = max(1, min(anzahl, len(passende)))
    random.shuffle(passende)
    fragen = passende[:anzahl]

    punkte = 0
    print("\n--- Prüfungsmodus ---")

    for i, karte in enumerate(fragen, 1):
        print(f"\nFrage {i}/{anzahl}:\n{karte['frage']}")
        user = input("\nAntwort: ").strip().lower()

        if user == karte["antwort"].lower():
            print("✔ Richtig!")
            punkte += 1
            karte["richtig"] += 1
        else:
            print("✘ Falsch. Richtige Antwort:", karte["antwort"])
            karte["falsch"] += 1

    print(f"\nErgebnis: {punkte}/{anzahl} Punkte ({int(punkte/anzahl*100)}%)")
    speichere_karten(karten_liste)


# ========= Bearbeiten =========
def bearbeiten(karten_liste):
    zeige_karten(karten_liste)
    idx = wähle_index(karten_liste)
    if idx is None: return

    karte = karten_liste[idx]
    neu = input(f"Frage [{karte['frage']}]: ").strip()
    if neu: karte["frage"] = neu

    neu = input(f"Antwort [{karte['antwort']}]: ").strip()
    if neu: karte["antwort"] = neu

    tags = input(f"Tags (Alt: {','.join(karte['tags'])}): ").strip()
    if tags: karte["tags"] = [t.strip() for t in tags.split(";")]

    speichere_karten(karten_liste)
    print("Änderung gespeichert.")


# ========= Löschen =========
def löschen(karten_liste):
    zeige_karten(karten_liste)
    idx = wähle_index(karten_liste)
    if idx is None: return
    if input("Sicher löschen? (j/N): ").lower() == "j":
        del karten_liste[idx]
        speichere_karten(karten_liste)
        print("Gelöscht.")
    else:
        print("Abbruch.")


# ========= Hinzufügen =========
def hinzufügen(karten_liste):
    frage = eingabe_nicht_leer("Frage: ")
    antwort = eingabe_nicht_leer("Antwort: ")
    tags = input("Tags (mit ; getrennt): ").strip()

    neue_karte = {
        "frage": frage,
        "antwort": antwort,
        "tags": [t.strip() for t in tags.split(";")] if tags else [],
        "richtig": 0,
        "falsch": 0
    }
    karten_liste.append(neue_karte)
    speichere_karten(karten_liste)
    print("Neue Karte gespeichert!")
