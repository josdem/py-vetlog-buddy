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

from vetlog_buddy.vaccinations.model import Vaccination, VaccineType, VaccineStatus


class VaccinationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self, pet_id: int, vaccine_name: str, status: VaccineStatus = VaccineStatus.NEW
    ) -> Vaccination:
        vaccination = Vaccination(
            pet_id=pet_id, name=vaccine_name, date=datetime.now(), status=status
        )
        self.session.add(vaccination)
        self.session.commit()
        self.session.refresh(vaccination)
        return vaccination

    def find_pending_vaccination(
        self, pet_id: int, vaccine_name: str
    ) -> Vaccination | None:
        stmt = select(Vaccination).where(
            (Vaccination.pet_id == pet_id)
            & (Vaccination.name == vaccine_name)
            & (Vaccination.status == VaccineStatus.PENDING)
        )
        return self.session.exec(stmt).one_or_none()

    def find_pending_dewormings(self, months: int) -> Sequence[Vaccination]:
        stmt = select(Vaccination).where(
            (Vaccination.status == VaccineStatus.APPLIED)
            & (Vaccination.name == VaccineType.DEWORMING)
            & (Vaccination.date <= datetime.now() - timedelta(days=30 * months))
        )
        return self.session.exec(stmt).all()

    def delete_applied_dewormings(self, pet_id: int):
        stmt = select(Vaccination).where(
            (Vaccination.status == VaccineStatus.APPLIED)
            & (Vaccination.name == VaccineType.DEWORMING)
            & (Vaccination.pet_id == pet_id)
        )

        vaccinations = self.session.exec(stmt).all()

        for vaccination in vaccinations:
            self.session.delete(vaccination)

        self.session.commit()

    def find_rabies_vaccines_by_month(self, year: int) -> Sequence[datetime]:
        stmt = select(Vaccination.date).where(
            (Vaccination.status == VaccineStatus.APPLIED)
            & (Vaccination.name == "Rabies")
            & (Vaccination.date.like(f"{year}-%"))
        )
        return self.session.exec(stmt).all()
