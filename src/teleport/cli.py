import typer
import os
import sys
from pathlib import Path
from typing import Optional, List
from rapidfuzz import process, fuzz, utils
from rich.console import Console
from rich.table import Table
from .db import TeleportDB
from .tui import select_path
from .utils import get_db_path

__version__ = "1.0.0"

# --- Translations ---
STRINGS = {
    "en": {
        "header": f"[bold cyan]Teleport v{__version__}[/bold cyan] - Smart Directory Navigation",
        "add_desc": "Add current directory to history.",
        "save_desc": "Save a command with an alias.",
        "list_desc": "List frequent directories.",
        "clean_desc": "Clean history/commands.",
        "scan_desc": "Auto-scan subdirectories.",
        "config_desc": "Switch Language: [bold yellow]tp config --lang tr[/bold yellow]",
        "jump_desc": "Jump to directory or run alias.",
        "add_msg": "Added: [bold green]{}[/bold green]",
        "scan_msg": "Found & Added: [bold green]{}[/bold green]",
        "scan_summary": "Scan complete. Added {count} directories.",
        "scan_progress": "Scanning [bold cyan]{}[/bold cyan]...",
        "save_msg": "Saved alias: [bold yellow]{}[/bold yellow]",
        "empty_msg": "No history found. Start with 'tp add'.",
        "wipe_confirm": "Delete EVERYTHING?",
        "wipe_msg": "Database wiped.",
        "lang_msg": "Language set to [bold green]English[/bold green].",
        "backup_msg": "Database backed up to [bold green]{}[/bold green]",
        "restore_msg": "Database restored from [bold green]{}[/bold green]",
        "error_msg": "[bold red]Error:[/bold red] {}",
        "usage_title": "Usage:",
        "usage_examples": "Examples:\n  tp              Interactive Menu\n  tp <query>      Jump (e.g. tp doc)\n  tp scan         Auto-discover folders\n  tp add          Save path\n  tp list         Show stats"
    },
    "tr": {
        "header": f"[bold cyan]Teleport v{__version__}[/bold cyan] - Akıllı Dizin Gezgini",
        "add_desc": "Mevcut dizini geçmişe ekler.",
        "save_desc": "Komutu takma adla kaydeder.",
        "list_desc": "Sık kullanılanları listeler.",
        "clean_desc": "Geçmişi temizler.",
        "scan_desc": "Alt klasörleri otomatik ekle.",
        "config_desc": "Dili Değiştir: [bold yellow]tp config --lang en[/bold yellow]",
        "jump_desc": "Dizine git veya alias çalıştır.",
        "add_msg": "Eklendi: [bold green]{}[/bold green]",
        "scan_msg": "Bulundu ve Eklendi: [bold green]{}[/bold green]",
        "scan_summary": "Tarama bitti. {count} dizin eklendi.",
        "scan_progress": "Taranıyor: [bold cyan]{}[/bold cyan]...",
        "save_msg": "Kaydedildi: [bold yellow]{}[/bold yellow]",
        "empty_msg": "Geçmiş boş. 'tp add' ile başlayın.",
        "wipe_confirm": "HER ŞEY silinsin mi?",
        "wipe_msg": "Veritabanı temizlendi.",
        "lang_msg": "Dil [bold green]Türkçe[/bold green] olarak ayarlandı.",
        "backup_msg": "Veritabanı yedeklendi: [bold green]{}[/bold green]",
        "restore_msg": "Veritabanı geri yüklendi: [bold green]{}[/bold green]",
        "error_msg": "[bold red]Hata:[/bold red] {}",
        "usage_title": "Kullanım:",
        "usage_examples": "Örnekler:\n  tp              Menüyü Aç\n  tp <sorgu>      Git (ör: tp belge)\n  tp scan         Klasörleri Keşfet\n  tp add          Kaydet\n  tp list         İstatistikler"
    }
}

def get_lang():
    lang_file = get_db_path().parent / "lang.txt"
    try:
        return lang_file.read_text().strip()
    except OSError:
        return "en"

def set_lang(lang: str):
    lang_file = get_db_path().parent / "lang.txt"
    lang_file.write_text(lang)

