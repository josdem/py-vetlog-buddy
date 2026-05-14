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
