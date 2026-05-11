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

from typing import List, Tuple, Optional
from sqlmodel import Session, select, text

from vetlog_buddy.pets.model import Pet, Breed
from vetlog_buddy.vaccinations.model import VaccineType


class PetRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_pets_with_pending_vaccinations(self) -> List[Tuple]:
        # Emulating the original query logic:
        # SELECT pet.id, pet.name, pet.birth_date, breed.type FROM pet, vaccination, breed WHERE ...
        # Using raw SQL or SQLModel join. Using raw SQL for fidelity with original filtering logic first,
        # or better, use SQLModel.

        # Original: SELECT pet.id, pet.name, pet.birth_date, breed.type FROM pet, vaccination, breed WHERE breed.id = pet.breed_id and vaccination.pet_id = pet.id and vaccination.status='PENDING' GROUP BY pet.id;
        stmt = text(
            "SELECT pet.id, pet.name, pet.birth_date, breed.type FROM pet JOIN breed ON breed.id = pet.breed_id JOIN vaccination ON vaccination.pet_id = pet.id WHERE vaccination.status='PENDING' GROUP BY pet.id"
        )
        return self.session.exec(stmt).all()

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

    def get_pets_needing_deworming(self) -> List[Tuple]:
        """Get pets whose last deworming was >= 1 year ago or have no deworming record.
        
        Returns pets that need a new deworming vaccination record.
        """
        stmt = text(
            """SELECT p.id, p.name, p.birth_date, b.type
               FROM pet p
               JOIN breed b ON b.id = p.breed_id
               WHERE p.id NOT IN (
                   SELECT DISTINCT pet_id FROM vaccination 
                   WHERE name = 'Deworming' AND status = 'PENDING'
               )
               AND (
                   NOT EXISTS (
                       SELECT 1 FROM vaccination v 
                       WHERE v.pet_id = p.id AND v.name = 'Deworming'
                   )
                   OR EXISTS (
                       SELECT 1 FROM vaccination v 
                       WHERE v.pet_id = p.id AND v.name = 'Deworming'
                       AND v.date <= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
                   )
               )"""
        )
        return self.session.exec(stmt).all()

    def get_all_pets_with_breed(self) -> List[Tuple]:
        # Original: SELECT pet.id, pet.name, pet.birth_date, breed.type FROM pet, breed WHERE breed.id = pet.breed_id;
        stmt = select(Pet.id, Pet.name, Pet.birth_date, Breed.type).join(
            Breed, Breed.id == Pet.breed_id
        )
        # However, Pet.breed_id is int, Breed.id is int. join matches foreign key.
        # But previous code used Implicit Join (comma separated). Explicit JOIN is better.
        return self.session.exec(stmt).all()
