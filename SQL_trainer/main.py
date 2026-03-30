import sqlite3
import os
import sys
import questionary
from rich.table import Table

# Importy z pliku modulu graficznego (sklonowanego z ISTQB Trainera)
from terminal_ui import console, print_banner, print_error, print_success, print_info

DB_PATH = os.path.join(os.path.dirname(__file__), "sandbox.db")

def init_db():
    if not os.path.exists(DB_PATH):
        import database_setup
        database_setup.create_corporate_sandbox()

def run_query(query):
    """Przechwytuje i uruchamia testowe uderzenie po SQL"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(query)
        
        # Filtorwanie Selectow od Update'ow
        if query.strip().upper().startswith(("SELECT", "WITH", "PRAGMA")):
            rows = c.fetchall()
            if not rows:
                print_info("Zapytanie nie zwróciło żadnych wyników (Pusta Tabela lub restrykcyjny WHERE).")
                return

            # Dynamiczna generacja nagłówków Kolumn
            colnames = [description[0] for description in c.description]
            table = Table(show_header=True, header_style="bold magenta")
            for col in colnames:
                table.add_column(col)
            
            # Formatyzowanie outputu rekrodow
            for row in rows:
                table.add_row(*[str(item) if item is not None else "NULL" for item in row])
                
            console.print(table)
            print_success(f"Zwrócono rekordów: {len(rows)}")
        else:
            conn.commit()
            print_success(f"Operacja DML/DDL wykonana pomyślnie. Zmienionych wierszy: {c.rowcount}")
        
    except sqlite3.Error as e:
        # Bardzo wazne do edukacji - wypluwa czerwony błąd z silnika (np. zła syntaksa)
        print_error(f"{e}")
    finally:
        if 'conn' in locals():
            conn.close()

def interactive_loop():
    print_info("Wpisz swoje zapytanie SQL. Zakończ je średnikiem ';' i wciśnij ENTER.\nNapisz 'exit' by wyjść 'clear' aby wyczyścić konsolę.")
    buffer = ""
    while True:
        try:
            line = input("SQL> " if not buffer else "...> ")
        except (KeyboardInterrupt, EOFError):
            print()
            break
            
        if line.strip().lower() in ['exit', 'quit']:
            break
        if line.strip().lower() == 'clear':
            os.system('clear' if os.name == 'posix' else 'cls')
            print_banner()
            continue
            
        buffer += line + " "
        
        # Oczekiwanie na znak zakonczenia zapytania SQL, czyli stary potężny średnik 
        if ';' in buffer:
            queries = buffer.split(';')
            for q in queries[:-1]: 
                if q.strip():
                    run_query(q)
            # Zerowanie bufora testowego 
            buffer = queries[-1].strip()

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print_banner()
    init_db()
    
    while True:
        choice = questionary.select(
            "Wybierz moduł treningowy SQL:",
            choices=[
                "1. 💻 Wejdź do interaktywnej piaskownicy (Terminal SQL)",
                "2. 🔄 Zresetuj DB (Wyczyść tabelki i wgraj firmę od zera)",
                "3. 🎓 Rozpocznij Kurs SQL (Dashboard Edukacyjny TUI)",
                "4. 🚪 Wyjście"
            ]
        ).ask()
        
        if not choice or "4" in choice:
            console.print("[dim]Koniec zmiany w dziale HR... Do zobaczenia![/dim]")
            sys.exit(0)
            
        elif "1" in choice:
            interactive_loop()
            
        elif "2" in choice:
            import database_setup
            database_setup.create_corporate_sandbox()
            
        elif "3" in choice:
            import dashboard_app
            app = dashboard_app.SQLDashboardApp()
            app.run()
            # Po wyjściu z TUI, przywracamy clearowane menu
            os.system('clear' if os.name == 'posix' else 'cls')
            print_banner()

if __name__ == "__main__":
    main()
