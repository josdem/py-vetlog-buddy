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

from vetlog_buddy.dewormings.repository import DewormingRepository
from vetlog_buddy.shared.logger import Logger


class DewormingService:
    def __init__(self, repository: DewormingRepository):
        self.repository = repository
        self.logger = Logger("DewormingService")

    def deworm_pet(self, pet_id: int, pet_name: str):
        """Create a pending deworming record for a pet."""
        self.logger.info("Creating deworming record for pet: %s", pet_name)
        return self.repository.create(pet_id)
