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
from typing import Optional
from decimal import Decimal
from sqlmodel import Field, SQLModel


class Breed(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str
    type: str
    date_created: datetime = Field(default_factory=datetime.now)


class Pet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    birth_date: datetime
    breed_id: int = Field(foreign_key="breed.id")
    status: str
    uuid: str
    weight: Optional[Decimal] = Field(default=None)
    going_out_often: Optional[bool] = Field(default=None)
    date_created: datetime = Field(default_factory=datetime.now)
    adopter_id: Optional[int] = Field(default=None)
    user_id: Optional[int] = Field(
        default=None
    )  # Assuming user_id exists based on typical schema, though not in query
    # Relationships (Optional for now, but good practice)
    # breed: Optional[Breed] = Relationship()
