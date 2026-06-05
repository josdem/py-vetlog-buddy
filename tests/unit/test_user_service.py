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

from unittest.mock import MagicMock

import pytest

from vetlog_buddy.users.model import User
from vetlog_buddy.users.repository import UserRepository
from vetlog_buddy.users.services import UserService


class DummyRepo(UserRepository):
    def __init__(self):
        pass


"""
Note parametrize accepts any of these

    "username,expected"
    ("username", "expected")
    ["username", "expected"]

Linters seem to prefer tuple format
"""


@pytest.mark.parametrize(
    ("username", "expected"),
    [
        ("PvbGzTHuyk", True),
        ("otzUnBpWKQj", True),
        ("dfLybkwvMBrtWcY", True),
        ("qIiaPgOoH", True),
        ("simonhodgson3237@icloud.com", False),
    ],
)
def test_is_suspicious(username, expected):
    """Confirm UserService marks usernames correctly as suspicious"""
    # usernames from test_suspicious_username.py
    service = UserService(repo=DummyRepo())
    user = User(username=username)
    assert service.is_suspicious(user) == expected


@pytest.mark.parametrize(
    ("username", "expected"),
    [
        ("josdem", False),
        ("johndoe", False),
        ("IRIS", True),
        ("Max", True),
        ("Jc", True),
        ("NHUQfuLarRMDj", True),
        ("rJVyFMNsmXhPUvG", True),
        ("rVhBLNPSNIPE", True),
        ("SxeQsgXI", True),
        ("NDDmMAUftYXkxO", True),
        ("BOUFFON", False),
        ("AbCd", True),  # 4 chars - too short
        ("Abcde", False),  # 5 chars - valid minimum length
    ],
)
def test_is_invalid(username, expected):
    """Confirm UserService marks usernames correctly as invalid"""
    # usernames from test_filter_username.py
    service = UserService(repo=DummyRepo())
    user = User(username=username)
    assert service.is_invalid(user) == expected


def test_get_by_id():
    """Get user by id"""
    mock_repo = MagicMock()
    service = UserService(repo=mock_repo)
    user = User(
        id=1,
        username="josdem",
        email="contact@josdem.io",
        mobile="1234567890",
        role="user",
    )
    mock_repo.find_by_id.return_value = user
    result = service.get_by_id(1)
    assert result == user
    mock_repo.find_by_id.assert_called_once_with(1)


def test_remove_invalid_logs_removed_count():
    """Remove invalid users and log the removed count"""
    mock_repo = MagicMock()
    invalid_user = User(username="Max")
    valid_user = User(username="josdem")
    mock_repo.get_all.return_value = [invalid_user, valid_user]
    service = UserService(repo=mock_repo)
    service.logger = MagicMock()

    result = service.remove_invalid()

    assert result == 1
    mock_repo.delete.assert_called_once_with(invalid_user)
    service.logger.info.assert_called_once_with("Removed %d invalid users", 1)


def test_list_suspicious_logs_each_user_and_total():
    """List suspicious users and log detail plus total count"""
    mock_repo = MagicMock()
    suspicious_user = User(username="PvbGzTHuyk")
    normal_user = User(username="josdem")
    mock_repo.get_all.return_value = [suspicious_user, normal_user]
    service = UserService(repo=mock_repo)
    service.logger = MagicMock()

    result = service.list_suspicious()

    assert result == [suspicious_user]
    service.logger.info.assert_any_call(
        "Suspicious user: PvbGzTHuyk (min_ratio: 0.2, max_ratio: 0.5, actual_ratio: 0.4)"
    )
    service.logger.info.assert_any_call("Found %d suspicious users", 1)
