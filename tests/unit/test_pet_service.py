import pytest
from unittest.mock import MagicMock

from vetlog_buddy.pets.model import Pet
from vetlog_buddy.pets.services import PetService


@pytest.fixture
def mock_repo():
    return MagicMock()


def test_get_pet_by_id(mock_repo):
    """Get pet by id"""
    service = PetService(repository=mock_repo, vaccination_service=MagicMock())
    pet = Pet(id=1, name="Sora")
    mock_repo.find_by_id.return_value = pet
    assert service.get_by_id(1) == pet
    mock_repo.find_by_id.assert_called_once_with(1)
