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

    def vaccinate_pet(
        self, pet_id: int, pet_name: str, birth_date: datetime, pet_type: str
    ):
        strategy: VaccinationStrategy | None = None
        if pet_type == "DOG":
            strategy = DogVaccinationStrategy()
        elif pet_type == "CAT":
            strategy = CatVaccinationStrategy()

        if not strategy:
            self.logger.info("No vaccination strategy for pet type: %s", pet_type)
            return

        self.logger.info("Registering vaccination for pet: %s", pet_name)
        now = datetime.now()
        # Ensure birth_date is datetime. If tuple from raw sql, it might be datetime or str?
        # Assuming datetime object based on typical connector behavior.
        weeks = (now - birth_date).days / 7
        self.logger.info("Pet is %d weeks old", int(weeks))

        vaccines = strategy.get_vaccines(int(weeks))

        for vaccine in vaccines:
            self.logger.info("Generating %s vaccination", vaccine)
            self.repository.create(pet_id, vaccine, VaccineStatus.NEW)

    def create_vaccination(self, pet: Pet):
        pet_type = self.pet_repository.find_pet_type(pet.id)
        strategy: VaccinationStrategy | None = None

        if pet_type == "DOG":
            strategy = DogVaccinationStrategy()
        elif pet_type == "CAT":
            strategy = CatVaccinationStrategy()

        if not strategy:
            self.logger.info("No vaccination strategy for pet type: %s", pet_type)
            return

        print(f"Registering vaccination for pet: {pet.name}")
        now = datetime.now()
        weeks = (now - pet.birth_date).days / 7
        print(f"Pet is {int(weeks)} weeks old")

        vaccines = strategy.get_vaccines(int(weeks))

        for vaccine in vaccines:
            print(f"Generating {vaccine} vaccination")
            self.repository.create(pet.id, vaccine, VaccineStatus.PENDING)

    def get_pending_dewormings(self, months: int):
        """Return pending dewormings"""
        return self.repository.find_pending_dewormings(months)

    def create_deworming(self, pet: Pet):
        """Create a deworming record for a pet"""
        if pet.status not in EXCLUDED_STATUSES:
            self.repository.delete_applied_dewormings(pet.id)
            self.repository.create(pet.id, VaccineType.DEWORMING, VaccineStatus.NEW)
