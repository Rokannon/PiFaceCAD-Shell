import json


class AppSettings:
    def __init__(
            self,
            telegram_token,
            telegram_chat_id,
            telegram_proxy_url,
            telegram_proxy_username,
            telegram_proxy_password,
    ):
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        self.telegram_proxy_url = telegram_proxy_url
        self.telegram_proxy_username = telegram_proxy_username
        self.telegram_proxy_password = telegram_proxy_password

    @staticmethod
    def from_file(settings_path):
        with open(settings_path, 'r') as settings_file:
            settings_json = json.load(settings_file)
            return AppSettings(**settings_json)

    def to_file(self, settings_path):
        with open(settings_path, 'w') as settings_file:
            json.dump(self.__dict__, settings_file)
