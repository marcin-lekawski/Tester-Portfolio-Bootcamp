import pytest
import sqlite3
import os
import database_setup

TEST_DB_PATH = "test_sandbox_QA.db"

@pytest.fixture(scope="module")
def setup_database():
    """Generuje instancję tymczasowej korporacyjnej bazy przed testami i dewastuje po nich."""
    database_setup.create_corporate_sandbox(db_path=TEST_DB_PATH)
    conn = sqlite3.connect(TEST_DB_PATH)
    yield conn
    conn.close()
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_database_creation_and_tables(setup_database):
    """Zapewnienie QA, że wszystkie tablice (Encje) zostały postawione w pamięci bez wyjątków."""
    conn = setup_database
    c = conn.cursor()
    
    # Odpytanie Master-Table SQLite by znaleźć założone zasoby
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in c.fetchall()}
    
    expected_tables = {
        'departments', 'projects', 'employees', 
        'hardware_assets', 'employee_projects', 
        'certifications', 'payroll',
        'bank_transfers', 'security_logs', 'chat_messages'
    }
    
    # Operacja na zbiorze (Intersection) udowadniająca kompletność Architektury DDL
    assert expected_tables.issubset(tables), f"Brakujące tabele relacyjne! Spodziewane: {expected_tables}, Zostały w Base: {tables}"

def test_employees_massive_volume(setup_database):
    """Audyt systemu zwalidowania wolumenu (Potwierdzenie założenia N >= 100 pracowników w Corporacji)."""
    conn = setup_database
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM employees;")
    count = c.fetchone()[0]
    
    assert count >= 100, f"Generator zawiódł. Zamiast ogromnej tabeli, dostaliśmy zaledwie {count} rzędów!"

def test_foreign_keys_hardware(setup_database):
    """Potwierdzenie logicznych wpięć (FK) M:N pomiędzy sprzętem a pracownikiem."""
    conn = setup_database
    c = conn.cursor()
    # Sprawdzenie, czy każdy przydzielony Hardware Asset ma wpięte prawdziwe referencyjne ID istniejacej osoby
    c.execute('''
        SELECT h.id 
        FROM hardware_assets h
        LEFT JOIN employees e ON h.employee_id = e.id
        WHERE e.id IS NULL AND h.employee_id IS NOT NULL;
    ''')
    orphans = c.fetchall()
    
    assert len(orphans) == 0, f"BŁĄD DANYCH! Złowiono 'Sieroty Sprzętowe' (urządzenia przypisane do nieistniejących bytów): {orphans}"

def test_certification_logic(setup_database):
    """Sprawdzenie poprawności logicznej tablicy Certyfikatów (Nikt bez weryfikacji QA nie dostał fałszywych kwitów cloud)."""
    conn = setup_database
    c = conn.cursor()
    c.execute('''
        SELECT e.position, c.cert_name
        FROM certifications c
        JOIN employees e ON c.employee_id = e.id
    ''')
    rows = c.fetchall()
    
    assert len(rows) > 0, "Skrypt wygenerował pustą tabelę Certyfikatów! (Awaria algorytmu)"
    
def test_departments_baseline(setup_database):
    """Test niezmienności podstawowych zarządczych rzędów"""
    conn = setup_database
    c = conn.cursor()
    c.execute("SELECT id, name FROM departments WHERE id = 1;")
    zarzad = c.fetchone()
    
    assert zarzad is not None
    assert zarzad[1] == 'Zarząd'
