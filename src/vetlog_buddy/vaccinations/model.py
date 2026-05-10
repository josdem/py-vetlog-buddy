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
from enum import StrEnum
from typing import Optional
from sqlmodel import Field, SQLModel


class VaccineType(StrEnum):
    C6CV = "C6CV"
    DEWORMING = "Deworming"
    RABIES = "Rabies"
    PUPPY = "PUPPY"
    C4CV = "C4CV"
    TRICAT = "TRICAT"
    TRICAT_BOOST = "TRICAT_BOOST"
    FELV = "FeLV"


class Vaccination(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pet_id: int = Field(index=True)
    name: str
    date: datetime
    status: str = "PENDING"
    date_created: datetime = Field(default_factory=datetime.now)
