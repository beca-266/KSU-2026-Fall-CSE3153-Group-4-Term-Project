def set_budget(connection, account_id: int, category_id: int, monthly_limit: float, month: int, year: int) -> dict | None:
    """
    Creates or updates a budget for an account and category
    for a specific month and year.
    Returns the budget object

    Should return:
    budget*
    account name
    category name
    """

    cursor = connection.cursor()

def get_budgets(connection, account_id: int = None, month: int = None, year: int = None) -> list[dict]:
    """
    Retrieve budgets.
    Optionally filter by account, month, and year.
    Returns a list of budget records.

    Should return:
    budget id
    account name
    category name
    monthly limit
    budget month
    budget year
    """

    cursor = connection.cursor()

def get_budget_remaining(connection, budget_id) -> dict | None:
    """
    Calculate a category's budget limit, amount spent,
    and remaining amount for a specific month.
    Returns a dictionary, or None if no budget exists.

    Basically tally all transactions for this month for this category for a net amount.

    Should return:
    budget id
    monthly limit
    COALESCED amount spent
    COALESCED remaining

    Group by:
    budget id, monthly limit
    """

    cursor = connection.cursor()

def fetch_months(connection) -> list[int]:
    """
    Fetches all valid months.

    Should return:
    DISTINCT budget month

    Order by:
    budget month asc
    """

    cursor = connection.cursor()

def fetch_years(connection) -> list[int]:
    """
    Fetches all valid years.

    Should return:
    DISTINCT budget year

    Order by:
    budget year asc
    """

    cursor = connection.cursor()