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
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT
            account_id,
            account_name,
            account_type,
            account_balance,
            created_at
        FROM tracker.Accounts
        ORDER BY account_id;
        """)

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]

    finally:
        cursor.close()

def add_account(connection, account_name: str, account_type: str, account_balance: float = 0.00) -> int | None:
    """
    Create a new account.
    Returns the new account ID, or 'None' if unsuccessful.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO tracker.Accounts (
                account_name, 
                account_type, 
                account_balance
            )
            OUTPUT INSERTED.account_id
            VALUES (?, ?, ?);
        """, (account_name, account_type, account_balance))

        account_id = cursor.fetchone()[0]

        connection.commit()

        return account_id

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()

# Keeping temporarily in case needed later
def get_account_balance(connection, account_id: int) -> Decimal | None:
    """
    Retrieve an account's current balance.
    Returns a decimal, or None if the account does not exist.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT account_balance
        FROM tracker.Accounts
        WHERE account_id = ?;
        """, (account_id,))

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        return rows[0][0]

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()

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
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                t.transaction_id,
                t.transaction_amount,
                t.transaction_date,
                t.transaction_description,
                c.category_name,
                c.category_type,
                m.merchant_name
            FROM tracker.Transactions AS t
            INNER JOIN tracker.Categories AS c
                ON t.category_id = c.category_id
            LEFT JOIN tracker.Merchants AS m
                ON t.merchant_id = m.merchant_id
            WHERE t.account_id = ?
            ORDER BY t.transaction_date DESC;
        """, (account_id,))

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]

    finally:
        cursor.close()

def get_categories(connection, category_type: str = None) -> list[dict]:
    """
    Retrieve available categories.
    Optionally filter by 'Income' or 'Expense' (not necessarily required, but should not be hard to implement)
    Returns a list of category records.
    """
    pass

    cursor = connection.cursor()

def get_merchants(connection) -> list[dict]:
    """
    Retrieve all available merchants.
    Returns a list of merchant records.
    """
    pass

    cursor = connection.cursor()