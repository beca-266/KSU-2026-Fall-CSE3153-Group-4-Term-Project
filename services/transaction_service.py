import datetime


def add_transaction(connection, account_id: int, category_id: int, amount: float, transaction_date: datetime.datetime = None, merchant_id: int = None, description: str = None) -> dict | None:
    """
    Create a new transaction.
    Returns the new transaction ID, or None if unsuccessful.

    I will add a way for the user to add a merchant in the middle of adding a transaction within the looping menu.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO tracker.Transactions (
                account_id,
                category_id,
                merchant_id,
                transaction_amount,
                transaction_date,
                transaction_description
            )
            OUTPUT INSERTED.transaction_id
            VALUES (?, ?, ?, ?, ?, ?)
        """, (account_id, category_id, merchant_id, amount, transaction_date, description))

        transaction_id = cursor.fetchone()[0]

        cursor.execute("""
            SELECT t.*,
                a.account_name,
                c.category_name,
                m.merchant_name
            FROM tracker.Transactions t
                JOIN tracker.Accounts a
                    ON t.account_id = a.account_id
                JOIN tracker.Categories c
                    ON t.category_id = c.category_id
                LEFT JOIN tracker.Merchants m
                    ON t.merchant_id = m.merchant_id
            WHERE t.transaction_id = ?
        """, (transaction_id,))

        row = cursor.fetchone()

        if row is None:
            connection.rollback()
            return None

        columns = [column[0] for column in cursor.description]

        transaction = dict(zip(columns, row))

        connection.commit()

        return transaction

    except Exception as error:
        connection.rollback()
        raise error

    finally:
        cursor.close()

def update_transaction(connection, transaction_id: int, account_id: int, category_id: int, amount: float, transaction_date, merchant_id: int = None, description: str = None) -> bool:
    cursor = connection.cursor()

    """
    Update an existing transaction using its ID.
    Returns True if updated, otherwise False.

    This one may be tricky because the account balances will also have to be updated if a transaction's amount is updated.
    So if the transaction is changed to have costed more, subtract more from the balance, if the transaction is less now, add to the balance.
    """
    pass

def delete_transaction(connection, transaction_id: int) -> bool:
    cursor = connection.cursor()

    """
    Delete a transaction using its ID.
    Returns True if deleted, otherwise False.

    Same as above, should reverse the initial effect on the account's balance.
    """
    pass