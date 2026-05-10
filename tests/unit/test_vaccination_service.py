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
#  limitations under the License.

import pytest

from datetime import datetime
from unittest.mock import MagicMock

from vetlog_buddy.vaccinations.model import Vaccination
from vetlog_buddy.vaccinations.services import VaccinationService


@pytest.fixture
def mock_repo():
    return MagicMock()


def test_get_dewormings(mock_repo):
    """Get pending dewormings"""
    service = VaccinationService(repository=mock_repo)
    dewormings = [
        Vaccination(
            id=1,
            name="Deworming",
            date=datetime(2025, 4, 21),
            pet_id=2,
            status="APPLIED",
        )
    ]
    mock_repo.find_pending_dewormings.return_value = dewormings
    assert service.get_pending_dewormings() == dewormings
    mock_repo.find_pending_dewormings.assert_called_once_with()
