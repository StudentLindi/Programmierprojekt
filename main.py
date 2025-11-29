from funktionen import *
from konstanten import DATEI

def menü():
    karten_liste = lade_karten()
    while True:
        print("\n=== FHNW Karteikarten-System ===")
        print("1) Lernen")
        print("2) Prüfung")
        print("3) Karte bearbeiten")
        print("4) Karte löschen")
        print("5) Neue Karte")
        print("0) Beenden")

        match input("Auswahl: "):
            case "1": lernen(karten_liste)
            case "2": prüfungsmodus(karten_liste)
            case "3": bearbeiten(karten_liste)
            case "4": löschen(karten_liste)
            case "5": hinzufügen(karten_liste)
            case "0": print("Auf Wiedersehen!"); return
            case _: print("Ungültige Eingabe.")

if __name__ == "__main__":
    menü()
