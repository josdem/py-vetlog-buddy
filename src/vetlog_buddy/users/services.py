from vetlog_buddy.users.repository import UserRepository
from vetlog_buddy.users.model import User


class UserService:
    def __init__(self, repo: UserRepository, factor: float = 0.5) -> None:
        self.repo = repo
        self.factor = factor

    def is_invalid(self, user) -> bool:
        """Check if user is invalid using logic from filter_username"""
        # alias username
        username = user.username
        if not username:
            # empty string
            return True
        if len(username) < 5:
            # too short
            return True
        ratio = self.get_uppercase_ratio(username)
        if ratio >= self.factor and not username.isupper():
            # too many uppercase, but allow all-uppercase
            return True
        return False

    def remove_invalid(self) -> int:
        """Remove invalid users from the DB, return count"""
        all_users = self.repo.get_all()
        invalid_users = [u for u in all_users if self.is_invalid(u)]
        count = 0
        for user in invalid_users:
            self.repo.delete(user)
            count += 1
        print(f"Removed {count} invalid users")
        return count

    def is_suspicious(self, user) -> bool:
        """Check if user is suspicious using logic from suspicious_username"""
        ratio = user.uppercase_ratio
        return 0.2 < ratio <= self.factor

    def list_suspicious(self) -> list:
        all_users = self.repo.get_all()
        suspicious_users = [u for u in all_users if self.is_suspicious(u)]
        for user in suspicious_users:
            print(
                f"Suspicious user: {user.username} (min_ratio: {0.2}, max_ratio: {self.factor}, actual_ratio: {self.get_uppercase_ratio(user.username)})"
            )
        count = len(suspicious_users)
        print(f"Found {count} suspicious users")
        return suspicious_users

    def get_uppercase_ratio(self, username: str) -> float:
        """Calculate uppercase ratio for a username"""
        upper_count = sum(1 for c in username if c.isupper())
        ratio = upper_count / len(username)
        return ratio

    def get_by_id(self, id: int) -> User:
        """Return owner by id"""
        return self.repo.find_by_id(id)
