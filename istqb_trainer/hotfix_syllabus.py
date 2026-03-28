import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "istqb_knowledge.db")

THEORY_1_1 = """1.1 Co to jest testowanie?

Testowanie oprogramowania to ewolucyjny proces obejmujący statyczną oraz dynamiczną weryfikację aplikacji (pod kątem zgodności z wymaganiami biznesowymi i technicznymi). 
Wielu ludzi myli testowanie z samym procesem "klikania aplikacji wg scenariusza" (Testowanie dynamiczne), jednak w rzeczywistości testowanie rozpoczyna się już na etapie planowania projektu poprzez Przeglądy Dokumentacji, Inspekcje (Testowanie statyczne).

Główne działania w procesie testowym to m.in.:
- Planowanie testów i sterowanie testami
- Analiza i projektowanie testów (Tworzenie Przypadków Testowych)
- Implementacja i wykonanie testów (wykonywanie manualne lub skryptowanie w np. Selenium)
- Ocena kryteriów zakończenia i raportowanie
- Czynności zamykające testy.

Ważne jest by zrozumieć różnicę między "Testowaniem" a "Debugowaniem". Testowanie polega na identyfikowaniu CZY oprogramowanie posiada defekt, z kolei Debugowanie to zjawisko ściśle developerskie, którego celem jest zlokalizowanie, przeanalizowanie w kodzie (np w oparciu o call-stack) i bezpowrotne wyeliminowanie (patch) znalezionego wcześniej za sprawą testów defektu."""

THEORY_1_3 = """1.3 Zasady testowania

Zgodnie z sylabusem ISTQB CTFL wyróżniamy 7 uniwersalnych zasad testowania oprogramowania:

1. Testowanie ujawnia obecność defektów, ale nie może dowieść ich braku. 
Zawsze istnieje prawdopodobieństwo, że błędy nadal istnieją mimo dogłębnych testów. Pamiętaj - nigdy nie udowodnisz że program jest w 100% czysty z problemów.

2. Testowanie gruntowne jest niemożliwe.
Sprawdzenie każdej permutacji danych wejściowych zająłoby nieskończoność. QA opiera się na umiejętnym analizowaniu "Ryzyka" (Podejście oparte na mitygowaniu ryzyka). 

3. Wczesne testowanie oszczędza czas i pieniądze.
Zasada shift-left testing. Błąd znaleziony podczas czytania specyfikacji na 1 etapie bywa tysiąckrotnie tańszy do naprawy niż ten sam błąd znaleziony w uruchomionym kodzie u Klienta na serwerze produkcyjnym.

4. Kumulowanie się defektów.
Błędy mają tendencję do skupiania się w pewnych fragmentach aplikacji (np. nowo zaimplementowanych, ekstremalnie trudnych klasach). Testy powinny uwzględniać to zjawisko w analizowaniu ryzyka.

5. Paradoks pestycydów (Pesticide Paradox).
Uruchamianie ciągle tego samego zestawu testów, przestaje wykrywać z czasem nowe defekty. Przypadek testowy musi "ewoluować" w czasie i być regularnie poszerzany o nowe kroki brzegowe.

6. Testowanie jest zależne od kontekstu.
Oprogramowanie branży lotniczej ubezpieczane standardami DO-178C testuje się kompletnie inną metodologią i skrupulatnością niż stronę typu Wirtualny Katalog Mebli-eCommerce.

7. Przekonanie o braku błędów jest błędem (The absence-of-errors fallacy).
Nawet idealnie naprawione 1000 błędów w systemie traci jakiekolwiek znaczenie biznesowe, jeżeli sam system będzie trudny w użyciu, zbudowany nie wg życzeń klienta lub całkowicie bezużyteczny w środowisku docelowym."""

