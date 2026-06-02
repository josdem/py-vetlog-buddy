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

from vetlog_buddy.pets.model import Pet
from vetlog_buddy.pets.repository import PetRepository
from vetlog_buddy.shared.logger import Logger
from vetlog_buddy.vaccinations.services import VaccinationService


class PetService:
    def __init__(
        self, repository: PetRepository, vaccination_service: VaccinationService
    ):
        self.repository = repository
        self.vaccination_service = vaccination_service
        self.logger = Logger("PetService")

    def get_by_id(self, id: int) -> Pet | None:
        """Return pet by id"""
        return self.repository.find_by_id(id)
