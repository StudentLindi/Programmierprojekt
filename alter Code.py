#Definitive Abgabe Programmierprojekt Karteikartensystem
#Carl Klein, Ylllind Gashi, David Lienhardt

from Hauptfunktionen import lernen, prüfungsmodus, bearbeiten, löschen, hinzufügen
from Konstanten import DATEI
import random


#evtl weitere Konstante verwenden falls mehrere Dateien import werden
#extra datei mit konstanten erstellen und dann import die datei
#richtig und falsch bspw als Konstante erstellen

# Karteikarten aus der Datei laden, #Lindi Teil 1

def lade_karten():
    karten_liste = []
#hier haben wir Datei direkt als Konstante gespeichert
    try:
        with open(DATEI, "r", encoding = "utf-8") as f:
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
        #Fehlermeldung noch eingeben 
        #permission error
        #io erorr

        pass

    return karten_liste


# Karteikarten in die Datei schreiben
#David, Encoding (utf8 gemäss Feedback von Felix)
def speichere_karten(karten_liste):
    with open(DATEI, "w", encoding="utf-8") as f:
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


# Benutzer-Eingabe, die nicht leer sein darf (evtl kürzer formulieren)
def eingabe_nicht_leer(prompt_text):
    text = input(prompt_text).strip()

    # So lange nachfragen, bis etwas drin steht
    while text == "":
        print("Eingabe darf nicht leer sein.")
        text = input(prompt_text).strip()

    return text

#Lindi Teil 1 Ende
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



# Nutzer wählt eine Karten-Nummer           Bis hier ist der code allgemein und von allen zu verstehen
#Carl
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

def menü():
    """Hauptmenü (Funktionskommentare in dieser Form hinterlegen)"""
    karten_liste = lade_karten()

    while True:
        print("\n=== Karteisystem by Carl, Ylllind & David ===")
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
            hinzufuegen(karten_liste) 
        elif wahl == "0":
            print("Tschüss!")
            break
        else:
            print("Ungültige Auswahl.")


# Programm starten
if __name__ == "__main__":
    menü()
