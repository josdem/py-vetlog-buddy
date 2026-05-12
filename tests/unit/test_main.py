from unittest.mock import MagicMock, patch

from vetlog_buddy import main


def test_remove_invalid_users():
    """Test remove invalid users command wiring"""
    mock_session_cm = MagicMock()

    with (
        patch("vetlog_buddy.main.get_session", return_value=mock_session_cm),
        patch("vetlog_buddy.main.UserRepository") as MockUserRepository,
        patch("vetlog_buddy.main.UserService") as MockUserService,
    ):
        mock_session = MagicMock()
        mock_session_cm.__enter__.return_value = mock_session

        main.remove_invalid_users()

        MockUserRepository.assert_called_once_with(mock_session)
        MockUserService.assert_called_once_with(MockUserRepository.return_value)
        MockUserService.return_value.remove_invalid.assert_called_once_with()


def test_list_suspicious_users():
    """Test list suspicious users command wiring"""
    mock_session_cm = MagicMock()

    with (
        patch("vetlog_buddy.main.get_session", return_value=mock_session_cm),
        patch("vetlog_buddy.main.UserRepository") as MockUserRepository,
        patch("vetlog_buddy.main.UserService") as MockUserService,
    ):
        mock_session = MagicMock()
        mock_session_cm.__enter__.return_value = mock_session

        main.list_suspicious_users()

        MockUserRepository.assert_called_once_with(mock_session)
        MockUserService.assert_called_once_with(MockUserRepository.return_value)
        MockUserService.return_value.list_suspicious.assert_called_once_with()


def test_vaccines():
    """Test vaccines command wiring"""
    mock_session_cm = MagicMock()

    with (
        patch("vetlog_buddy.main.get_session", return_value=mock_session_cm),
        patch("vetlog_buddy.main.PetRepository") as MockPetRepository,
        patch("vetlog_buddy.main.VaccinationRepository") as MockVaccRepository,
        patch("vetlog_buddy.main.VaccinationService") as MockVaccService,
        patch("vetlog_buddy.main.PetService") as MockPetService,
    ):
        mock_session = MagicMock()
        mock_session_cm.__enter__.return_value = mock_session

        main.vaccines()

        MockPetRepository.assert_called_once_with(mock_session)
        MockVaccRepository.assert_called_once_with(mock_session)
        MockVaccService.assert_called_once_with(MockVaccRepository.return_value)
        MockPetService.assert_called_once_with(
            MockPetRepository.return_value, MockVaccService.return_value
        )
        MockPetService.return_value.process_vaccinations.assert_called_once_with()


def test_pending_dewormings():
    """Test pending dewormings"""
    mock_session_cm = MagicMock()

    with (
        patch("vetlog_buddy.main.get_session", return_value=mock_session_cm),
        patch("vetlog_buddy.main.VaccinationService") as MockVaccService,
        patch("vetlog_buddy.main.PetService") as MockPetService,
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

        main.dewormings()

        # Assertions to ensure the correct calls were made
        mock_vacc_service.get_pending_dewormings.assert_called_once()
        assert mock_pet_service.get_pet_by_id.call_count == 2


def test_version_check(capsys):
    """Test version check output"""
    main.version_check()

    captured = capsys.readouterr()

    assert captured.out == f"{main.__project__} version {main.__version__}\n"
