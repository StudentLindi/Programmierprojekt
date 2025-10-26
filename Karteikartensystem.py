print("Hallo Welt")

print("Hallo Zusammen")

print("Bastardo")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Karteikarten-System (CLI)

Funktionen gemäß Anforderung:
1) Karteikarte hinzufügen
2) Lernmodus (durchgehen, Antwort anzeigen, Wiederholen)
3) Prüfmodus (Eingabe der Antwort, richtig/falsch, Wiederholung)
4) Karteikarte bearbeiten
5) Karteikarte löschen
6) Themen verwalten (anlegen/umbenennen/löschen)
7) Programm beenden

Persistenz: JSON-Datei cards.json
Abhängigkeiten: nur Standardbibliothek (json, os, random, dataclasses, typing)
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import json
import os
import random

DATA_FILE = "cards.json"

# -----------------------------
# Datenmodell
# -----------------------------
@dataclass
class Card:
    id: int
    question: str
    answer: str
    topic: str

# -----------------------------
# Speicher-Schicht
# -----------------------------

def _empty_store() -> Dict:
    return {"next_id": 1, "cards": [], "topics": []}


def load_store() -> Dict:
    if not os.path.exists(DATA_FILE):
        store = _empty_store()
        save_store(store)
        return store
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            # falls Datei korrupt ist, neu beginnen aber Sicherung anlegen
            backup = DATA_FILE + ".bak"
            try:
                os.replace(DATA_FILE, backup)
            except Exception:
                pass
            data = _empty_store()
            save_store(data)
        # Backfill für alte Strukturen
        data.setdefault("next_id", 1)
        data.setdefault("cards", [])
        data.setdefault("topics", [])
        return data


def save_store(store: Dict) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)


# -----------------------------
# Hilfsfunktionen Domänenlogik
# -----------------------------

def list_cards(store: Dict, topic: Optional[str] = None) -> List[Card]:
    cards = [Card(**c) for c in store["cards"]]
    if topic is None or topic == "*":
        return cards
    return [c for c in cards if c.topic == topic]


def list_topics(store: Dict) -> List[str]:
    return list(store.get("topics", []))


def ensure_topic(store: Dict, topic: str) -> None:
    if topic and topic not in store["topics"]:
        store["topics"].append(topic)


def add_card(store: Dict, question: str, answer: str, topic: str) -> Card:
    cid = store["next_id"]
    store["next_id"] += 1
    card = Card(id=cid, question=question.strip(), answer=answer.strip(), topic=topic.strip())
    ensure_topic(store, card.topic)
    store["cards"].append(asdict(card))
    save_store(store)
    return card


def find_card(store: Dict, card_id: int) -> Optional[Card]:
    for c in store["cards"]:
        if c["id"] == card_id:
            return Card(**c)
    return None


def update_card(store: Dict, card_id: int, *, question: Optional[str] = None,
                answer: Optional[str] = None, topic: Optional[str] = None) -> bool:
    for c in store["cards"]:
        if c["id"] == card_id:
            if question is not None and question.strip() != "":
                c["question"] = question.strip()
            if answer is not None and answer.strip() != "":
                c["answer"] = answer.strip()
            if topic is not None and topic.strip() != "":
                c["topic"] = topic.strip()
                ensure_topic(store, c["topic"])
            save_store(store)
            return True
    return False


def delete_card(store: Dict, card_id: int) -> bool:
    before = len(store["cards"])
    store["cards"] = [c for c in store["cards"] if c["id"] != card_id]
    after = len(store["cards"])
    if after != before:
        save_store(store)
        return True
    return False


def rename_topic(store: Dict, old: str, new: str) -> int:
    if old == new:
        return 0
    count = 0
    for c in store["cards"]:
        if c["topic"] == old:
            c["topic"] = new
            count += 1
    if old in store["topics"]:
        store["topics"].remove(old)
    ensure_topic(store, new)
    save_store(store)
    return count


