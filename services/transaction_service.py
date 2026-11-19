import datetime
from decimal import Decimal, InvalidOperation

from services import services_utils

def add_transaction(connection, account_id: int, category_id: int, amount: Decimal, transaction_date: datetime.datetime = None, merchant_id: int = None, description: str = None) -> dict | None:
    """
    Create a new transaction.
    Update the associated account balance based on the category type.
    Returns the new transaction record, or None if unsuccessful.

    can use transaction = services_utils.get_transaction(connection, transaction_id) to return transaction
    """

def update_transaction(connection, transaction_id: int, account_id: int | None, category_id: int | None, updated_amount: Decimal | None, transaction_date: datetime.datetime | None, merchant_id: int | None, description: str | None) -> dict | None:
    """
    Update an existing transaction using its ID.
    Returns True if updated, otherwise False.

    This one may be tricky because the account balances will also have to be updated if a transaction's amount is updated.
    So if the transaction is changed to have costed more, subtract more from the balance, if the transaction is less now, add to the balance.
    """

def delete_transaction(connection, transaction_id: int) -> bool:
    """
    Delete a transaction using its ID.
    Reverses the transaction's effect on the account balance.
    Returns True if deleted, otherwise False.
    """
