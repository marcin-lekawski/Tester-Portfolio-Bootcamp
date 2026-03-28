import pytest
import sqlite3
import tempfile
import sys
import os

# Wymuszamy aby importy potrafiły zlokalizować skrypty powłokę wyżej
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="function", autouse=True)
def mock_db_path(monkeypatch):
    """
    Tworzy izolowaną plikową bazę danych wymuszoną przez moduł tempfile
    przed każdym testem. Inicjalizowana od czystej, usuwana po teście.
    """
    temp_db = tempfile.NamedTemporaryFile(delete=False)
    temp_db.close()
    
    # Import modułów za pomocą pythona
    import database_setup
    monkeypatch.setattr(database_setup, "DB_PATH", temp_db.name)
    
    import admin
    import knowledge_base
    import main
    
    def patched_get_db():
        return sqlite3.connect(temp_db.name)
        
    monkeypatch.setattr(admin, "get_db", patched_get_db)
    monkeypatch.setattr(knowledge_base, "get_db", patched_get_db)
    monkeypatch.setattr(main, "DB_PATH", temp_db.name)
    
    yield temp_db.name
    
    # Utylizacja pliku tymczasowego na dysku po teście (Wipe/Teardown)
    if os.path.exists(temp_db.name):
        try:
            os.remove(temp_db.name)
        except OSError:
            pass