def delete_topic(store: Dict, topic: str, *, reassign_to: Optional[str] = None) -> int:
    """Löscht ein Thema. Karten werden entweder gelöscht (reassign_to=None)
    oder auf ein anderes Thema umgehängt."""
    affected = 0
    if reassign_to:
        ensure_topic(store, reassign_to)
        for c in store["cards"]:
            if c["topic"] == topic:
                c["topic"] = reassign_to
                affected += 1
    else:
        before = len(store["cards"])
        store["cards"] = [c for c in store["cards"] if c["topic"] != topic]
        affected = before - len(store["cards"])
    if topic in store["topics"]:
        store["topics"].remove(topic)
    save_store(store)
    return affected

# -----------------------------
# Use-Cases (Interaktion)
# -----------------------------

def ui_select_topic(store: Dict) -> Optional[str]:
    topics = list_topics(store)
    if not topics:
        print("\nEs gibt noch keine Themen. Du kannst beim Hinzufügen einer Karte eines anlegen.")
        return None
    print("\nVerfügbare Themen:")
    for i, t in enumerate(topics, 1):
        print(f"  {i}) {t}")
    print("  * ) alle Themen")
    choice = input("Thema wählen (Zahl oder *): ").strip()
    if choice == "*":
        return "*"
    if choice.isdigit() and 1 <= int(choice) <= len(topics):
        return topics[int(choice) - 1]
    print("Ungültige Auswahl.")
    return None


def usecase_add_card(store: Dict) -> None:
    print("\n— Karteikarte hinzufügen —")
    q = input("Frage: ").strip()
    a = input("Antwort: ").strip()
    topic = input("Thema (neu oder bestehend): ").strip() or "Allgemein"
    card = add_card(store, q, a, topic)
    print(f"Karte {card.id} gespeichert.")


def usecase_learn_mode(store: Dict) -> None:
    print("\n— Lernmodus —")
    topic = ui_select_topic(store)
    cards = list_cards(store, topic)
    if not cards:
        print("Keine Karten vorhanden.")
        return
    queue = cards[:]  # einfache Wiederhol-Schlange
    random.shuffle(queue)
    repeat: List[Card] = []
    while queue:
        c = queue.pop(0)
        print(f"\nFrage (#{c.id}, Thema: {c.topic}):\n{c.question}")
        input("(Enter) um Antwort anzuzeigen…")
        print(f"Antwort:\n{c.answer}")
        again = input("Nochmal wiederholen? (j/N): ").strip().lower()
        if again == "j":
            repeat.append(c)
    if repeat:
        print(f"\n{len(repeat)} Karte(n) zur Wiederholung…")
        queue = repeat
        repeat = []
        random.shuffle(queue)
        while queue:
            c = queue.pop(0)
            print(f"\nFrage (#{c.id}, Thema: {c.topic}):\n{c.question}")
            input("(Enter) um Antwort anzuzeigen…")
            print(f"Antwort:\n{c.answer}")
    print("\nLernmodus beendet.")


def normalize(s: str) -> str:
    return " ".join(s.strip().lower().split())


def usecase_quiz_mode(store: Dict) -> None:
    print("\n— Prüfmodus —")
    topic = ui_select_topic(store)
    cards = list_cards(store, topic)
    if not cards:
        print("Keine Karten vorhanden.")
        return
    random.shuffle(cards)
    total = len(cards)
    correct = 0
    wrong: List[Tuple[Card, str]] = []
    for c in cards:
        print(f"\nFrage (#{c.id}, Thema: {c.topic}):\n{c.question}")
        user = input("Deine Antwort: ")
        if normalize(user) == normalize(c.answer):
            print("✅ Richtig!")
            correct += 1
        else:
            print(f"❌ Falsch. Richtig wäre: {c.answer}")
            wrong.append((c, user))
    print(f"\nErgebnis: {correct}/{total} richtig")
    if wrong:
        rep = input("Falsche wiederholen? (j/N): ").strip().lower()
        if rep == "j":
            for c, _ in wrong:
                print(f"\nFrage (#{c.id}):\n{c.question}")
                user = input("Deine Antwort: ")
                if normalize(user) == normalize(c.answer):
                    print("✅ Jetzt richtig!")
                else:
                    print(f"❌ Immer noch falsch. Lösung: {c.answer}")


