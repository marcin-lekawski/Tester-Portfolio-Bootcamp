import time
import os
import random
import sqlite3
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

# Importujemy nowy moduł CRUD
try:
    import admin
    import knowledge_base
except ImportError:
    pass # Obsługa błędu gdyby skrypt był uruchamiany dziwnie z wewnątrz

console = Console()
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "istqb_knowledge.db")

def get_db_data():
    if not os.path.exists(DB_PATH):
        return {}
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("SELECT id, chapter_number, title, theory FROM chapters")
    except sqlite3.OperationalError:
        conn.close()
        return {}
        
    chapters = {}
    for row in c.fetchall():
        chapters[str(row[1])] = {
            "id": row[0],
            "title": row[2],
            "theory": row[3],
            "questions": []
        }
    
    c.execute("SELECT id, chapter_id, question_text, correct_answer_letter FROM questions")
    qs = c.fetchall()
    
    for q_row in qs:
        q_id, chap_id, q_text, ans_letter = q_row
        
        c.execute("SELECT letter, choice_text FROM choices WHERE question_id=?", (q_id,))
        choices_raw = c.fetchall()
        choices = [f"{ch[0]}) {ch[1]}" for ch in choices_raw]
        
        for ch_key, ch_data in chapters.items():
            if ch_data["id"] == chap_id:
                correct_letters = [l.strip().lower() for l in ans_letter.split(",")]
                
                ch_data["questions"].append({
                    "q": q_text,
                    "choices": choices,
                    "ans_letters": correct_letters,
                    "ans_raw": ans_letter
                })
    conn.close()
    return chapters

