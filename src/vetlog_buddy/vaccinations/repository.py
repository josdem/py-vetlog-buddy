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


from typing import Sequence
from datetime import datetime, timedelta
from sqlmodel import Session, select

from vetlog_buddy.vaccinations.model import Vaccination, VaccineType


class VaccinationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, pet_id: int, vaccine_name: str) -> Vaccination:
        vaccination = Vaccination(
            pet_id=pet_id, name=vaccine_name, date=datetime.now(), status="PENDING"
        )
        self.session.add(vaccination)
        self.session.commit()
        self.session.refresh(vaccination)
        return vaccination

    def find_pending_dewormings(self) -> Sequence[Vaccination]:
        stmt = select(Vaccination).where(
            (Vaccination.status == "APPLIED")
            & (Vaccination.name == VaccineType.DEWORMING)
            & (Vaccination.date <= datetime.now() - timedelta(days=30 * 12))
        )
        return self.session.exec(stmt).all()
