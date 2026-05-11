from vetlog_buddy.main import dewormings
from unittest.mock import MagicMock, patch


def test_pending_dewormings():
    """Test pending dewormings"""
    mock_session_cm = MagicMock()

    with (
        patch("vetlog_calendar.main.get_session", return_value=mock_session_cm),
        patch("vetlog_calendar.main.VaccinationService") as MockVaccService,
        patch("vetlog_calendar.main.PetService") as MockPetService,
    ):
        mock_session = MagicMock()
        mock_session_cm.__enter__.return_value = mock_session

        mock_vacc_service = MockVaccService.return_value
        mock_pet_service = MockPetService.return_value

        # Setup the vaccination service to return pending dewormings
        mock_vacc_service.get_pending_dewormings.return_value = [
            MagicMock(pet_id=1),
            MagicMock(pet_id=2),
        ]

        # Setup the pet service to return pet details
        mock_pet_service.get_pet_by_id.side_effect = lambda pet_id: MagicMock(
            name=f"Pet{pet_id}", id=pet_id
        )

        dewormings()

        # Assertions to ensure the correct calls were made
        mock_vacc_service.get_pending_dewormings.assert_called_once()
        assert mock_pet_service.get_pet_by_id.call_count == 2
