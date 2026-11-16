from decimal import Decimal

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

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
            get_account_message(connection)

        elif choice == "Add Account":
            add_account_prompt(connection)

        elif choice == "Get Account Transactions":
            get_account_transactions(connection)

        elif choice == "Get Account Categories":
            pass

        elif choice == "Get Account Merchants":
            pass

def get_account_message(connection):
    console.clear()

    accounts = account_service.get_accounts(connection)

    console.print(
        Panel(
            f"[bold {account_color}]YOUR ACCOUNTS[/bold {account_color}]\n"
            "View all registered accounts",
            border_style=f"{account_color}",
            padding=1
        )
    )

    if not accounts:
        console.print("\n[yellow]No accounts have been created yet...[/yellow]")

    else:
        table = Table(
            border_style=account_color,
            header_style=f"bold {account_color}",
            show_lines=True
        )

        table.add_column("ID", justify="center")
        table.add_column("Account Name")
        table.add_column("Account Type")
        table.add_column("Balance", justify="right")

        for account in accounts:
            table.add_row(
                str(account["account_id"]),
                account["account_name"],
                account["account_type"],
                f"${account['account_balance']:,.2f}"
            )

        console.print(table)

    questionary.text("\nPress Enter to return to the accounts menu.").ask()

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

    account_balance = Decimal(account_balance)

    try:
        account_id = account_service.add_account(connection, account_name.strip(), account_type, account_balance)

        console.print(
            Panel(
                f"[bold green]Account created successfully![/bold green]\n\n"
                f"Account ID: {account_id}\n"
                f"Account Name: {account_name.strip()}\n"
                f"Account Type: {account_type}\n"
                f"Starting Balance: ${account_balance:,.2f}",
                border_style="green",
                padding=1
            )
        )

    except Exception as error:
        console.print(f"\n[bold red]Failed to create account:[/bold red] {error}")

    questionary.text("\nPress Enter to return to the accounts menu.").ask()

def get_account_transactions(connection):
    console.clear()

    console.print(
        Panel(
            f"[bold {account_color}]ACCOUNT TRANSACTIONS[/bold {account_color}]\n"
            "View transactions associated with an account",
            border_style=account_color,
            padding=1
        )
    )

    account_id = select_account(connection)

    if account_id is None:
        return

    transactions = account_service.get_account_transactions(connection, account_id)

    console.clear()

    console.print(
        Panel(
            f"[bold {account_color}]ACCOUNT TRANSACTIONS[/bold {account_color}]",
            border_style=account_color,
            padding=1
        )
    )

    if not transactions:
        console.print("\n[yellow]No transactions found for this account.[/yellow]")

    else:
        table = Table(
            border_style=account_color,
            header_style=f"bold {account_color}",
            show_lines=True
        )

        table.add_column("ID", justify="center")
        table.add_column("Date")
        table.add_column("Category")
        table.add_column("Merchant")
        table.add_column("Description")
        table.add_column("Amount", justify="right")

        for transaction in transactions:
            is_income = transaction["category_type"] == "Income"

            amount = transaction["transaction_amount"]
            formatted_amount = (
                f"[green]+${amount:.2f}[/green]"
                if is_income
                else f"[red]+${amount:.2f}[/red]"
            )

            table.add_row(
                str(transaction["transaction_id"]),
                transaction["transaction_date"].strftime("%m/%d/%Y"),
                transaction["category_name"],
                transaction["merchant_name"] or "N/A",
                transaction["transaction_description"] or "N/A",
                formatted_amount
            )

        console.print(table)

    questionary.text("\nPress Enter to return to the accounts menu.").ask()

# Account Selection Helper
def select_account(connection):
    accounts = account_service.get_accounts(connection)

    if not accounts:
        console.print("\n[yellow]No accounts available.[/yellow]")
        questionary.text("Press Enter to continue.").ask()
        return None

    choices = [
        questionary.Choice(
            title=f"{account['account_name']} ({account['account_type']})",
            value=account["account_id"],
        )
        for account in accounts
    ]

    return questionary.select(
        "Select an account:",
        choices=choices,
        qmark="",
        pointer="❯"
    ).ask()