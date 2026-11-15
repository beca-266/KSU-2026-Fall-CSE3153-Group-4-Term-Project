import questionary
from rich.console import Console
from rich.panel import Panel

from services import budget_service

console = Console()

budget_color = "#f4a261"

def budget_menu(connection):
    console.clear()

    console.print(
        Panel(
            f"[bold {budget_color}]PERSONAL FINANCE TRACKER - BUDGET MENU[/bold {budget_color}]\n"
            "Manage your budgets",
            border_style=f"{budget_color}",
            padding=1
        )
    )

    choice = questionary.select(
        "Select an interaction:",
        choices=[
            "Set Budget",
            "Get Budgets",
            "Calculate Remaining Budget",
            "Back"
        ],
        qmark="",
        pointer="❯"
    ).ask()

    if choice is None or choice == "Back":
        return

    elif choice == "Set Budget":
        pass

    elif choice == "Get Budgets":
        pass

    elif choice == "Calculate Remaining Budget":
        pass