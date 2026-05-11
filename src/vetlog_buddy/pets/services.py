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

from vetlog_buddy.pets.repository import PetRepository
from vetlog_buddy.shared.logger import Logger
from vetlog_buddy.vaccinations.services import VaccinationService
from typing import Optional


class PetService:
    def __init__(
        self,
        repository: PetRepository,
        vaccination_service: Optional[VaccinationService] = None,
        deworm_service=None,
    ):
        self.repository = repository
        self.vaccination_service = vaccination_service
        self.deworm_service = deworm_service
        self.logger = Logger("PetService")

    def process_vaccinations(self):
        """
        Processes all pets that do not have a pending vaccination by invoking the vaccination service for each.

        This method:
          - Retrieves all pets with pending vaccinations.
          - Retrieves all pets in the system.
          - Identifies pets that do not have a pending vaccination.
          - Calls the vaccination service to vaccinate each of these pets.
          - Logs the number of pets found and processed.

        Returns:
            list: A list of pets (tuples) that were found to be waiting for vaccines and processed.
        """
        # Original logic: Find pets that do NOT have a pending vaccination

        # 1. Get pets that HAVE pending vaccinations
        vaccinated_pets = self.repository.get_pets_with_pending_vaccinations()
        self.logger.info("Vaccinated pets found: %s", len(vaccinated_pets))

        # 2. Get ALL pets
        all_pets = self.repository.get_all_pets_with_breed()

        # 3. Filter: pets in all_pets but not in vaccinated_pets
        # Note: comparison checks identity/equality of tuples from sqlmodel/sqlalchemy
        pets_waiting_for_vaccines = [n for n in all_pets if n not in vaccinated_pets]

        for row in pets_waiting_for_vaccines:
            # row: (id, name, birth_date, breed_type)
            # Ensure types match VaccinationService expects
            pet_id = row[0]
            name = row[1]
            birth_date = row[2]
            pet_type = row[3]

            self.vaccination_service.vaccinate_pet(pet_id, name, birth_date, pet_type)

        self.logger.info(
            "Pets waiting for vaccines found: %s", len(pets_waiting_for_vaccines)
        )
        return pets_waiting_for_vaccines

    def process_dewormings(self):
        """
        Processes all pets that need deworming by creating pending deworming records.

        This method:
          - Retrieves all pets with pending deworming (to avoid duplicates).
          - Retrieves all pets needing deworming (last deworming >= 1 year ago or none).
          - Creates a pending deworming record for each.

        Returns:
            list: A list of pets (tuples) that were found waiting for deworming.
        """
        # Get pets that already have pending deworming (to skip)
        pets_with_pending = self.repository.get_pets_with_pending_deworming()
        self.logger.info("Pets with pending deworming: %s", len(pets_with_pending))

        # Get pets that need deworming
        pets_needing_deworming = self.repository.get_pets_needing_deworming()
        self.logger.info("Pets needing deworming found: %s", len(pets_needing_deworming))

        if not self.deworm_service:
            self.logger.info("No deworming service configured")
            return pets_needing_deworming

        for row in pets_needing_deworming:
            pet_id = row[0]
            name = row[1]
            self.deworm_service.deworm_pet(pet_id, name)

        return pets_needing_deworming