def t(key, *args, **kwargs):
    lang = get_lang()
    # Fallback to English if key missing
    text = STRINGS.get(lang, STRINGS["en"]).get(key, key)
    # Handle positional args
    if args: return text.format(*args)
    # Handle kwargs
    return text.format(**kwargs)

# --- Custom Help System ---
app = typer.Typer(add_completion=False, help=None)

db_instance = None
def get_db():
    global db_instance
    if db_instance is None:
        db_instance = TeleportDB()
    return db_instance

@app.command(name="help", hidden=True)
def help_cmd():
    _show_custom_help()

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, version: bool = typer.Option(False, "--version", "-v"), help: bool = typer.Option(False, "--help", "-h")):
    if version:
        print(f"Teleport v{__version__}")
        raise typer.Exit()
    if help or ctx.invoked_subcommand is None:
        if ctx.invoked_subcommand is None and len(sys.argv) > 1:
             pass # Handled by jump
        elif help:
             _show_custom_help()
             raise typer.Exit()

@app.command(name="add")
def add_cmd(path: Optional[str] = typer.Argument(None)):
    db = get_db()
    target = str(Path(path or os.getcwd()).resolve())
    db.add_path(target)
    Console().print(t("add_msg", target))

@app.command(name="save")
def save_cmd(command: str = typer.Argument(...), name: str = typer.Option(..., "--name", "-n")):
    get_db().add_command(name, command)
    Console().print(t("save_msg", name))

@app.command(name="list")
def list_cmd():
    paths = get_db().get_frequent_paths()
    if not paths:
        Console().print(t("empty_msg"))
        return
    
    table = Table(box=None, padding=(0, 2))
    table.add_column("Score", justify="right", style="cyan")
    table.add_column("Path", style="green")
    
    for p, score in paths[:20]:
        table.add_row(f"{score:.1f}", p)
        
    Console().print(table)

@app.command(name="config")
def config_cmd(lang: str = typer.Option(None, "--lang", "-l")):
    if lang == "tr":
        set_lang("tr")
        Console().print(t("lang_msg"))
    elif lang == "en":
        set_lang("en")
        Console().print(t("lang_msg"))
    else:
        print(f"Current: {get_lang()} (Options: tr, en)")

@app.command(name="scan")
def scan_cmd(path: Optional[str] = typer.Argument(None)):
    """Auto-discovery (Subdirectories)."""
    db = get_db()
    
    if path:
        start_dir = Path(path).resolve()
    else:
        start_dir = Path(os.getcwd()).resolve()

    t_msg = t("scan_progress", str(start_dir))
    Console().print(t_msg)
    
    count = 0
    
    # 1 Level deep scan (Direct subdirectories only)
    try:
        subdirs = [d for d in os.listdir(start_dir) if os.path.isdir(start_dir / d)]
    except OSError:
        subdirs = []

    for d in subdirs:
        if d in {".git", "node_modules", "venv", ".venv", "__pycache__", ".idea", ".vscode", "dist", "build", "target", "vendor", "bin", "obj", ".hg", ".svn"}:
            continue
            
        target = str(start_dir / d)
        db.add_path(target)
        Console().print(t("scan_msg", target))
        count += 1
            
    Console().print(t("scan_summary", count=count))

@app.command(name="clean")
def clean_cmd(
    items: Optional[List[str]] = typer.Argument(None),
    all: bool = typer.Option(False, "--all", "-a")
):
    """Clean history."""
    db = get_db()
    if all:
        if typer.confirm(t("wipe_confirm")):
            db.clear_history()
            db.clear_commands()
            Console().print(t("wipe_msg"))
        return
    
    if not items:
        # Show help if no args for clean
        _show_custom_help()
        return

    for item in items:
        if db.remove_command(item):
            print(f"Removed alias: {item}")
        elif db.remove_path(item):
            print(f"Removed path: {item}")

@app.command(name="backup")
def backup_cmd(path: str = typer.Argument(...)):
    """Backup database."""
    target = Path(path).resolve()
    if get_db().backup(str(target)):
        Console().print(t("backup_msg", str(target)))
    else:
        Console().print(t("error_msg", "Backup failed"))

