import questionary
from typing import List

def select_path(paths: List[str]) -> str:
    """
    Interactive selection of a path from a list.
    Returns the selected path or None if cancelled.
    """
    if not paths:
        return None

    # Custom style for a premium look
    custom_style = questionary.Style([
        ('qmark', 'fg:#673ab7 bold'),
        ('question', 'bold'),
        ('answer', 'fg:#f44336 bold'),
        ('pointer', 'fg:#ff9800 bold'),
        ('highlighted', 'fg:#ff9800 bold'),
        ('selected', 'fg:#cc5454'),
        ('separator', 'fg:#cc5454'),
        ('instruction', ''),
        ('text', ''),
        ('disabled', 'fg:#858585 italic')
    ])

    try:
        selection = questionary.select(
            "Select destination:",
            choices=paths,
            style=custom_style,
            use_indicator=True,
            use_shortcuts=True,
            show_selected=True
        ).ask()
        return selection
    except KeyboardInterrupt:
        return None
