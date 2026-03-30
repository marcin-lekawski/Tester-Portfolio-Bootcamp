# Wielka Encyklopedia Magii Danych - SQLite dla Bohaterów

CHEAT_SHEET_MD = """
# 📋 Tablice Informatyczne SQL (Wzorce i Komendy)

> [!WARNING] Zastrzeżenie Prawne (Fan Fiction & Fair Use)
> Niniejsza baza treningowa "D&D_sandbox" ma charakter wyłącznie edukacyjny. Użyte imiona postaci (np. Geralt, Frodo) i potworów nawiązują do twórczości literackiej m.in. J.R.R. Tolkiena i Andrzeja Sapkowskiego. Dzieło stanowi Fan Fiction i nie jest produktem komercyjnym objętym licencją, powołuje się na granice dozwolonego użytku edukacyjnego (Fair Use).

Poniższe kompendium grupuje najistotniejsze konstrukcje. 
Zaprojektowane jako szybka pościągawka przy pracy ratunkowej.

## 1. DQL (Data Query Language)
Podstawowa ekstrakcja i wyciąganie danych:
```sql
SELECT * FROM tabela;
SELECT kol1, kol2 FROM tabela;
SELECT DISTINCT dzial FROM tabela;
```
Filtrowanie predykatami (WHERE):
```sql
SELECT * FROM tabela WHERE wiek BETWEEN 18 AND 65;
SELECT * FROM tabela WHERE nazwa LIKE 'Tech%';
SELECT * FROM tabela WHERE kategoria IN ('IT', 'HR');
```

## 2. Funkcje Analityczne (Agregacje i Okna)
Zwijanie wielowierszowego stosu do pojedynczych liczb:
```sql
SELECT dzial, AVG(pensja), SUM(budzet) 
FROM pracownicy 
GROUP BY dzial;
```

## 3. Łączenie Zbiorów Danych (JOIN)
Mostkowanie i spinanie tabel po kluczach (ID).
```sql
-- INNER JOIN: Ścisła restrykcja (Bez odpowiednika odpada)
SELECT p.imie, d.nazwa 
FROM pracownicy p 
INNER JOIN dzialy d ON p.id_dzialu = d.id;

-- LEFT JOIN: Prawo Lewego - chroni wszystko z lewej tabeli
SELECT p.imie, d.nazwa 
FROM pracownicy p 
LEFT JOIN dzialy d ON p.id_dzialu = d.id;
```
"""