THEORY_5_4 = """5.4 Zarządzanie Konfiguracją (Configuration Management)

Celem zarządzania konfiguracją w testowaniu jest zagwarantowanie spójności i integralności tak zwanego "Testware" (Oprogramowania Testowego, środowisk, wtyczek i zbiorów danych wejściowych) z wersjami aplikacji poddawanej testom ("Software"). Bądź świadom na jakiej wersji aplikacji aktualnie wbijasz Bug Report, a na którą wgrywano patch!

Na Zarządzanie Konfiguracją składają się następujące techniki z punktu widzenia Testowania:
- Identyfikowanie Elementów Konfiguracji: Każdy element biorący udział w testach (plik konfiguracyjny, build, Docker image) otrzymuje jasno opisany, konkretny znacznik i status rewizji w Git. 
- Kontrola i Modyfikowanie: Każda zmiana jest rejestrowana (Auditing), odtwarzalna oraz akceptowalna, celem zwalczania zjawiska "U mnie działało i przestało". Odtworzalność pozwala na precyzyjne symulowanie problemów.
- Audytowane Raportowanie: Podawanie precyzyjnych informacji powiązanych ze stanami metrycznymi testowego otoczenia by decydenci na zarządzie mogli w sposób świadomy weryfikować środowisko.

Narzędzia wspomagające to min: GitLab CI, Docker, Ansible, Jenkins czy Terraform."""

THEORY_6_1 = """6.1 Wprowadzenie do Narzędzi Wspomagających Testowanie (Tool Support)

Testowania w dzisiejszym Inżynieryjnym wydaniu nie przeprowadza się wyłącznie używając rąk. Narzędzia pomagają obniżać koszty cyklu, weryfikować metryki a przede wszystkim – oszczędzać czas QA na zautomatyzowanym powtarzaniu tego samego setu działań.

Narzędzia wykorzystywane w teście możemy generalizować do kategorii zadań:
- Wsparcie dla Planowania i Sterowania: ALM (Application Lifecycle Management), Narzędzia klasy Jira (Zarządzanie Defektami).
- Wsparcie Static Testing (Przeglądy Statyczne): SonarQube, kompilatory analizujące code-flow w IDE, Pylint.
- Narzędzia do Skryptowania & Egzekucji Testów Dynamicznych: Selenium (UI Driver API), Cypress, Playwright czy Pytest (Framework Automatyzacyjny). Wykrywają regresywne dziury.
- Wsparcie dla Optymalizacji Środowisk VDI: Docker Compose, VMware. Służą generowaniu czystych serwowanych od nowa OS do badań testowych.
- Wsparcie dla symulowania integracji (Performance Testing & API): JMeter (symulowanie tysięcy userów naciskających witrynę / stress test), Postman do uderzania maszynowo w endpointy REST. 

Uwaga: Ważnym pojęciem rekruracyjnym jest świadomość, że bezkrytyczne ufanie Narzędziu prowadzi do iluzji posiadania zbadanej i działającej aplikacji. Mówi się wręcz ewidentnie "Automatyzacja Złego Procesu przyniesie Szybszy Zły Wynik". Narzędzia to uzupełnienie myśli, heurystyk i zdolności poznawczych inżynierów testujących (Exploratory Testing)."""

def execute_patch():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # KROK 1: Usunięcie buga z "datami" wciągniętymi do formatu Sylabusa. Oczyszczamy z bazy 8 śmieci.
    c.execute("DELETE FROM syllabus_sections WHERE subchapter_number LIKE '% r.'")
    deleted_junk = c.rowcount
    
    # KROK 2: Wstrzykiwanie rzetelnej merytoryki do uszkodzonych obciętych działów (Data Injection).
    c.execute("UPDATE syllabus_sections SET content = ? WHERE subchapter_number LIKE '1.1 %'", (THEORY_1_1,))
    c.execute("UPDATE syllabus_sections SET content = ? WHERE subchapter_number LIKE '1.3 %'", (THEORY_1_3,))
    c.execute("UPDATE syllabus_sections SET content = ? WHERE subchapter_number LIKE '5.4 %'", (THEORY_5_4,))
    c.execute("UPDATE syllabus_sections SET content = ? WHERE subchapter_number LIKE '6.1 %'", (THEORY_6_1,))
    
    conn.commit()
    conn.close()
    
    print(f"🔥 Operacja czyszczenia i Patchowania Sylabusa zakończona.")
    print(f"   └─ Wymazano śmieciowych indeksów z Bazy Danych (Ze stopek PDF): {deleted_junk}")
    print(f"   └─ Zaktualizowano (Wstrzyknięto) wiedzę objętościową do Sekcji: 1.1, 1.3, 5.4, 6.1.")

if __name__ == "__main__":
    execute_patch()