@app.command(name="restore")
def restore_cmd(path: str = typer.Argument(...)):
    """Restore database."""
    target = Path(path).resolve()
    if not target.exists():
        Console().print(t("error_msg", "File not found"))
        return
        
    if get_db().restore(str(target)):
        Console().print(t("restore_msg", str(target)))
    else:
         Console().print(t("error_msg", "Restore failed"))

@app.command(name="jump", hidden=True)
def jump_cmd(
    query: Optional[List[str]] = typer.Argument(None),
    output_file: Optional[Path] = typer.Option(None, "--output-file", "-o"),
    interactive: bool = typer.Option(False, "--interactive", "-i"),
):
    db = get_db()
    full_query = " ".join(query) if query else None
    
    if full_query:
        cmd = db.get_command(full_query)
        if cmd:
            _write(f"CMD:{cmd}", output_file)
            return

    paths = db.get_frequent_paths()
    if not paths:
        if not full_query:
            _show_custom_help()
            return
        else:
            Console().print(t("empty_msg"))
            _show_custom_help()
            return

    candidates = [p[0] for p in paths]
    
    if full_query and not interactive:
        # Use extractOne for single best match with processor for better case handling
        # Lower threshold to catch partials like 'pro' -> 'Projects'
        match = process.extractOne(full_query, candidates, scorer=fuzz.WRatio, processor=utils.default_process)
        
        if match and match[1] > 50: # Threshold 50
            _write(f"CD:{match[0]}", output_file)
            return
        else:
            lang = get_lang()
            msg = f"Bulunamadı: {full_query}" if lang == 'tr' else f"Not found: {full_query}"
            Console().print(f"[bold red]{msg}[/bold red]")
            suggestion = f"Eklemek için o dizine gidin ve 'tp add' yazın." if lang == 'tr' else "Go there and type 'tp add' to save it."
            Console().print(f"[dim]{suggestion}[/dim]")
            return
    
    # Interactive Search
    selected = select_path(candidates[:25])
    if selected:
        db.add_path(selected)
        _write(f"CD:{selected}", output_file)

def _write(content: str, output_file: Optional[Path]):
    if output_file:
        output_file.write_text(content)
    else:
        print(content.replace("CD:", "").replace("CMD:", ""))

def _show_custom_help():
    console = Console()
    console.print(t("header"))
    console.print("")
    
    table = Table(show_header=True, header_style="bold magenta", box=None, padding=(0, 2))
    lang = get_lang()
    
    if lang == "tr":
        table.add_column("Komut", style="bold green")
        table.add_column("İşlev")
        table.add_column("Örnek", style="dim")
        
        table.add_row("tp", "Etkileşimli Menü", "tp")
        table.add_row("tp <sorgu>", "Dizine Git", "tp bel")
        table.add_row("tp scan", "Klasörleri Keşfet", "tp scan ~/Projeler")
        table.add_row("tp add", "Dizini Ekle", "tp add")
        table.add_row("tp save", "Komut Kaydet", "tp save 'ls -la' -n ll")
        table.add_row("tp list", "İstatistikler", "tp list")
        table.add_row("tp clean", "Temizlik Yap", "tp clean --all")
        table.add_row("tp backup", "Yedekle", "tp backup ~/tp.bak")
        table.add_row("tp restore", "Geri Yükle", "tp restore ~/tp.bak")
        table.add_row("tp config", "Dili Değiştir", "tp config --lang en")
    else:
        table.add_column("Command", style="bold green")
        table.add_column("Action")
        table.add_column("Example", style="dim")
        
        table.add_row("tp", "Interactive Menu", "tp")
        table.add_row("tp <query>", "Jump to directory", "tp doc")
        table.add_row("tp scan", "Auto-discover folders", "tp scan ~/Projects")
        table.add_row("tp add", "Add current directory", "tp add")
        table.add_row("tp save", "Save command alias", "tp save 'ls -la' -n ll")
        table.add_row("tp list", "Show stats", "tp list")
        table.add_row("tp clean", "Clean history", "tp clean --all")
        table.add_row("tp backup", "Backup DB", "tp backup ~/tp.bak")
        table.add_row("tp restore", "Restore DB", "tp restore ~/tp.bak")
        table.add_row("tp config", "Change language", "tp config --lang tr")

    console.print(table)
    console.print("")
    console.print(f"[dim]Version: {__version__}[/dim]")

if __name__ == "__main__":
    app()
