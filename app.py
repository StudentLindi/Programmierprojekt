"""
Autovermietung - Vollständige Version
Demonstriert: Dateien, Ausnahmen, Datensätze
"""

# ============================================
# DATEI-OPERATIONEN
# ============================================


def autos_laden():
    """Lädt alle Autos aus der Datei."""
    autos = []
    try:
        with open("autos.txt", "r") as datei:
            zeile = datei.readline()
            while zeile != "":
                auto = {
                    "modell": zeile.rstrip(),
                    "kennzeichen": datei.readline().rstrip(),
                    "preis": datei.readline().rstrip(),
                    "status": datei.readline().rstrip(),
                }
                autos.append(auto)
                zeile = datei.readline()
    except FileNotFoundError:
        pass  # Leere Liste zurückgeben
    except Exception as e:
        print(f"Fehler beim Laden: {e}")

    return autos


def autos_speichern(autos):
    """Speichert alle Autos in die Datei."""
    try:
        with open("autos.txt", "w") as datei:
            for auto in autos:
                datei.write(auto["modell"] + "\n")
                datei.write(auto["kennzeichen"] + "\n")
                datei.write(auto["preis"] + "\n")
                datei.write(auto["status"] + "\n")
        return True
    except IOError as e:
        print(f"Fehler beim Speichern: {e}")
        return False


# ============================================
# AUTO-OPERATIONEN
# ============================================


def auto_hinzufuegen():
    """Fügt ein neues Auto hinzu."""
    print("\n" + "=" * 50)
    print("NEUES AUTO HINZUFÜGEN")
    print("=" * 50)

    try:
        modell = input("Marke/Modell: ").strip()
        if not modell:
            print("Modell darf nicht leer sein!")
            return

        kennzeichen = input("Kennzeichen: ").strip()
        preis = input("Preis pro Tag (CHF): ").strip()

        # Autos laden und neues hinzufügen
        autos = autos_laden()
        autos.append(
            {
                "modell": modell,
                "kennzeichen": kennzeichen,
                "preis": preis,
                "status": "verfuegbar",
            }
        )

        if autos_speichern(autos):
            print(f'\n[OK] Auto "{modell}" erfolgreich gespeichert!')

        # Ein weiteres Auto hinzufügen oder zurück zum Hauptmenu?
        while True:
            aktion = (
                input(
                    "Möchten Sie ein weiteres Auto hinzufügen (a) oder zum Hauptmenü zurückkehren (m)? "
                )
                .strip()
                .lower()
            )
            if aktion == "a":
                auto_hinzufuegen()
                break
            elif aktion == "m":
                return
            else:
                print("Ungültige Eingabe! Bitte wählen Sie (a) oder (m).")
                continue

    except KeyboardInterrupt:
        print("\n\nAbgebrochen.")
    except Exception as e:
        print(f"[FEHLER] Fehler: {e}")


def autos_anzeigen():
    """Zeigt alle Autos an."""
    autos = autos_laden()

    print("\n" + "=" * 50)
    print(f"ALLE AUTOS ({len(autos)} im System)")
    print("=" * 50)

    if not autos:
        print("Keine Autos vorhanden.")
        input("\nDrücken Sie Enter, um zum Menü zurückzukehren...")
        return

    for i, auto in enumerate(autos, start=1):
        symbol = "[V]" if auto["status"] == "verfuegbar" else "[X]"
        print(f'\n{i}. {symbol} {auto["modell"]}')
        print(f'   Kennzeichen: {auto["kennzeichen"]}')
        print(f'   Preis/Tag: {auto["preis"]} CHF')
        print(f'   Status: {auto["status"]}')
    input("\nDrücken Sie Enter, um zum Menü zurückzukehren...")


def auto_suchen():
    """Sucht nach einem Auto."""
    autos = autos_laden()

    if not autos:
        print("\nKeine Autos vorhanden.")
        input("\nDrücken Sie Enter, um zum Menü zurückzukehren...")
        return

    suchbegriff = input("\nSuchbegriff: ").lower().strip()

    print("\n" + "=" * 50)
    print("SUCHERGEBNISSE")
    print("=" * 50)

    gefunden = []
    for i, auto in enumerate(autos, start=1):
        if (
            suchbegriff in auto["modell"].lower()
            or suchbegriff in auto["kennzeichen"].lower()
            or suchbegriff in auto["status"].lower()
        ):
            gefunden.append((i, auto))

    if gefunden:
        for nr, auto in gefunden:
            print(f'\n#{nr} {auto["modell"]}')
            print(f'    Kennzeichen: {auto["kennzeichen"]}')
            print(f'    Preis/Tag: {auto["preis"]} CHF')
            print(f'    Status: {auto["status"]}')
    else:
        print(f'\n[X] Keine Autos mit "{suchbegriff}" gefunden.')

    input("\nDrücken Sie Enter, um zum Menü zurückzukehren...")


