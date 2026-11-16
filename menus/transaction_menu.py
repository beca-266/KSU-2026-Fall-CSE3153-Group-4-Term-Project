import questionary
from rich.console import Console
from rich.panel import Panel

from services import transaction_service

console = Console()

transaction_color = "#34435E"

def transaction_menu(connection):
    console.clear()

    console.print(
        Panel(
            f"[bold {transaction_color}]PERSONAL FINANCE TRACKER - TRANSACTION MENU[/bold {transaction_color}]\n"
            "Manage your transactions",
            border_style=f"{transaction_color}",
            padding=1
        )
    )

    choice = questionary.select(
        "Select an interaction:",
        choices=[
            "Add Transaction",
            "Delete Transaction",
            "Update Transaction",
            "Get Transactions",
            "Back"
        ],
        qmark="",
        pointer="❯"
    ).ask()

    if choice is None or choice == "Back":
        return

    elif choice == "Add Transaction":
        pass

    elif choice == "Delete Transaction":
        pass

    elif choice == "Update Transaction":
        pass

    elif choice == "Get Transactions":
        pass