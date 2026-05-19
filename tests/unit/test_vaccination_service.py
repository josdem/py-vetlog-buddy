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
#  limitations under the License.

import pytest

from datetime import datetime
from unittest.mock import MagicMock

from vetlog_buddy.pets.model import Pet
from vetlog_buddy.vaccinations.model import Vaccination
from vetlog_buddy.vaccinations.services import VaccinationService


@pytest.fixture
def mock_repo():
    return MagicMock()


def test_get_pending_dewormings(mock_repo):
    """Get pending dewormings"""
    service = VaccinationService(repository=mock_repo)
    dewormings = [
        Vaccination(
            id=1,
            name="Deworming",
            date=datetime(2025, 4, 21),
            pet_id=2,
            status="APPLIED",
        )
    ]
    mock_repo.find_pending_dewormings.return_value = dewormings
    assert service.get_pending_dewormings(12) == dewormings
    mock_repo.find_pending_dewormings.assert_called_once_with(12)


def test_create_deworming(mock_repo):
    """Create a deworming record for a pet"""
    service = VaccinationService(repository=mock_repo)
    pet = Pet(
        id=2,
        name="Buddy",
        birth_date=datetime(2020, 1, 1),
        status="ACTIVE",
    )
    service.create_deworming(pet)
    mock_repo.delete_applied_dewormings.assert_called_once_with(pet.id)
    mock_repo.create.assert_called_once_with(pet.id, "Deworming")


def test_should_not_create_deworming_for_inactive_pet(mock_repo):
    """Do not create a deworming record for an inactive pet"""
    service = VaccinationService(repository=mock_repo)
    pet = Pet(
        id=3,
        name="Whiskers",
        birth_date=datetime(2019, 6, 1),
        status="INACTIVE",
    )
    service.create_deworming(pet)
    mock_repo.create.assert_not_called()


def test_should_not_create_deworming_for_deceased_pet(mock_repo):
    """Do not create a deworming record for a deceased pet"""
    service = VaccinationService(repository=mock_repo)
    pet = Pet(
        id=4,
        name="Shadow",
        birth_date=datetime(2018, 3, 15),
        status="DECEASED",
    )
    service.create_deworming(pet)
    mock_repo.create.assert_not_called()
