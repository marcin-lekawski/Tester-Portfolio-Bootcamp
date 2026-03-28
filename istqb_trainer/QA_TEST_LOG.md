# Dziennik Rozwoju i Testowania (QA Backlog)
Projekt: ISTQB Interaktywny Trener (Podstawy)

Poniższy dokument rejestruje historię testów, zidentyfikowanych błędów oraz cykli wydawniczych dla aplikacji szkoleniowej, zgodnie z wzorcami dobrych praktyk Software QA.

---

## [Wydanie 1.0.0] - Środowisko MVP (Dzień 1)
- **Status:** Wdrożone
- **Zmiany:** 
  - Budowa bazowego Menu CLI (Python) za pomocą silników `rich` oraz `questionary`.
  - Stworzenie ustandaryzowanych trybów `learn_mode` i `exam_mode`.
  - Wstrzyknięcie prostego słownika `DATA` zawierającego statyczne definicje z sylabusa (Rozdział 1 i 2).
- **Testy Black-Box:** 
  - Zweryfikowano działanie aplikacji pod systemem natywnym (Brak błędów logicznych, pętla nieskończona main() działa poprawnie do wyboru `Wyjście`). Był 1 błąd w formacie słownika (braki przecinków), szybko wykryty przez interpreter podczas smoke testu.

---

## [Wydanie 1.1.0] - Integracja z SQLite & Regex (Dzień 1->2)
- **Status:** Wdrożone
- **Zmiany:**
  - Migracja słownika `DATA` do trwałej bazy relacyjnej `sqlite3`.
  - Stworzenie skryptów Inżynierii Wstecznej (`parser.py` z wyrażeniami regularnymi), wyłuskujących oficjalne zestawy PDF/TXT testów ISTQB. Wyciągnięto bezbłędnie 58 pytań.

---

## [Wydanie 1.2.0] - Patch UX & Trackowania Błędów (Bieżące prace QA)
**SESJA TESTOWA BLACK-BOX (DATA: DZIEŃ 2)**
Zidentyfikowane zgłoszenia błędu po wdrożeniu 1.1.0:

1. **Bug #001: Nieczytelność Formatowania (UI)**
   - *Opis:* `questionary.select()` zawija długie testowe stringi dołączając je jako Prompt. Sprawia to, że czytanie "krótkich powieści" pytań ISTQB jest na niektórych rozdzielczościach terminala udręką.
   - *Planowana Naprawa:* Drukować treść pytania przed selectem w oknie typu odseparowany `Panel` (biblioteka rich).

2. **Incident #002: Brak ucieczki w Trybie Nauki (Funkcjonalne)**
   - *Opis:* Algorytm zmusza do dokończenia całego działu iterując po wszystkich zapytaniach (np. X/40) i podlicza wynik dopiero na końcu deamonizując proces nauki.
   - *Planowana Naprawa:* Wprowadzenie elementu `[Zakończ i podlicz]` do listy `choices`. Przechwycenie przerywania skrótem komendowym z klawiatury.

3. **Feature-Request #003: Brak zapisu statystyk (Funkcjonalność)**
   - *Opis:* Użytkownik nie wie czy staje się lepszy czy gorszy w dane partie materiałów, ponieważ CLI nie posiada pamięci trwałej sesji.
   - *Planowane Wdrożenie:* 4 tabela `exam_results`. Zapis z każdego cyklu oraz menu główne oferujące Tabularny podgląd wyników.

---

## [Wydanie 1.3.0] - Architektura Bazy Wiedzy i Bugfix Parsera #004 (Dzień 2)
**SESJA TESTOWA BLACK-BOX / DEPLOYMENT**
Zidentyfikowane zgłoszenia błędu po wprowadzeniu Tablic 1.2:

