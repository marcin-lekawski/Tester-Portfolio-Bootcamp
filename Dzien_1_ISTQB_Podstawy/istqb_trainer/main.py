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

# Baza Wiedzy (MVP) - zalążek z Rozdziału 1 i 2. 
# Jako zadanie z Pythona będziesz musiał stworzyć moduł rozszerzający to o pliki JSON!
DATA = {
    "1": {
        "title": "Podstawy testowania (Rozdział 1)",
        "theory": (
            "1.1. Cel testowania: Znajdowanie defektów, upewnianie się, że oprogramowanie spełnia wymagania, "
            "zmniejszanie ryzyka obniżenia jakości.\n"
            "1.2. Testowanie vs Debugowanie: Testowanie znajduje usterki (Testerzy/Narzędzia). Debugowanie je naprawia (Programiści).\n"
            "1.3. 7 Zasad Testowania:\n"
            "   1) Testowanie ujawnia usterki, ale nie dowodzi ich braku.\n"
            "   2) Testowanie gruntowne jest niemożliwe.\n"
            "   3) Wczesne testowanie oszczędza czas (Shift-Left).\n"
            "   4) Kumulowanie się defektów w modułach (Zasada Pareto).\n"
            "   5) Testowanie zależy od kontekstu (e-commerce testujemy inaczej niż system w samolocie).\n"
            "   6) Paradoks pestycydów (powtarzanie tych samych testów przestaje wykrywać błędy).\n"
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
                "choices": ["Uruchomienie aplikacji w celu znalezienia błędów", "Wykrycie defektów zanim powstanie kod (np. przez przegląd wymagań)", "Zautomatyzowanie klikania w GUI", "Zbadanie bazy danych produkcyjnej"],
                "ans": "Wykrycie defektów zanim powstanie kod (np. przez przegląd wymagań)"
            }
        ]
    },
    "2": {
        "title": "Testowanie w Cyklu Życia Oprogramowania (Rozdział 2)",
        "theory": (
            "2.1. Oprogramowanie rozwija się w modelach: Sekwencyjnych (V-Model, Waterfall) lub Iteracyjnych (Agile, Scrum).\n"
            "2.2. W Agile testowanie dzieje się na każdym etapie (Continuous Testing) i włącza się testerów bardzo wcześnie (Shift-Left).\n"
            "2.3. Testowanie potwierdzające (Re-testing): Sprawdzanie, czy konkretny zgłoszony błąd został na pewno usunięty.\n"
            "2.4. Testowanie regresyjne (Regression testing): Sprawdzanie, czy nowa zmiana lub błąd nie popsuły innej części systemu, która wcześniej działała."
        ),
        "questions": [
            {
                "q": "Developer zgłasza, że rzekomo usunął zgłoszonego przez Ciebie defektu na formularzu logowania. Jakie Testy teraz wykonasz?",
                "choices": ["Testy regresyjne", "Testy potwierdzające (re-testing)", "Testy wydajnościowe", "Testy jednostkowe"],
                "ans": "Testy potwierdzające (re-testing)"
            },
            {
                "q": "Dodano moduł 'Koszyk' w nowej wersji systemu, a przestał działać 'Moduł Płatności'. Czego tu zabrakło?",
                "choices": ["Wystarczających testów regresyjnych", "Testów akceptacyjnych użytkownika", "Debugowania", "Testów modułowych UI"],
                "ans": "Wystarczających testów regresyjnych"
            }
        ]
    }
}

def display_welcome():
    console.print(Panel.fit("[bold cyan]🎓 ISTQB Foundation Level 4.0.1 - INTERAKTYWNY TRENER[/bold cyan]\n"
                            "Wersja Kubuntu Terminal - Mentor QA Edition",
                            border_style="cyan"))

def learn_mode():
    chap = questionary.select(
        "Wybierz rozdział do nauki:",
        choices=[f"{k} - {v['title']}" for k,v in DATA.items()] + ["Wróć"]
    ).ask()

    if chap == "Wróć":
        return

    chap_idx = chap.split(" ")[0]
    data = DATA[chap_idx]

    console.print(Panel(data["theory"], title=f"[bold green]Teoria: {data['title']}[/bold green]"))
    Prompt.ask("\n[bold yellow]Naciśnij ENTER, by przejść do szybkiego quizu przyswajającego...[/bold yellow]")

    score = 0
    total = len(data["questions"])
    random.shuffle(data["questions"])

    for idx, q_item in enumerate(data["questions"]):
        answer = questionary.select(
            f"Pytanie {idx + 1}/{total}: {q_item['q']}",
            choices=q_item["choices"]
        ).ask()

        if answer == q_item["ans"]:
            console.print("[bold green]✅ Dobrze![/bold green]\n")
            score += 1
        else:
            console.print(f"[bold red]❌ Źle![/bold red] Poprawna odpowiedź: {q_item['ans']}\n")

    console.print(f"[bold cyan]Wynik częściowy: {score}/{total}[/bold cyan]")
    time.sleep(2)

def exam_mode():
    console.print(Panel.fit("[bold red]🚨 PRÓBNY EGZAMIN ISTQB V4.0 🚨[/bold red]\n"
                            "- 40 Pytan (według limitów z pliku wytycznych)\n"
                            "- 60 Minut czasu\n"
                            "- Zdajesz od 65% (min. 26/40 pkt)\n"
                            "[yellow]UWAGA:[/yellow] Wersja demonstracyjna pobiera pytania ze wszystkich sekcji bazy i losuje."))
    
    start = Prompt.ask("Wpisz 'START', by rozpocząć (lub anuluj)")
    if start.upper() != 'START': return

    all_questions = []
    for k, v in DATA.items():
        all_questions.extend(v["questions"])
    
    # Dla dema losujemy to co jest, w pełnej wersji byłoby 40
    exam_qs = random.sample(all_questions, min(len(all_questions), 40))
    score = 0
    start_time = time.time()

    for idx, q_item in enumerate(exam_qs):
        ans = questionary.select(
            f"[Q {idx+1}/{len(exam_qs)}] {q_item['q']}",
            choices=q_item["choices"]
        ).ask()
        if ans == q_item["ans"]: score += 1

    end_time = time.time()
    duration = round((end_time - start_time) / 60, 2)
    
    console.print("\n[bold]========== WYNIK EGZAMINU ==========[/bold]")
    console.print(f"Zdobyte punkty: {score} na {len(exam_qs)}")
    console.print(f"Zajęło Ci to: {duration} minut")
    
    if score >= (0.65 * len(exam_qs)):
        console.print("[bold green]🏆 ZDAŁEŚ (PASS)[/bold green]")
    else:
        console.print("[bold red]💀 NIE ZDAŁEŚ (FAIL)[/bold red]")
    time.sleep(3)

def main():
    while True:
        os.system('clear')
        display_welcome()
        choice = questionary.select(
            "📍 Wybierz tryb działania:",
            choices=[
                "📖 Tryb: NAUKA (Teoria + Szybkie Quizy by Rozdział)",
                "🎓 Tryb: EGZAMIN (Seryjny mock egzaminacyjny v4.0.1)",
                "🚪 Wyjdź"
            ]
        ).ask()

        if choice.startswith("📖"):
            learn_mode()
        elif choice.startswith("🎓"):
            exam_mode()
        else:
            console.print("[bold cyan]Koniec treningu. Do zobaczenia jutro![/bold cyan]")
            break

if __name__ == "__main__":
    main()