def auto_status_aendern():
    """Ändert den Status eines Autos (vermieten/zurückgeben)."""
    autos = autos_laden()

    if not autos:
        print("\nKeine Autos vorhanden.")
        input("\nDrücken Sie Enter, um zum Menü zurückzukehren...")
        return

    # Autos anzeigen
    print("\n" + "=" * 50)
    print("AUTO STATUS ÄNDERN")
    print("=" * 50)

    for i, auto in enumerate(autos, start=1):
        print(f'{i}. {auto["modell"]} - {auto["status"]}')

    try:
        nr = int(input("\nAuto-Nummer: "))

        if 1 <= nr <= len(autos):
            auto = autos[nr - 1]

            print(f"\n--- Aktuelles Auto ---")
            print(f'Modell: {auto["modell"]}')
            print(f'Kennzeichen: {auto["kennzeichen"]}')
            print(f'Status: {auto["status"]}')

            if auto["status"] == "verfuegbar":
                auto["status"] = "vermietet"
                aktion = "vermietet"
            else:
                auto["status"] = "verfuegbar"
                aktion = "zurückgegeben"

            if autos_speichern(autos):
                print(f"\n[OK] Auto erfolgreich {aktion}!")
                input("\nDrücken Sie Enter, um zum Menü zurückzukehren...")
        else:
            print("[X] Ungültige Nummer!")

    except ValueError:
        print("[X] Bitte eine Zahl eingeben!")
    except Exception as e:
        print(f"[X] Fehler: {e}")


def auto_loeschen():
    """Löscht ein Auto."""
    autos = autos_laden()

    if not autos:
        print("\nKeine Autos vorhanden.")
        input("\nDrücken Sie Enter, um zum Menü zurückzukehren...")
        return

    print("\n" + "=" * 50)
    print("AUTO LÖSCHEN")
    print("=" * 50)

    for i, auto in enumerate(autos, start=1):
        print(f'{i}. {auto["modell"]} ({auto["kennzeichen"]})')

    try:
        nr = int(input("\nAuto-Nummer: "))

        if 1 <= nr <= len(autos):
            auto = autos[nr - 1]
            antwort = input(f'Wirklich "{auto["modell"]}" löschen? (j/n): ')

            if antwort.lower() == "j":
                autos.pop(nr - 1)

                if autos_speichern(autos):
                    print("\n[OK] Auto erfolgreich gelöscht!")
                    input("\nDrücken Sie Enter, um zum Menü zurückzukehren...")
            else:
                print("Löschen abgebrochen.")
                input("\nDrücken Sie Enter, um zum Menü zurückzukehren...")
        else:
            print("[X] Ungültige Nummer!")

    except ValueError:
        print("[X] Bitte eine Zahl eingeben!")
    except Exception as e:
        print(f"[X] Fehler: {e}")


def statistiken_anzeigen():
    """Zeigt Statistiken über die Autos."""
    autos = autos_laden()

    print("\n" + "=" * 50)
    print("STATISTIKEN")
    print("=" * 50)

    print(f"Anzahl Autos: {len(autos)}")

    if not autos:
        print("Keine Autos vorhanden.")
        input("\nDrücken Sie Enter, um zum Menü zurückzukehren...")
        return
    else:
        # Verfügbare vs. vermietete Autos:

        # Summiert die Autos auf, welche den Status verfügbar haben
        verfuegbar = sum(1 for a in autos if a["status"] == "verfuegbar")
        print(f"Verfügbar: {verfuegbar}")

        # Zieht die Anzahl der verfügbaren Autos von der Gesamtanzahl ab, um die vermieteten Autos zu erhalten
        vermietet = len(autos) - verfuegbar
        print(f"Vermietet: {vermietet}")

        # Durchschnittspreis:

        # Kreeiert eine Liste [] mit den Preisen der Autos aus der Liste der Autos
        preise = [float(a["preis"]) for a in autos]
        durchschnitt = sum(preise) / len(preise)
        print(f"Durchschnittspreis: {durchschnitt:.2f} CHF/Tag")

        # Potenzielle Tageseinnahmen
        potential = sum(preise)
        print(f"Max. Tageseinnahmen: {potential:.2f} CHF")

    input("\nDrücken Sie Enter, um zum Menü zurückzukehren...")


# ============================================
# HAUPTPROGRAMM
# ============================================


def Menü_anzeigen():
    """Zeigt das Hauptmenü an."""
    print("\n" + "=" * 50)
    print("AUTOVERMIETUNG - HAUPTMENÜ")
    print("=" * 50)
    print("1. Auto hinzufügen")
    print("2. Alle Autos anzeigen")
    print("3. Auto suchen")
    print("4. Auto vermieten/zurückgeben")
    print("5. Auto löschen")
    print("6. Statistiken anzeigen")
    print("0. Beenden")
    print("=" * 50)


def main():
    """Hauptfunktion der Anwendung."""
    print("\n*** AUTOVERMIETUNG ***")
    print("Willkommen!")

    while True:
        try:
            Menü_anzeigen()
            wahl = input("\nIhre Wahl: ").strip()

            if wahl == "1":
                auto_hinzufuegen()
            elif wahl == "2":
                autos_anzeigen()
            elif wahl == "3":
                auto_suchen()
            elif wahl == "4":
                auto_status_aendern()
            elif wahl == "5":
                auto_loeschen()
            elif wahl == "6":
                statistiken_anzeigen()
            elif wahl == "0":
                print("\nAuf Wiedersehen!")
                break
            else:
                print("\n[X] Ungültige Eingabe! Bitte 0-6 wählen.")

        # Wenn CTRL-C gedrückt wird
        except KeyboardInterrupt:
            print("\n\nProgramm abgebrochen.")
            break
        # Allgemeiner Fehler
        except Exception as e:
            print(f"\n[X] Unerwarteter Fehler: {e}")


if __name__ == "__main__":
    main()