4. **Bug #004: Fikcyjne braki poprawnych odpowiedzi w Nauce i Egzaminach**
   - *Opis:* Tabela SQL zawierała rzędy, w których parser PDF-u zamiast liter 'a', 'b', wstrzykiwał słowo `brak`, ponieważ dekoder tekstowy złamał szpalte tabelaryczną PDF do jednej cienkiej, długiej kolumny uniemożliwiając czytanie wierszami. Przez to poprawne kliknięcia Użytkownika rzucały "Błędna odpowiedź".
   - *Naprawa:* Re-inżynieria skryptu parsującego, zastosowanie głębokiego czytania sekcji "Uzasadnienie" i weryfikacja regex na dystansie 40 linijek od odnalezionej litery pod numerycznym indykatorze. Bezlitosny drop starych wpisów i re-indeksacja tabel w SQLite.

5. **Feature-Request #005: Pełnowymiarowa Baza Wiedzy (Słownik i Sylabus)**
   - *Wdrożenie:* Nowa, kolosalna komenda pobierająca do bazy danych 250 Kilobajtów surowej teorii i setek pojęć definicyjnych ISTQB. Stworzono dwa nowe zasoby: Słownik (`glossary`) i Podrozdziały `syllabus_sections` posiadające stopnie ważności e.g., (K2). Wykreowano dla administratora system CRUD i terminalowy menadżer wiedzy do ręcznej "wlocie" edycji i tworzenia nowych pytań!

---

## [Wydanie 1.4.0] - Refaktoryzacja Interfejsu (UX/UI) & Autorski TUI Pager (Dzień 5)
- **Status:** Wdrożone
- **Zidentyfikowane Problemy (Usability Bug #006 & #007):**
  - [Bug #006] Czytelnicy narzekali na rażącą "pomarańczkową dżunglę" wywoływaną przez defaultowe okna `questionary.text()`, która przy wielogodzinnym trybie nocnym uciska wzrok. Dodatkowo kursor wyboru to była tylko niečitěłna `>`.
  - [Bug #007] Drukowany długimi stakami (300+ linii) tekst Sylabusa z poziomu edytora brutalnie wyrzucał listę pytań CRUD pod tło ekranu, powodując całkowitą dezorientację na liście wyboru operacji na bazie Danych.
- **Wdrożona Architektura (Feature #008 Pełny TUI i Nano-Pager):**
  - Wykreowano dedykowany plik architektoniczny `terminal_ui.py` wstrzykujący głębokie modyfikacje kolorystyczne do Questionary. Skonstruowano chłodną niebiesko-zielonkawą paletę CSS.
  - Skonstruowano "Od Zera" modalny Pager (`nano_pager()`), symulujący Unixowego "Nano" lub "less". Łapie on surowe wciśnięcia klawiatury bez blokowania standardowego strumienia wejścia z buforem. Moduł od tego momentu sam się czyści przy używaniu Bazy Wiedzy lub Panelu Administratora, trzymając opcję wyjścia/edycji (`[Q]`, `[E]`, `[M]`) na samym dnie. Zakończono pełną rozbudowę systemu CRUD (możliwość edycji tagów K-level, oraz zawartości wariantów a, b, c i d dla pytań certyfikacyjnych).

---

## [Wydanie 1.5.0] - Implementacja Środowiska CI (Automatyzacja Pytest)
- **Status:** Wdrożone
- **Zmiany (Rozbudowa Inżynieryjna TDD):**
  - Stworzono dedykowaną architekturę w folderze głównym: `tests/`
  - Wdrożenie in-memory baz danych za pomocą systemowych `Fixtur` (`conftest.py`) i izolowanych plików tymczasowych (`tempfile`). Zastosowano technikę `monkeypatch` aby zminimalizować ryzyko skażenia docelowej, produkcyjnej bazy `istqb_knowledge.db` w trakcie testowania zmian (np. usunięcia przez pomyłkę historii gracza `exam_results`).
  - [Automatyzacja Zapytań] Stworzono dedykowany zestaw testowy pod matematyczną kalkulację wyników oraz tworzenie samych struktur tabel w module SQL SQLite - `test_database.py` oraz `test_main.py`.
  - [Zabezpieczenie przed błędem z Parserów #004] Przekuto bug pod silnik testowy w `test_parser.py` i dodano stałą asercję wyłapującą wielokrotne odpowiedzi typu "a, b". Uchroni to od tego samego problemu przy przesiadce na nowszy standard ISTQB V5 w przyszłości.
