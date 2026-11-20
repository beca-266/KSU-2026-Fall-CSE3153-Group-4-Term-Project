import datetime
from decimal import Decimal, InvalidOperation

from services import services_utils


def add_transaction(connection, account_id: int, category_id: int, amount: Decimal, transaction_date: datetime.datetime = None, merchant_id: int = None, description: str = None) -> dict | None:
    """
    Create a new transaction and update the account balance.
    Returns the new transaction record, or None if unsuccessful.
    """

    cursor = connection.cursor()

    try:
    
        cursor.execute("""
        SELECT category_type
        FROM tracker.Categories
        WHERE category_id = ?;
        """, (category_id,))

        category = cursor.fetchone()

        if category is None:
            return None

        category_type = category[0]

        try:
            amount = Decimal(str(amount))
        except (InvalidOperation, TypeError, ValueError):
            raise ValueError("Please enter a valid transaction amount.")

        if amount <= 0:
            raise ValueError("Transaction amount must be greater than zero.")

        if transaction_date is None:
            transaction_date = datetime.datetime.now()

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
        VALUES (?, ?, ?, ?, ?, ?);
        """, (account_id, category_id, merchant_id, amount, transaction_date, description))

        transaction_id = cursor.fetchone()[0]

        if category_type == "Income":
            cursor.execute("""
            UPDATE tracker.Accounts
            SET account_balance = account_balance + ?
            WHERE account_id = ?;
            """, (amount, account_id))
        else:
            cursor.execute("""
            UPDATE tracker.Accounts
            SET account_balance = account_balance - ?
            WHERE account_id = ?;
            """, (amount, account_id))

        connection.commit()

        return services_utils.get_transaction(connection, transaction_id)

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()


def update_transaction(connection, transaction_id: int, account_id: int | None, category_id: int | None, updated_amount: Decimal | None, transaction_date: datetime.datetime | None, merchant_id: int | None, description: str | None) -> dict | None:
    """
    Update an existing transaction and adjust the account balance.
    Returns the updated transaction record, or None if it was not found.
    """

    old_transaction = services_utils.get_transaction(connection, transaction_id)

    if old_transaction is None:
        return None

    old_account_id = old_transaction["account_id"]
    old_category_id = old_transaction["category_id"]
    old_amount = Decimal(str(old_transaction["transaction_amount"]))

