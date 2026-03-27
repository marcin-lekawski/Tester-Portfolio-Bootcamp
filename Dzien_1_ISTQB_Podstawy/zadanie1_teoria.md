# 🚀 Dzień 1: Backlog Teoretyczny i Praktyczny (Rozdziały 1 i 2 ISTQB)

## 📖 Część 1: Pytania Teoretyczne (Rozdział 1 - Podstawy testowania)
Odpowiedz krótko i własnymi słowami, używając terminologii ISTQB:

1. **Analiza na wczesnym etapie:** Opisz krótko, w jakim celu wykonuje się analizę na samym etapie planowania nowej funkcjonalności (zanim powstanie kod – *Static Testing*).
   > [ testowanie statyczne pozwala na znalezienie bledów logicznych w załorzeniach projektowania nowej funkcjonalnosci. pozwala to znacznie obnizyc koszty bledy nie nakładają sie na siebie w kolejnych iteracjach. daje pewnosc ze wszyscy na pokladzie wiedzą co mają robic co pozwala uniknąc nieporozumień]

2. **Shift-Left w praktyce:** Jak w praktyce zastosujesz podejście *Shift-Left* (Przesunięcie w lewo) podczas projektowania nowej wtyczki "Koszyka" i jak uzasadnisz biznesowi zysk z tego podejścia?
   > [shift left w praktyce zrobiłbym w momencie gdy podczas testu okazuje sie na przykład ze koszyk gubi produkt, uzasadnieniem w tym momencie są wymierne straty finansowe oraz wizerunkowe dla firmy]

3. **Fałszywe ostrzeżenie:** Podaj realny przykład fałszywego ostrzeżenia (*False-positive*) podczas autoryzowania płatności (np. w systemie bankowym/Blik).
   > [taki przypadek moze nastapic kiedy system bankowy blokuje transakcję bo klient zapomnał pinu i system sie blokuje albo nagla platnosc kartą z drugiego końca świata na wiekszą kwotę np 5000 zł za wynajem łodzi na hawajach co jest normalne kiedy wyjezdzasz daleko na wakacje ale system bankowy tego nie wie i blokuje transakcje ]

4. **QA vs QC:** Jaka jest główna różnica między Zapewnieniem Jakości (*Quality Assurance*) a Kontrolą Jakości (*Quality Control*)? Jak Twoja praca jako testera wpasowuje się w te pojęcia?
   > [QA jest proaktywne i polega na tym zeby wszystko gladko działało skupia się na zapobieganiu bledom i wypadkom a qc jest reaktywne i polega na testowaniu i szukaniu bledów i wypadków moja rola jako testera to głównie qc ale tez w ramach qa zglaszam bledy logiczne i sugeruje usprawnienia tak aby ulepszac proces powstawania produktu a co za tym idzie zmniejszyc liczbe bledów]

5. **Zasady Testowania:** Wyjaśnij swoimi słowami, na czym polega zasada "Paradoksu pestycydów" i jak można zapobiegać temu zjawisku w długoterminowych projektach.
   > [ paradoks pestycydów polega na tym ze ciagle wykonywanie tych samych testów w koncu przestaje przynosic efekty bo stare bledy juz zostaly znalezione a nowe moga sie czaić w innych miejscach. Aby temu zapobiegać nalezy regularnie aktualizowac i rozszerzac zestaw testów do tego warto zmieniac techniki testowania i uzywac losowych danych testowych. warto jednak wsponiec ze testy regresyjne sa wazne i nie nalezy ich pomijac ]

---

## 📖 Część 2: Pytania Teoretyczne (Rozdział 2 - Cykl Życia Oprogramowania)

6. **Regresja vs Re-testing:** Podaj sytuację z życia (np. aplikacja webowa), kiedy Testowanie Potwierdzające (*Re-testing*) zakończyło się sukcesem (zgłoszony błąd usunięto), ale wykonane zaraz po nim Testowanie Regresyjne (*Regression Testing*) udowodniło, że coś innego uległo awarii.
   > [Twoja odpowiedź tutaj] 
   
   w zaleznosci od tego co jest w kodzie wystarczy zmienić ilość argumentów konstruktora klasy i juz sie wszystko sypie albo zmienic definicję interfejsu. W przypadku testowania regresyjnego musimy sprawdzić czy zmiana nie wpłynęła na inne części aplikacji.

7. **Modele wytwarzania:** Jak różni się moment "wejścia" testera do projektu w kaskadowym modelu V (*V-Model*), a jak w zwinnym modelu iteracyjnym (*Agile/Scrum*)?
   > [w modelu V tester wchodzi do projektu w fazie analizy wymagan i projektowania systemu zeby zaplanowac testy i przygotowac dane testowe jednak faktyczne testowanie rozpoczyna się po zakonczeniu pisania kodu w modelu zwinnym tester wchodzi do projektu od razu i bierze udzial w calym procesie tworzenia oprogramowania razem z programistami i calym zespolem
   podejscie agile jest znacznie lepsze bo pozwala na prawie natychmiastowe wykrywanie bledow i reagowanie na zmiany w wymaganiach]

8. **Testy komponentowe a integracyjne:** Otrzymałeś do przetestowania pole wyszukiwarki na stronie. Czym będzie testowanie komponentowe w tym wypadku, a na czym skupisz się wykonując testowanie integracyjne (np. po podłączeniu bazy produktów)?
   > [testowanie komponentowe to testowanie konkretnego elementu na stronie i czy jest on zgodny z wymaganiami np czy wogole jest widoczne czy mozna w nie wpisac tekst czy ewnetualne zakresy np tekstu znaków dziala poprawnie co sie dzieke po wcisnieciu entera czy wysyla zadane a integracyjne to czy wyszukiwanie zwraca poprawne dane z bazy produktow czy dzialaja mechanizmy dodatkowe jak np sortowanie czy filtrowanie wydajnosc wyszukiwania i obciazenie serwera reasumujac testowanie komponentowe skupia sie na frontendzie a integracyjne na backendzie ]

---

## 💻 Część 3: Wyzwanie Programistyczne (White-box / Python)
Skoro przeszedłeś pierwsze testy Black-box naszej aplikacji konsolowej, pora zejść warstwę niżej do kodu źródłowego:

1. Otwórz w VS Code plik `istqb_trainer/main.py`.
2. Przeanalizuj słownik `DATA` znajdujący się na samej górze. Zauważ strukturę list i słowników.
3. **Zadanie (Rozdział 1):** Dodaj do słownika z palca 2 własne, prawdziwe pytania testowe.
4. **Zadanie (Rozdział 2):** Zaktualizuj sekcję `"theory"` dla rozdziału 2 na podstawie oficjalnego PDFa oraz dodaj 3 kolejne pytania.
5. Uruchom skrypt `./run_trainer.sh`, aby udowodnić, że w JSON-podobnym słowniku nie zgubiłeś przecinka ani klamry, a skrypt dalej odpala się bez błędów (wykonasz tym samym *testy potwierdzające* swojego kodu).

---

## 🔗 Część 4: Integracja z Repozytorium (Git)
Gdy odpowiesz na powyższe pytania i zaktualizujesz kod Pythona w pliku `main.py`:
1. Wpisz w terminalu: `git add .`
2. Następnie wykonaj commit: `git commit -m "feat: Rozwiązanie zadań z Rozdziału 1 i 2"`
3. Wypchnij pracę na GitHub: `git push origin main`