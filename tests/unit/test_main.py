from unittest.mock import MagicMock, patch
from datetime import datetime

from vetlog_buddy import main
from vetlog_buddy.users.model import User
from vetlog_buddy.pets.model import Pet
from vetlog_buddy.vaccinations.model import Vaccination


def deworming():
    return Vaccination(
        pet_id=1,
        name="Deworming",
        date=datetime(2024, 5, 21),
    )


def owner():
    return User(
        id=1,
        username="josdem",
        first_name="Jose",
        last_name="Morales",
        email="contact@josdem.io",
        mobile="1234567890",
        role="USER",
    )


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
        patch("vetlog_buddy.main.VaccinationRepository") as MockVaccinationRepository,
        patch("vetlog_buddy.main.VaccinationService") as MockVaccinationService,
    ):
        mock_session = MagicMock()
        mock_session_cm.__enter__.return_value = mock_session

        main.vaccines(id=1)

        MockPetRepository.assert_called_once_with(mock_session)
        MockVaccinationRepository.assert_called_once_with(mock_session)
        MockVaccinationService.assert_called_once_with(
            MockVaccinationRepository.return_value, MockPetRepository.return_value
        )
        MockPetRepository.return_value.find_by_id.assert_called_once_with(1)
        MockVaccinationService.return_value.create_vaccination.assert_called_once_with(
            MockPetRepository.return_value.find_by_id.return_value
        )


def test_vaccination_cli():
    """Test vaccinations CLI command wiring"""
    mock_session_cm = MagicMock()

    with (
        patch("sys.argv", ["app.py", "--id", "1"]),
        patch("vetlog_buddy.main.get_session", return_value=mock_session_cm),
        patch("vetlog_buddy.main.PetRepository") as MockPetRepository,
        patch("vetlog_buddy.main.VaccinationRepository") as MockVaccinationRepository,
        patch("vetlog_buddy.main.VaccinationService") as MockVaccinationService,
    ):
        mock_session = MagicMock()
        mock_session_cm.__enter__.return_value = mock_session

        main.vaccinations_cli()

        MockPetRepository.assert_called_once_with(mock_session)
        MockVaccinationRepository.assert_called_once_with(mock_session)
        MockVaccinationService.assert_called_once_with(
            MockVaccinationRepository.return_value, MockPetRepository.return_value
        )
        MockPetRepository.return_value.find_by_id.assert_called_once_with(1)
        MockVaccinationService.return_value.create_vaccination.assert_called_once_with(
            MockPetRepository.return_value.find_by_id.return_value
        )


def test_generate_stats():
    """Test generate_stats command wiring"""
    mock_session_cm = MagicMock()

    with (
        patch("vetlog_buddy.main.get_session", return_value=mock_session_cm),
        patch("vetlog_buddy.main.VaccinationRepository") as MockVaccinationRepository,
        patch("vetlog_buddy.main.VaccinationService") as MockVaccinationService,
    ):
        mock_session = MagicMock()
        mock_session_cm.__enter__.return_value = mock_session
        MockVaccinationService.return_value.get_rabies_vaccines_by_month.return_value = {
            "01": 2,
            "02": 0,
        }

        main.generate_stats(year=2026)

        MockVaccinationRepository.assert_called_once_with(mock_session)
        MockVaccinationService.assert_called_once_with(
            MockVaccinationRepository.return_value
        )
        MockVaccinationService.return_value.get_rabies_vaccines_by_month.assert_called_once_with(
            2026
        )


def test_stats_cli():
    """Test stats CLI command wiring"""
    mock_session_cm = MagicMock()

    with (
        patch("sys.argv", ["app.py", "--year", "2026"]),
        patch("vetlog_buddy.main.get_session", return_value=mock_session_cm),
        patch("vetlog_buddy.main.VaccinationRepository") as MockVaccinationRepository,
        patch("vetlog_buddy.main.VaccinationService") as MockVaccinationService,
    ):
        mock_session = MagicMock()
        mock_session_cm.__enter__.return_value = mock_session
        MockVaccinationService.return_value.get_rabies_vaccines_by_month.return_value = {
            "01": 2,
            "02": 0,
        }

        main.stats_cli()

        MockVaccinationRepository.assert_called_once_with(mock_session)
        MockVaccinationService.assert_called_once_with(
            MockVaccinationRepository.return_value
        )
        MockVaccinationService.return_value.get_rabies_vaccines_by_month.assert_called_once_with(
            2026
        )


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
        mock_pet_service.get_by_id.side_effect = lambda pet_id: MagicMock(
            name=f"Pet{pet_id}", id=pet_id
        )

        main.dewormings()

        # Assertions to ensure the correct calls were made
        assert mock_pet_service.get_by_id.call_count == 2
        assert mock_vacc_service.create_deworming.call_count == 2


def test_pending_dewormings_with_excluded_status():
    """Test pending dewormings with pets having excluded statuses"""
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

        # Setup the pet service to return pet details with one having an excluded status
        def get_by_id_side_effect(pet_id):
            if pet_id == 1:
                return MagicMock(name="Pet1", id=1, status="INACTIVE")
            else:
                return MagicMock(name="Pet2", id=2, status="ACTIVE")

        mock_pet_service.get_by_id.side_effect = get_by_id_side_effect

        main.dewormings()

        # Assertions to ensure the correct calls were made
        assert mock_pet_service.get_by_id.call_count == 2
        # Only one deworming should be created for the active pet
        assert mock_vacc_service.create_deworming.call_count == 1


def test_list_dewormings_no_duplicate_events_when_pet_in_both_lists():
    """No duplicate calendar event when a pet appears in both the 12-month and 6-month required lists"""

    outdoor_pet = Pet(
        id=1,
        user_id=1,
        adopter_id=None,
        name="Sora",
        birth_date=datetime(2020, 1, 1, 0, 0, 0),
        breed_id=1,
        going_out_often=True,
    )

    mock_session_cm = MagicMock()

    with (
        patch("vetlog_buddy.main.get_session", return_value=mock_session_cm),
        patch("vetlog_buddy.main.PetRepository.find_by_id", return_value=outdoor_pet),
        patch("vetlog_buddy.main.UserRepository.find_by_id", return_value=owner()),
        patch("vetlog_buddy.main.VaccinationService") as MockVaccinationService,
        patch("vetlog_buddy.main.PetService") as MockPetService,
    ):
        mock_vaccination_service = MockVaccinationService.return_value
        mock_pet_service = MockPetService.return_value

        # Same pet appears in both the 12-month and 6-month results
        mock_vaccination_service.get_pending_dewormings.side_effect = lambda months: (
            [deworming()] if months in (12, 6) else []
        )

        main.dewormings()

        mock_pet_service.create_deworming.call_once_with(outdoor_pet)


def test_version_check(capsys):
    """Test version check output"""
    main.version_check()

    captured = capsys.readouterr()

    assert captured.out == f"{main.__project__} version {main.__version__}\n"