CURRICULUM = {
    "R1": {
        "title": "🏰 Rozdział I: Wgląd w Księgi (Querying)",
        "chapter_theory": """
# 1. SELECT – Zaklęcie Jasnowidzenia

**Teoria:** Wyobraź sobie, że stoisz przed ogromną ścianą szuflad w Królewskiej Bibliotece. Każda szuflada to Tabela, a każda kartka w środku to Rekord (wiersz). Komenda SELECT to Twoja latarka. Nie musisz wyciągać całej szuflady – możesz poprosić tylko o „Imię” i „Poziom Magii”. Jeśli użyjesz gwiazdki *, otwierasz szufladę na oścież i wysypujesz wszystko na podłogę.

**Przykład:** Chcesz sprawdzić, jakie mikstury masz w plecaku.
```sql
SELECT nazwa, moc FROM Plecak;
```
""",
        "missions": [
            {
                "id": 1,
                "task": "Nasz Magiczny Archiwista prosi o zbadanie księgi inwentarza. Rzuć absolutne zaklęcie jasnowidzenia (Gwiazdka *) aby odkryć wszystko co skrywa potworna księga `Bestiariusz`.",
                "hint": "Użyj SELECT * FROM ...",
                "expected_sql": "SELECT * FROM Bestiariusz;"
            },
            {
                "id": 2,
                "task": "Gwiazdka otwiera zbyt wiele skrzyń naraz. Mag prosi o dyskrecję: odczytaj z księgi `Bohaterowie` jedynie trzy wąskie informacje dla króla: `imie`, `rasa` oraz powołana `klasa`.",
                "hint": "Podaj kolumny po przecinku: SELECT kol1, kol2, kol3 FROM Bohaterowie;",
                "expected_sql": "SELECT imie, rasa, klasa FROM Bohaterowie;"
            },
            {
                "id": 3,
                "task": "Mamy tysiące wojaków i magów, ale Król chce poznać zestawienie różnorodności swoich rycerzy! Wydobądź jednorodną listę zawodów używając magicznego odrzucacza dubli DISTINCT na polu `klasa` czerpiąc z tabeli `Bohaterowie`.",
                "hint": "Zastosuj słowo kluczowe DISTINCT: SELECT DISTINCT klasa FROM Bohaterowie;",
                "expected_sql": "SELECT DISTINCT klasa FROM Bohaterowie;"
            }
        ]
    },
    "R2": {
        "title": "🌲 Rozdział II: Segregacja i Filtrowanie",
        "chapter_theory": """
# 2. ORDER BY – Magia Porządku
**Teoria:** W chaosie bitwy trudno znaleźć najostrzejszy miecz. ORDER BY to Twój osobisty ochmistrz, który ustawia przedmioty w rzędzie. ASC (rosnąco) to jak wchodzenie po schodach (od 1 do 10), a DESC (malejąco) to zjeżdżalnia (od najsilniejszego do najsłabszego).
**Przykład:**
```sql
SELECT * FROM Druzyna ORDER BY HP DESC;
```

# 3. DISTINCT – Kryształ Unikalności
**Teoria:** Czasem nie interesuje Cię, ilu masz rycerzy, ale jakie w ogóle rodzaje jednostek stacjonują w zamku. DISTINCT działa jak filtr, który wyrzuca powtórki. Widzisz każdą wartość tylko raz, nawet jeśli w tabeli występuje tysiąc razy.
**Przykład:**
```sql
SELECT DISTINCT rasa FROM NapotkaneIstoty;
```

# 4. WHERE – Strażnik Bramy
**Teoria:** To najważniejszy filtr. WHERE to strażnik, który mówi: „Przejdą tylko ci, którzy mają niebieskie oczy” albo „Tylko ci, którzy mają więcej niż 50 sztuk złota”. Bez tego polecenia zawsze widziałbyś wszystkich, co w wielkim królestwie byłoby męczące.
**Przykład:**
```sql
SELECT * FROM Ekwipunek WHERE czy_magiczny = 1;
```

# 5. AND & OR – Logiczne Ścieżki
**Teoria:** To spójniki Twoich rozkazów. AND jest surowy: oba warunki muszą być prawdziwe. OR jest łagodniejszy: wystarczy, że spełniasz jeden z nich.
**Przykład:**
```sql
SELECT * FROM Bohaterowie WHERE rasa = 'Elf' AND klasa = 'Lucznik';
```

# 6. LIMIT i OFFSET – Krótka Wieść
**Teoria:** Czasem Twoja księga ma 1000 stron, a Ty chcesz przeczytać tylko pierwsze trzy. LIMIT ucina listę po określonej liczbie. OFFSET pozwala Ci przeskoczyć kilka pierwszych pozycji.
**Przykład:**
```sql
SELECT imie FROM Turniej ORDER BY punkty DESC LIMIT 3;
```

# 7. BETWEEN – Widełki Przeznaczenia
**Teoria:** Zamiast pisać „większe od 10 i mniejsze od 20”, używasz BETWEEN. To jak rzucanie czaru na konkretny obszar mapy – wszystko, co wpadnie w ten zakres, zostaje wybrane.
**Przykład:**
```sql
SELECT * FROM Smoki WHERE wiek BETWEEN 100 AND 500;
```

# 8. IN – Krąg Wybranych
**Teoria:** Zamiast zadawać wiele pytań („Czy to Elf? Czy to krasnolud?”), rzucasz jedną sieć IN. Jeśli wartość znajduje się w Twoim magicznym worku, zostaje złapana.
**Przykład:**
```sql
SELECT * FROM Mieszkancy WHERE miasto IN ('Avalon', 'Neverwinter', 'Gondor');
```

# 9. LIKE & GLOB – Tropiciele Śladów
**Teoria:** To Twoi zwiadowcy. LIKE szuka tekstów, które „wyglądają podobnie”. Znak % to „cokolwiek”, a _ to „jeden nieznany znak”. GLOB jest bardziej precyzyjny i czuły na wielkie litery.
**Przykład:**
```sql
SELECT * FROM Biblioteka WHERE tytul LIKE 'Wielka%';
```

# 10. IS NULL – Wykrywanie Pustki
**Teoria:** W magii danych zero to nie to samo co pustka. NULL to „nieznane” lub „brak danych”. Jeśli zapomnisz nadać imię swojemu koniowi, jego imię będzie NULL. Używamy IS NULL, by znaleźć te luki w historii.
**Przykład:**
```sql
SELECT * FROM Misje WHERE id_bohatera IS NULL;
```
""",
        "missions": [
            {
                "id": 4,
                "task": "Nadszedł czas polowania na tytanów. Odbierz mapę (ksero wszystkiego *) przerażających monstrów z księgi `Bestiariusz` pod warunkiem ( Strażnik WHERE ) że ich parametr krwawego zżycia `hp_max` leży grubo powyżej granicy > 100.",
                "hint": "SELECT * FROM Bestiariusz WHERE hp_max > 100;",
                "expected_sql": "SELECT * FROM Bestiariusz WHERE hp_max > 100;"
            },
            {
                "id": 5,
                "task": "Dzieci kupca zgubiły ścieżkę do szkoły w lesie pełnym wargów. Odnajdźmy im gładką drogę! Spójrz głęboko w całą księgę `Lokacje` ale rozstrzel po parametrze ochrony `bezpieczenstwo` puszczając Widełki Przeznaczenia `BETWEEN` obejmujące wartości od 50 do 100.",
                "hint": "Zastosuj logikę widełek: WHERE kolumna BETWEEN dolna AND gorna;",
                "expected_sql": "SELECT * FROM Lokacje WHERE bezpieczenstwo BETWEEN 50 AND 100;"
            },
            {
                "id": 6,
                "task": "Zbadajmy poszlaki dotyczące knujących właścicieli kranów od piwa po miastach! Wypożycz całość ze spisu The `NPC` dla których zajęcie pod etykietą `funkcja` rozpoczyna lewe koryto liter na `Karczmarz` dając z prawej nieznane ślazy zjaw (% LIKE).",
                "hint": "Wykorzystaj 'wildcard' (procent)! Zapisz go na prawej flance: WHERE funkcja LIKE 'Karczmarz%';",
                "expected_sql": "SELECT * FROM NPC WHERE funkcja LIKE 'Karczmarz%';"
            }
        ]
    },
    "R3": {
        "title": "🤝 Rozdział III: Wielkie Przymierza (Joining Tables)",
        "chapter_theory": """
# 11. Magia Łączenia (INNER, LEFT, CROSS, SELF JOIN)

**Teoria:** W Twoim świecie masz różne tabele: Bohaterowie, Bronie, Zamki. JOIN to mosty między nimi.

- **INNER JOIN:** Łączy tylko „pary idealne” (np. bohatera z jego bronią – jeśli bohater nie ma broni, nie zobaczysz go).
- **LEFT JOIN:** To „lista obecności” (np. wszyscy bohaterowie, a jeśli ktoś ma broń, dopisz ją obok; jeśli nie, zostaw puste pole).
- **CROSS JOIN:** To „każdy z każdym” – tworzy wszystkie możliwe kombinacje (np. każdy rycerz przymierza każdy pancerz w sklepie).
- **SELF JOIN:** Tabela przegląda się w lustrze. Przydatne, gdy chcesz sprawdzić, kto z tabeli Ludzie jest ojcem kogoś innego z tej samej tabeli.

**Przykład:** Pokaż imię rycerza i nazwę jego wierzchowca.
```sql
SELECT Rycerze.imie, Konie.rasa 
FROM Rycerze 
INNER JOIN Konie ON Rycerze.id_konia = Konie.id;
```
""",
        "missions": [
            {
                "id": 7,
                "task": "Każdy z `Bohaterowie` (b) nosi na swych barkach ciężar wykreowanych pod spodem numerycznych parametrów fizycznych pod tabelą `Statystyki` (s). Rozkaż podpięcie ich w jedno pod mostkiem idealnego dopasowania `INNER JOIN`. Zwróć kolumny: b.imie ze strony woja oraz podpiętą z podbazy s.sila w oparciu o ich identyfikatory ciała (ON b.id_bohatera = s.id_bohatera).",
                "hint": "Pokaż dwie połączone krainy... SELECT b.imie, s.sila FROM Bohaterowie b INNER JOIN Statystyki s ON b.id_bohatera = s.id_bohatera;",
                "expected_sql": "SELECT b.imie, s.sila FROM Bohaterowie b INNER JOIN Statystyki s ON b.id_bohatera = s.id_bohatera;"
            },
            {
                "id": 8,
                "task": "Nikt nie zostaje w Królestwie zapomniany! Wszyscy `Bohaterowie` (b) muszą złożyć sprawozdanie ze swoich misji z wielkiego rejestru `Kronika_Przygód` (k). Rzuć twardy pakt chroniący każdego członka Bohaterów przed zniknięciem z Listy (LEFT JOIN) nawet jeżeli stchórzyli na całej linii omijając wpisy Kroniki. Wydobądź do tablic: b.imie obok ich zjaw z wpisów w k.opis_czynu za pomocą kluczy id_bohatera u ON.",
                "hint": "Użyj ochronnej kotwicy w locie! ... FROM Bohaterowie b LEFT JOIN Kronika_Przygód k ON b.id_bohatera = k.id_bohatera;",
                "expected_sql": "SELECT b.imie, k.opis_czynu FROM Bohaterowie b LEFT JOIN Kronika_Przygód k ON b.id_bohatera = k.id_bohatera;"
            }
        ]
    },
    "R4": {
        "title": "📊 Rozdział IV: Statystyki i Zbiory (Grouping)",
        "chapter_theory": """
# 12. GROUP BY i HAVING – Liczenie Armii
**Teoria:** GROUP BY bierze wszystkich Twoich żołnierzy i rozkazuje: „Wszyscy łucznicy na lewo, rycerze na prawo!”. Teraz możesz ich policzyć (COUNT) lub zsumować ich złoto (SUM). HAVING to filtr dla tych grup (np. „pokaż mi tylko te oddziały, które liczą więcej niż 50 osób”).
**Przykład:**
```sql
SELECT wioska, SUM(zloto) FROM Mieszkancy GROUP BY wioska HAVING SUM(zloto) > 1000;
```

# 13. UNION, EXCEPT, INTERSECT – Operacje na Armiach
**Teoria:** To jak dowodzenie wielkimi jednostkami.
- **UNION:** Łączy dwie armie w jedną (usuwając tych, którzy są w obu, by nie liczyć ich dwa razy).
- **INTERSECT:** Znajduje tylko tych szpiegów, którzy są w obu armiach jednocześnie.
- **EXCEPT:** Pokazuje żołnierzy z pierwszej armii, którzy NIE służą w drugiej.
**Przykład:**
```sql
SELECT imie FROM Sojusznicy_A UNION SELECT imie FROM Sojusznicy_B;
```
""",
        "missions": [
            {
                "id": 9,
                "task": "Musimy rzetelnie skategoryzować stłoczonych na rynkach miejskich gości ze szklanego domku the `NPC`. Zawołaj by rzucili na stół wydruk stanowisk (`funkcja`) dając przy tym sprytne sprasowanie ich stada do liczebników na koszyk poprzez `COUNT(id_npc)`. Pamiętaj założyć wiaderkowanie po uformowanych klasach jako `GROUP BY funkcja` by nie wywalić się na sumatorze całej wsi na twarz!",
                "hint": "SELECT funkcja, COUNT(id_npc) FROM NPC GROUP BY funkcja;",
                "expected_sql": "SELECT funkcja, COUNT(id_npc) FROM NPC GROUP BY funkcja;"
            },
            {
                "id": 10,
                "task": "Który z naszych herosów wyrzucił łącznie swoimi koścmi na matę najgłębsze i najdalsze wartości trafień krytycznych? Ściągnij pętle `SUM(wynik_kosci)` prosto z tablicy The `Kronika_Przygód`, zachowując unikalny przydział zasobu na konkretną unikalną tożsamość `id_bohatera` (To twoja kolumna widoczna). Narzuć wielkoformatowe wiaderkowanie The GROUP BY twardym obrysem o ramię `id_bohatera` by pozyskać petycję poprawną.",
                "hint": "SELECT id_bohatera, SUM(wynik_kosci) FROM Kronika_Przygód GROUP BY id_bohatera;",
                "expected_sql": "SELECT id_bohatera, SUM(wynik_kosci) FROM Kronika_Przygód GROUP BY id_bohatera;"
            }
        ]
    },
    "R5": {
        "title": "🧙 Rozdział V: Wyższa Magia",
        "chapter_theory": """
# 14. Subquery i EXISTS – Ukryte Pytania
**Teoria:** Podzapytanie to małe pytanie wewnątrz dużego. Najpierw znajdujesz odpowiedź na małe pytanie (np. „Jaka jest średnia siła?”), a potem używasz jej w dużym (np. „Pokaż mi tych, co są silniejsi od średniej”). EXISTS sprawdza tylko, czy podzapytanie w ogóle kogoś znalazło.
**Przykład:**
```sql
SELECT imie FROM Gracze WHERE poziom = (SELECT MAX(poziom) FROM Gracze);
```

# 15. CASE – Rozdroża Losu
**Teoria:** To Twoja instrukcja „Jeśli... to...”. Pozwala dynamicznie zmieniać to, co widzisz. Jeśli postać ma mało HP, nazwij ją „Konającą”, jeśli dużo – „Zdrową”.
**Przykład:**
```sql
SELECT imie, 
CASE 
  WHEN sila > 80 THEN 'Gigant'
  WHEN sila > 40 THEN 'Silny'
  ELSE 'Słabeusz'
END AS Klasyfikacja
FROM Postacie;
```
""",
        "missions": []
    },
    "R6": {
        "title": "🛠️ Rozdział VI: Kształtowanie Materii",
        "chapter_theory": """
# 16. INSERT, UPDATE, DELETE – Tworzenie i Niszczenie
**Teoria:** To są Twoje moce boskie.
- **INSERT:** Tchniesz życie w nową postać.
- **UPDATE:** Zmieniasz bieg historii (np. ktoś został uleczony albo okradziony).
- **DELETE:** Wymazujesz kogoś z kart historii. Uwaga: Jeśli zapomnisz WHERE, wymażesz całe królestwo!
- **UPSERT:** Magiczny bezpiecznik – „Jeśli ta postać już jest, to ją zaktualizuj, a jeśli jej nie ma, to ją stwórz”.
""",
        "missions": []
    },
    "R7": {
        "title": "🔒 Rozdział VII: Pakt Niezmienności",
        "chapter_theory": """
# 17. Transactions – Przysięga Maga
**Teoria:** W świecie danych niektóre rzeczy muszą dziać się jednocześnie. Jeśli kupujesz miecz, musisz stracić złoto I zyskać przedmiot. Jeśli stracisz złoto, a sklepikarz nie da Ci miecza (bo np. serwer padnie), transakcja zostanie cofnięta (ROLLBACK). Jeśli wszystko się uda, zostaje zatwierdzona (COMMIT).
**Przykład:** Handel wymienny.
```sql
BEGIN; -- Zaczynamy pakt
UPDATE Portfele SET zloto = zloto - 10 WHERE id = 1;
UPDATE Plecaki SET przedmiot = 'Miecz' WHERE id = 1;
COMMIT; -- Wszystko się udało, zmiana na stałe!
```
""",
        "missions": []
    },
    "R8": {
        "title": "🏗️ Rozdział VIII: Architektura Świata",
        "chapter_theory": """
# 18. Materiały i Fundamenty (Create, Alter, Drop)
**Teoria:** Zanim wpuścisz bohaterów, musisz zbudować świat.
- **Data Types:** Określasz, co można trzymać w kolumnie (Liczby, Tekst, Obrazki).
- **CREATE TABLE:** Budujesz fundamenty (np. tabela „Lochy”).
- **ALTER TABLE:** Remontujesz budynek (np. dobudowujesz nową komnatę/kolumnę).
- **DROP TABLE:** Burzysz wszystko do fundamentów.
- **VACUUM:** Magiczne sprzątanie pyłu, który został po burzeniu i budowaniu, by świat zajmował mniej miejsca.

# 19. Prawa Natury (Constraints)
**Teoria:** To zasady fizyki Twojego świata.
- **PRIMARY KEY:** Każda rzecz musi mieć swój unikalny „kod kreskowy”.
- **NOT NULL:** Pole nie może być próżnią (np. każda postać musi mieć rasę).
- **UNIQUE:** Coś musi być jedyne w swoim rodzaju (np. tylko jeden gracz może mieć dany login).
- **CHECK:** Strażnik logiki (np. punkty many nie mogą być ujemne).
""",
        "missions": []
    },
    "R9": {
        "title": "⚡ Rozdział IX: Skróty i Automaty",
        "chapter_theory": """
# 20. Magiczne Ułatwienia
**Teoria:**
- **VIEW (Widok):** Zapisane zaklęcie SELECT. Zamiast pisać co rano skomplikowane zapytanie o statystyki, zaglądasz do widoku RaportDnia.
- **INDEX:** Spis treści na końcu wielkiej księgi. Pozwala znaleźć imię „Zygfryd” w sekundę, zamiast przeglądać 100 000 stron.
- **TRIGGER:** Pułapka logiczna. „Jeśli gracz wejdzie do tej komnaty (INSERT), automatycznie zapal światło (wykonaj inne polecenie)”.
""",
        "missions": []
    },
    "R10": {
        "title": "🎒 Rozdział X: Narzędzia Mistrza Gry (Tools)",
        "chapter_theory": """
# 21. Komendy Mistrza (SQLite Commands)
**Teoria:** To są „meta-zaklęcia”, które nie działają na dane, ale na samą strukturę bazy. Pozwalają zobaczyć listę wszystkich tabel (`.tables`), sprawdzić ich budowę (`.schema`) lub przenieść dane do innego świata (`.import` / `.export`).
""",
        "missions": []
    }
}