def usecase_edit_card(store: Dict) -> None:
    print("\n— Karte bearbeiten —")
    try:
        cid = int(input("Karten-ID: "))
    except ValueError:
        print("Ungültige ID.")
        return
    card = find_card(store, cid)
    if not card:
        print("Nicht gefunden.")
        return
    print(f"Aktuell:\nFrage: {card.question}\nAntwort: {card.answer}\nThema: {card.topic}")
    q = input("Neue Frage (leer = unverändert): ")
    a = input("Neue Antwort (leer = unverändert): ")
    t = input("Neues Thema (leer = unverändert): ")
    ok = update_card(store, cid, question=q if q.strip() else None,
                     answer=a if a.strip() else None,
                     topic=t if t.strip() else None)
    print("Gespeichert." if ok else "Speichern fehlgeschlagen.")


def usecase_delete_card(store: Dict) -> None:
    print("\n— Karte löschen —")
    try:
        cid = int(input("Karten-ID: "))
    except ValueError:
        print("Ungültige ID.")
        return
    card = find_card(store, cid)
    if not card:
        print("Nicht gefunden.")
        return
    confirm = input(f"Wirklich Karte #{cid} löschen? (j/N): ").strip().lower()
    if confirm == "j":
        ok = delete_card(store, cid)
        print("Gelöscht." if ok else "Konnte nicht gelöscht werden.")
    else:
        print("Abgebrochen.")


def usecase_manage_topics(store: Dict) -> None:
    while True:
        print("\n— Themen verwalten —")
        topics = list_topics(store)
        if topics:
            print("Themen:")
            for i, t in enumerate(topics, 1):
                print(f"  {i}) {t}")
        else:
            print("(Noch keine Themen)")
        print("\nAktionen: 1) Hinzufügen  2) Umbenennen  3) Löschen  4) Zurück")
        choice = input("> ").strip()
        if choice == "1":
            t = input("Neues Thema: ").strip()
            if not t:
                print("Leer nicht erlaubt.")
                continue
            ensure_topic(store, t)
            save_store(store)
            print("Hinzugefügt.")
        elif choice == "2":
            old = input("Altes Thema: ").strip()
            if old not in topics:
                print("Nicht gefunden.")
                continue
            new = input("Neuer Name: ").strip()
            n = rename_topic(store, old, new)
            print(f"Umbenannt. {n} Karte(n) angepasst.")
        elif choice == "3":
            t = input("Thema löschen: ").strip()
            if t not in topics:
                print("Nicht gefunden.")
                continue
            mode = input("Karten behalten und umhängen? (Zielthema eingeben) oder leer = Karten löschen: ").strip()
            affected = delete_topic(store, t, reassign_to=mode or None)
            print(f"Thema gelöscht. {affected} betroffene Karte(n).")
        elif choice == "4":
            break
        else:
            print("Ungültig.")

# -----------------------------
# Menü / Steuerung
# -----------------------------

def main() -> None:
    store = load_store()
    while True:
        print("\n========== Karteikarten-System ==========")
        print("1) Karte hinzufügen")
        print("2) Lernmodus")
        print("3) Prüfmodus")
        print("4) Karte bearbeiten")
        print("5) Karte löschen")
        print("6) Themen verwalten")
        print("7) Beenden")
        choice = input("> ").strip()
        if choice == "1":
            usecase_add_card(store)
        elif choice == "2":
            usecase_learn_mode(store)
        elif choice == "3":
            usecase_quiz_mode(store)
        elif choice == "4":
            usecase_edit_card(store)
        elif choice == "5":
            usecase_delete_card(store)
        elif choice == "6":
            usecase_manage_topics(store)
        elif choice == "7":
            print("Auf Wiedersehen!")
            break
        else:
            print("Ungültige Auswahl.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n(Abgebrochen)")
