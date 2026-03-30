#!/bin/bash
# Zautomatyzowany skrypt uruchamiający SQL Trainer
# Autokonfiguracja środowiska wirtualnego dla projektu pobocznego.

# Ścieżki
BASE_DIR="$(dirname "$0")/.."
VENV_DIR="$BASE_DIR/venv"
DB_PATH="$(dirname "$0")/sandbox.db"
TRAINER_DIR="$(dirname "$0")"

echo "=================================================="
echo "🛡️ SQL Trainer: Automatyczny Konfigurator Systemu"
echo "=================================================="

# 1. Sprawdzanie Głównego Środowiska VENV (Znajduje się piętro wyżej)
if [ ! -d "$VENV_DIR" ]; then
    echo "[1/4] 📦 Nie wykryto Głównego Środowiska VENV. Zostanie użyty globalny Python."
else
    echo "[1/4] 📦 Główne Środowisko VENV wykryte. Aktywuję..."
    source "$VENV_DIR/bin/activate"
fi

# 2. Instalacja Wymagań (Biblioteki graficzne CLI / TUI)
echo "[2/4] 🔍 Sprawdzanie zależności TUI (rich, questionary, textual)..."
pip install -q rich questionary textual pandas
echo "  └─ ✅ Pakiety graficzne i analityczne instalacji TUI gotowe."

# 3. Sprawdzanie Bazy SQLite (Poligonu)
if [ ! -f "$DB_PATH" ]; then
    echo "[3/4] 🏗️ Pierwsze uruchomienie! Nie znaleziono bazy danych sandbox.db."
    echo "  └─ 🤖 Generuję architekturę ERD korporacji na czysto..."
    python3 "$TRAINER_DIR/database_setup.py"
    echo "  └─ ✅ Generowanie czystej bazy ukończone."
else
    echo "[3/4] 🗄️ Znaleziono gotową bazę testową sandbox.db (OK)."
fi

# 4. Wystrzał w Główny Program (Teraz jest to Natywny Dashboard Textual)
echo "[4/4] 🚀 Rozpoczynanie interaktywnego kursu QA SQL Trainer PRO..."
sleep 1
cd "$TRAINER_DIR" || exit
python3 dashboard_app.py
