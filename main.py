from Hauptfunktionen import *
# was macht der Stern? beim Import
def menü():
    karten_liste = lade_karten()
    print(f"\n=== Abgabe Karteikarten-System — {len(karten_liste)} Karten geladen ===")
    while True:
        print("1) Lernen")
        print("2) Prüfung")
        print("3) Karte bearbeiten")
        print("4) Karte löschen")
        print("5) Neue Karte")
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
            print("Auf Wiedersehen!")
            return

        else:
            print("Ungültige Eingabe — bitte erneut versuchen.")

if __name__ == "__main__":
    try:
        menü()
    except KeyboardInterrupt:
        print("\nProgramm manuell beendet. Auf Wiedersehen!")
