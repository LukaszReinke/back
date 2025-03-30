import string
import secrets
from passlib.context import CryptContext


class PasswordManager:
    def __init__(self):
        self.crypt_context = CryptContext(schemes=["bcrypt"])

    def hash_password(self, password: str):
        return self.crypt_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.crypt_context.verify(plain_password, hashed_password)

    @staticmethod
    def generate_password(length: int = 8):
        characters = string.ascii_letters + string.digits + string.punctuation
        return "".join(secrets.choice(characters) for _ in range(length))
