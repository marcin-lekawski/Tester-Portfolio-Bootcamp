import pytest
import sqlite3
import database_setup

def test_database_creation(mock_db_path):
    """
    Asercja (Test) upewniająca się że konstruktor architektoniczny DB działa niezawodnie.
    """
    # Budowa struktury Test-Driven wg. założeń biznesowych
    database_setup.create_database()
    
    # Zapytanie do silnika o istniejące tabele
    conn = sqlite3.connect(mock_db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cur.fetchall()]
    
    # Asercje TDD - wszystkie węzły C.R.U.D obligatoryjne (!)
    assert "chapters" in tables, "Błąd! Brakuje tabeli chapters"
    assert "questions" in tables, "Błąd! Brakuje głównej tabeli Pytań"
    assert "choices" in tables, "Błąd! Brakuje tabeli wyborów"
    assert "glossary" in tables, "Błąd! Gdzie wcięło słownik definicji pojęciowej?"
    assert "syllabus_sections" in tables, "Błąd integralności Bazy Wiedzy!"
    assert "exam_results" in tables, "Skasowanie tabeli wyników oznacza utratę cennych postępów nauki!"
    
    # Asercja na działanie fizycznych wstrzyknięć przez API SQL
    cur.execute("INSERT INTO glossary (term, definition) VALUES ('BlackBox', 'Testowanie czarnoskrzynkowe')")
    conn.commit()
    conn.close()
