# 🗃️ SQL Trainer PRO - Product Backlog

Poniższy dokument śledzi historyczny rozwój (Changelog) oraz plany na przyszłe funkcjonalności w fazie wydawania wersji Beta i pełnego 1.0 Release.

## 📌 Zaplanowane Rozszerzenia (Future Sprints)
1. **[Feature] Autouzupełnianie Składni (Syntax Autocomplete):**
   Wdrożenie w `TextArea` podpowiadacza składni wyciągającego nazwy tabel z silnika SQLite w czasie rzeczywistym (np. po wpisaniu liter "em" aplikacja podświetli "employees").
2. **[Feature] Ocenianie i Logika Wyników (Gamification):**
   Implementacja systemu zbierania punktów (Score) za nieużywanie "Hinta" (strata -1 pkt za ułatwienie). Przerzucanie progresu do pliku JSON.
3. **[Architecture] Zapis stanu (State Save):**
   Powrót do programu podświetli w Drzewie `Tree` zielonym "X" wszystkie ukończone wczoraj sekcje zadań, korzystając z lokalnego Cache.
4. **[Content] Dodanie modułu DML (Manipulacja):**
   Odblokowanie zapytań `UPDATE`, `INSERT` na środowisku po wcześniejszym wczytywaniu Save-pointów.

## 🐛 Zidentyfikowane Długi Techniczne (Technical Debt)
- *Obsługa Błędów:* Aktualny popup informujący o "Błędzie kompilatora" nie wskazuje Inżynierowi dokładnie, w której linijce wystąpił błąd w wielolinijkowym SQLu. Wymagany lepszy Parsing błędu SQLite.
- *Testy Integracyjne:* Należy pokryć proces GUI `Textual` biblioteką `pytest-textual-snapshot`.

## 📦 Lista Wdrożeń:
**v0.1.0-beta (Wielka Rozbudowa Corporacyjna)**
- Całkowity reset TUI z podwójnymi Modal Boxami.
- Zamiana silnika CLI na okna `ContentSwitcher` i rendering asynchroniczny `Markdown`.
- Wypompowanie bazy na logikę potężnej spłki (Generatory po 150 Inżynierów, Hardware'u i certyfikatów).
- Uregulowanie zdarzeń klawiszowych systemu (Control-lock mitigation).
