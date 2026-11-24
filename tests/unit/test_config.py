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
