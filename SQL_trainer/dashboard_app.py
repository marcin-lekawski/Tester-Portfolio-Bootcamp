import sqlite3
import os
from typing import Any, List, Tuple
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Static, TextArea, DataTable, Tree, Label, ContentSwitcher, Markdown, Button
from textual.screen import ModalScreen
from textual import events

from curriculum import CURRICULUM, CHEAT_SHEET_MD
import database_setup
import progress_manager
import quest_data

DB_PATH = "D&D_sandbox.db"

ASCII_ERD = """
# 🗺️ Mapa Główna (Corporate Database System ERD)

```text
┌────────────────────┐       ┌────────────────────────┐
│    DEPARTMENTS     │       │     PROJECTS           │
├────────────────────┤       ├────────────────────────┤
│ 🔑 id (PK)         │       │ 🔑 id (PK)             │
│ ⚪ name            │       │ ⚪ name                │
│ ⚪ location        │       │ ⚪ start_date          │
│ ⚪ budget          │       │ ⚪ status              │
└─────────┬──────────┘       └─────────┬──────────────┘
          │ 1                            │ 1
          │                              │
          │ N                            │ N
┌─────────▼──────────┐       ┌─────────▼──────────────┐
│     EMPLOYEES      │   1   │ EMPLOYEE_PROJECTS      │
├────────────────────┤◄──────┤ (Tabela mostkowa M:N)  │
│ 🔑 id (PK)         │   N   ├────────────────────────┤
│ ⚪ first_name       │       │ 🗝️ employee_id (FK)    │
│ ⚪ last_name        │       │ 🗝️ project_id (FK)     │
│ ⚪ email            │       │ ⚪ hours_allocated     │
│ ⚪ salary           │       └────────────────────────┘
│ 🗝️ department_id ──┘       
└────┬───────────┬───┘       
     │ 1         │ 1
     │           │
     │ N         │ N
┌────▼───────┐ ┌─▼──────────────────┐
│ HARDWARE   │ │ CERTIFICATIONS     │
├────────────┤ ├────────────────────┤
│ 🔑 id (PK) │ │ 🔑 id (PK)         │
│ 🗝️ emp_id │ │ 🗝️ employee_id (FK)│
│ ⚪ model   │ │ ⚪ cert_name       │
│ ⚪ status  │ │ ⚪ valid_until     │
└────────────┘ └────────────────────┘
```
**Legenda Architektury:** `PK` = Primary Key (Główna Unikalna Oś), `FK` = Foreign Key (Klucz Obcy, czyli strzałka wędrująca do rodzica).
"""

class ERDModal(ModalScreen):
    """Pływające wielkie okno z Mapą Architektury Bazy Danych"""
    def compose(self) -> ComposeResult:
        with Vertical(id="erd_dialog"):
            yield Markdown(ASCII_ERD, id="erd_md")
            yield Label("\n[dim]Naciśnij pojedynczy klawisz ESCAPE by zamknąć podgląd...[/dim]", id="close_hint")
            
    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.app.pop_screen()

class HintModal(ModalScreen):
    """Pływające okienko z podpowiedzią z wymuszonym paskiem przewijania"""
    def __init__(self, hint_text: str):
        super().__init__()
        self.hint_text = hint_text

    def compose(self) -> ComposeResult:
        with Vertical(id="hint_dialog"):
            yield Label("[bold cyan]💡 Wskazówka Ratunkowa:[/bold cyan]\n", id="hint_label")
            yield Label(self.hint_text, id="theory_label")
            yield Label("\n[dim]Naciśnij ESC by ukryć...[/dim]", id="close_hint")
            
    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.app.pop_screen()

class QuestSummaryScreen(ModalScreen):
    """Pływające wielkie okno z podsumowaniem testu na Arenie"""
    def __init__(self, summary_md: str):
        super().__init__()
        self.summary_md = summary_md

    def compose(self) -> ComposeResult:
        with Vertical(id="erd_dialog"):
            yield Markdown(self.summary_md, id="quest_summary_md")
            yield Label("\n[dim]Naciśnij ESCAPE by zamknąć Raport...[/dim]", id="close_hint")
            
    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.app.pop_screen()

