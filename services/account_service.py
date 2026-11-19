from decimal import Decimal

def get_accounts(connection) -> list[dict]:
    """
    Retrieve all accounts.
    Returns a list of account records.

    Should return:
    account id
    account name
    account type
    account balance
    created at

    Order by:
    account id
    """

def get_account(connection, account_id: int) -> dict | None:
    """
    Retrieves a single account.

    Should return:
    account id
    account name
    account type
    account balance
    created at
    """

def add_account(connection, account_name: str, account_type: str, account_balance: Decimal = Decimal(0.00)) -> int | None:
    """
    Create a new account.
    Returns the new account ID, or 'None' if unsuccessful.

    Should return:
    account id
    """

def delete_account(connection, account_id: int) -> None:
    """
    Deletes the specified account.
    """

# Keeping temporarily in case needed later
def get_account_balance(connection, account_id: int) -> Decimal | None:
    """
    Retrieve an account's current balance.
    Returns a decimal, or None if the account does not exist.

    Should return:
    account balance
    """

def get_account_transactions(connection, account_id: int) -> list[dict]:
    """
    Retrieve all transactions belonging to a specific account.
    Returns a list of transaction records.

    Should return:
    transaction id
    transaction amount
    transaction description
    category name
    category type
    merchant name

    Order by:
    transaction id DESC
    """

def get_account_categories(connection, account_id: int) -> list[dict]:
    """
    Retrieve available categories used by an account.

    Should return:
    category id
    category name
    category type

    Order by:
    category type, category name
    """

def get_account_merchants(connection, account_id: int) -> list[dict]:
    """
    Retrieve all distinct merchants used by an account.

    Should return:
    merchant id
    merchant name

    Order by:
    merchant name
    """
