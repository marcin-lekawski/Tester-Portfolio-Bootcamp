import pytest
import re

def test_regex_matching_correct_answer():
    """
    Kluczowy test analizy zapór 'Brak'. Bug #004 polegał na tym że regex
    nie odczytywał poprawnie 'A, C' albo psuł się na nowej linii ułamanej z PDFu.
    """
    
    # Symulacja surowego bloku tekstu wyrwanego żywcem z PDF z Uzasadnieniami ISTQB
    text_scenario_1 = "Odpowiedź b) to słuszna opcja wg Sylabusa."
    
    # Skomplikowany Regex użyty głęboko w core parsera
    regex_pattern = r'(?:Odpowiedź|Poprawną odpowiedzią|Odp\.)\s*(?:to\s*)?([abcdABCD](?:\s*,\s*[abcdABCD])*)\)'
    
    match_1 = re.search(regex_pattern, text_scenario_1, re.IGNORECASE)
    assert match_1 is not None, "Asercja zrąbana! Silnik Regex nie złapał klasycznego wariantu Odp b)"
    assert match_1.group(1).lower() == "b", "Regex złapał śmieci pomiast litery 'b'"
    
    # Sprawdzanie Bugu #004 (Omijanie 'Brak' przy odpowiedziach wielokrotnego wyboru)
    text_scenario_2 = "Uzasadnienia po Egzaminie:\nOdp. a, d) są prawidłowymi wyborami."
    match_2 = re.search(regex_pattern, text_scenario_2, re.IGNORECASE)
    assert match_2 is not None, "Wyłożył się na skrótach Odp a, d)!"
    assert match_2.group(1).lower() == "a, d", f"Parsuje z błedem: Oczekiwałem 'a, d', dostałem {match_2.group(1).lower()}"
    
    text_scenario_3 = "Odpowiedź to c)"
    match_3 = re.search(regex_pattern, text_scenario_3, re.IGNORECASE)
    assert match_3 is not None
    assert match_3.group(1).lower() == "c"