class SQLDashboardApp(App):
    """Złożony edukacyjny Dashboard SQL podzielony na drzewo nawigacji i strefę operacyjną."""
    
    CSS = """
    #main_layout {
        height: 100%;
    }
    #sidebar {
        width: 30%;
        height: 100%;
        border-right: solid vkey;
        dock: left;
        background: $surface;
    }
    #switcher {
        width: 70%;
        height: 100%;
    }
    #workspace_io {
        height: 100%;
    }
    #theory_view {
        width: 100%;
        height: 100%;
        padding: 1 4;
        overflow-y: auto;
    }
    Markdown {
        max-width: 100%;
        width: 100%;
    }
    #task_panel {
        height: 25%;
        border: solid cyan;
        padding: 1;
        background: $surface;
        overflow-y: auto;
    }
    #quest_nav_bar {
        height: 3;
        padding: 0 1;
        background: $primary-darken-3;
        border-bottom: solid green;
    }
    #quest_nav_bar Button {
        margin-right: 2;
        min-width: 15;
    }
    #editor_zone {
        height: 30%;
    }
    #placeholder_label {
        color: gray;
        padding-left: 2;
        background: $boost;
    }
    #sql_input {
        border: solid green;
    }
    #sql_output {
        height: 45%;
        border: solid yellow;
    }

    /* Modal Styling */
    #hint_dialog {
        padding: 2 4;
        width: 60%;
        height: 40%;
        border: thick $primary;
        background: $surface;
        align: center middle;
    }
    #erd_dialog {
        padding: 2 4;
        width: 80%;
        height: 90%;
        border: thick $secondary;
        background: $surface;
        align: center middle;
        overflow-y: auto;
    }
    """
    
    BINDINGS = [
        ("f2", "show_erd", "Mapa ERD Bazy [F2]"),
        ("f4", "show_hint", "Wskazówka [F4]"),
        ("f6", "toggle_placeholder", "Poprzednie / Ukryj Instrukcję [F6]"),
        ("f7", "prev_quest", "Poprz. Pyt [F7]"),
        ("f8", "next_quest", "Nastę. Pyt [F8]"),
        ("f9", "finish_quest", "Zakończ Rajd [F9]"),
        ("f5", "execute_sql", "WYKONAJ SQL [F5]"),
        ("ctrl+q", "quit", "Wyjście")
    ]

    def __init__(self):
        super().__init__()
        self.current_mission = None
        self.current_mission_node = None
        self.is_quest_mode = False
        self.quest_questions = []
        self.current_quest_idx = 0
        self.quest_answers = {}

    def compose(self) -> ComposeResult:
        yield Header()
        
        with Horizontal(id="main_layout"):
            yield Tree("KURS SQL (Tester/DBA)", id="sidebar")
            
            with ContentSwitcher(initial="workspace_io", id="switcher"):
                with Vertical(id="theory_view"):
                    yield Markdown("", id="theory_md")
                
                with Vertical(id="workspace_io"):
                    with Horizontal(id="quest_nav_bar"):
                        yield Button("⬅️ Wstecz [F7]", id="btn_f7", variant="primary")
                        yield Button("💾 Zapisz Kod [F5]", id="btn_f5", variant="success")
                        yield Button("Dalej [F8] ➡️", id="btn_f8", variant="primary")
                        yield Button("🔥 Zakończ Rajd [F9]", id="btn_f9", variant="error")
                        
                    yield Markdown("Wybierz moduł z lewego menu by rozpocząć...", id="task_panel")
                    
                    with Vertical(id="editor_zone"):
                        yield Label("Wpisz zapytanie SQL i naciśnij F5 by wykonać...", id="placeholder_label")
                        yield TextArea(language="sql", id="sql_input")
                        
                    yield DataTable(id="sql_output")
                
        yield Footer()

    def on_mount(self) -> None:
        database_setup.create_fantasy_sandbox()
        progress_manager.init_state_db()
            
        self.title = "SQL Trainer PRO - Interaktywne RDBMS"
        self.query_one("#quest_nav_bar").display = False
        
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        
        tree = self.query_one(Tree)
        tree.root.expand()
        
        for ch_key, ch_data in CURRICULUM.items():
            chapter_node = tree.root.add(f"[bold white]{ch_data['title']}[/bold white]", expand=False)
            chapter_node.add_leaf("📚 Wstęp Teoretyczny", data={"type": "theory", "text": ch_data['chapter_theory']})
            for mission in ch_data['missions']:
                is_done = progress_manager.is_mission_completed(mission['id'])
                prefix = "[bold green][✓][/bold green]" if is_done else "[bold yellow][ ][/bold yellow]"
                chapter_node.add_leaf(f"{prefix} Zadanie {mission['id']}", data={"type": "mission", "mission_data": mission})

        tree.root.add_leaf("[bold gold1]📋 TABLICE INFORMACJI (Cheat-Sheet)[/bold gold1]", data={"type": "theory", "text": CHEAT_SHEET_MD})
        
        quest_node = tree.root.add("[bold red]🏰 QUESTY (RPG Style)[/bold red]", expand=True)
        quest_node.add_leaf("🗡️ Quest R1: Podstawy (15 Pyt.)", data={"type": "quest_start", "q_type": "R1"})
        quest_node.add_leaf("🗡️ Quest R2: Selekcje (15 Pyt.)", data={"type": "quest_start", "q_type": "R2"})
        quest_node.add_leaf("🗡️ Quest R3: Agregacje (15 Pyt.)", data={"type": "quest_start", "q_type": "R3"})
        quest_node.add_leaf("🗡️ Quest R4: Złączenia (15 Pyt.)", data={"type": "quest_start", "q_type": "R4"})
        quest_node.add_leaf("🐉 EPICKI QUEST (Całość 40 Pyt.)", data={"type": "quest_start", "q_type": "ALL"})

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        node_data = event.node.data
        if not node_data:
            return
            
        switcher = self.query_one(ContentSwitcher)
        
        if node_data["type"] == "theory":
            switcher.current = "theory_view"
            md_widget = self.query_one("#theory_md", Markdown)
            md_widget.update(node_data["text"])
            self.current_mission = None
            
        elif node_data["type"] == "mission":
            switcher.current = "workspace_io"
            self.load_mission(node_data["mission_data"], event.node)
            
        elif node_data["type"] == "quest_start":
            self.start_quest(node_data["q_type"])

    def start_quest(self, q_type: str) -> None:
        import random
        self.is_quest_mode = True
        self.quest_answers = {}
        self.current_quest_idx = 0
        self.current_mission = None
        
        if q_type == "ALL":
            all_q = []
            for k in quest_data.QUESTS:
                all_q.extend(quest_data.QUESTS[k])
            self.quest_questions = random.sample(all_q, min(40, len(all_q)))
        else:
            self.quest_questions = list(quest_data.QUESTS[q_type])
            random.shuffle(self.quest_questions)
            
        self.query_one("#quest_nav_bar").display = True
        switcher = self.query_one(ContentSwitcher)
        switcher.current = "workspace_io"
        self.load_quest_task()

    def load_quest_task(self) -> None:
        q = self.quest_questions[self.current_quest_idx]
        total = len(self.quest_questions)
        curr = self.current_quest_idx + 1
        
        text = f"# ⚔️ TABLICA QUESTA | Wyzwanie {curr} z {total}\n\n{q['task']}"
        
        panel = self.query_one("#task_panel", Markdown)
        panel.update(text)
        
        editor = self.query_one(TextArea)
        editor.text = self.quest_answers.get(self.current_quest_idx, "")
        editor.focus()
        
        self.query_one(DataTable).clear(columns=True)

    def action_prev_quest(self) -> None:
        if self.is_quest_mode and self.current_quest_idx > 0:
            self.current_quest_idx -= 1
            self.load_quest_task()

    def action_next_quest(self) -> None:
        if self.is_quest_mode and self.current_quest_idx < len(self.quest_questions) - 1:
            self.current_quest_idx += 1
            self.load_quest_task()
            
    def action_finish_quest(self) -> None:
        if self.is_quest_mode:
            self.evaluate_quest()

    def load_mission(self, mission: dict, node: Any) -> None:
        self.is_quest_mode = False
        self.current_mission = mission
        self.current_mission_node = node
        self.query_one("#quest_nav_bar").display = False
        text = f"# Wyzwanie nr {mission['id']}\n\n{mission['task']}"
        panel = self.query_one("#task_panel", Markdown)
        panel.update(text)
        
        editor = self.query_one(TextArea)
        editor.text = ""
        editor.focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "btn_f7":
            self.action_prev_quest()
        elif btn_id == "btn_f8":
            self.action_next_quest()
        elif btn_id == "btn_f9":
            self.action_finish_quest()
        elif btn_id == "btn_f5":
            self.action_execute_sql()

    def action_show_hint(self) -> None:
        if self.current_mission:
            self.push_screen(HintModal(self.current_mission['hint']))
            
    def action_show_erd(self) -> None:
        """Klawisz ratunkowy wywołujący Półprzezroczystą Mapę Architektury (UML ERD)"""
        self.push_screen(ERDModal())

    def action_toggle_placeholder(self) -> None:
        lbl = self.query_one("#placeholder_label", Label)
        lbl.display = not lbl.display

    def action_execute_sql(self) -> None:
        if not self.current_mission and not self.is_quest_mode:
            self.notify("Wybierz zadanie ze spisu przed próbą kompilacji!", severity="warning")
            return
            
        editor = self.query_one(TextArea)
        query = editor.text
        
        if not query.strip():
            return
            
        expected_query = self.current_mission['expected_sql'] if self.current_mission else self.quest_questions[self.current_quest_idx]['expected_sql']
        expected_is_select = expected_query.strip().upper().startswith(("SELECT", "WITH", "PRAGMA"))
        
        if expected_is_select:
            is_success, user_rows, user_cols = self.execute_and_display(query)
            if is_success:
                if self.is_quest_mode:
                    self.quest_answers[self.current_quest_idx] = query
                    self.notify("Zapisano wpis w Plecaku Osiągnięć. Edytuj go pod F5 lub strzelając [F8].", title="SZKIC ZAPISANY", timeout=2)
                else:
                    self.verify_mission(user_rows)
        else:
            # DML/DDL operations
            if self.is_quest_mode:
                self.quest_answers[self.current_quest_idx] = query
                self.notify("Kod DML/DDL zachowany w Plecaku. Zostanie zrzucony w pamięć i ewaluowany przy [F9]!", title="SZKIC ZAPISANY", timeout=3)
            else:
                self.verify_mission_dml(query, expected_query)

    def compare_dml_queries(self, user_sql: str, expected_sql: str) -> bool:
        try:
            source_conn = sqlite3.connect(DB_PATH)
            
            mem_a = sqlite3.connect(':memory:')
            source_conn.backup(mem_a)
            
            mem_b = sqlite3.connect(':memory:')
            source_conn.backup(mem_b)
            
            c_a = mem_a.cursor()
            c_a.executescript(expected_sql)
            
            c_b = mem_b.cursor()
            c_b.executescript(user_sql)
            
            c_a.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            tables_a = c_a.fetchall()
            
            c_b.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            tables_b = c_b.fetchall()
            
            if tables_a != tables_b:
                return False
                
            for table in tables_a:
                table_name = table[0]
                c_a.execute(f"SELECT * FROM {table_name}")
                rows_a = c_a.fetchall()
                
                c_b.execute(f"SELECT * FROM {table_name}")
                rows_b = c_b.fetchall()
                
                if set(rows_a) != set(rows_b) or len(rows_a) != len(rows_b):
                    return False
                    
            return True
        except sqlite3.Error:
            return False
        finally:
            if 'source_conn' in locals(): source_conn.close()
            if 'mem_a' in locals(): mem_a.close()
            if 'mem_b' in locals(): mem_b.close()

    def verify_mission_dml(self, user_query: str, expected_sql: str) -> None:
        is_correct = self.compare_dml_queries(user_query, expected_sql)
        
        table = self.query_one(DataTable)
        table.clear(columns=True)
        
        if is_correct:
            try:
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.executescript(user_query)
                conn.commit()
                conn.close()
                self.notify("✅ Doskonale! Baza została pomyślnie i trwale zmodyfikowana!", title="100% ZALICZONE!", timeout=5)
                progress_manager.mark_mission_completed(self.current_mission['id'])
                if hasattr(self, 'current_mission_node') and self.current_mission_node:
                    self.current_mission_node.label = f"[bold green][✓][/bold green] Zadanie {self.current_mission['id']}"
                    
                table.add_column("Sukces Operacji DML/DDL")
                table.add_row("Twardy zapis komendy ukończony. Plik D&D_sandbox.db zaktualizowany.")
            except sqlite3.Error as e:
                self.notify(f"Błąd podczas zapisu: {e}", severity="error")
        else:
            self.notify("Pudło! Zapytanie DML nie przyniosło odpowiednich rezultatów lub jest błędne. Spróbuj powtórnie!", title="Odrzucono!", severity="warning")
            table.add_column("Blokada Ewaluatora Ochronnego")
            table.add_row("Aplikacja bezpiecznie stłumiła błędną operację. Twoja oryginalna Baza danych przetrwała nietknięta.")

    def execute_and_display(self, query: str) -> Tuple[bool, List[tuple], List[str]]:
        table = self.query_one(DataTable)
        table.clear(columns=True)
        
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            
            if query.strip().upper().startswith(("SELECT", "WITH", "PRAGMA")):
                c.execute(query)
                rows = c.fetchall()
                cols = [description[0] for description in c.description]
                
                table.add_columns(*cols)
                for r in rows:
                    table.add_row(*[str(i) if i is not None else "NULL" for i in r])
                    
                return True, rows, cols
            else:
                table.add_column("Bezpieczeństwo Wykonania")
                table.add_row("Baza znajduje się w trybie ewaluacji testowej. Zapytanie DML nie wykonano na fizycznym pliku by chronić stan zapisu.")
                return False, [], []
                
        except sqlite3.Error as e:
            table.add_column("❌ Critical SQL Engine Error!")
            table.add_row(str(e))
            self.notify("Niekompilujący się Twór! Brak Średnika lub Błąd Składni.", title="BŁĄD PARSOWANIA", severity="error", timeout=4)
            return False, [], []
        finally:
            conn.close()

    def verify_mission(self, user_rows: List[tuple]) -> None:
        expected_sql = self.current_mission['expected_sql']
        
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute(expected_sql)
            expected_rows = c.fetchall()
            
            if set(user_rows) == set(expected_rows):
                self.notify("✅ Doskonale! Wynik zapytania dopasował się do Klucza Odpowiedzi! Wybierz kolejne strzałkami.", title="100% ZALICZONE!", timeout=5)
                progress_manager.mark_mission_completed(self.current_mission['id'])
                if hasattr(self, 'current_mission_node') and self.current_mission_node:
                    self.current_mission_node.label = f"[bold green][✓][/bold green] Zadanie {self.current_mission['id']}"
            else:
                self.notify("Pudło! Output wyprodukowany przez Twój algorytm różni się od narzuconego zadaniem.", title="Błędny Kod SQL", severity="warning")
                
        except Exception:
            pass
        finally:
            conn.close()

    def evaluate_quest(self) -> None:
        import sqlite3
        correct = 0
        total = len(self.quest_questions)
        summary = f"# 📜 WYNIK STARCIA NA ARENIE\n\nTwój Końcowy Wynik: X_SCORE_X / {total}\n\n---\n\n"
        
        for idx, q in enumerate(self.quest_questions):
            expected_sql = q['expected_sql']
            user_sql = self.quest_answers.get(idx, "").strip()
            
            is_ok = False
            if user_sql:
                is_select = expected_sql.strip().upper().startswith(("SELECT", "WITH", "PRAGMA"))
                if is_select:
                    try:
                        conn = sqlite3.connect(DB_PATH)
                        c = conn.cursor()
                        c.execute(expected_sql)
                        exp_rows = c.fetchall()
                        
                        c.execute(user_sql)
                        usr_rows = c.fetchall()
                        if set(exp_rows) == set(usr_rows) and len(exp_rows) == len(usr_rows):
                            is_ok = True
                    except Exception:
                        pass
                    finally:
                        conn.close()
                else:
                    is_ok = self.compare_dml_queries(user_sql, expected_sql)
                
            if is_ok:
                correct += 1
                summary += f"### ✅ Zadanie {idx+1}: ZALICZONE ŚPIEWAJĄCO\n"
            else:
                summary += f"### ❌ Zadanie {idx+1}: OBLANE\n\n"
                summary += f"**Twoja taktyka bojowa:**\n```sql\n{user_sql if user_sql else '-- BRAK ODPOWIEDZI --'}\n```\n"
                summary += f"**Oczekiwane Złote Złączenie SQL:**\n```sql\n{expected_sql}\n```\n"
            summary += "---\n"
            
        summary = summary.replace("X_SCORE_X", str(correct))
        self.is_quest_mode = False
        switcher = self.query_one(ContentSwitcher)
        switcher.current = "theory_view"
        self.query_one("#theory_md", Markdown).update("# Rajd Zakończony!\n\nSprawdź pojawiający się ekran ewaluacyjny by przeanalizować rany odniesione na Arenie!")
        self.push_screen(QuestSummaryScreen(summary))

if __name__ == "__main__":
    app = SQLDashboardApp()
    app.run()
