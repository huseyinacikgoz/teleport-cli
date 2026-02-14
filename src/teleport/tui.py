from typing import List, Optional
import questionary
from rich.console import Console
from prompt_toolkit.styles import Style

def select_path(paths: List[str]) -> Optional[str]:
    """
    Interactive fuzzy search selection.
    User can type to filter the list instantly.
    """
    if not paths:
        return None

    # Custom Style matching Teleport branding
    custom_style = Style([
        ('qmark', 'fg:#673ab7 bold'),       # violet
        ('question', 'bold'),               # bold default
        ('answer', 'fg:#f44336 bold'),      # red answer
        ('pointer', 'fg:#ff9800 bold'),     # orange pointer
        ('highlighted', 'fg:#ff9800 bold')  # orange highlight
    ])

    try:
        # Using autocomplete for better UX (type-to-filter)
        # Note: autocomplete might feel slow with huge lists, but for <100 paths it's perfect.
        # Fallback to select if list is huge? No, usually paths are filtered first.
        
        # Simple selection with search capability via questionary.select usually handles basic filtering
        # But let's try 'autocomplete' style behavior if possible.
        # Actually, questionary.select uses prompt_toolkit which supports type-to-navigate.
        # Let's stick to .select() but refine the prompt.
        
        selection = questionary.select(
            "Where to?",
            choices=paths,
            style=custom_style,
            use_indicator=True,
            use_shortcuts=False, # Disable shortcuts to allow more than 36 items
            show_selected=True,
            instruction="(Use arrow keys or type to filter)"
        ).ask()
        
        return selection
    except KeyboardInterrupt:
        return None
