# 🚀 Dzień 1: Backlog Teoretyczny i Praktyczny (Rozdziały 1 i 2 ISTQB)

## 📖 Część 1: Pytania Teoretyczne (Rozdział 1 - Podstawy testowania)
Odpowiedz krótko i własnymi słowami, używając terminologii ISTQB:

1. **Analiza na wczesnym etapie:** Opisz krótko, w jakim celu wykonuje się analizę na samym etapie planowania nowej funkcjonalności (zanim powstanie kod – *Static Testing*).
   > [Twoja odpowiedź tutaj]

2. **Shift-Left w praktyce:** Jak w praktyce zastosujesz podejście *Shift-Left* (Przesunięcie w lewo) podczas projektowania nowej wtyczki "Koszyka" i jak uzasadnisz biznesowi zysk z tego podejścia?
   > [Twoja odpowiedź tutaj]

3. **Fałszywe ostrzeżenie:** Podaj realny przykład fałszywego ostrzeżenia (*False-positive*) podczas autoryzowania płatności (np. w systemie bankowym/Blik).
   > [Twoja odpowiedź tutaj]

4. **QA vs QC:** Jaka jest główna różnica między Zapewnieniem Jakości (*Quality Assurance*) a Kontrolą Jakości (*Quality Control*)? Jak Twoja praca jako testera wpasowuje się w te pojęcia?
   > [Twoja odpowiedź tutaj]

5. **Zasady Testowania:** Wyjaśnij swoimi słowami, na czym polega zasada "Paradoksu pestycydów" i jak można zapobiegać temu zjawisku w długoterminowych projektach.
   > [Twoja odpowiedź tutaj]

---

## 📖 Część 2: Pytania Teoretyczne (Rozdział 2 - Cykl Życia Oprogramowania)

6. **Regresja vs Re-testing:** Podaj sytuację z życia (np. aplikacja webowa), kiedy Testowanie Potwierdzające (*Re-testing*) zakończyło się sukcesem (zgłoszony błąd usunięto), ale wykonane zaraz po nim Testowanie Regresyjne (*Regression Testing*) udowodniło, że coś innego uległo awarii.
   > [Twoja odpowiedź tutaj]

7. **Modele wytwarzania:** Jak różni się moment "wejścia" testera do projektu w kaskadowym modelu V (*V-Model*), a jak w zwinnym modelu iteracyjnym (*Agile/Scrum*)?
   > [Twoja odpowiedź tutaj]

8. **Testy komponentowe a integracyjne:** Otrzymałeś do przetestowania pole wyszukiwarki na stronie. Czym będzie testowanie komponentowe w tym wypadku, a na czym skupisz się wykonując testowanie integracyjne (np. po podłączeniu bazy produktów)?
   > [Twoja odpowiedź tutaj]

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