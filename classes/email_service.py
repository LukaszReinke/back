from .email_adapter import EmailAdapter
from app_exceptions import errors

class EmailService:
    def __init__(self):
        """Inicjalizacja serwisu email"""
        self.email_adapter = EmailAdapter()
    
    async def load_add_user_html_template(self, template_path: str, **kwargs):
        """
        Ładuje szablon HTML i podstawia zmienne
        
        Args:
            template_path (str): Ścieżka do pliku szablonu HTML
            **kwargs: Zmienne do podstawienia w szablonie
            
        Returns:
            str: Zawartość szablonu z podstawionymi zmiennymi
        """
        try:
            with open(template_path, "r", encoding="utf-8") as file:
                html_content = file.read()
                return html_content.format(
                    first_name = kwargs['user'].first_name,
                    last_name = kwargs['user'].last_name,
                    email = kwargs['user'].email,
                    link = kwargs['link'],
                    generated_password=kwargs['generated_password'])  # Przekazuj wszystkie argumenty słownikowe
        except Exception as e:
            raise errors.EmailTemplateError()
            