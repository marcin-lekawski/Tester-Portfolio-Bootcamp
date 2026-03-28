#!/bin/bash
# Zautomatyzowany skrypt uruchamiający ISTQB Trainer
# Sprawdza i instaluje absolutnie wszystkie zależności dla rekrutera/testera w 1 kliknięcie.

# Ścieżki
BASE_DIR="$(dirname "$0")/.."
VENV_DIR="$BASE_DIR/venv"
DB_PATH="$(dirname "$0")/data/istqb_knowledge.db"
TRAINER_DIR="$(dirname "$0")"

echo "=================================================="
echo "🛡️ ISTQB Trainer: Automatyczny Konfigurator Systemu"
echo "=================================================="

# 1. Generowanie Środowiska VENV (Jeśli nie istnieje)
if [ ! -d "$VENV_DIR" ]; then
    echo "[1/4] 📦 Nie wykryto Środowiska VENV. Trwa generowanie odizolowanego systemu..."
    python3 -m venv "$VENV_DIR"
    echo "  └─ ✅ VENV zbudowany."
else
    echo "[1/4] 📦 Środowisko VENV jest obecne (OK)."
fi

# 2. Aktywacja Środowiska
source "$VENV_DIR/bin/activate"

# 3. Instalacja Wymagań (Biblioteki zewn.)
echo "[2/4] 🔍 Sprawdzanie i pobieranie paczek z PyPI (rich, questionary)..."
pip install -q rich questionary
echo "  └─ ✅ Pakiety zatwierdzone i gotowe."

# 4. Sprawdzanie Czystości/Istnienia Bazy SQL i parsowanie
if [ ! -f "$DB_PATH" ]; then
    echo "[3/4] 🏗️ Nie znaleziono bazy danych sqlite3! Uruchamiam boty inżynieryjne..."
    python3 "$TRAINER_DIR/database_setup.py"
    
    echo "[3.5/4] 🤖 Generowanie Wiedzy z PDF w locie (Parser):"
    python3 "$TRAINER_DIR/parser.py"
    echo "  └─ ✅ Tworzenie bazy ISTQB ukończone."
else
    echo "[3/4] 🗄️ Znaleziono bazę istqb_knowledge.db (OK)."
fi

# 5. Wystrzał w Główny Program z odpowiednim śledzeniem katalogu roboczego
echo "[4/4] 🚀 Startowanie Interaktywnego Terminala..."
sleep 1
cd "$TRAINER_DIR" || exit
python3 main.py
