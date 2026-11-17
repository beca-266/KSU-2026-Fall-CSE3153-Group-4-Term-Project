from decimal import Decimal

def _rows_to_dicts(cursor) -> list[dict]:
     """
    Helper: turns the rows from the last query into a list of dictionaries,
    using the column names as keys. Example: {"account_id": 1, "account_name": "John_Checking", ...}
    """
     columns = [column[0] for column in cursor.description]
     return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_accounts(connection) -> list[dict]:
    cursor = connection.cursor()

    """
    Retrieve all accounts.
    Returns a list of account records.
    """
    cursor.execute("""
        SELECT account_id, account_name, account_type, account_balance, created_at
        FROM tracker.Accounts
        ORDER BY account_id
    """)
    return _rows_to_dicts(cursor)

def add_account(connection, account_name: str, account_type: str, starting_balance: float = 0.00) -> int | None:
    cursor = connection.cursor()

    """
    Create a new account.
    Returns the new account ID, or 'None' if unsuccessful.
    """

    try:
            # OUTPUT INSERTED.account_id hands back the ID SQL Server just created
            cursor.execute("""
                INSERT INTO tracker.Accounts (account_name, account_type, account_balance)
                OUTPUT INSERTED.account_id
                VALUES (?, ?, ?)
            """, (account_name, account_type, starting_balance))
            new_id = cursor.fetchone()[0]
            connection.commit()
            return new_id
    
    except Exception:
            # Fails if the name already exists (UNIQUE) or the type isn't Checking/Savings/Cash (CHECK)
            connection.rollback()
            return None
    
def get_account_balance(connection, account_id: int) -> Decimal | None:
    cursor = connection.cursor()

    """
    Retrieve an account's current balance.
    Returns the balance, or None if the account does not exist.
    """
    cursor.execute("""
        SELECT account_balance
        FROM tracker.Accounts
        WHERE account_id = ?
    """, (account_id,))
    row = cursor.fetchone()
    return row[0] if row else None

def get_account_transactions(connection, account_id: int) -> list[dict]:
    cursor = connection.cursor()

    """
    Retrieve all transactions belonging to a specific account.
    Returns a list of transaction records.
    """
    # JOIN pulls in the category name/type; LEFT JOIN on Merchants because merchant_id can be NULL
    cursor.execute("""
        SELECT
            t.transaction_id,
            t.transaction_date,
            c.category_name,
            c.category_type,
            m.merchant_name,
            t.transaction_amount,
            t.transaction_description
        FROM tracker.Transactions AS t
        INNER JOIN tracker.Categories AS c ON t.category_id = c.category_id
        LEFT JOIN tracker.Merchants AS m ON t.merchant_id = m.merchant_id
        WHERE t.account_id = ?
        ORDER BY t.transaction_date DESC
    """, (account_id,))
    return _rows_to_dicts(cursor)


def get_categories(connection, category_type: str = None) -> list[dict]:
    cursor = connection.cursor()

    """
    Retrieve available categories.
    Optionally filter by 'Income' or 'Expense' (not necessarily required, but should not be hard to implement)
    Returns a list of category records.
    """
    if category_type:
        cursor.execute("""
            SELECT category_id, category_name, category_type
            FROM tracker.Categories
            WHERE category_type = ?
            ORDER BY category_name
        """, (category_type,))
    else:
        cursor.execute("""
            SELECT category_id, category_name, category_type
            FROM tracker.Categories
            ORDER BY category_type, category_name
        """)
    return _rows_to_dicts(cursor)

def get_merchants(connection) -> list[dict]:
    cursor = connection.cursor()

    """
    Retrieve all available merchants.
    Returns a list of merchant records.
    """
    cursor.execute("""
        SELECT merchant_id, merchant_name
        FROM tracker.Merchants
        ORDER BY merchant_name
    """)
    return _rows_to_dicts(cursor)
     
