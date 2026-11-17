from decimal import Decimal


def _rows_to_dicts(cursor) -> list[dict]:
    """
    Helper: turns the rows from the last query into a list of dictionaries,
    using the column names as keys, e.g. {"account_id": 1, "account_name": "John_Checking", ...}
    """
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


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

    cursor.execute("""
        SELECT account_id, account_name, account_type, account_balance, created_at
        FROM tracker.Accounts
        ORDER BY account_id
    """)

    return _rows_to_dicts(cursor)


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

    cursor.execute("""
        SELECT account_id, account_name, account_type, account_balance, created_at
        FROM tracker.Accounts
        WHERE account_id = ?
    """, (account_id,))

    rows = _rows_to_dicts(cursor)
    return rows[0] if rows else None


def add_account(connection, account_name: str, account_type: str, account_balance: float = 0.00) -> int | None:
    """
    Create a new account.
    Returns the new account ID, or 'None' if unsuccessful.
    """

    cursor = connection.cursor()

    try:
        # OUTPUT INSERTED.account_id hands back the ID SQL Server just created
        cursor.execute("""
            INSERT INTO tracker.Accounts (account_name, account_type, account_balance)
            OUTPUT INSERTED.account_id
            VALUES (?, ?, ?)
        """, (account_name, account_type, account_balance))

        row = cursor.fetchone()
        connection.commit()
        return row[0] if row else None

    except Exception:
        # Undo the failed insert, then pass the error up so the menu can show it
        # (e.g. duplicate account name)
        connection.rollback()
        raise


def delete_account(connection, account_id: int) -> None:
    """
    Deletes the specified account.
    """

    cursor = connection.cursor()

    try:
        # Budgets and Transactions point to this account with foreign keys,
        # so their rows have to be removed first or SQL Server blocks the delete
        cursor.execute("DELETE FROM tracker.Budgets WHERE account_id = ?", (account_id,))
        cursor.execute("DELETE FROM tracker.Transactions WHERE account_id = ?", (account_id,))
        cursor.execute("DELETE FROM tracker.Accounts WHERE account_id = ?", (account_id,))

        connection.commit()

    except Exception:
        # If any of the three deletes fail, undo all of them
        connection.rollback()
        raise


# Keeping temporarily in case needed later
def get_account_balance(connection, account_id: int) -> Decimal | None:
    """
    Retrieve an account's current balance.
    Returns a decimal, or None if the account does not exist.
    """

    cursor = connection.cursor()

    cursor.execute("""
        SELECT account_balance
        FROM tracker.Accounts
        WHERE account_id = ?
    """, (account_id,))

    row = cursor.fetchone()
    return row[0] if row else None


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

    # transaction_date is included too because the menu shows it in the Date column.
    # LEFT JOIN on Merchants because merchant_id can be NULL (e.g. paychecks).
    cursor.execute("""
        SELECT
            t.transaction_id,
            t.transaction_date,
            t.transaction_amount,
            t.transaction_description,
            c.category_name,
            c.category_type,
            m.merchant_name
        FROM tracker.Transactions AS t
        INNER JOIN tracker.Categories AS c ON t.category_id = c.category_id
        LEFT JOIN tracker.Merchants AS m ON t.merchant_id = m.merchant_id
        WHERE t.account_id = ?
        ORDER BY t.transaction_date DESC
    """, (account_id,))

    return _rows_to_dicts(cursor)


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

    # DISTINCT so each category shows once, even if the account used it many times
    cursor.execute("""
        SELECT DISTINCT c.category_id, c.category_name, c.category_type
        FROM tracker.Categories AS c
        INNER JOIN tracker.Transactions AS t ON t.category_id = c.category_id
        WHERE t.account_id = ?
        ORDER BY c.category_type, c.category_name
    """, (account_id,))

    return _rows_to_dicts(cursor)


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

    cursor.execute("""
        SELECT DISTINCT category_id, category_name, category_type
        FROM tracker.Categories
        ORDER BY category_type, category_name
    """)

    return _rows_to_dicts(cursor)


def create_category(connection, category_name, category_type) -> int | None:
    """
    Creates a new category with the specified name and type, returning the id.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO tracker.Categories (category_name, category_type)
            OUTPUT INSERTED.category_id
            VALUES (?, ?)
        """, (category_name, category_type))

        row = cursor.fetchone()
        connection.commit()
        return row[0] if row else None

    except Exception:
        # Undo the failed insert, then pass the error up so the menu can show it
        # (e.g. a category with that name already exists)
        connection.rollback()
        raise


def get_account_merchants(connection, account_id: int) -> list[dict]:
    """
    Retrieve all distinct merchants used by an account.
    """

    cursor = connection.cursor()

    cursor.execute("""
        SELECT DISTINCT m.merchant_id, m.merchant_name
        FROM tracker.Merchants AS m
        INNER JOIN tracker.Transactions AS t ON t.merchant_id = m.merchant_id
        WHERE t.account_id = ?
        ORDER BY m.merchant_name
    """, (account_id,))

    return _rows_to_dicts(cursor)
