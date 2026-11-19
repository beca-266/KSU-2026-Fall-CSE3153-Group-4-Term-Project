import questionary
from rich.console import Console
from rich.panel import Panel

from services import report_service

console = Console()

report_color = "#B88E8D"

def report_menu(connection):
    console.clear()

    console.print(
        Panel(
            f"[bold {report_color}]PERSONAL FINANCE TRACKER - REPORT MENU[/bold {report_color}]\n"
            "Manage your reports",
            border_style=f"{report_color}",
            padding=1
        )
    )

    choice = questionary.select(
        "Select an interaction:",
        choices=[
            "Get Spending By Category",
            "Get Income vs Expenses",
            "Get Top Merchants",
            "Back"
        ],
        qmark="",
        pointer="❯"
    ).ask()

    if choice is None or choice == "Back":
        return

    elif choice == "Get Spending By Category":
        pass

    elif choice == "Get Income vs Expenses":
        pass

    elif choice == "Get Top Merchants":
        pass