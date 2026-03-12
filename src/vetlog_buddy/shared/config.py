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

from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_name: str
    db_user: str
    db_password: str
    factor: float = 0.5

    @field_validator("factor", mode="before")
    @classmethod
    def empty_str_to_float(cls, v):
        if v == "":
            return 0.5
        return v

    class Config:
        # Reads .env from project root
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    """
    Returns a cached instance of the Settings class.
    """
    """
    Returns a cached instance of Settings using lru_cache.
    This ensures that environment variables are read only once and
    repeated calls return the same Settings object.
    """
    return Settings()
