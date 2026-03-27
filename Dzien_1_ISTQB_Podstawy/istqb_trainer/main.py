import time
import json
import os
import random
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
import questionary

console = Console()

DATA = {
    "1": {
        "title": "Podstawy testowania (Rozdział 1)",
        "theory": (
            "1.1. Cel testowania: Znajdowanie defektów, upewnianie się, że oprogramowanie spełnia wymagania...\n"
            "1.3. 7 Zasad Testowania:\n"
            "   1) Testowanie ujawnia usterki, ale nie dowodzi ich braku.\n"
            "   2) Testowanie gruntowne jest niemożliwe.\n"
            "   3) Wczesne testowanie oszczędza czas (Shift-Left).\n"
            "   4) Kumulowanie się defektów w modułach (Zasada Pareto).\n"
            "   5) Testowanie zależy od kontekstu.\n"
            "   6) Paradoks pestycydów.\n"
            "   7) Przekonanie o braku błędów to fałsz.\n"
        ),
        "questions": [
            {
                "q": "Która z 7 zasad mówi o tym, że aby testy wciąż wykrywały nowe usterki, trzeba je aktualizować?",
                "choices": ["Paradoks pestycydów", "Wczesne testowanie", "Brak błędów to fałsz", "Zlepki defektów"],
                "ans": "Paradoks pestycydów"
            },
            {
                "q": "Główny cel testowania statycznego (Static Testing) to:",
                "choices": ["Uruchomienie aplikacji w celu znalezienia błędów", "Wykrycie defektów zanim powstanie kod", "Zautomatyzowanie logowania", "Badanie bazy produkcyjnej"],
                "ans": "Wykrycie defektów zanim powstanie kod"
            }
        ]
    },
    "2": {
        "title": "Testowanie w Cyklu Życia Oprogramowania (Rozdział 2)",
        "theory": (
            "Modele: Sekwencyjne (V-Model, Waterfall) lub Iteracyjne (Agile, Scrum).\n"
            "Testowanie potwierdzające (Re-testing): Sprawdzanie naprawionego błędu.\n"
            "Testowanie regresyjne (Regression testing): Sprawdzanie czy nic się nie zepsuło obok."
        ),
        "questions": [
            {
                "q": "Developer naprawia błąd. Co wykonasz?",
                "choices": ["Testy regresyjne", "Testy potwierdzające (re-testing)", "Testy wydajnościowe", "Jednostkowe"],
                "ans": "Testy potwierdzające (re-testing)"
            }
        ]
    }
}

def display_welcome():
    console.print(Panel.fit("[bold cyan]🎓 ISTQB Trainer[/bold cyan]", border_style="cyan"))

def learn_mode():
    chap = questionary.select(
        "Wybierz rozdział:",
        choices=[f"{k} - {v['title']}" for k,v in DATA.items()] + ["Wróć"]
    ).ask()
    if chap == "Wróć": return
    
    data = DATA[chap.split(" ")[0]]
    console.print(Panel(data["theory"], title=f"[bold green]Teoria: {data['title']}[/bold green]"))
    Prompt.ask("\n[bold yellow]Naciśnij ENTER, by przejść do quizu...[/bold yellow]")

    score = 0
    total = len(data["questions"])
    for idx, q_item in enumerate(data["questions"]):
        ans = questionary.select(f"Pytanie {idx + 1}/{total}: {q_item['q']}", choices=q_item["choices"]).ask()
        if ans == q_item["ans"]:
            console.print("[bold green]✅ Dobrze![/bold green]\n")
            score += 1
        else:
            console.print(f"[bold red]❌ Źle![/bold red] Odp: {q_item['ans']}\n")
    console.print(f"[bold cyan]Wynik: {score}/{total}[/bold cyan]")
    time.sleep(2)

def exam_mode():
    console.print(Panel.fit("[bold red]🚨 PRÓBNY EGZAMIN ISTQB 🚨[/bold red]"))
    start = Prompt.ask("Wpisz 'START' (lub anuluj)")
    if start.upper() != 'START': return

    all_qs = [q for v in DATA.values() for q in v["questions"]]
    exam_qs = random.sample(all_qs, min(len(all_qs), 40))
    score = 0
    for idx, q_item in enumerate(exam_qs):
        ans = questionary.select(f"[Q {idx+1}/{len(exam_qs)}] {q_item['q']}", choices=q_item["choices"]).ask()
        if ans == q_item["ans"]: score += 1
    
    console.print(f"\nZdobyte punkty: {score} na {len(exam_qs)}")
    if score >= (0.65 * len(exam_qs)): console.print("[bold green]🏆 ZDAŁEŚ[/bold green]")
    else: console.print("[bold red]💀 NIE ZDAŁEŚ[/bold red]")
    time.sleep(3)

def main():
    while True:
        os.system('clear')
        display_welcome()
        choice = questionary.select("Tryb:", choices=["📖 NAUKA", "🎓 EGZAMIN", "🚪 Wyjście"]).ask()
        if choice.startswith("📖"): learn_mode()
        elif choice.startswith("🎓"): exam_mode()
        else: break

if __name__ == "__main__":
    main()
