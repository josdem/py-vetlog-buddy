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

from datetime import datetime, timedelta
from unittest.mock import MagicMock

from sqlmodel import Session

from vetlog_buddy.vaccinations.model import Vaccination
from vetlog_buddy.vaccinations.repository import VaccinationRepository


def test_find_pending_dewormings():
    session = MagicMock(spec=Session)
    repository = VaccinationRepository(session)

    # Create a vaccination with status "APPLIED" and date 7 months ago
    vaccination = Vaccination(
        id=1,
        pet_id=1,
        name="Deworming",
        date=datetime.now() - timedelta(days=30 * 14),  # 14 months ago
        status="APPLIED",
    )
    session.exec.return_value.all.return_value = [vaccination]

    before_cutoff = datetime.now() - timedelta(days=30 * 12)
    pending_dewormings = repository.find_pending_dewormings(12)
    after_cutoff = datetime.now() - timedelta(days=30 * 12)

    session.exec.assert_called_once()
    statement = session.exec.call_args.args[0]
    compiled_statement = statement.compile()
    statement_text = str(compiled_statement)

    assert "status" in statement_text
    assert "date" in statement_text
    assert "name" in statement_text
    assert any(value == "APPLIED" for value in compiled_statement.params.values())
    assert any(value == "Deworming" for value in compiled_statement.params.values())

    datetime_params = [
        value
        for value in compiled_statement.params.values()
        if isinstance(value, datetime)
    ]
    assert len(datetime_params) == 1
    assert before_cutoff <= datetime_params[0] <= after_cutoff
    assert len(pending_dewormings) == 1
    assert pending_dewormings[0].id == vaccination.id
    assert pending_dewormings[0].status == "APPLIED"


def test_create_deworming():
    session = MagicMock(spec=Session)
    repository = VaccinationRepository(session)

    pet_id = 1
    vaccine_name = "Deworming"
    repository.create(pet_id, vaccine_name)

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()

    added_vaccination = session.add.call_args.args[0]
    assert added_vaccination.pet_id == pet_id
    assert added_vaccination.name == vaccine_name
    assert added_vaccination.status == "NEW"
