# 🛡️ Quality Assurance Portfolio: ISTQB & SQL Interactive Trainers

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

## ⌨️ Jak Uruchomić Trenera? (Automatyczny Deployment)

Zapomnij o ręcznej rzeźbie i budowaniu wirtualnych środowisk. Jako Q&A i inżynier procesów, szanuję czas recenzentów i użytkowników. Przygotowałem zautomatyzowany skrypt All-In-One służący jako **One-Click Installer**.

Skrypt samoistnie wykryje brak środowiska `venv`, postawi w izolacji Pythona, doczyta ciche zależności `pip` i poprosi zrobotyzowany Parser o stworzenie kompletnej natywnej bazy Sylabusa od zera dla Ciebie do folderu `data`.

Aby zobaczyć ten system w akcji, otwórz terminal w głównym katalogu pobranego repozytorium i po prostu wykonaj poniższy plik wsadowy:

```bash
./istqb_trainer/run_trainer.sh
```

*(Jeśli potrzebujesz mu nadać prawa do wykonywania w Linuksie zrób to wpisując `chmod +x istqb_trainer/run_trainer.sh` przed aktywacją).*

Przetestuj moje UI. Zerknij do kodu z komentarzami. Podejrzyj dziennik testów QA. 
**Ta aplikacja nie udaje – ona jest twardym dowodem pasji i analitycznego podejścia Inżyniera. Dziękuję za wizytę na moim profilu GitHub!**

---

## 🐉 Moduł 2: Edukacyjny SQL Trainer (D&D Sandbox)

Drugim potężnym narzędziem w tym repozytorium jest aplikacja terminalowa **SQL Trainer**. Jest to interaktywny symulator relacyjnych baz danych, zaprogramowany w estetyce gier RPG (Dungeons & Dragons), mający na celu łagodne i bezpieczne wprowadzanie w tajniki `SQL`.

**Kluczowe innowacje trenera SQL:**
- 🧙‍♂️ **Rozbudowane Uniwersum D&D**: Baza danych zaprojektowana jako fantastyczny świat z relacjonowanymi tabelkami takimi jak `Bohaterowie`, `Konie`, `Bestiariusz` czy `Kronika_Przygód`. Nauka SQL staje się przygodą.
- 🛡️ **In-Memory DML Sandbox Evaluator**: Wysoce nowoczesny inżynieryjny filtr komend modyfikujących bazę (`INSERT`, `UPDATE`, `DELETE`). System pod spodem błyskawicznie klonuje w RAM (`:memory:`) natywną bazę danych. Komendy są wykonywane w izolacji od pliku źródłowego `D&D_sandbox.db` a modyfikacje analizowane przez masowe skanowanie tablic (Dual Table Audit). Efekt: 100% uodpornienia na błędy ucznia bez zawieszania aplikacji.
- 📊 **UI bazujące na Textual**: Konsolowy, okienkowy interfejs symulujący środowiska IDE, z podświetlaniem składni i wsparciem na żywo.

*(Obecnie zrealizowano migrację do systemu D&D na etapie rozdziałów R1-R5. Operacje DML, R6+ w trakcie).*
