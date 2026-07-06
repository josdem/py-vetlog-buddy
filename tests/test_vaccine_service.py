import unittest
from unittest.mock import MagicMock
from src.vetlog_buddy.vaccinations.services import VaccinationService

class TestVaccineService(unittest.TestCase):

    def test_get_rabies_vaccines_by_month_counts_correctly(self):
        # Create a mock repository and stub its function return value
        mock_repository = MagicMock()
        mock_repository.find_rabies_vaccines_by_month.return_value = [
            {'date': '2026-01-15'},
            {'date': '2026-01-22'},
            {'date': '2026-04-05'},
            {'date': '2026-12-25'}
        ]

        # Inject the mock repository into the service layer and run the test
        service = VaccinationService(vaccinationRepository=mock_repository)
        result = service.get_rabies_vaccines_by_month(2026)

        # Assert expectations match execution matrix
        self.assertEqual(result['01'], 2) # 2 in January
        self.assertEqual(result['04'], 1) # 1 in April
        self.assertEqual(result['12'], 1) # 1 in December
        self.assertEqual(result['02'], 0) # Unaffected months stay 0

if __name__ == '__main__':
    unittest.main()
