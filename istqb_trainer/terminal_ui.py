import sys
import os
import tty
import termios
import questionary
from rich.console import Console

console = Console()

def get_custom_style():
    """Zwraca dedykowany styl zapobiegający oczopląsowi z questionary."""
    return questionary.Style([
        ('qmark', 'fg:#5f87d7 bold'),       # Znak zapytania
        ('question', 'bold fg:#ffffff'),    # Tytul pytania / menu
        ('answer', 'fg:#00afaf bold'),      # Kolor wpisywanego tekstu (biurowy błękit zamiast pomarańczu)
        ('pointer', 'fg:#ffffff bg:#005f87 bold'), # Focus cursor
        ('highlighted', 'fg:#ffffff bg:#005f87 bold'), # Cale tlo wybranego rzedu w menu
        ('selected', 'fg:#00d700'),         # Zaznaczone checkboxy
        ('separator', 'fg:#6c6c6c'),        
        ('instruction', 'fg:#808080 italic'),
        ('text', 'fg:#e4e4e4'),
    ])

def getch():
    """Niskopoziomowe pobieranie znaków na Linux/Mac (bez potrzeby wciskania Enter)."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        # Obsługa strzałek (sekwencje escape na Uniksie to zazwyczaj \x1b[A, \x1b[B)
        if ch == '\x1b':
            ch += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def nano_pager(title, content, allow_edit=False):
    """
    Renderuje pełnoekranowe okienko dla długiego tekstu używając strzałek i skrótów klawiszowych.
    Zwraca string z kodem wciśniętego skótu: 'quit', 'menu', lub 'edit'.
    """
    lines = content.split('\n')
    offset = 0
    
    while True:
        try:
            term_cols, term_lines = os.get_terminal_size()
        except OSError:
            term_cols, term_lines = 80, 24

        # Zostawiamy 4 linie na tytuł (z kreska) i 3 linie na stopkę
        visible_lines_count = max(5, term_lines - 7)
        max_offset = max(0, len(lines) - visible_lines_count)

        if offset > max_offset:
            offset = max_offset
        if offset < 0:
            offset = 0

        visible_portion = lines[offset : offset + visible_lines_count]

        # Czyść ekran
        print('\033c', end='')
        
        # Wyświetl nagłówek
        console.print(f"[bold cyan]--- {title} ---[/bold cyan]")
        console.print("[dim]" + ("-" * (term_cols - 1)) + "[/dim]")
        
        # Wyświetl tekst
        for line in visible_portion:
            console.print(line)
            
        # Puste miejsca by stopka była zakotwiczona na dole (Sticky footer)
        empty_lines_needed = visible_lines_count - len(visible_portion)
        for _ in range(empty_lines_needed):
            print()

        # Wyświetl stopkę w stylu Nano
        console.print("[dim]" + ("-" * (term_cols - 1)) + "[/dim]")
        footer_shortcuts = "[bold][↑/↓][/bold] Przewiń   [bold][Q][/bold] Wyjdź   [bold][M][/bold] Wróć do menu"
        if allow_edit:
            footer_shortcuts += "   [bold][E][/bold] Edytuj zawartość"
            
        console.print(f"{footer_shortcuts}")

        # Pętla nasłuchu na akcję użytkownika
        c = getch()
        
        if c.lower() == 'q':
            return 'quit'
        elif c.lower() == 'm':
            return 'menu'
        elif c.lower() == 'e' and allow_edit:
            return 'edit'
        elif c == '\x1b[A': # Up Arrow
            offset -= 1
        elif c == '\x1b[B': # Down Arrow
            offset += 1
        elif c == '\x1b[5~': # Page Up (możliwy w niektórych terminalach)
            offset -= visible_lines_count
        elif c == '\x1b[6~': # Page Down
            offset += visible_lines_count
