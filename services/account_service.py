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

    cursor = connection.cursor()

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

    cursor = connection.cursor()

def add_account(connection, account_name: str, account_type: str, account_balance: float = 0.00) -> int | None:
    """
    Create a new account.
    Returns the new account ID, or 'None' if unsuccessful.
    """

    cursor = connection.cursor()

def delete_account(connection, account_id: int) -> None:
    """
    Deletes the specified account.
    """

    cursor = connection.cursor()

# Keeping temporarily in case needed later
def get_account_balance(connection, account_id: int) -> Decimal | None:
    """
    Retrieve an account's current balance.
    Returns a decimal, or None if the account does not exist.
    """

    cursor = connection.cursor()

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
    transaction date DESC
    """

    cursor = connection.cursor()

def get_account_categories(connection, account_id: int) -> list[dict]:
    """
    Retrieve available categories used by an account.

    Should return:
    category id
    category name
    category type

    Order by:
    category type
    category name
    """

    cursor = connection.cursor()

def get_categories(connection) -> list[dict]:
    """
    Retrieve all available categories.

    Should return:
    DISTINCT
    category id
    category name
    category type

    Order by:
    category_type, category_name
    """

    cursor = connection.cursor()

def create_category(connection, category_name, category_type) -> int | None:
    """
    Creates a new category with the specified name and type, returning the id.
    """

    cursor = connection.cursor()

def get_account_merchants(connection, account_id: int) -> list[dict]:
    """
    Retrieve all distinct merchants used by an account.
    """

    cursor = connection.cursor()