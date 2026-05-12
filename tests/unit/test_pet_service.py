import pytest
from unittest.mock import MagicMock
from datetime import datetime

from vetlog_buddy.pets.model import Pet
from vetlog_buddy.pets.services import PetService


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def mock_vacc_service():
    return MagicMock()


@pytest.fixture
def pet_service(mock_repo, mock_vacc_service):
    return PetService(mock_repo, mock_vacc_service)


def test_process_vaccinations(pet_service, mock_repo, mock_vacc_service):
    # Setup
    # 1. pets with pending vaccinations (should be ignored)
    vaccinated_pet = (1, "Rex", datetime.now(), "DOG")
    mock_repo.get_pets_with_pending_vaccinations.return_value = [vaccinated_pet]

    # 2. all pets
    waiting_pet = (2, "Fido", datetime.now(), "DOG")
    mock_repo.get_all_pets_with_breed.return_value = [vaccinated_pet, waiting_pet]

    # Execute
    result = pet_service.process_vaccinations()

    # Verify
    assert len(result) == 1
    assert result[0] == waiting_pet

    # Verify vaccination service called for waiting pet ONLY
    mock_vacc_service.vaccinate_pet.assert_called_once_with(
        2, "Fido", waiting_pet[2], "DOG"
    )


def test_get_pet_by_id(mock_repo):
    """Get pet by id"""
    service = PetService(repository=mock_repo, vaccination_service=MagicMock())
    pet = Pet(id=1, name="Sora")
    mock_repo.find_by_id.return_value = pet
    assert service.get_by_id(1) == pet
    mock_repo.find_by_id.assert_called_once_with(1)
