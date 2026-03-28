import sqlite3
import questionary
from rich.console import Console
from rich.panel import Panel

console = Console()

def get_db():
    import os
    db_path = os.path.join(os.path.dirname(__file__), "data", "istqb_knowledge.db")
    return sqlite3.connect(db_path)

import terminal_ui

def admin_menu():
    style = terminal_ui.get_custom_style()
    while True:
        choice = questionary.select(
            "⚙️ PANEL ADMINISTRATORA (Zarządzanie Danymi/CRUD)",
            choices=[
                "1. Słownik Pojęć (Edycja Definicji/Dodawanie)",
                "2. Sylabus ISTQB (Edycja Treści/Dodawanie/Metadane)",
                "3. Pytania Quizu (Modyfikacja Wariantów/Dodawanie/Kasacja)",
                "4. 🚪 Wyjdź do Menu Głównego"
            ],
            style=style
        ).ask()

        if not choice or choice.startswith("4"):
            break
        elif choice.startswith("1"):
            edit_glossary(style)
        elif choice.startswith("2"):
            edit_syllabus(style)
        elif choice.startswith("3"):
            edit_questions(style)

def edit_glossary(style):
    conn = get_db()
    c = conn.cursor()
    while True:
        c.execute("SELECT id, term, definition FROM glossary ORDER BY term ASC")
        terms = c.fetchall()
        
        choices = [f"{t[1]}" for t in terms] + ["➕ [Nowe Pojęcie]", "🚪 [Wróć]"]
        term_choice = questionary.select(
            "Wybierz pojęcie z Glosariusza:", 
            choices=choices,
            style=style
        ).ask()
        
        if not term_choice or term_choice == "🚪 [Wróć]":
            break
        elif term_choice == "➕ [Nowe Pojęcie]":
            nowe = questionary.text("Podaj nowe pojęcie:").ask()
            if nowe:
                df = questionary.text("Podaj definicję pojęcia:", style=style).ask()
                c.execute("INSERT INTO glossary (term, definition) VALUES (?, ?)", (nowe, df))
                conn.commit()
                console.print("[green]✅ Dodano do Słownika![/green]")
        else:
            t = next(x for x in terms if x[1] == term_choice)
            action = terminal_ui.nano_pager(f"Glosariusz: {t[1]}", t[2], allow_edit=True)
            
            if action == 'edit':
                sub_action = questionary.select("Wybierz czynność:", choices=["✏️ Zmień definicję", "❌ Usuń pojęcie", "Wróć"], style=style).ask()
                if sub_action == "✏️ Zmień definicję":
                    new_def = questionary.text("Nowa definicja:", default=t[2], style=style).ask()
                    if new_def:
                        c.execute("UPDATE glossary SET definition = ? WHERE id = ?", (new_def, t[0]))
                        conn.commit()
                elif sub_action == "❌ Usuń pojęcie":
                    if questionary.confirm(f"Na pewno usunąć '{t[1]}' ze Słownika?").ask():
                        c.execute("DELETE FROM glossary WHERE id = ?", (t[0],))
                        conn.commit()
            elif action == 'menu':
                break
    conn.close()

def edit_syllabus(style):
    conn = get_db()
    c = conn.cursor()
    while True:
        c.execute("SELECT id, subchapter_number, k_level, content FROM syllabus_sections ORDER BY chapter_id, id ASC")
        secs = c.fetchall()
        
        choices = [f"{s[1]} ({s[2]})" for s in secs] + ["➕ [Dodaj Nową Sekcję]", "🚪 [Wróć]"]
        s_choice = questionary.select("Wybierz Podrozdział Sylabusa:", choices=choices, style=style).ask()
        
        if not s_choice or s_choice == "🚪 [Wróć]":
            break
        elif s_choice == "➕ [Dodaj Nową Sekcję]":
            sub = questionary.text(" Numer podrozdziału (np. 1.1.2 Nowy Moduł):", style=style).ask()
            kl = questionary.text(" Poziom nauczania (K1/K2/K3):", style=style).ask()
            ct = questionary.text(" Treść Sylabusa:", style=style).ask()
            if sub and ct:
                c.execute("INSERT INTO syllabus_sections (chapter_id, subchapter_number, k_level, content) VALUES (1, ?, ?, ?)", (sub, kl, ct))
                conn.commit()
        else:
            s_data = next(x for x in secs if f"{x[1]} ({x[2]})" == s_choice)
            
            action = terminal_ui.nano_pager(f"Edytor: {s_data[1]} (Poziom {s_data[2]})", s_data[3], allow_edit=True)
            
            if action == 'edit':
                sub_action = questionary.select("Zarządzaj Podrozdziałem:", choices=["✏️ Zmień Treść Sylabusa", "✏️ Zmień Metadane (Nagłówek/Poziom K)", "❌ Usuń Sekcję", "Wróć"], style=style).ask()
                if sub_action == "✏️ Zmień Treść Sylabusa":
                    new_text = questionary.text("Modyfikuj Treść:", default=s_data[3], style=style).ask()
                    if new_text and new_text != s_data[3]:
                        c.execute("UPDATE syllabus_sections SET content = ? WHERE id = ?", (new_text, s_data[0]))
                        conn.commit()
                elif sub_action == "✏️ Zmień Metadane (Nagłówek/Poziom K)":
                    new_title = questionary.text("Nagłówek:", default=s_data[1], style=style).ask()
                    new_k = questionary.text("Poziom:", default=s_data[2], style=style).ask()
                    if new_title and new_k:
                        c.execute("UPDATE syllabus_sections SET subchapter_number = ?, k_level = ? WHERE id = ?", (new_title, new_k, s_data[0]))
                        conn.commit()
                elif sub_action == "❌ Usuń Sekcję":
                    if questionary.confirm("Na pewno usunąć trwale ten podrozdział?").ask():
                        c.execute("DELETE FROM syllabus_sections WHERE id = ?", (s_data[0],))
                        conn.commit()
            elif action == 'menu':
                break
    conn.close()

