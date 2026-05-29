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

from sqlmodel import Session
from unittest.mock import MagicMock

from vetlog_buddy.pets.repository import PetRepository
from vetlog_buddy.pets.model import Pet


def test_get_pet_type():
    """Get pet type"""
    session = MagicMock(spec=Session)
    repo = PetRepository(session)
    pet = Pet(id=1, name="Sora")

    repo.find_pet_type.return_value = "DOG"

    assert repo.find_pet_type(pet.id) == "DOG"
    repo.find_pet_type.assert_called_once_with(pet.id)
