def get_categories(connection) -> list[dict]:
    """
    Retrieve all available categories.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT DISTINCT
            category_id,
            category_name,
            category_type
        FROM tracker.Categories
        ORDER BY category_type, category_name;
        """)

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        return [dict(zip(columns, row))for row in rows]

    finally:
        cursor.close()

def create_category(connection, category_name, category_type) -> int | None:
    """
    Creates a new category with the specified name and type, returning the id.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        INSERT INTO tracker.Categories (
            category_name,
            category_type
        )
        OUTPUT INSERTED.category_id
        VALUES (?, ?);
        """, (category_name, category_type))

        category_id = cursor.fetchone()[0]

        connection.commit()

        return category_id

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()

def create_merchant(connection, merchant_name) -> int | None:
    """
    Creates a new merchant with the specified name, returning the id.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        INSERT INTO tracker.Merchants (
            merchant_name
        )
        OUTPUT INSERTED.merchant_id
        VALUES (?);
        """, merchant_name)

        merchant_id = cursor.fetchone()[0]

        connection.commit()

        return merchant_id

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()

def get_merchants(connection) -> list[dict] | None:
    """
        Retrieve all merchants.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT DISTINCT 
            merchant_id,
            merchant_name
        FROM tracker.Merchants 
        ORDER BY merchant_id;
        """)

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]

    finally:
        cursor.close()

def fetch_months(connection) -> list[int]:
    """
    Fetches all valid months.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT DISTINCT budget_month
        FROM tracker.Budgets
        ORDER BY budget_month asc
        """)

        rows = cursor.fetchall()

        months = []
        for row in rows:
            months.append(row)

        return months

    except Exception as error:
        print(error)
        raise

    finally:
        cursor.close()

def fetch_years(connection) -> list[int]:
    """
    Fetches all valid months.
    """

    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT DISTINCT budget_year
        FROM tracker.Budgets
        ORDER BY budget_year asc
        """)

        rows = cursor.fetchall()

        years = []
        for row in rows:
            years.append(row)

        return years

    except Exception as error:
        print(error)
        raise

    finally:
        cursor.close()

def get_transaction(connection, transaction_id: int) -> dict | None:
    """
    Fetches a single transaction based on the transaction id.
    """
    cursor = connection.cursor()

    cursor.execute("""
        SELECT t.*,
            a.account_name,
            c.category_name,
            c.category_type,
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

    return dict(zip(columns, row))