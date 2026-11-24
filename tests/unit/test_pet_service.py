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
