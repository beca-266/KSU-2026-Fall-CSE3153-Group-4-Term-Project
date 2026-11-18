from datetime import datetime

import questionary
from rich.console import Console
from rich.panel import Panel

from menus import menu_utils
from services import transaction_service

console = Console()

transaction_color = "#e76f51"

def transaction_menu(connection):
    while True:
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
                "Back"
            ],
            qmark="",
            pointer="❯"
        ).ask()

        if choice is None or choice == "Back":
            return

        elif choice == "Add Transaction":
            add_transaction_prompt(connection)

        elif choice == "Delete Transaction":
            pass

        elif choice == "Update Transaction":
            pass

def add_transaction_prompt(connection):
    console.clear()

    console.print(
        Panel(
            f"[bold {transaction_color}]ADD NEW TRANSACTION[/bold {transaction_color}]\n"
            "Record a new income or expense",
            border_style=transaction_color,
            padding=1
        )
    )

    console.print(
        "\n[bold]Follow the prompts below to record your transaction.[/bold]"
    )

    account_id = menu_utils.select_account(connection)

    if account_id is None:
        return

    category_id = menu_utils.select_category(connection)

    if category_id is None:
        return

    merchant_id = None

    choice = questionary.select(
        "Would you like to associate a merchant with this transaction:",
        choices=[
            "Yes",
            "No"
        ],
        qmark="",
        pointer="❯"
    ).ask()

    if choice == "Yes":
        merchant_id = menu_utils.select_merchant(connection)

    transaction_amount = questionary.text(
        "Transaction amount:",
        validate=lambda value: (
            True if value.strip() else "Amount cannot be empty."
        )
    ).ask()

    if transaction_amount is None:
        return

    transaction_date_input = questionary.text(
        "Enter transaction date (MM/DD/YYYY):",
        qmark=""
    ).ask()

    if transaction_date_input is None:
        return

    try:
        transaction_date = datetime.strptime(
            transaction_date_input,
            "%m/%d/%Y"
        )
    except ValueError:
        console.print("[red]Invalid date. Please use MM/DD/YYYY.[/red]")
        return

    transaction_description = questionary.text(
        "Transaction description (optional):",
        validate=lambda value: (
            "Category name cannot be over 255 characters."
            if not (len(value.strip()) < 255)
            else True
        )
    ).ask()

    try:
        transaction = transaction_service.add_transaction(
            connection,
            account_id,
            category_id,
            transaction_amount,
            transaction_date,
            merchant_id,
            transaction_description
        )

        console.print(
            Panel(
                f"[bold green]Transaction saved successfully![/bold green]\n\n"
                f"Transaction ID: {transaction["transaction_id"]}\n"
                f"Account Name: {transaction["account_name"]}\n"
                f"Category Name: {transaction["category_name"]}\n"
                f"Merchant Name: {transaction.get('merchant_name') or 'N/A'}\n"
                f"Transaction Amount: ${transaction["transaction_amount"]:,.2f}\n"
                f"Transaction Date: {datetime.strftime(transaction["transaction_date"], "%B %d, %Y, %I:%M:%S %p")}\n"
                f"Transaction Description: {transaction.get('transaction_description') or 'N/A'}\n",
            border_style="green",
                padding=1
            )
        )

    except Exception as error:
        console.print(f"\n[bold red]Failed to save transaction:[/bold red] {error}")

    questionary.text("\nPress Enter to return to the transactions menu.", qmark="").ask()