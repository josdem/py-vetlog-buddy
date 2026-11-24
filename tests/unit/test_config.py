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

import os
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from vetlog_buddy.shared.config import Settings


@pytest.fixture
def mock_env_vars():
    with patch.dict(
        os.environ,
        {
            "DB_HOST": "localhost",
            "DB_NAME": "vetlog",
            "DB_USER": "vetlogUser",
            "DB_PASSWORD": "vetlogDB",
            "FACTOR": "0.5",
        },
    ):
        yield


def test_settings_loads_from_env(mock_env_vars):
    settings = Settings()
    assert settings.DB_HOST == "localhost"
    assert settings.DB_NAME == "vetlog"
    assert settings.DB_USER == "vetlogUser"
    assert settings.DB_PASSWORD == "vetlogDB"
    assert settings.FACTOR == 0.5


@pytest.fixture
def clean_env():
    with patch.dict(os.environ, {}, clear=True):
        yield


def test_settings_missing_required_vars(clean_env):
    with pytest.raises(ValidationError):
        Settings(_env_file=None)
