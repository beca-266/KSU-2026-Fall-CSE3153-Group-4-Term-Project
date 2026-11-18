from calendar import month


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

    try:

        cursor.execute(
            """
        SELECT budget_id
        FROM tracker.Budgets
        WHERE account_id = ? AND category_id = ? 
            AND budget_month = ? 
            AND budget_year = ?
        """, 
        (account_id, category_id, month, year)
        )

        existing_budget = cursor.fetchone()

        if existing_budget is not None:
            cursor.execute(
                """
                UPDATE tracker.Budgets
                SET monthly_limit = ?
                WHERE budget_id = ?
                """,
                (monthly_limit, existing_budget[0])
            )

        else:
            cursor.execute(
                """
                INSERT INTO tracker.Budgets
                    (account_id, category_id, monthly_limit,
                    budget_month, budget_year)
                VALUES (?, ?, ?, ?, ?)
                """,
                (account_id, category_id, monthly_limit, month, year)
            )

        cursor.execute(
            """
            SELECT b.budget_id, 
                a.account_name, 
                c.category_name, 
                b.monthly_limit, 
                b.budget_month, 
                b.budget_year
            FROM tracker.Budgets b
            INNER JOIN tracker.Accounts a
                ON b.account_id = a.account_id
            INNER JOIN tracker.Categories c
                ON b.category_id = c.category_id
            WHERE b.account_id = ? 
                AND b.category_id = ? 
                AND b.budget_month = ? 
                AND b.budget_year = ?
            """,
            (account_id, category_id, month, year)
        )

        columns = [column[0] for column in cursor.description]
        row = cursor.fetchone()

        connection.commit()

        return dict(zip(columns, row)) if row is not None else None

    except Exception:
        connection.rollback()
        raise

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

    query =  """
        SELECT b.budget_id, 
            a.account_name, 
            c.category_name, 
            b.monthly_limit, 
            b.budget_month, 
            b.budget_year
        FROM tracker.Budgets b
        INNER JOIN tracker.Accounts a
            ON b.account_id = a.account_id
        INNER JOIN tracker.Categories c
            ON b.category_id = c.category_id
"""
    conditions = []
    parameters = []

    if account_id is not None:
        conditions.append("b.account_id = ?")
        parameters.append(account_id)

    if month is not None:
        conditions.append("b.budget_month = ?")
        parameters.append(month)

    if year is not None:
        conditions.append("b.budget_year = ?")
        parameters.append(year) 

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, tuple(parameters))

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()

    return [dict(zip(columns, row)) for row in rows]

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

    cursor.execute(
        """
        SELECT b.budget_id, 
            b.monthly_limit, 
            COALESCE(SUM(t.transaction_amount), 0) AS amount_spent,
            b.monthly_limit - COALESCE(SUM(t.transaction_amount), 0) 
                AS remaining
        FROM tracker.Budgets b
        LEFT JOIN tracker.Transactions t
            ON b.account_id = t.account_id 
            AND b.category_id = t.category_id 
            AND MONTH(t.transaction_date) = b.budget_month 
            AND YEAR(t.transaction_date) = b.budget_year
        WHERE b.budget_id = ?
        GROUP BY b.budget_id, b.monthly_limit
        """,
        (budget_id,)
    )

    columns = [column[0] for column in cursor.description]
    row = cursor.fetchone()

    return dict(zip(columns, row)) if row is not None else None

def fetch_months(connection) -> list[int]:
    """
    Fetches all valid months.

    Should return:
    DISTINCT budget month

    Order by:
    budget month asc
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT DISTINCT budget_month
        FROM tracker.Budgets 
        ORDER BY budget_month ASC
        """
    )

    return [row[0] for row in cursor.fetchall()]

def fetch_years(connection) -> list[int]:
    """
    Fetches all valid years.

    Should return:
    DISTINCT budget year

    Order by:
    budget year asc
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT DISTINCT budget_year
        FROM tracker.Budgets 
        ORDER BY budget_year ASC
        """
    )

    return [row[0] for row in cursor.fetchall()]