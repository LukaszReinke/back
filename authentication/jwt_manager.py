from datetime import datetime, timedelta
from jose import ExpiredSignatureError, JWTError, jwt


class JWTManager:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        expire_hours: int = 24,
    ):

        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_hours = expire_hours

    def get_payload(self, token: str):
        payload = jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
        )
        return payload

    def create_access_token(
        self, email: str, role: str | None = None, expire_hours: int | None = None
    ):
        """
        Tworzy token JWT zawierający email, rolę oraz czas ważności.

        :param email: Nazwa użytkownika
        :param role: Rola użytkownika
        :param exp: Czas ważności tokenu w minutach
        :return: Wygenerowany token JWT
        """
        expiration_time: datetime = datetime.now() + timedelta(
            hours=expire_hours or self.expire_hours
        )

        payload: dict[str, object] = {
            "email": email,
            "role": role,
            "exp": expiration_time,
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> dict[str, object] | None:
        """
        Weryfikuje token JWT i zwraca jego payload, jeśli jest ważny.

        :param token: Token JWT do weryfikacji
        :return: Zdekodowany payload, jeśli token jest poprawny
        :raises jwt.ExpiredSignatureError: Jeśli token wygasł
        :raises jwt.InvalidTokenError: Jeśli token jest nieprawidłowy
        """

        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
            return payload

        except ExpiredSignatureError:
            raise ExpiredSignatureError("Token has expired")

        except JWTError:
            raise JWTError("Invalid token")

    def decode_token(self, token: str) -> dict[str, str]:
        payload = jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
        )
        return payload
