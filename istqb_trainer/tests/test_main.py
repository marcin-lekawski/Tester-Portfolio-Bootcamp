import pytest
import sqlite3
import main
import database_setup

def test_save_result_logic(mock_db_path):
    """
    Integracyjny test funkcji podliczającej punkty w głównym procesie.
    Test symuluje sztuczne zagranie przez gracza i liczy % asertywnie.
    """
    # 0. Przygotowanie izolowanej bazy
    database_setup.create_database()
    
    # 1. Wywołanie na sztywno sztucznej logiki (Gracz zdobywa 35/40, Egzamin Mode)
    main.save_result("MockExam", 35, 40)
    main.save_result("Nauka-Rozdzial1", 5, 10)
    
    # 2. Odczytanie wstrzykniętych danych z RAMu (Bazy Fixture)
    conn = sqlite3.connect(mock_db_path)
    cur = conn.cursor()
    cur.execute("SELECT mode, score, total_questions, percentage FROM exam_results ORDER BY id ASC")
    rows = cur.fetchall()
    
    # 3. Zestaw ostrych asercji biznesowych
    assert len(rows) == 2, "Metoda zapisu statystyk failuje, bo zrzuciła błędną ilość kolumn!"
    
    row_exam = rows[0]
    assert row_exam[0] == "MockExam"
    assert row_exam[1] == 35
    assert row_exam[2] == 40
    assert row_exam[3] == 87.5  # Wiarygodny procesor matematyczny: (35/40) * 100
    
    row_learn = rows[1]
    assert row_learn[0] == "Nauka-Rozdzial1"
    assert row_learn[3] == 50.0 # 5 z 10 to punktowo 50%
