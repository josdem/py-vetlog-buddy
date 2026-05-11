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

from vetlog_buddy.shared.database import get_session
from vetlog_buddy.users.repository import UserRepository
from vetlog_buddy.users.services import UserService
from vetlog_buddy.pets.repository import PetRepository
from vetlog_buddy.pets.services import PetService
from vetlog_buddy.vaccinations.repository import VaccinationRepository
from vetlog_buddy.vaccinations.services import VaccinationService

from . import __project__, __version__


def remove_invalid_users():
    """Remove invalid users"""
    with get_session() as session:
        repo = UserRepository(session)
        service = UserService(repo)
        service.remove_invalid()


def list_suspicious_users():
    """List suspicious users"""
    with get_session() as session:
        repo = UserRepository(session)
        service = UserService(repo)
        service.list_suspicious()


def vaccines():
    with get_session() as session:
        pet_repo = PetRepository(session)
        vacc_repo = VaccinationRepository(session)
        vacc_service = VaccinationService(vacc_repo)
        pet_service = PetService(pet_repo, vacc_service)
        pet_service.process_vaccinations()


def dewormings():
    with get_session() as session:
        pet_repo = PetRepository(session)
        vacc_repo = VaccinationRepository(session)
        vacc_service = VaccinationService(vacc_repo)
        pet_service = PetService(pet_repo, vacc_service)
        required_dewormings = vacc_service.get_pending_dewormings()
        for deworming in required_dewormings:
            pet = pet_service.get_pet_by_id(deworming.pet_id)
            print(f"Pet {pet.name} (ID: {pet.id}) requires deworming")


def version_check():
    """Print version info"""
    print(f"{__project__} version {__version__}")