def edit_questions(style):
    conn = get_db()
    c = conn.cursor()
    while True:
        c.execute("SELECT id, source, question_text, correct_answer_letter FROM questions ORDER BY id ASC")
        qs = c.fetchall()
        
        choices = [f"[ID:{q[0]}] {q[2][:50]}... (Odp: {q[3]})" for q in qs] + ["➕ [Dodaj Nowe Własne Pytanie]", "🚪 [Wróć]"]
        q_choice = questionary.select("Zarządzaj Pytaniami ISTQB:", choices=choices, style=style).ask()
        
        if not q_choice or q_choice == "🚪 [Wróć]":
            break
        elif q_choice == "➕ [Dodaj Nowe Własne Pytanie]":
            txt = questionary.text("Treść Pytania:", style=style).ask()
            if txt:
                ans = questionary.text("Poprawna Odpowiedź (np. c lub a, d):", style=style).ask()
                c.execute("INSERT INTO questions (chapter_id, source, learning_objective, question_text, correct_answer_letter) VALUES (1, 'Baza Osobista', 'FL-0.0', ?, ?)", (txt, ans))
                new_id = c.lastrowid
                
                for letter in ["a", "b", "c", "d"]:
                    ch_t = questionary.text(f"Podaj wariant {letter}):", style=style).ask()
                    c.execute("INSERT INTO choices (question_id, letter, choice_text) VALUES (?, ?, ?)", (new_id, letter, ch_t))
                conn.commit()
        else:
            q_id = int(q_choice.split("]")[0].replace("[ID:", ""))
            q_data = next(x for x in qs if x[0] == q_id)
            
            c.execute("SELECT id, letter, choice_text FROM choices WHERE question_id = ?", (q_id,))
            ch_list = c.fetchall()
            warianty_tekst = "\n".join([f"{ch[1]}) {ch[2]}" for ch in ch_list])
            
            full_text = f"TREŚĆ:\n{q_data[2]}\n\nWARIANTY:\n{warianty_tekst}\n\nKLUCZ POPRAWNY: {q_data[3]}"
            action = terminal_ui.nano_pager(f"Edytor Pytania [ID:{q_id}]", full_text, allow_edit=True)
            
            if action == 'edit':
                sub_action = questionary.select("Modyfikuj Pytanie:", choices=["✏️ Zmień Treść (Prompt)", "✏️ Zmień Konkretny Wariant (A/B/C/D)", "✏️ Zmień Klucz Odpowiedzi", "❌ Skasuj to Pytanie (Odrzuć)", "Wróć"], style=style).ask()
                
                if sub_action == "✏️ Zmień Treść (Prompt)":
                    new_txt = questionary.text("Treść pytania:", default=q_data[2], style=style).ask()
                    if new_txt:
                        c.execute("UPDATE questions SET question_text = ? WHERE id = ?", (new_txt, q_id))
                        conn.commit()
                elif sub_action == "✏️ Zmień Konkretny Wariant (A/B/C/D)":
                    v_choice = questionary.select("Wybierz wariant do edycji:", choices=[f"{ch[1]}) {ch[2]}" for ch in ch_list] + ["Wróć"], style=style).ask()
                    if v_choice != "Wróć":
                        ch_letter = v_choice.split(")")[0]
                        target_ch = next(x for x in ch_list if x[1] == ch_letter)
                        new_vt = questionary.text(f"Nowa treść {ch_letter}):", default=target_ch[2], style=style).ask()
                        if new_vt:
                            c.execute("UPDATE choices SET choice_text = ? WHERE id = ?", (new_vt, target_ch[0]))
                            conn.commit()
                elif sub_action == "✏️ Zmień Klucz Odpowiedzi":
                    new_ans = questionary.text("Nowy klucz (np. b):", default=q_data[3], style=style).ask()
                    if new_ans:
                        c.execute("UPDATE questions SET correct_answer_letter = ? WHERE id = ?", (new_ans, q_id))
                        conn.commit()
                elif sub_action == "❌ Skasuj to Pytanie (Odrzuć)":
                    if questionary.confirm("Usunąć pytanie permanentnie?").ask():
                        c.execute("DELETE FROM choices WHERE question_id = ?", (q_id,))
                        c.execute("DELETE FROM questions WHERE id = ?", (q_id,))
                        conn.commit()
            elif action == 'menu':
                break
    conn.close()
