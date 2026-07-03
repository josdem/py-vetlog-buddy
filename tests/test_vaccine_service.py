import unittest
from unittest.mock import MagicMock
from vetlog_buddy.vaccine_service import get_rabies_vaccines_by_month

class TestVaccineService(unittest.TestCase):

    def test_get_rabies_vaccines_by_month_counts_correctly(self):
        # Create a mock database session
        mock_session = MagicMock()
        
        # Simulate rows matching the repository data schema
        mock_session.execute.return_value.fetchall.return_value = [
            {'date': '2026-01-15'},
            {'date': '2026-01-22'},
            {'date': '2026-04-05'},
            {'date': '2026-12-25'}
        ]
        
        result = get_rabies_vaccines_by_month(mock_session, 2026)
        
        # Assert expectations match execution matrix
        self.assertEqual(result['01'], 2)  # 2 in January
        self.assertEqual(result['04'], 1)  # 1 in April
        self.assertEqual(result['12'], 1)  # 1 in December
        self.assertEqual(result['02'], 0)  # Unaffected months stay 0

if __name__ == '__main__':
    unittest.main()
