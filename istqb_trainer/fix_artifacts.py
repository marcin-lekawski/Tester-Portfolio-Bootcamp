import sqlite3
import os
import re

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "istqb_knowledge.db")

def fix_ocr_artifacts():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Naprawa Pkt 2: Usuwanie Stopek PDF ze Zbioru C i D
    # Wybieramy wszystkie choices
    c.execute("SELECT id, choice_text FROM choices")
    rows = c.fetchall()
    fixes = 0
    for row in rows:
        cid = row[0]
        text = row[1]
        if "Wersja" in text or "Certyfikowany tester" in text or "©" in text:
            # Ucinamy chamski bloczek strony od słowa "Wersja", "Strona" itp.
            clean_text = re.sub(r"Wersja 1\.[45].*", "", text, flags=re.DOTALL).strip()
            clean_text = re.sub(r"Strona \d+ z \d+.*", "", clean_text, flags=re.DOTALL).strip()
            # Sprawdzenie czy wyczyszczono poprawnie
            c.execute("UPDATE choices SET choice_text = ? WHERE id = ?", (clean_text, cid))
            fixes += 1
            
    conn.commit()
    conn.close()
    print(f"🧹 Oczyszczono {fixes} zabrudzonych artefaktów stopek PDF w tabeli 'choices'!")

if __name__ == "__main__":
    fix_ocr_artifacts()
