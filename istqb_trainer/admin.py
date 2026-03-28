import sqlite3
import questionary
from rich.console import Console
from rich.panel import Panel

console = Console()

def get_db():
    import os
    db_path = os.path.join(os.path.dirname(__file__), "data", "istqb_knowledge.db")
    return sqlite3.connect(db_path)

def admin_menu():
    while True:
        choice = questionary.select(
            "⚙️ PANEL ADMINISTRATORA (Zarządzanie Danymi/CRUD)",
            choices=[
                "1. Słownik Pojęć (Edycja Definicji/Dodawanie)",
                "2. Sylabus ISTQB (Edycja Treści/Dodawanie)",
                "3. Pytania Quizu (Modyfikacja/Dodawanie/Kasacja)",
                "4. 🚪 Wyjdź do Menu Głównego"
            ]
        ).ask()

        if not choice or choice.startswith("4"):
            break
        elif choice.startswith("1"):
            edit_glossary()
        elif choice.startswith("2"):
            edit_syllabus()
        elif choice.startswith("3"):
            edit_questions()

def edit_glossary():
    conn = get_db()
    c = conn.cursor()
    while True:
        c.execute("SELECT id, term, definition FROM glossary ORDER BY term ASC")
        terms = c.fetchall()
        
        # Paginated limit? No, questionary handles huge lists perfectly
        choices = [f"{t[1]}" for t in terms] + ["➕ [Nowe Pojęcie]", "🚪 [Wróć]"]
        term_choice = questionary.select("Wybierz pojęcie z Glosariusza (Wpisz literę na klawiaturze by szukać!):", choices=choices).ask()
        
        if not term_choice or term_choice == "🚪 [Wróć]":
            break
        elif term_choice == "➕ [Nowe Pojęcie]":
            nowe = questionary.text("Podaj nowe pojęcie:").ask()
            if nowe:
                df = questionary.text("Podaj definicję pojecia:").ask()
                c.execute("INSERT INTO glossary (term, definition) VALUES (?, ?)", (nowe, df))
                conn.commit()
                console.print("[green]✅ Nowe pojęcie dodano do Słownika![/green]")
        else:
            t = next(x for x in terms if x[1] == term_choice)
            console.print(Panel(t[2], title=f"📗 {t[1]}", border_style="cyan"))
            action = questionary.select("Co chcesz zrobić?", choices=["✏️ Zmień definicję", "❌ Usuń pojęcie", "Wróć"]).ask()
            if action == "✏️ Zmień definicję":
                new_def = questionary.text("Nowa definicja:", default=t[2]).ask()
                if new_def:
                    c.execute("UPDATE glossary SET definition = ? WHERE id = ?", (new_def, t[0]))
                    conn.commit()
                    console.print("[green]✅ Zaktualizowano definicję wpisu![/green]")
            elif action == "❌ Usuń pojęcie":
                confirm = questionary.confirm(f"Na pewno usunąć '{t[1]}' ze Słownika?").ask()
                if confirm:
                    c.execute("DELETE FROM glossary WHERE id = ?", (t[0],))
                    conn.commit()
                    console.print("[red]✅ Pojęcie wymazano z bazy.[/red]")
    conn.close()

def edit_syllabus():
    conn = get_db()
    c = conn.cursor()
    while True:
        c.execute("SELECT id, subchapter_number, k_level, content FROM syllabus_sections ORDER BY chapter_id, id ASC")
        secs = c.fetchall()
        
        choices = [f"{s[1]} ({s[2]})" for s in secs] + ["➕ [Dodaj Nową Sekcję]", "🚪 [Wróć]"]
        s_choice = questionary.select("Wybierz Podrozdział Sylabusa:", choices=choices).ask()
        
        if not s_choice or s_choice == "🚪 [Wróć]":
            break
        elif s_choice == "➕ [Dodaj Nową Sekcję]":
            sub = questionary.text("Numer podrozdziału (np. 1.1.2 Nowy Moduł):").ask()
            kl = questionary.text("Poziom nauczania (K1/K2/K3):").ask()
            ct = questionary.text("Treść Sylabusa:").ask()
            if sub and ct:
                # Wpychamy w domyślny 1 chapter
                c.execute("INSERT INTO syllabus_sections (chapter_id, subchapter_number, k_level, content) VALUES (1, ?, ?, ?)", (sub, kl, ct))
                conn.commit()
                console.print("[green]✅ Dodano do bazy wiedzy![/green]")
        else:
            s_data = next(x for x in secs if f"{x[1]} ({x[2]})" == s_choice)
            
            # Print content preview
            snippet = s_data[3] if len(s_data[3]) < 500 else s_data[3][:500] + "...\n[Czytaj dalej - wejdź w Edytuj]"
            console.print(Panel(snippet, title=f"📘 Teoria u Źródła: {s_data[1]} (Poziom {s_data[2]})", border_style="blue"))
            
            action = questionary.select("Akcja administracyjna:", choices=["✏️ Edytuj/Czytaj Całą Treść", "❌ Usuń Sekcję", "Wróć"]).ask()
            if action == "✏️ Edytuj/Czytaj Całą Treść":
                # Używamy default, co powoduje wyświetlenie w całości i opcję edycji tego ciągu
                new_text = questionary.text("Teoria (Używaj Strzałek by przewijać, Enter by zatwierdzić, żeby przejść do nowej linii użyj np. spacji+enter w zalezności od terminala):", default=s_data[3]).ask()
                if new_text and new_text != s_data[3]:
                    c.execute("UPDATE syllabus_sections SET content = ? WHERE id = ?", (new_text, s_data[0]))
                    conn.commit()
                    console.print("[green]✅ Poprawiono literówki w Sylabusie![/green]")
            elif action == "❌ Usuń Sekcję":
                c.execute("DELETE FROM syllabus_sections WHERE id = ?", (s_data[0],))
                conn.commit()
                console.print("[red]Usunięto sekcję z bazy wiedzy.[/red]")
    conn.close()

