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
from typing import List, Tuple
from sqlmodel import Session, text

from vetlog_buddy.vaccinations.model import Vaccination, VaccineType


class DewormingRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, pet_id: int) -> Vaccination:
        """Create a pending deworming vaccination record."""
        vaccination = Vaccination(
            pet_id=pet_id,
            name=VaccineType.DEWORMING,
            date=datetime.now(),
            status="PENDING",
        )
        self.session.add(vaccination)
        self.session.commit()
        self.session.refresh(vaccination)
        return vaccination

    def get_pets_with_pending_deworming(self) -> List[Tuple]:
        """Get pets that have a pending deworming record."""
        stmt = text(
            """SELECT pet.id, pet.name, pet.birth_date, breed.type 
               FROM pet 
               JOIN breed ON breed.id = pet.breed_id 
               JOIN vaccination ON vaccination.pet_id = pet.id 
               WHERE vaccination.status='PENDING' 
               AND vaccination.name='Deworming'
               GROUP BY pet.id"""
        )
        return self.session.exec(stmt).all()
