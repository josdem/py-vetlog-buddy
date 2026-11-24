#  Copyright 2026 Jose Morales contact@josdem.io
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License


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
