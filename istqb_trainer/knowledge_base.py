import sqlite3
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def get_db():
    import os
    db_path = os.path.join(os.path.dirname(__file__), "data", "istqb_knowledge.db")
    return sqlite3.connect(db_path)

def kb_menu():
    while True:
        choice = questionary.select(
            "📚 BAZA WIEDZY (Czytanie)",
            choices=[
                "1. Słownik Pojęć (Przegląd)",
                "2. Sylabus ISTQB (Czytanie podrozdziałów)",
                "3. 🚪 Wyjdź do Menu Głównego"
            ]
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
    while True:
        c.execute("SELECT id, term, definition FROM glossary ORDER BY term ASC")
        terms = c.fetchall()
        
        choices = [f"{t[1]}" for t in terms] + ["🚪 [Wróć]"]
        term_choice = questionary.select("Wybierz pojęcie z Glosariusza (Wpisz literę na klawiaturze by szukać!):", choices=choices).ask()
        
        if not term_choice or term_choice == "🚪 [Wróć]":
            break
        else:
            t = next(x for x in terms if x[1] == term_choice)
            console.print(Panel(t[2], title=f"📗 {t[1]}", border_style="cyan"))
            Prompt.ask("\n[dim]Naciśnij ENTER by wrócić do pojęć...[/dim]")
    conn.close()

def view_syllabus():
    conn = get_db()
    c = conn.cursor()
    while True:
        c.execute("SELECT id, subchapter_number, k_level, content FROM syllabus_sections ORDER BY chapter_id, id ASC")
        secs = c.fetchall()
        
        choices = [f"{s[1]} ({s[2]})" for s in secs] + ["🚪 [Wróć]"]
        s_choice = questionary.select("Wybierz Podrozdział Sylabusa:", choices=choices).ask()
        
        if not s_choice or s_choice == "🚪 [Wróć]":
            break
        else:
            s_data = next(x for x in secs if f"{x[1]} ({x[2]})" == s_choice)
            
            console.print(Panel(s_data[3], title=f"📘 Teoria u Źródła: {s_data[1]} (Poziom {s_data[2]})", border_style="blue"))
            Prompt.ask("\n[dim]Naciśnij ENTER by przewinąć / wrócić do podrozdziałów...[/dim]")
    conn.close()
