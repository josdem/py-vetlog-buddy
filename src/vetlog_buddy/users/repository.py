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
