from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import questionary

console = Console()

def print_banner(version="0.1.0-alpha"):
    console.print(Panel.fit(
        "[bold cyan]🔥 SQL TRAINER - INTERACTIVE SANDBOX 🔥[/bold cyan]\n"
        "[dim]Ukryty Silnik: SQLite (ANSI SQL Compliant)[/dim]\n"
        "[dim]Zbudowane jako moduł treningowy dla Junior QA[/dim]",
        title=f"Wersja: {version}",
        border_style="cyan"
    ))

def print_error(msg):
    console.print(f"[bold red]❌ Błąd Serwera SQL:[/bold red] {msg}")

def print_success(msg):
    console.print(f"[bold green]✅ Sukces:[/bold green] {msg}")

def print_info(msg):
    console.print(f"[bold blue]ℹ️ Info:[/bold blue] {msg}")
