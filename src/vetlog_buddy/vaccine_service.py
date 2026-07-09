def get_rabies_vaccines_by_month(db_session, year: int) -> dict:
    """
    Returns a dictionary with months as keys and the count of applied Rabies vaccines as values.
    """
    # Initialize all 12 months with 0 counts to ensure a complete dataset
    monthly_counts = {f"{i:02d}": 0 for i in range(1, 13)}

    # Target query pattern requested by the acceptance criteria
    query_string = f"SELECT date FROM vaccination WHERE status='APPLIED' AND name='Rabies' AND date LIKE '{year}-%'"

    # Execute database lookup payload
    results = db_session.execute(query_string).fetchall()

    for row in results:
        # Assuming date string format is 'YYYY-MM-DD'
        date_str = row["date"]
        month = date_str.split("-")[1]
        if month in monthly_counts:
            monthly_counts[month] += 1

    return monthly_counts
