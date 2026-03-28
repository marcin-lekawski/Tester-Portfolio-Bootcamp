import sqlite3
import questionary
from rich.console import Console

import terminal_ui

console = Console()

def get_db():
    import os
    db_path = os.path.join(os.path.dirname(__file__), "data", "istqb_knowledge.db")
    return sqlite3.connect(db_path)

def kb_menu():
    style = terminal_ui.get_custom_style()
    while True:
        choice = questionary.select(
            "📚 BAZA WIEDZY (Czytanie)",
            choices=[
                "1. Słownik Pojęć (Przegląd)",
                "2. Sylabus ISTQB (Czytanie podrozdziałów)",
                "3. 🚪 Wyjdź do Menu Głównego"
            ],
            style=style
        ).ask()

        if not choice or choice.startswith("3"):
            break
        elif choice.startswith("1"):
            view_glossary()
        elif choice.startswith("2"):
            view_syllabus()

def view_glossary():
    conn = get_db()
    c = conn.cursor()
    style = terminal_ui.get_custom_style()
    while True:
        c.execute("SELECT id, term, definition FROM glossary ORDER BY term ASC")
        terms = c.fetchall()
        
        choices = [f"{t[1]}" for t in terms] + ["🚪 [Wróć]"]
        term_choice = questionary.select(
            "Wybierz pojęcie z Glosariusza:", 
            choices=choices,
            style=style
        ).ask()
        
        if not term_choice or term_choice == "🚪 [Wróć]":
            break
        else:
            t = next(x for x in terms if x[1] == term_choice)
            action = terminal_ui.nano_pager(f"Pojęcie: {t[1]}", t[2])
            if action == 'menu':
                break
    conn.close()

def view_syllabus():
    conn = get_db()
    c = conn.cursor()
    style = terminal_ui.get_custom_style()
    while True:
        c.execute("SELECT id, subchapter_number, k_level, content FROM syllabus_sections ORDER BY chapter_id, id ASC")
        secs = c.fetchall()
        
        choices = [f"{s[1]} ({s[2]})" for s in secs] + ["🚪 [Wróć]"]
        s_choice = questionary.select(
            "Wybierz Podrozdział Sylabusa:", 
            choices=choices,
            style=style
        ).ask()
        
        if not s_choice or s_choice == "🚪 [Wróć]":
            break
        else:
            s_data = next(x for x in secs if f"{x[1]} ({x[2]})" == s_choice)
            action = terminal_ui.nano_pager(f"Źródło Syllabus: {s_data[1]} (Poziom {s_data[2]})", s_data[3])
            if action == 'menu':
                break
    conn.close()
