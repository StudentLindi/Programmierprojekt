import random

DATEI = "karteikarten.txt"

def lade_karten():
    k=[]
    try:
        with open(DATEI,"r",encoding="utf-8") as f:
            for z in f:
                z=z.rstrip("\n")
                if not z: continue
                t=z.split("|")
                if len(t)<5: continue
                frage,antwort,tags_str,richtig,falsch=t
                tags=tags_str.split(";") if tags_str else []
                k.append({"frage":frage,"antwort":antwort,"tags":tags,"richtig":int(richtig),"falsch":int(falsch)})
    except FileNotFoundError:
        pass
    return k

def speichere_karten(k):
    with open(DATEI,"w",encoding="utf-8") as f:
        for x in k:
            tags_str=";".join(x["tags"]) if x["tags"] else ""
            f.write("|".join([x["frage"],x["antwort"],tags_str,str(x["richtig"]),str(x["falsch"])])+"\n")

def eingabe_nicht_leer(p):
    s=input(p).strip()
    while s=="": print("Eingabe darf nicht leer sein."); s=input(p).strip()
    return s

def zeige_karten(karten,tag_filter=None):
    print("\n--- Karteikarten ---")
    c=0
    for i,k in enumerate(karten,1):
        if tag_filter and (tag_filter not in k["tags"]): continue
        c+=1; tags=", ".join(k["tags"]) if k["tags"] else "-"
        print(f"{i:>3}. {k['frage']}   [Tags: {tags}]   Richtig: {k['richtig']}  Falsch: {k['falsch']}")
    if c==0: print("(keine passenden Karten)")

def wähle_index(k):
    if not k: print("Keine Karten vorhanden."); return None
    try:
        n=int(input("Nummer der Karte (oder 0 zum Abbrechen): ").strip())
        if n==0: return None
        if 1<=n<=len(k): return n-1
    except ValueError: pass
    print("Ungültige Auswahl."); return None

def lernen(k):
    if not k: print("Noch keine Karten vorhanden."); return
    tag=input("Nur Karten mit Tag üben (Enter = alle): ").strip()
    r=list(range(len(k))); random.shuffle(r); geübt=0
    for idx in r:
        x=k[idx]
        if tag and (tag not in x["tags"]): continue
        print("\nFrage:\n"+x["frage"]); input("\n[Enter] für die Antwort...")
        print("\nAntwort:\n"+x["antwort"])
        bw=input("\nWar deine Antwort richtig? (r/f/Enter=überspringen): ").strip().lower()
        if bw=="r": x["richtig"]+=1
        elif bw=="f": x["falsch"]+=1
        geübt+=1
        if input("Weiter? (Enter = ja, q = beenden): ").strip().lower()=="q": break
    if geübt==0: print("Keine passende Karte geübt.")
    speichere_karten(k)

def prüfungsmodus(k):
    if not k: print("Noch keine Karten vorhanden."); return
    tag=input("Nur Karten mit Tag prüfen (Enter = alle): ").strip()
    p=[x for x in k if (not tag or tag in x["tags"])]
    if not p: print("Keine passenden Karten gefunden."); return
    try: a=int(input(f"Wieviele Fragen? (1–{len(p)}): ").strip())
    except ValueError: a=min(10,len(p)); print(f"Ungültige Zahl, nehme {a}.")
    a=max(1,min(a,len(p))); random.shuffle(p); f=p[:a]; punkte=0
    print("\n--- Prüfungsmodus ---")
    for i,x in enumerate(f,1):
        print(f"\nFrage {i}/{a}:\n{x['frage']}")
        if input("\nDeine Antwort: ").strip().lower()==x["antwort"].strip().lower():
            print("✅ Richtig!"); punkte+=1; x["richtig"]+=1
        else:
            print("❌ Falsch.\nRichtig:",x["antwort"]); x["falsch"]+=1
    print("\n--- Ergebnis ---"); print(f"Punkte: {punkte}/{a}  |  Quote: {int(punkte*100/a)}%")
    speichere_karten(k)

def bearbeiten(k):
    if not k: print("Noch keine Karten vorhanden."); return
    zeige_karten(k); idx=wähle_index(k)
    if idx is None: return
    x=k[idx]; print("\nLeere Eingabe = Feld behalten, '-' = Feld leeren.")
    s=input(f"Frage [{x['frage']}]: ").strip()
    if s=="-": x["frage"]=""
    elif s: x["frage"]=s
    s=input(f"Antwort [{x['antwort']}]: ").strip()
    if s=="-": x["antwort"]=""
    elif s: x["antwort"]=s
    talt=";".join(x["tags"]); s=input(f"Tags (Semikolon-getrennt) [{talt}]: ").strip()
    if s=="-": x["tags"]=[]
    elif s: x["tags"]=[t.strip() for t in s.split(";") if t.strip()]
    speichere_karten(k); print("Änderungen gespeichert.")

def löschen(k):
    if not k: print("Noch keine Karten vorhanden."); return
    zeige_karten(k); idx=wähle_index(k)
    if idx is None: return
    if input("Wirklich löschen? (j/N): ").strip().lower()=="j":
        del k[idx]; speichere_karten(k); print("Karte gelöscht.")
    else: print("Abgebrochen.")

def hinzufügen(k):
    frage=eingabe_nicht_leer("Frage: "); antwort=eingabe_nicht_leer("Antwort: ")
    te=input("Tags (Semikolon-getrennt, optional): ").strip()
    tags=[t.strip() for t in te.split(";") if t.strip()] if te else []
    k.append({"frage":frage,"antwort":antwort,"tags":tags,"richtig":0,"falsch":0})
    speichere_karten(k); print("Karte hinzugefügt.")

def menü():
    k=lade_karten()
    while True:
        print("\n=== Karteikarten (einfach) ===")
        print("1) Lernen\n2) Prüfungsmodus\n3) Karteikarte bearbeiten\n4) Karteikarte löschen\n5) Karte hinzufügen\n0) Beenden")
        w=input("Auswahl: ").strip()
        if   w=="1": lernen(k)
        elif w=="2": prüfungsmodus(k)
        elif w=="3": bearbeiten(k)
        elif w=="4": löschen(k)
        elif w=="5": hinzufügen(k)
        elif w=="0": print("Tschüss!"); break
        else: print("Ungültige Auswahl.")

if __name__=="__main__": menü()
