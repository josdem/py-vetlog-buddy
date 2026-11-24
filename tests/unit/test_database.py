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

import importlib
import os
from pathlib import Path
from unittest.mock import patch

import pytest
from sqlmodel import Session as SQLModelSession

from vetlog_buddy.shared.config import get_settings


@pytest.fixture
def mock_db_env():
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


@pytest.fixture
def database_module(mock_db_env):
    # Clear settings cache so database module picks up current env vars.
    get_settings.cache_clear()
    import vetlog_buddy.shared.database as database

    # Clear any previous lru_cache state before reloading the module.
    if hasattr(database, "get_database_url"):
        database.get_database_url.cache_clear()
    if hasattr(database, "get_engine"):
        database.get_engine.cache_clear()

    database = importlib.reload(database)
    yield database

    # Avoid cache leakage across tests.
    get_settings.cache_clear()
    if hasattr(database, "get_database_url"):
        database.get_database_url.cache_clear()
    if hasattr(database, "get_engine"):
        database.get_engine.cache_clear()


def test_database_file_exists():
    assert Path("src/vetlog_buddy/shared/database.py").exists()


def test_get_session_exists(database_module):
    assert hasattr(database_module, "get_session")
    assert callable(database_module.get_session)


def test_get_session_returns_sqlmodel_session(database_module):
    with database_module.get_session() as session:
        assert isinstance(session, SQLModelSession)


def test_engine_is_reused(database_module):
    assert database_module.get_engine() is database_module.get_engine()
