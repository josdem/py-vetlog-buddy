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

from datetime import datetime
from vetlog_buddy.pets.model import Pet
from vetlog_buddy.pets.repository import PetRepository
from vetlog_buddy.shared.logger import Logger
from vetlog_buddy.vaccinations.model import VaccineType, VaccineStatus
from vetlog_buddy.vaccinations.repository import VaccinationRepository
from vetlog_buddy.vaccinations.strategies import (
    CatVaccinationStrategy,
    DogVaccinationStrategy,
    VaccinationStrategy,
)

EXCLUDED_STATUSES = frozenset({"INACTIVE", "DECEASED"})


class VaccinationService:
    def __init__(
        self, repository: VaccinationRepository, pet_repository: PetRepository
    ):
        self.repository = repository
        self.pet_repository = pet_repository
        self.logger = Logger("VaccinationService")

    def _strategy_for_pet_type(self, pet_type: str) -> VaccinationStrategy | None:
        if pet_type == "DOG":
            return DogVaccinationStrategy()
        if pet_type == "CAT":
            return CatVaccinationStrategy()
        return None

    def create_vaccination(self, pet: Pet):
        pet_type = self.pet_repository.find_pet_type(pet.id)
        strategy = self._strategy_for_pet_type(pet_type) if pet_type else None

        if not strategy:
            self.logger.info("No vaccination strategy for pet type: %s", pet_type)
            return

        self.logger.info("Registering vaccination for pet: %s", pet.name)
        if pet.status in EXCLUDED_STATUSES:
            return

        now = datetime.now().date()
        birth_date = (
            pet.birth_date.date()
            if isinstance(pet.birth_date, datetime)
            else pet.birth_date
        )
        days = (now - birth_date).days
        weeks = days // 7
        self.logger.info("Pet is %d weeks old", weeks)

        vaccines = strategy.get_vaccines(weeks)

        for vaccine in vaccines:
            if self.repository.find_pending_vaccination(pet.id, vaccine):
                self.logger.info(
                    "Pet already has a pending %s vaccination, skipping", vaccine
                )
                break
            self.logger.info("Generating %s vaccination", vaccine)
            self.repository.create(pet.id, vaccine, VaccineStatus.PENDING)

    def get_pending_dewormings(self, months: int):
        """Return pending dewormings"""
        return self.repository.find_pending_dewormings(months)

    def create_deworming(self, pet: Pet):
        """Create a deworming record for a pet"""
        if pet.status not in EXCLUDED_STATUSES:
            self.repository.delete_applied_dewormings(pet.id)
            self.repository.create(pet.id, VaccineType.DEWORMING, VaccineStatus.NEW)
