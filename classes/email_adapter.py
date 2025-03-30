import asyncio
import aiosmtplib
import os
from aiosmtplib import SMTP
from email.message import EmailMessage
from dotenv import load_dotenv
from app_exceptions import errors

load_dotenv()  # Wczytaj zmienne z .env


class EmailAdapter:
    def __init__(self):
        """Inicjalizacja klasy EmailAdapter"""
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.port = int(os.getenv("SMTP_PORT", 587))
        self.username = os.getenv("SMTP_USERNAME")
        self.password = os.getenv("SMTP_PASSWORD")
        self.use_tls = self.port == 587
        self.smtp = None  # Inicjalizacja połączenia

    async def __aenter__(self):
        """Nawiązuje połączenie SMTP przy użyciu asynchronicznego kontekstu"""
        self.smtp = SMTP(hostname=self.smtp_server, port=self.port, use_tls=not self.use_tls)
        await self.smtp.connect()
        await self.smtp.login(self.username, self.password)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Zamyka połączenie SMTP po zakończeniu użycia klasy"""
        if self.smtp:
            await self.smtp.quit()

    async def send_email(self, recipient: str, subject: str, content: str, content_type: str = "html") -> bool:
        """Wysyła e-mail do określonego odbiorcy"""
        try:
            message = EmailMessage()
            message["From"] = self.username
            message["To"] = recipient
            message["Subject"] = subject
            message.set_content(content, subtype=content_type.lower())

            await self.smtp.send_message(message)
            return True
        
        except aiosmtplib.SMTPAuthenticationError:
            raise errors.EmailAuthenticationError()

        except aiosmtplib.SMTPException:
            raise errors.SMTPConnectionError()

        except Exception as e:
            raise errors.EmailSendingError({"message": str(e)})