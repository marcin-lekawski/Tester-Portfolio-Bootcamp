import sqlite3
import os
import random
from datetime import datetime, timedelta

def create_fantasy_sandbox(db_path="D&D_sandbox.db"):
    """
    Inicjalizuje i zasila bazę danych D&D RPG do nauki SQL!
    Zastępuje całkowicie starą, nudną bazę "Kadrowo-Płacową".
    """
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # ---------------------------------------------------------
    # GŁÓWNY SCHEMAT ZAPROPONOWANY PRZEZ MISTRZA GRY (USER)
    # ---------------------------------------------------------

    # 0. Bohaterowie (Podstawa do Kluczy Obcych, których wymagał model użytkownika)
    c.execute('''CREATE TABLE IF NOT EXISTS Bohaterowie (
                    id_bohatera INTEGER PRIMARY KEY AUTOINCREMENT,
                    imie TEXT NOT NULL,
                    rasa TEXT,
                    klasa TEXT,
                    poziom INTEGER DEFAULT 1,
                    zloto INTEGER DEFAULT 0
                )''')

    # 1. Statystyki Bazowe (System D&D: Siła, Zręczność, Kondycja, Inteligencja, Mądrość, Charyzma)
    c.execute('''CREATE TABLE IF NOT EXISTS Statystyki (
                    id_bohatera INTEGER PRIMARY KEY,
                    sila INTEGER DEFAULT 10,
                    zrecznosc INTEGER DEFAULT 10,
                    kondycja INTEGER DEFAULT 10,
                    inteligencja INTEGER DEFAULT 10,
                    madrosc INTEGER DEFAULT 10,
                    charyzma INTEGER DEFAULT 10,
                    FOREIGN KEY (id_bohatera) REFERENCES Bohaterowie(id_bohatera)
                )''')

    # 2. Bestiariusz (Tu mieszkają Twoi przeciwnicy)
    c.execute('''CREATE TABLE IF NOT EXISTS Bestiariusz (
                    id_potwora INTEGER PRIMARY KEY AUTOINCREMENT,
                    nazwa TEXT NOT NULL,
                    typ TEXT,
                    poziom_zagrozenia INTEGER,
                    hp_max INTEGER,
                    opis_ataku TEXT,
                    drop_zloto_min INTEGER,
                    drop_zloto_max INTEGER
                )''')

    # 3. Lokacje i Regiony (Mapa świata)
    c.execute('''CREATE TABLE IF NOT EXISTS Lokacje (
                    id_lokacji INTEGER PRIMARY KEY AUTOINCREMENT,
                    nazwa TEXT NOT NULL,
                    typ TEXT,
                    opis TEXT,
                    bezpieczenstwo INTEGER CHECK(bezpieczenstwo BETWEEN 0 AND 100),
                    id_regionu_nadrzednego INTEGER,
                    FOREIGN KEY (id_regionu_nadrzednego) REFERENCES Lokacje(id_lokacji)
                )''')

    # 4. Dziennik Zdarzeń (Logi sesji - tu będziemy zapisywać co się stało)
    c.execute('''CREATE TABLE IF NOT EXISTS Kronika_Przygód (
                    id_wpisu INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_gry TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    id_bohatera INTEGER,
                    opis_czynu TEXT,
                    wynik_kosci INTEGER,
                    czy_sukces BOOLEAN,
                    FOREIGN KEY (id_bohatera) REFERENCES Bohaterowie(id_bohatera)
                )''')

    # 5. System Relacji i NPC
    c.execute('''CREATE TABLE IF NOT EXISTS NPC (
                    id_npc INTEGER PRIMARY KEY AUTOINCREMENT,
                    imie TEXT NOT NULL,
                    funkcja TEXT,
                    nastawienie INTEGER DEFAULT 50,
                    id_lokacji INTEGER,
                    FOREIGN KEY (id_lokacji) REFERENCES Lokacje(id_lokacji)
                )''')


    # ---------------------------------------------------------
    # TABLICE SZKOLENIOWE (ŻEBY KODY SELECT Z CURRICULUM DZIAŁAŁY 1:1)
    # ---------------------------------------------------------
    c.execute('''CREATE TABLE Plecak (nazwa TEXT, moc INTEGER)''')
    c.execute('''CREATE TABLE Druzyna (imie TEXT, HP INTEGER)''')
    c.execute('''CREATE TABLE NapotkaneIstoty (rasa TEXT)''')
    c.execute('''CREATE TABLE Ekwipunek (nazwa TEXT, czy_magiczny INTEGER)''')
    c.execute('''CREATE TABLE Turniej (imie TEXT, punkty INTEGER)''')
    c.execute('''CREATE TABLE Smoki (imie TEXT, wiek INTEGER)''')
    c.execute('''CREATE TABLE Mieszkancy (miasto TEXT, zloto INTEGER)''')
    c.execute('''CREATE TABLE Biblioteka (tytul TEXT)''')
    c.execute('''CREATE TABLE Misje (id_misji INTEGER PRIMARY KEY, nazwa TEXT, id_bohatera INTEGER)''')
    c.execute('''CREATE TABLE Konie (id INTEGER PRIMARY KEY, rasa TEXT)''')
    c.execute('''CREATE TABLE Rycerze (id INTEGER PRIMARY KEY, imie TEXT, id_konia INTEGER)''')
    c.execute('''CREATE TABLE Sojusznicy_A (imie TEXT)''')
    c.execute('''CREATE TABLE Sojusznicy_B (imie TEXT)''')
    c.execute('''CREATE TABLE Gracze (imie TEXT, poziom INTEGER)''')
    c.execute('''CREATE TABLE Postacie (imie TEXT, sila INTEGER)''')
    c.execute('''CREATE TABLE Portfele (id INTEGER PRIMARY KEY, zloto INTEGER)''')
    c.execute('''CREATE TABLE Plecaki (id INTEGER PRIMARY KEY, przedmiot TEXT)''')


    # ---------------------------------------------------------
    # ZASILANIE DANYMI (INSERTY ŚWIATA MAGII)
    # ---------------------------------------------------------
    
    # Bohaterowie & Druzyna & Postacie & Gracze
    heroes = [
        ("Geralt", "Wiedzmin", "Wojownik", 35, 1500),
        ("Zygfryd", "Czlowiek", "Paladyn", 20, 200),
        ("Legolas", "Elf", "Lucznik", 50, 0),
        ("Gimli", "Krasnolud", "Wojownik", 45, 800),
        ("Gandalf", "Majowie", "Mag", 99, 10000),
        ("Frodo", "Niziolek", "Zlodziej", 10, 50)
    ]
    c.executemany("INSERT INTO Bohaterowie(imie, rasa, klasa, poziom, zloto) VALUES (?,?,?,?,?)", heroes)
    
    for idx, h in enumerate(heroes):
        # Statystyki (D&D 5e style)
        c.execute("INSERT INTO Statystyki(id_bohatera, sila, zrecznosc, kondycja, inteligencja, madrosc, charyzma) VALUES (?,?,?,?,?,?,?)",
                  (idx+1, random.randint(8,20), random.randint(8,20), random.randint(8,20), random.randint(8,20), random.randint(8,20), random.randint(8,20)))
        c.execute("INSERT INTO Druzyna(imie, HP) VALUES (?,?)", (h[0], random.randint(50, 200)))
        c.execute("INSERT INTO Gracze(imie, poziom) VALUES (?,?)", (h[0], h[3]))
        c.execute("INSERT INTO Postacie(imie, sila) VALUES (?,?)", (h[0], random.randint(10, 95)))
        c.execute("INSERT INTO Portfele(id, zloto) VALUES (?,?)", (idx+1, h[4]))
        c.execute("INSERT INTO Plecaki(id, przedmiot) VALUES (?,?)", (idx+1, "Puste Miejsce"))

    # Bestiariusz & Smoki
    monsters = [
        ("Czerwony Smok", "Smok", 17, 450, "Zionie ogniem w ksztalcie stozka", 1000, 5000),
        ("Bandyta", "Czlowiek", 1, 15, "Atak mieczem z ukrycia", 0, 10),
        ("Prastary Lisz", "Nieumarly", 21, 135, "Dotyk smierci", 2000, 10000),
        ("Goblin", "Bestia", 1, 7, "Machanie maczuga", 1, 5),
        ("Wilkor", "Bestia", 3, 30, "Rozszarpanie", 0, 0)
    ]
    c.executemany("INSERT INTO Bestiariusz(nazwa, typ, poziom_zagrozenia, hp_max, opis_ataku, drop_zloto_min, drop_zloto_max) VALUES (?,?,?,?,?,?,?)", monsters)
    
    c.execute("INSERT INTO Smoki(imie, wiek) VALUES ('Smaug', 450)")
    c.execute("INSERT INTO Smoki(imie, wiek) VALUES ('Villentretenmerth', 200)")
    c.execute("INSERT INTO Smoki(imie, wiek) VALUES ('Maly Jasio', 5)")

    # Lokacje i Regiony
    # Główny region:
    c.execute("INSERT INTO Lokacje(nazwa, typ, opis, bezpieczenstwo, id_regionu_nadrzednego) VALUES ('Wielkie Krolestwo', 'Stolica', 'Glowne miasto imperium', 100, NULL)")
    c.execute("INSERT INTO Lokacje(nazwa, typ, opis, bezpieczenstwo, id_regionu_nadrzednego) VALUES ('Karczma Pod Rozbrykanym Kucykiem', 'Karczma', 'Dobre piwo', 80, 1)")
    c.execute("INSERT INTO Lokacje(nazwa, typ, opis, bezpieczenstwo, id_regionu_nadrzednego) VALUES ('Mroczny Las', 'Las', 'Pelno pajakow', 10, NULL)")
    c.execute("INSERT INTO Lokacje(nazwa, typ, opis, bezpieczenstwo, id_regionu_nadrzednego) VALUES ('Jaskinia Czerwonego Smoka', 'Loch', 'Smierdzaca siarka jama', 0, 3)")

    # NPC
    npcs = [
        ("Barliman", "Karczmarz", 80, 2),
        ("Kowal Kofur", "Paser", 40, 1),
        ("Foltest", "Krol", 50, 1)
    ]
    c.executemany("INSERT INTO NPC(imie, funkcja, nastawienie, id_lokacji) VALUES (?,?,?,?)", npcs)

    # Kronika Przygód
    logs = [
        (1, "Zabil Goblina uzywajac miecza", 18, True),
        (2, "Otworzyl zamek w drzwiach wytrychem", 15, True),
        (3, "Ostrzal pajaki w lesie", 5, False),
        (4, "Negocjowal cene miecza z uzyciem persfazji", 2, False), # failure
        (5, "Rozproszyl zaklecie na klatce", 20, True) # critical hit!
    ]
    base_date = datetime.strptime("2026-06-01", "%Y-%m-%d")
    for lg in logs:
        time_str = (base_date + timedelta(hours=random.randint(0,400))).strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO Kronika_Przygód(data_gry, id_bohatera, opis_czynu, wynik_kosci, czy_sukces) VALUES (?,?,?,?,?)",
                  (time_str, lg[0], lg[1], lg[2], lg[3]))

    # Inne tabele szkoleniowe z curriculum
    c.executemany("INSERT INTO Plecak(nazwa, moc) VALUES (?,?)", [("Mikstura Leczenia", 50), ("Maly Kamien", 0), ("Zwoj Ognistej Kuli", 100)])
    c.executemany("INSERT INTO Ekwipunek(nazwa, czy_magiczny) VALUES (?,?)", [("Prosty Miecz", 0), ("Buty Szybkosci", 1), ("Drewniana Tarcza", 0), ("Rozdzka Many", 1)])
    c.executemany("INSERT INTO NapotkaneIstoty(rasa) VALUES (?)", [("Elf",), ("Krasnolud",), ("Troll",), ("Elf",), ("Elf",), ("Zombiak",)])
    c.executemany("INSERT INTO Turniej(imie, punkty) VALUES (?,?)", [("Lancelot", 100), ("Artur", 95), ("Gawen", 90), ("Percival", 85)])
    
    towns = [("Avalon", 1500), ("Neverwinter", 5000), ("Gondor", 10000), ("Novigrad", 25000), ("Ciemny Zaulek", 10)]
    c.executemany("INSERT INTO Mieszkancy(miasto, zloto) VALUES (?,?)", towns)
    
    c.executemany("INSERT INTO Biblioteka(tytul) VALUES (?)", [("Wielka Ksiega Magii",), ("Wielka Historia Gondoru",), ("Maly Traktat o Mieczach",)])
    
    c.executemany("INSERT INTO Misje(nazwa, id_bohatera) VALUES (?,?)", [("Zabij szczury", 1), ("Idz po piwo", 2), ("Uratuj ksiezniczke", None)])
    
    c.executemany("INSERT INTO Konie(id, rasa) VALUES (?,?)", [(1, "Plotka"), (2, "Arab"), (3, "Mustang")])
    c.executemany("INSERT INTO Rycerze(imie, id_konia) VALUES (?,?)", [("Geralt", 1), ("Lancelot", 2), ("Pieszy Zygfryd", None)])
    
    c.executemany("INSERT INTO Sojusznicy_A(imie) VALUES (?)", [("Elfy",), ("Krasnoludy",)])
    c.executemany("INSERT INTO Sojusznicy_B(imie) VALUES (?)", [("Ludzie",), ("Krasnoludy",)])


    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_fantasy_sandbox()
