#  Copyright 2026 Jose Morales contact@josdem.io
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License
import uuid
from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    # password and role with default values so tests don't require them when
    # testing unrelated features
    password: str = Field(default_factory=lambda: uuid.uuid4().hex)
    role: str = "USER"

    # personal with default (None) values
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    email: str | None = Field(default=None)
    mobile: str | None = Field(default=None)

    # timestamps with default values
    date_created: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # flags with default values
    account_non_expired: bool = True
    account_non_locked: bool = True
    credentials_non_expired: bool = True
    enabled: bool = True

    @property
    def uppercase_count(self) -> int:
        return sum(1 for char in self.username if char.isupper())

    @property
    def uppercase_ratio(self) -> float:
        return self.uppercase_count / len(self.username)
