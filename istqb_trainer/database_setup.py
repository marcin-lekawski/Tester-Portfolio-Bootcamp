import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "istqb_knowledge.db")

def create_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Twardy reset tabel Wiedzy.
    # Uzupełnimy nowym poprawionym formatem (Z zachowaniem bezcennej tabeli Twoich statystyk exam_results!)
    cursor.execute("DROP TABLE IF EXISTS choices;")
    cursor.execute("DROP TABLE IF EXISTS syllabus_sections;")
    cursor.execute("DROP TABLE IF EXISTS questions;")
    cursor.execute("DROP TABLE IF EXISTS glossary;")
    cursor.execute("DROP TABLE IF EXISTS chapters;")

    # Tabela 1: Rozdziały Główne (Chapters)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chapters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chapter_number TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        theory TEXT NOT NULL
    )
    """)

    # Tabela 2: Pytania (Questions)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chapter_id INTEGER NOT NULL,
        source TEXT,
        learning_objective TEXT,
        question_text TEXT NOT NULL,
        correct_answer_letter TEXT NOT NULL,
        FOREIGN KEY (chapter_id) REFERENCES chapters (id)
    )
    """)

    # Tabela 3: Możliwe odpowiedzi (Choices)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS choices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER NOT NULL,
        letter TEXT NOT NULL,
        choice_text TEXT NOT NULL,
        FOREIGN KEY (question_id) REFERENCES questions (id)
    )
    """)

    # Tabela 4: Historia Testów (Exam Results - NIERUSZALNA PODCZAS RESETOW)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exam_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mode TEXT NOT NULL,
        score INTEGER NOT NULL,
        total_questions INTEGER NOT NULL,
        percentage REAL NOT NULL,
        timestamp_taken DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Tabela 5: Sylabus (Syllabus Sections)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS syllabus_sections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chapter_id INTEGER NOT NULL,
        subchapter_number TEXT NOT NULL,
        k_level TEXT,
        content TEXT NOT NULL,
        FOREIGN KEY (chapter_id) REFERENCES chapters (id)
    )
    """)

    # Tabela 6: Słownik (Glossary)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS glossary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        term TEXT UNIQUE NOT NULL,
        definition TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print(f"✅ Baza danych SQLite została przygotowana do odlewu: {DB_PATH}")

if __name__ == "__main__":
    create_database()
