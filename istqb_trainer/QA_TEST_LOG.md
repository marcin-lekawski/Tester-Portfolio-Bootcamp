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
   - *Opis:* Użytkownik chce mieć natychmiastowy dostęp do wiedzy i pojęć z wnętrza CLI, z powodu niedokładności parserów na dokumentach tekstowych.
   - *Wdrożenie:* Nowa, kolosalna komenda pobierająca do bazy danych 250 Kilobajtów surowej teorii i setek pojęć definicyjnych ISTQB. Stworzono dwa nowe zasoby: Słownik (`glossary`) i Podrozdziały `syllabus_sections` posiadające stopnie ważności e.g., (K2). Wykreowano dla administratora system CRUD i terminalowy menadżer wiedzy do ręcznej "wlocie" edycji i tworzenia nowych pytań!
