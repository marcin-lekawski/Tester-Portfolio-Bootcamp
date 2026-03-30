import sys
import os

# Wstrzykiwanie ścieżki głównej katalogu SQL_trainer by ułatwić importy w testach (np. database_setup)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
