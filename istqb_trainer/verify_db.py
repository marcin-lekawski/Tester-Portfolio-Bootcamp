import sqlite3
import os
import re

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "istqb_knowledge.db")

def verify_db():
    print("====================================")
    print("🔍 DATA VERIFIER (DB SANITY CHECK)")
    print("====================================")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 1. Sprawdzanie struktury Pytaniowej (Ilość Opcji Dostępnych)
    c.execute("SELECT id, question_text FROM questions")
    qs = c.fetchall()
    print(f"Baza posiada łącznie {len(qs)} zaimportowanych pytań.")
    
    anomalies = 0
    
    for q_id, q_text in qs:
        # Pytania posiadają zwykle opcje A,B,C,D. Rzadko więcej, czasem wielokrotny wybór to A-E. Sprawdzamy podwiązaną tabele "choices"
        c.execute("SELECT id, letter, choice_text FROM choices WHERE question_id=?", (q_id,))
        choices = c.fetchall()
        
        if len(choices) < 4:
            anomalies += 1
            print(f"[OSTRZEŻENIE] Pytanie ID {q_id} posada tylko {len(choices)} wyciągniętych odpowiedzi! Być może ucięte warianty.")
            print(f"   -> Treść: {q_text[:60]}...")
            
        # 2. Sprawdzanie czy w Choice Text nie nagrały się Stopki Stron (Symptom zepsutego OCR)
        for ch_id, letter, choice_text in choices:
            if "Strona" in choice_text or "Wybierz JEDN" in choice_text or "©" in choice_text or len(choice_text) < 2:
                anomalies += 1
                print(f"[BŁAD PARSOWANIA] Pytanie ID {q_id}, Odp: {letter}) zawiera śmieci ze stron.")
                print(f"   -> Śmieć: {choice_text}")
                
        # 3. Sprawdzanie Treści pytania
        if len(q_text) < 10:
            anomalies += 1
            print(f"[BŁAD ZDAN] Pytanie ID {q_id} jest nielogicznie krótkie (możliwy breakline zepsuty).")
            print(f"   -> Tekst: {q_text}")
    
    # 4. Sprawdzanie Poprawnych Liter Odpowiedzi
    c.execute("SELECT id, correct_answer_letter FROM questions")
    ans_data = c.fetchall()
    for q_id, ans in ans_data:
        ans_clean = ans.lower().strip()
        # poprawna liera to miala byc tylko np a albo d, albo na wielokrotnym wyborze "a, c" 
        # ale jesli ma na liscie "brak", to znaczy że klucz odpowiedzi wcale nie trafil !
        if "brak" in ans_clean:
            anomalies += 1
            print(f"[KRYTYCZNE] Pytanie ID {q_id} nie ma podpiętej ŻADNEJ poprawnej odpowiedzi z Arkusza KLUCZY! Zagraża Egzaminowi.")
        elif not re.match(r"^[a-e](\s*,\s*[a-e])*$", ans_clean):
            anomalies += 1
            print(f"[KRYTYCZNE] Pytanie ID {q_id} ma bezsensowny format poprawnej Litery Odpowiedzi:")
            print(f"   -> Litera: {ans}")
            
    print("====================================")
    print(f"Koniec Audytu. Znaleziono Anomalii: {anomalies}")
    print("====================================")
    
if __name__ == "__main__":
    verify_db()
