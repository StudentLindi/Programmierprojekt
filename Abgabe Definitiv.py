import random
#Test
DATEI = "karteikartenfile.txt"


def löschen(k):
    if not k: print("Noch keine Karten vorhanden."); return
    zeige_karten(k); idx=wähle_index(k)
    if idx is None: return
    if input("Wirklich löschen? (j/N): ").strip().lower()=="j":
       






#ab hier Carl's Teil also Lernmodus und Prüfungsmodus:
def prüfungsmodus(k, speichere_karten_func):
    if not k:
        print("Noch keine Karten vorhanden.")
        return
#Funktion Prüfungsmodus erstellt und variable k und speichere_karten_func erstellt. 
#falls k nicht vorhanden ist (da bisher keine Karteikarte erstellt wurde print)

