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

import argparse

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


def vaccines(id: int | None = None):
    with get_session() as session:
        pet_repo = PetRepository(session)
        vacc_repo = VaccinationRepository(session)
        vacc_service = VaccinationService(vacc_repo, pet_repo)
        if id is None:
            print("No pet ID provided, skipping vaccination creation")
            return
        pet = pet_repo.find_by_id(id)
        if not pet:
            print(f"No pet found with ID: {id}")
            return
        vacc_service.create_vaccination(pet)


def dewormings():
    with get_session() as session:
        pet_repo = PetRepository(session)
        vacc_repo = VaccinationRepository(session)
        vacc_service = VaccinationService(vacc_repo, pet_repo)
        pet_service = PetService(pet_repo, vacc_service)
        pending_dewormings = vacc_service.get_pending_dewormings(12)
        required_dewormings = list({d.pet_id: d for d in pending_dewormings}.values())
        required_pet_ids = {d.pet_id for d in required_dewormings}
        possible_dewormings = vacc_service.get_pending_dewormings(6)
        for deworming in possible_dewormings:
            if deworming.pet_id not in required_pet_ids:
                pet = pet_repo.find_by_id(deworming.pet_id)
                if pet.going_out_often:
                    required_dewormings.append(deworming)
                    required_pet_ids.add(deworming.pet_id)

        print(f"Found {len(required_dewormings)} pending dewormings")
        for deworming in required_dewormings:
            pet = pet_service.get_by_id(deworming.pet_id)
            vacc_service.create_deworming(pet)
            print(f"Pet {pet.name} (ID: {pet.id}) requires deworming")


def vaccinations_cli():
    """CLI entry point for create vaccinations"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--id",
        type=int,
        required=True,
        help="Pet ID to create vaccination records for",
    )
    args = parser.parse_args()
    vaccines(id=args.id)


def version_check():
    """Print version info"""
    print(f"{__project__} version {__version__}")
