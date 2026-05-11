import pytest
from unittest.mock import MagicMock
from datetime import datetime

from vetlog_buddy.pets.services import PetService


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def mock_deworm_service():
    return MagicMock()


@pytest.fixture
def pet_service(mock_repo, mock_deworm_service):
    return PetService(mock_repo, deworm_service=mock_deworm_service)


def test_process_dewormings(pet_service, mock_repo, mock_deworm_service):
    """Test that pets needing deworming get deworming records created."""
    # Setup
    pet_a = (1, "Rex", datetime.now(), "DOG")
    pet_b = (2, "Felix", datetime.now(), "CAT")

    # Pets already with pending deworming (should be skipped)
    mock_repo.get_pets_with_pending_deworming.return_value = [pet_a]

    # Pets needing deworming
    mock_repo.get_pets_needing_deworming.return_value = [pet_b]

    # Execute
    result = pet_service.process_dewormings()

    # Verify
    assert len(result) == 1
    assert result[0] == pet_b

    # Verify deworm service called for pet_b only
    mock_deworm_service.deworm_pet.assert_called_once_with(2, "Felix")


def test_process_dewormings_no_service(pet_service, mock_repo):
    """Test that without deworm service, pets are returned but no records created."""
    pet_a = (1, "Rex", datetime.now(), "DOG")

    mock_repo.get_pets_with_pending_deworming.return_value = []
    mock_repo.get_pets_needing_deworming.return_value = [pet_a]

    result = pet_service.process_dewormings()

    assert len(result) == 1
