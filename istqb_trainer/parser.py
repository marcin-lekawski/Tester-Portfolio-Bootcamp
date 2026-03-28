import re
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "istqb_knowledge.db")
TEORIA_PATH = os.path.join(os.path.dirname(__file__), "..", "ISTQB teoria testy")

class ISTQBParser:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        
    def add_chapter_if_missing(self, lo):
        # np. FL-2.1.2 -> chapter_number: "2"
        chapter_match = re.search(r"FL-(\d+)", lo)
        if chapter_match:
            ch_num = chapter_match.group(1)
            self.cursor.execute("SELECT id FROM chapters WHERE chapter_number = ?", (ch_num,))
            row = self.cursor.fetchone()
            if row:
                return row[0]
            else:
                self.cursor.execute("INSERT INTO chapters (chapter_number, title, theory) VALUES (?, ?, ?)", 
                                    (ch_num, f"Rozdział {ch_num}", "Syllabus w module Bazy Wiedzy."))
                self.conn.commit()
                return self.cursor.lastrowid
        return None

    def get_answers_dict(self, answers_file):
        """Map Q_NUM -> {ans: 'a', lo: 'FL-1.1.1'} by searching blocks. FIX FOR BUG #004"""
        ans_dict = {}
        with open(answers_file, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f.read().splitlines() if l.strip()]

        for i in range(len(lines)-1):
            if lines[i].isdigit() and 1 <= int(lines[i]) <= 40:
                ans_str = lines[i+1].replace(" ", "")
                if re.match(r"^[a-eA-E](?:,[a-eA-E])*$", ans_str):
                    # Znalaziono cyfre + w kolejnej linijce literki: mamy komplet! Szukamy FL- na dystansie 40 linijek
                    lo = "FL-1.1.1" # Domyślny fallback
                    for j in range(1, 40):
                        if i+j < len(lines):
                            if "FL-" in lines[i+j]:
                                lo_match = re.search(r"FL-\d+\.\d+(\.\d+)?", lines[i+j])
                                if lo_match:
                                    lo = lo_match.group(0)
                                    break
                    ans_dict[int(lines[i])] = {"ans": ans_str.lower(), "lo": lo}
        return ans_dict

    def parse_mock_exam(self, questions_file, answers_file, source_name):
        ans_dict = self.get_answers_dict(answers_file)
        
        with open(questions_file, 'r', encoding='utf-8') as f:
            text = f.read()

        parts = re.split(r"Pytanie nr (\d+) \(\d+ p\.\)", text)
        q_count = 0
        
        for i in range(1, len(parts), 2):
            q_num = int(parts[i])
            q_block = parts[i+1]
            
            # Znajdź sekcje z wariantami
            choice_split = re.split(r"\n([a-eA-E]\)) ", "\n" + q_block)
            if len(choice_split) > 1:
                q_text = choice_split[0].strip()
                # Oczyść nagłówki/stopki PDF
                q_text = re.sub(r"wersja 1\.6.*", "", q_text, flags=re.DOTALL).strip()
                q_text = re.sub(r"Strona \d+ z \d+.*", "", q_text, flags=re.DOTALL).strip()
                q_text = re.sub(r"©.*", "", q_text, flags=re.DOTALL).strip()
                
                # Zapisz pytanie w DB
                answer_info = ans_dict.get(q_num, {"ans": "brak", "lo": "brak"})
                ch_id = self.add_chapter_if_missing(answer_info["lo"])
                if not ch_id:
                    self.cursor.execute("SELECT id FROM chapters WHERE chapter_number = '1'")
                    row = self.cursor.fetchone()
                    if row:
                        ch_id = row[0]
                    else:
                        self.cursor.execute("INSERT INTO chapters (chapter_number, title, theory) VALUES ('1', 'Rozdział 1', 'Brak')")
                        ch_id = self.cursor.lastrowid

                self.cursor.execute("""
                    INSERT INTO questions (chapter_id, source, learning_objective, question_text, correct_answer_letter)
                    VALUES (?, ?, ?, ?, ?)
                """, (ch_id, source_name, answer_info["lo"], q_text, answer_info["ans"]))
                
                q_id = self.cursor.lastrowid
                
                # Zapisz Choices
                for j in range(1, len(choice_split), 2):
                    letter = choice_split[j].replace(")", "").strip()
                    val = choice_split[j+1]
                    # Odcięcie brudów po pętli
                    val = re.split(r"Wybierz JEDN", val)[0]
                    val = re.split(r"Wybierz D", val)[0].strip()
                    
                    self.cursor.execute("""
                        INSERT INTO choices (question_id, letter, choice_text) VALUES (?, ?, ?)
                    """, (q_id, letter, val))
                q_count += 1
        
        self.conn.commit()
        print(f"✅ Zparsowano i wrzucono {q_count} pytań z {source_name}")

    def parse_syllabus_and_glossary(self):
        syllabus_file = os.path.join(TEORIA_PATH, "ISTQB_CertyfikowanyTester_PoziomPodstawowy_v4.0.1.txt")
        if not os.path.exists(syllabus_file):
            print("⚠️ Brak pliku sylabusa.")
            return

        with open(syllabus_file, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f.read().splitlines() if l.strip()]

        glossary_words = set()
        in_keywords = False
        
        # Zbieranie Słów kluczowych do Glosariusza
        for line in lines:
            if "Strona" in line or "©" in line or "wersja " in line.lower() or "Certyfikowany" in line: continue
            if "Słowa kluczowe" in line:
                in_keywords = True
                continue
            if in_keywords:
                if re.match(r"^\d+\.\d+", line):
                    in_keywords = False
                    continue
                words = [w.strip() for w in line.split(',') if w.strip()]
                for w in words:
                    if len(w) < 50: # pomijanie zdan z tekstu
                        glossary_words.add(w)
        
        for w in glossary_words:
            self.cursor.execute("INSERT OR IGNORE INTO glossary (term, definition) VALUES (?, ?)", (w, "Brak definicji. Otwórz Edytor (Tryb Admina) by przypisać znaczenie!"))
        
        # Sekcje Sylabusa
        current_ch_id = 1
        current_sub = "Wstęp"
        current_k = "N/A"
        current_text = []

        for line in lines:
            if "Strona" in line or "©" in line or "wersja " in line.lower() or "Certyfikowany" in line: continue
            # Szukamy naglowka np "1.2.1 Cos (K2)"  lub "3.2 Cos"
            match = re.match(r"^(\d+)\.(\d+(?:\.\d+)?)\s+(.*?)(?:\(([Kk][1-3])\))?$", line)
            if match:
                if current_text:
                    self.cursor.execute("""
                        INSERT INTO syllabus_sections (chapter_id, subchapter_number, k_level, content)
                        VALUES (?, ?, ?, ?)
                    """, (current_ch_id, current_sub, current_k, "\n".join(current_text)))
                
                ch_num, sub_num, title, k = match.groups()
                current_sub = f"{ch_num}.{sub_num} {title}"
                current_k = k.upper() if k else "N/A"
                current_text = []
                
                self.cursor.execute("SELECT id FROM chapters WHERE chapter_number = ?", (ch_num,))
                row = self.cursor.fetchone()
                if row:
                    current_ch_id = row[0]
                else:
                    self.cursor.execute("INSERT INTO chapters (chapter_number, title, theory) VALUES (?, ?, ?)", 
                                        (ch_num, f"Rozdział {ch_num}", "Sylabus Baza Wiedzy"))
                    current_ch_id = self.cursor.lastrowid
            else:
                current_text.append(line)
        
        if current_text:
            self.cursor.execute("""
                INSERT INTO syllabus_sections (chapter_id, subchapter_number, k_level, content)
                VALUES (?, ?, ?, ?)
            """, (current_ch_id, current_sub, current_k, "\n".join(current_text)))

        self.conn.commit()
        print(f"✅ Zessano 250 KB Sylabusa m.in. z {len(glossary_words)} Hasłami słownikowymi.")


    def run_all(self):
        print("Startuję potężnego parsera V2 (Hybryda: Pytań, Teorii, Glosariusza)...")
        self.parse_syllabus_and_glossary()

        # Zbior A
        q_file_a = os.path.join(TEORIA_PATH, "CTFL_4.0_Egzamin_przykladowy_zbior_A_v.1.61.0.0.3-PL.txt")
        a_file_a = os.path.join(TEORIA_PATH, "CTFL-4.0_Egzamin-przykladowy-zbior-A-odpowiedzi_v.-1.61.0.0.5-PL.txt")
        if os.path.exists(q_file_a) and os.path.exists(a_file_a):
            self.parse_mock_exam(q_file_a, a_file_a, "Zbiór A")

        # Zbior B
        q_file_b = os.path.join(TEORIA_PATH, "CTFL_4.0_Pytania_przykladowe_zbior_B_w.1.61.0.0.4-PL.txt")
        a_file_b = os.path.join(TEORIA_PATH, "CTFL_4.0_Pytania_przykladowe_odpowiedzi_zbior_B_w.1.6_w.1.0.0.5-PL.txt")
        if os.path.exists(q_file_b) and os.path.exists(a_file_b):
            self.parse_mock_exam(q_file_b, a_file_b, "Zbiór B")

        self.conn.close()

if __name__ == "__main__":
    parser = ISTQBParser()
    parser.run_all()