def edit_questions():
    conn = get_db()
    c = conn.cursor()
    while True:
        c.execute("SELECT id, source, question_text, correct_answer_letter FROM questions ORDER BY id ASC")
        qs = c.fetchall()
        
        choices = [f"[ID:{q[0]}] {q[2][:50]}... (Odp: {q[3]})" for q in qs] + ["➕ [Dodaj Nowe Własne Pytanie]", "🚪 [Wróć]"]
        q_choice = questionary.select("Zarządzaj Bazą Zapytań ISTQB:", choices=choices).ask()
        
        if not q_choice or q_choice == "🚪 [Wróć]":
            break
        elif q_choice == "➕ [Dodaj Nowe Własne Pytanie]":
            txt = questionary.text("Treść Pytania:").ask()
            if txt:
                ans = questionary.text("Poprawna Odpowiedź (np. c):").ask()
                c.execute("INSERT INTO questions (chapter_id, source, learning_objective, question_text, correct_answer_letter) VALUES (1, 'Vłasne', 'FL-0.0', ?, ?)", (txt, ans))
                new_id = c.lastrowid
                
                # Dodawanie wyborów A-D
                for letter in ["a", "b", "c", "d"]:
                    ch_t = questionary.text(f"Podaj wariant {letter}):").ask()
                    c.execute("INSERT INTO choices (question_id, letter, choice_text) VALUES (?, ?, ?)", (new_id, letter, ch_t))
                conn.commit()
                console.print("[green]✅ Nowe pytanko quizowe wbite do bazy![/green]")
        else:
            q_id = int(q_choice.split("]")[0].replace("[ID:", ""))
            q_data = next(x for x in qs if x[0] == q_id)
            
            c.execute("SELECT letter, choice_text FROM choices WHERE question_id = ?", (q_id,))
            ch_list = c.fetchall()
            
            warianty = "\n".join([f"{ch[0]}) {ch[1]}" for ch in ch_list])
            console.print(Panel(f"{q_data[2]}\n\n[Warianty]:\n{warianty}", title=f"Pytanie ID: {q_id} | Set: {q_data[1]} | Klucz: '{q_data[3]}'", border_style="magenta"))
            
            action = questionary.select("Zmień coś w Pytaniu:", choices=["✏️ Zmień Klucz Odpowiedzi", "✏️ Zmień Treść", "❌ Skasuj to Pytanie (Odrzuć)", "Wróć"]).ask()
            
            if action == "✏️ Zmień Klucz Odpowiedzi":
                new_ans = questionary.text("Wpisz poprawną literę np. 'b' lub 'a, e':", default=q_data[3]).ask()
                if new_ans:
                    c.execute("UPDATE questions SET correct_answer_letter = ? WHERE id = ?", (new_ans, q_id))
                    conn.commit()
                    console.print("[green]✅ Nadpisano oficjalny klucz rozwiązania![/green]")
            elif action == "✏️ Zmień Treść":
                new_txt = questionary.text("Nowa treść pytania:", default=q_data[2]).ask()
                if new_txt:
                    c.execute("UPDATE questions SET question_text = ? WHERE id = ?", (new_txt, q_id))
                    conn.commit()
                    console.print("[green]✅ Przepisano usterkę w tekście pytania![/green]")
            elif action == "❌ Skasuj to Pytanie (Odrzuć)":
                if questionary.confirm("Na pewno? Kasacja kaskadowa z choices.").ask():
                    c.execute("DELETE FROM choices WHERE question_id = ?", (q_id,))
                    c.execute("DELETE FROM questions WHERE id = ?", (q_id,))
                    conn.commit()
                    console.print("[red]Wymazano śmieciowe pytanie![/red]")
    conn.close()
