# 🛡️ Quality Assurance Portfolio: ISTQB Interactive CLI Trainer

Witaj w moim repozytorium! Projekt, na który aktualnie patrzysz, został zbudowany od zera w ramach intensywnego, inżynieryjnego bootcampu QA. Celem repozytorium jest udowodnienie moich szerokich kompetencji na styku **Testowania Oprogramowania (QA)** oraz **Programowania w języku Python**.

Projekt nie jest jedynie zestawem skryptów – to w pełni interaktywna, seryjna aplikacja ułatwiająca certyfikację ISTQB® Foundation Level (v4.0). Wyposażyłem ją w system śledzenia testów, panel administracyjny C.R.U.D oraz potężny silnik parsowania danych arkuszowych.

---

## 🚀 Główne Cele i Funkcjonalności

Z punktu widzenia rekrutera technicznego, aplikacja jest "Dowodem Koncepcji" (Proof of Concept) udowadniającym moje twarde kompetencje techniczne:

1. **System Inżynierii Wstecznej Dokumentacji (Parser Regex)**
   - Zaprojektowałem skrypt w Pythonie analizujący w locie ponad **250 Kilobajtów** surowych danych (Sylabusa oraz Próbnych Arkuszy Egzaminacyjnych ISTQB). 
   - Aplikacja za pomocą potężnych bloków wyrażeń regularnych (`re`) poszukuje definicji, "Zdań Kluczowych", tablic uzasadnień poprawnych odpowiedzi i tworzy z nich czyste zbiory danych wejściowych, omijając zakłócenia wizualne i stopki z plików tekstowych zrzuconych z PDF.

2. **Zaawansowana Relacyjna Baza Danych (SQLite)**
   - Każdy strzęp wiedzy wyodrębniony przez Skrypt zasilający trafia prosto do natywnej, zbudowanej skryptami DDL bazy `sqlite3`.
   - Struktura opiera się o kilka autonomicznych, połączonych relacjami tabel: Główne Rozdziały (`chapters`), Pytania i Warianty (`questions`, `choices`), Wyniki Egzaminacyjne dla statystyk postępów (`exam_results`) oraz Baza Wiedzy łącząca się w Edytowalne Podrozdziały i Glosariusz Terminów (`glossary`).

3. **Moduł Zarządzania Danymi (Panel CRUD z poziomu Konsoli)**
   - Wdrożyłem wydzielony moduł administracyjny w oparciu o architekturę terminalową, umożliwiający w locie zarządzanie strukturą: Od dodawania nowych pytań (Create), przeglądania i analizy Słownika (Read), potężnego edytora definicji i sylabusa uruchamianego wieloliniowym promptem (Update), na cichym i bezlitosnym usuwaniu śmieciowych pytań z kaskadowymi wyborami skończywszy (Delete).

4. **Kultura i Rygor Jakości (Quality Assurance / Backlog)**
   - Aplikacja to dom dla systematycznej pracy testera. Repozytorium korzysta z autorskiego podziału na Release Cycles prezentowanego z detalami. Zobacz chociażby mój plik `istqb_trainer/QA_TEST_LOG.md`, który prowadzony jest skrupulatnie w stylu raportowania Black-Box Bugs z podaniem przyczyny i zastosowanego naprawczego "Leku" (Patch Release).

---

## 🛠️ Stack Technologiczny i Narzędzia

Do stworzenia tej aplikacji w najświeższych standardach pisania oprogramowania terminalowego w Pythonie użyłem:
- **Python 3.x** - Jako główny, silnie obiektowy i przejrzysty język programowania back-endowego,
- **Moduł `sqlite3`** - Do płynnej obsługi struktur relacyjnej bazy danych i nauki potężnych kwerend SQL (JOIN, DML),
- **Moduł `re` (RegEx)** - Odporna matryca matematyczna do automatycznej analizy lingwistyki szpalet zrzuconych z pdf-ów,
- **Biblioteka `Rich`** - Do dynamicznego, pięknego pod kątem UI formatowania napisów, oddzielania treści i malowania terminalowych "Paneli" i ustandaryzowanych "Tabel" wyników,
- **Biblioteka `Questionary`** - Płynna, współczesna biblioteka budująca CLI intefejs Promtów, Pętli Wyboru Kółkowego, Pytaniowych Check-box'ów (Dozwalających np. precyzyjne śledzenie wielokrotnego wyboru: 2/4 odpowiedzi) i edytorów,
- **System Git / Git-Bash** - Do ciągłej implementacji (Continuous Integration), wersjonowania kodu źródłowego na stabilne branche.

---

## ⌨️ Jak Uruchomić Trenera na Twojej Maszynie?

Skrypt obsługi wirtualnego środowiska `venv` postawi u Ciebie aplikację bezboleśnie.
W środowisku uniksowym (MacOS, Linux, WSL) wpisz komendę z głównego folderu z pobranym kodem:

```bash
./run_trainer.sh
```

*(Jeżeli to twoje pierwsze chwile z aplikacją, upewnij się wcześniej, że zaktualizowałeś pakiety lokalne poleceniem: `pip install rich questionary` bądź postawiłeś czysty `python -m venv venv` w rewirze dokumentu, a następnie wywołałeś Setupera SQL i parser przez `python istqb_trainer/database_setup.py`)*

Przetestuj moje UI. Zerknij do kodu z komentarzami. Podejrzyj dziennik testów QA. 
**Ta aplikacja nie udaje – ona jest twardym dowodem pasji i logicznego pomyślenia w dziedzinie IT.** Dziękuję za wizytę na moim profilu GitHub!
