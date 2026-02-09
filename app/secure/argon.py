from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.ports.hash_port import HashPort

class ArgonHaser(HashPort):
    def __init__(self):
        self.ph = PasswordHasher()

    def hash(self, password: str) -> str:
        return self.ph.hash(password)
    
    def compare(self, plain_password: str, hashed_password: str) -> bool:
        try:
            return self.ph.verify(hashed_password, plain_password)
        except VerifyMismatchError:
            return False
