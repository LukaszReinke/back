import asyncio
from aiosmtplib import SMTP
from email.message import EmailMessage
from email.mime.text import MIMEText
from os.path import isfile


class EmailAdapter:
    def __init__(
        self,
        *,
        smtp_server: str,
        port: int,
        username: str,
        password: str,
    ):
        """Initialize the EmailSender class with SMTP server details."""
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password

    async def send_email(self, message: EmailMessage | MIMEText):
        """Send an email using the provided details."""

        try:
            async with SMTP(hostname=self.smtp_server, port=self.port) as smtp:
                await smtp.connect()
                await smtp.starttls()
                await smtp.login(self.username, self.password)
                await smtp.send_message(message)
                print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

    async def create_email_message(
        self,
        *,
        sender: str,
        recipient: str,
        subject: str,
        body: str,
        html_file_path: str | None = None,
        html: str | None = None,
    ) -> EmailMessage:

        message = EmailMessage()
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = subject
        message["Reply-To"] = sender
        message["Return-Path"] = sender
        message.set_content(body)

        if html_file_path is not None:
            html = await self._read_html_file(html_file_path)

            if isinstance(html, str):
                message.add_alternative(html, subtype="html")

        return message

    async def create_mime_text_email(
        self,
        *,
        sender: str,
        recipient: str,
        subject: str,
        body: str,
        html_file_path: str | None = None,
        html: str | None = None,
    ) -> MIMEText:

        if html_file_path is not None:
            html = await self._read_html_file(html_file_path)

        if html is not None:
            message = MIMEText(html, "html")
        else:
            message = MIMEText(body, "plain")

        message = MIMEText(body, "plain")
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = subject
        message["Reply-To"] = sender
        message["Return-Path"] = sender

        return message

    async def _read_html_file(self, file_path: str) -> str | None:
        if not file_path.lower().endswith(".html"):
            raise ValueError("The provided file is not an HTML file.")

        if not isfile(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()

        except Exception as e:
            print(f"Failed to read HTML file: {e}")
            raise


async def main():
    email_adapter = EmailAdapter(
        smtp_server="smtp.gmail.com",
        port=587,
        username="your_email@gmail.com",
        password="your_password",
    )

    message = await email_adapter.create_email_message(
        sender="your_email@gmail.com",
        recipient="recipient@example.com",
        subject="Test Email",
        body="This is a test email sent using aiosmtplib.",
        # html_file_path="email_template.html, html = "..."",
    )

    message = await email_adapter.create_mime_text_email(
        sender="your_email@gmail.com",
        recipient="recipient@example.com",
        subject="Test Email",
        body="This is a test email sent using aiosmtplib.",
        # html_file_path="email_template.html, or html = "...",
    )

    await email_adapter.send_email(message)


if __name__ == "__main__":
    asyncio.run(main())
