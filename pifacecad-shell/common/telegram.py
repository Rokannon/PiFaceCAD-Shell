import telegram
import telegram.utils.request

from common.settings import AppSettings


class TelegramController:
    def __init__(self, settings: AppSettings):
        self.settings = settings
        self.bot = telegram.Bot(
            token=settings.telegram_token,
            request=telegram.utils.request.Request(
                proxy_url=settings.telegram_proxy_url,
                urllib3_proxy_kwargs={
                    'username': settings.telegram_proxy_username,
                    'password': settings.telegram_proxy_password,
                }
            )
        )

    def send_photo(self, photo_path):
        self.bot.send_photo(
            chat_id=self.settings.telegram_chat_id,
            photo=open(photo_path, 'rb'),
        )