def save_result(mode, score, total):
    if total == 0:
        return
    pct = round((score / total) * 100, 2)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO exam_results (mode, score, total_questions, percentage)
        VALUES (?, ?, ?, ?)
    """, (mode, score, total, pct))
    conn.commit()
    conn.close()

def display_welcome():
    console.print(Panel.fit("[bold cyan]🎓 ISTQB Foundation Level 4.0.1 - INTERAKTYWNY TRENER (V 1.3.1)[/bold cyan]\n"
                            "Wersja Hybryda - Moduł Separacji Danych",
                            border_style="cyan"))

def do_quiz_question(idx, total_qs, q_item):
    console.print(Panel(q_item['q'], title=f"[bold cyan]Pytanie {idx}/{total_qs}[/bold cyan]", border_style="yellow"))
    
    is_multi = len(q_item["ans_letters"]) > 1
    
    if is_multi:
        console.print("[dim italic]To pytanie wymaga zanzaczenia kilku wariantów! Używaj SPACJI by zaznaczyć, ENTER by potwierdzić.[/dim italic]")
        answer = questionary.checkbox(
            "Zaznacz poprawne odpowiedzi:",
            choices=q_item["choices"]
        ).ask()
        
        if not answer:
            return 0
            
        selected_letters = [a.split(")")[0].strip().lower() for a in answer]
        selected_letters.sort()
        correct_sorted = sorted(q_item["ans_letters"])
        
        if selected_letters == correct_sorted:
            console.print("[bold green]✅ Dobrze![/bold green]\n")
            return 1
        else:
            console.print(f"[bold red]❌ Źle![/bold red] Poprawna odpowiedź: {q_item['ans_raw']}\n")
            return 0

    else:
        options = q_item["choices"] + ["🚪 Zakończ quiz i podlicz"]
        answer = questionary.select(
            "Wybierz poprawną odpowiedź (lub wyjdź):",
            choices=options
        ).ask()

        if answer is None or answer == "🚪 Zakończ quiz i podlicz":
            return -1

        ans_letter_picked = answer.split(")")[0].strip().lower()
        if ans_letter_picked in q_item["ans_letters"]:
            console.print("[bold green]✅ Dobrze![/bold green]\n")
            return 1
        else:
            console.print(f"[bold red]❌ Źle![/bold red] Poprawna odpowiedź: {q_item['ans_raw']}\n")
            return 0

def learn_mode(data):
    if not data:
        console.print("[red]Brak danych. Odpal najpierw skrypty konfiguracyjne SQL![/red]")
        time.sleep(2)
        return

    chap = questionary.select(
        "Wybierz rozdział do nauki by losować pytania:",
        choices=[f"{k} - {v['title']}" for k,v in data.items() if v['questions']] + ["Wróć"]
    ).ask()

    if chap is None or chap == "Wróć":
        return

    chap_idx = chap.split(" ")[0]
    ch_data = data[chap_idx]

    score = 0
    total_qs = len(ch_data["questions"])
    if total_qs == 0:
        return

    qs_sample = ch_data["questions"]
    random.shuffle(qs_sample)
    questions_answered = 0

    for idx, q_item in enumerate(qs_sample):
        res = do_quiz_question(idx+1, total_qs, q_item)
        if res == -1:
            console.print("[yellow]Przerwano na życzenie użytkownika. Zapisuję obecny wynik![/yellow]")
            break
        questions_answered += 1
        if res == 1:
            score += 1

    if questions_answered > 0:
        console.print(f"[bold cyan]Wynik częściowy: {score}/{questions_answered}[/bold cyan]")
        save_result(f"Nauka (Rozdział {chap_idx})", score, questions_answered)
        
    time.sleep(2)

def exam_mode(data):
    if not data:
        console.print("[red]Brak danych. Odpal najpierw skrypty konfiguracyjne SQL![/red]")
        time.sleep(2)
        return

    console.print(Panel.fit("[bold red]🚨 PRÓBNY EGZAMIN ISTQB V4.0 (Z BAZY SQL) 🚨[/bold red]\n"
                            "- 40 Pytan (według limitów z pliku wytycznych)\n"
                            "- Skrypt odporny na oszustwa\n"
                            "- Egzamin z zegarem bez drogi ucieczki!"))
    
    start = Prompt.ask("Wpisz 'START', by rozpocząć (lub cokolwiek by wyjść)")
    if getattr(start, 'upper', lambda: '')() != 'START': return

    all_questions = []
    for k, v in data.items():
        all_questions.extend(v["questions"])
    
    exam_qs = random.sample(all_questions, min(len(all_questions), 40))
    score = 0
    start_time = time.time()

    for idx, q_item in enumerate(exam_qs):
        os.system('clear')
        console.print(Panel(q_item['q'], title=f"[bold red]Q {idx+1}/{len(exam_qs)}[/bold red]", border_style="red"))
        
        is_multi = len(q_item["ans_letters"]) > 1
        if is_multi:
            console.print("[dim]Pytanie wielokrotnego wyboru (Używaj Spacji)[/dim]")
            answer = questionary.checkbox("Twój wybór:", choices=q_item["choices"]).ask()
            if not answer: continue
            selected = [a.split(")")[0].strip().lower() for a in answer]
            selected.sort()
            correct = sorted(q_item["ans_letters"])
            if selected == correct: score += 1
        else:
            ans = questionary.select("Twój wybór:", choices=q_item["choices"]).ask()
            if ans is None:
                console.print("[red]Pominięto pytanie (odpowiedź pusta)![/red]")
                time.sleep(1)
                continue
            picked = ans.split(")")[0].strip().lower()
            if picked in q_item["ans_letters"]:
                score += 1

    end_time = time.time()
    duration = round((end_time - start_time) / 60, 2)
    
    os.system('clear')
    console.print("\n[bold]========== WYNIK EGZAMINU ==========[/bold]")
    console.print(f"Zdobyte punkty: {score} na {len(exam_qs)}")
    console.print(f"Zajęło Ci to: {duration} minut\n")
    
    save_result("Egzamin", score, len(exam_qs))
    
    if score >= (0.65 * len(exam_qs)):
        console.print("[bold green]🏆 ZDAŁEŚ (PASS)[/bold green]")
    else:
        console.print("[bold red]💀 NIE ZDAŁEŚ (FAIL)[/bold red]")
    time.sleep(4)

def show_stats():
    os.system('clear')
    if not os.path.exists(DB_PATH):
        console.print("[red]Brak bazy danych![/red]")
        time.sleep(2)
        return
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("SELECT id, mode, score, total_questions, percentage, timestamp_taken FROM exam_results ORDER BY id DESC LIMIT 15")
        rows = c.fetchall()
    except sqlite3.OperationalError:
        rows = []
    conn.close()

    if not rows:
        console.print("[yellow]Nie masz jeszcze zapisanej na swoim koncie żadnej historii podejść.[/yellow]")
        time.sleep(2)
        return

    table = Table(title="[bold]📊 Historia Twoich Podejść (Ostatnie 15)[/bold]")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Data", style="cyan")
    table.add_column("Rozdział/Tryb", style="magenta")
    table.add_column("Wynik", justify="right")
    table.add_column("%", justify="right", style="bold green")

    for r in rows:
        dt_str = r[5]
        score_str = f"{r[2]}/{r[3]}"
        pct_color = "green" if r[4] >= 65 else "red"
        pct_str = f"[{pct_color}]{r[4]}%[/{pct_color}]"
        table.add_row(str(r[0]), dt_str, r[1], score_str, pct_str)

    console.print(table)
    Prompt.ask("\n[bold dim]Naciśnij ENTER, by wrócić do Menu[/bold dim]")

def main():
    while True:
        os.system('clear')
        display_welcome()
        
        db_data = get_db_data()
        qs_count = sum(len(d["questions"]) for d in db_data.values())
        console.print(f"[bold dim]Baza danych: Aktywne {qs_count} pytań w pamięci.[/bold dim]\n")

        choice = questionary.select(
            "📍 Wybierz tryb działania:",
            choices=[
                "📚 Tryb: BAZA WIEDZY (Czytanie Sylabusa i Słownika)",
                "📖 Tryb: INTERAKTYWNA NAUKA (Szybkie Quizy by Rozdział)",
                "🎓 Tryb: EGZAMIN (Seryjny mock egzaminacyjny v4.0.1)",
                "📊 Tryb: STATYSTYKI (Moje postępy)",
                "⚙️ Tryb: PANEL ADMINISTRATORA (Edycja Bazy & CRUD)",
                "🚪 Wyjdź"
            ]
        ).ask()

        if choice and choice.startswith("📚"):
            knowledge_base.kb_menu()
        elif choice and choice.startswith("📖"):
            learn_mode(db_data)
        elif choice and choice.startswith("🎓"):
            exam_mode(db_data)
        elif choice and choice.startswith("📊"):
            show_stats()
        elif choice and choice.startswith("⚙️"):
            admin.admin_menu()
        else:
            console.print("[bold cyan]Koniec treningu. Do zobaczenia jutro![/bold cyan]")
            break

if __name__ == "__main__":
    main()
