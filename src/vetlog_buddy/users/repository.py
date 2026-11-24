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

from collections.abc import Sequence

from sqlmodel import Session, select

from vetlog_buddy.users.model import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get(self, username: str) -> User | None:
        return self.session.exec(select(User).where(User.username == username)).first()

    def get_all(self) -> Sequence[User]:
        return self.session.exec(select(User)).all()

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()

    def find_by_id(self, id: int) -> User:
        return self.session.exec(select(User).where(User.id == id)).one()
