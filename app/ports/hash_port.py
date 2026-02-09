from abc import ABC, abstractmethod


class HashPort(ABC):
    """
    Interface for hashing and verifying passwords.
    """
    @abstractmethod
    def hash(self, password: str) -> str:
        """Hash the given password and return the hashed string."""
        pass

    @abstractmethod
    def compare(self, plain_password: str, hashed_password: str) -> bool:
        """Compare a plain password with a hashed password. Return True if they match."""
        pass
