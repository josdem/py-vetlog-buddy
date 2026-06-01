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

from datetime import datetime, timedelta
from unittest.mock import MagicMock

from vetlog_buddy.pets.model import Pet
from vetlog_buddy.vaccinations.model import Vaccination, VaccineStatus
from vetlog_buddy.vaccinations.services import VaccinationService


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def mock_pet_repo():
    return MagicMock()


@pytest.fixture
def service(mock_repo, mock_pet_repo):
    return VaccinationService(repository=mock_repo, pet_repository=mock_pet_repo)


def test_get_pending_dewormings(service, mock_repo):
    """Get pending dewormings"""
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


def test_create_deworming(service, mock_repo):
    """Create a deworming record for a pet"""
    pet = Pet(
        id=2,
        name="Buddy",
        birth_date=datetime(2020, 1, 1),
        status="ACTIVE",
    )
    service.create_deworming(pet)
    mock_repo.delete_applied_dewormings.assert_called_once_with(pet.id)
    mock_repo.create.assert_called_once_with(pet.id, "Deworming", VaccineStatus.NEW)


def test_should_not_create_deworming_for_inactive_pet(service, mock_repo):
    """Do not create a deworming record for an inactive pet"""
    pet = Pet(
        id=3,
        name="Whiskers",
        birth_date=datetime(2019, 6, 1),
        status="INACTIVE",
    )
    service.create_deworming(pet)
    mock_repo.create.assert_not_called()


def test_should_not_create_deworming_for_deceased_pet(service, mock_repo):
    """Do not create a deworming record for a deceased pet"""
    pet = Pet(
        id=4,
        name="Shadow",
        birth_date=datetime(2018, 3, 15),
        status="DECEASED",
    )
    service.create_deworming(pet)
    mock_repo.create.assert_not_called()


def test_create_vaccination_for_dog(service, mock_repo, mock_pet_repo):
    """Create vaccination records for a dog"""
    mock_pet_repo.find_pet_type.return_value = "DOG"
    mock_repo.find_pending_vaccination.return_value = None
    pet = Pet(
        id=5,
        name="Rex",
        birth_date=datetime.now() - timedelta(weeks=8),
        status="ACTIVE",
    )

    service.create_vaccination(pet)

    mock_pet_repo.find_pet_type.assert_called_once_with(pet.id)
    mock_repo.create.assert_any_call(pet.id, "PUPPY", VaccineStatus.PENDING)
    mock_repo.create.assert_any_call(pet.id, "Deworming", VaccineStatus.PENDING)


def test_should_not_create_vaccination_for_inactive_pet(service, mock_repo, mock_pet_repo):
    """Do not create vaccination records for an inactive pet"""
    mock_pet_repo.find_pet_type.return_value = "DOG"
    pet = Pet(
        id=10,
        name="Rex",
        birth_date=datetime.now() - timedelta(weeks=8),
        status="INACTIVE",
    )

    service.create_vaccination(pet)

    mock_pet_repo.find_pet_type.assert_called_once_with(pet.id)
    mock_repo.find_pending_vaccination.assert_not_called()
    mock_repo.create.assert_not_called()


def test_should_not_create_vaccination_for_deceased_pet(service, mock_repo, mock_pet_repo):
    """Do not create vaccination records for a deceased pet"""
    mock_pet_repo.find_pet_type.return_value = "DOG"
    pet = Pet(
        id=11,
        name="Shadow",
        birth_date=datetime.now() - timedelta(weeks=8),
        status="DECEASED",
    )

    service.create_vaccination(pet)

    mock_pet_repo.find_pet_type.assert_called_once_with(pet.id)
    mock_repo.find_pending_vaccination.assert_not_called()
    mock_repo.create.assert_not_called()
def test_create_vaccination_for_cat(service, mock_repo, mock_pet_repo):
    """Create vaccination records for a cat"""
    mock_pet_repo.find_pet_type.return_value = "CAT"
    mock_repo.find_pending_vaccination.return_value = None
    pet = Pet(
        id=6,
        name="Mittens",
        birth_date=datetime.now() - timedelta(weeks=10),
        status="OWNED",
    )

    service.create_vaccination(pet)

    mock_pet_repo.find_pet_type.assert_called_once_with(pet.id)
    mock_repo.create.assert_any_call(pet.id, "TRICAT", VaccineStatus.PENDING)
    mock_repo.create.assert_any_call(pet.id, "Deworming", VaccineStatus.PENDING)


def test_create_vaccination_for_young_cat(service, mock_repo, mock_pet_repo):
    pet = Pet(
        id=1,
        name="Whiskers",
        birth_date=datetime.now() - timedelta(weeks=6),
        status="OWNED",
    )
    mock_pet_repo.find_pet_type.return_value = "CAT"
    mock_repo.find_pending_vaccination.return_value = None

    service.create_vaccination(pet)

    mock_repo.find_pending_vaccination.assert_called_once_with(pet.id, "Deworming")
    mock_repo.create.assert_called_once_with(pet.id, "Deworming", VaccineStatus.PENDING)


def test_create_vaccination_for_young_dog(service, mock_repo, mock_pet_repo):
    pet = Pet(
        id=7,
        name="Buddy",
        birth_date=datetime.now() - timedelta(weeks=5),
        status="OWNED",
    )
    mock_pet_repo.find_pet_type.return_value = "DOG"
    mock_repo.find_pending_vaccination.return_value = None

    service.create_vaccination(pet)

    mock_repo.find_pending_vaccination.assert_called_once_with(pet.id, "Deworming")
    mock_repo.create.assert_called_once_with(pet.id, "Deworming", VaccineStatus.PENDING)


def test_create_vaccination_for_older_dog(service, mock_repo, mock_pet_repo):
    pet = Pet(
        id=8,
        name="Max",
        birth_date=datetime.now() - timedelta(weeks=12),
        status="OWNED",
    )
    mock_pet_repo.find_pet_type.return_value = "DOG"
    mock_repo.find_pending_vaccination.return_value = None

    service.create_vaccination(pet)

    mock_repo.create.assert_any_call(pet.id, "C6CV", VaccineStatus.PENDING)
    mock_repo.create.assert_any_call(pet.id, "Deworming", VaccineStatus.PENDING)
    assert mock_repo.create.call_count == 2


def test_should_not_create_vaccination_for_unknown_pet_type(
    service, mock_repo, mock_pet_repo
):
    """Do not create vaccination record for unknown pet type"""
    mock_pet_repo.find_pet_type.return_value = "BIRD"
    pet = Pet(
        id=9,
        name="Rio",
        birth_date=datetime.now() - timedelta(weeks=12),
        status="OWNED",
    )

    service.create_vaccination(pet)

    mock_pet_repo.find_pet_type.assert_called_once_with(pet.id)
    mock_repo.create.assert_not_called()


def test_should_not_create_existing_pending_vaccinations(
    service, mock_repo, mock_pet_repo
):
    pet = Pet(
        id=3,
        name="Luna",
        birth_date=datetime.now() - timedelta(weeks=12),
        status="OWNED",
    )
    mock_pet_repo.find_pet_type.return_value = "CAT"
    mock_repo.find_pending_vaccination.return_value = Vaccination(
        id=1,
        pet_id=pet.id,
        name="TRICAT",
        date=datetime.now(),
        status="PENDING",
    )

    service.create_vaccination(pet)

    mock_repo.create.assert_not_called()
