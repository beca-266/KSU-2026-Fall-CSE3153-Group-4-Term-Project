import questionary
from rich.console import Console
from rich.panel import Panel

from services import account_service

console = Console()

account_color = "#2a9d8f"

def account_menu(connection):
    while True:
        console.clear()

        console.print(
            Panel(
                f"[bold {account_color}]PERSONAL FINANCE TRACKER - ACCOUNTS MENU[/bold {account_color}]\n"
                "Manage your account",
                border_style=f"{account_color}",
                padding=1
            )
        )

        choice = questionary.select(
            "Select an interaction:",
            choices=[
                "Get Accounts",
                "Add Account",
                "Get Account Balance",
                "Get Account Transactions",
                "Get Account Categories",
                "Get Account Merchants",
                "Back"
            ],
            qmark="",
            pointer="❯"
        ).ask()

        if choice is None or choice == "Back":
            return

        elif choice == "Get Accounts":
            pass

        elif choice == "Add Account":
            add_account_prompt(connection)

        elif choice == "Get Account Balance":
            pass

        elif choice == "Get Account Transactions":
            pass

        elif choice == "Get Account Categories":
            pass

        elif choice == "Get Account Merchants":
            pass

def add_account_prompt(connection):
    console.clear()

    console.print(
        Panel(
            f"[bold {account_color}]ADD NEW ACCOUNT[/bold {account_color}]\n"
            "Create a new account",
            border_style=f"{account_color}",
            padding=1
        )
    )

    console.print("\n[bold]Follow the prompts below to create your account.[/bold]")
    console.print(
        "[dim]Enter the following information to continue.[/dim]\n"
    )

    account_name = questionary.text(
        "Account name:",
        validate=lambda value: (
            "Account name cannot be empty."
            if not (len(value.strip()) > 0)
            else "Account name cannot be over 100 characters."
            if not (len(value.strip()) < 100)
            else True
        )
    ).ask()

    if account_name is None:
        return

    account_type = questionary.select(
        "Account type:",
        choices=[
            "Checking",
            "Savings",
            "Cash"
        ],
        qmark="",
        pointer="❯"
    ).ask()

    if account_type is None:
        return

    account_balance = questionary.text(
        "Account balance:",
        default="0.00"
    ).ask()

    if account_balance is None:
        return

