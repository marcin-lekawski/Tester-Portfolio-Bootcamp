import os
import re

def debug_answers():
    answers_file = "ISTQB teoria testy/CTFL_4.0_Pytania_przykladowe_odpowiedzi_zbior_C_w.1.5_w.1.0.0.4-PL.txt"
    with open(answers_file, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f.read().splitlines() if l.strip()]

    print("Checking first 1000 lines for digit -> letter matches...")
    matches = 0
    for i in range(len(lines)):
        if lines[i] == "14":
            print("Znalazłem '14'! Oto kontekst:")
            for j in range(max(0, i-2), min(len(lines), i+8)):
                print(f"L{j}: {lines[j]}")
    print("GOTOWE")
    
if __name__ == "__main__":
    debug_answers()
