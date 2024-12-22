from django.conf import settings
import requests


class TelegramAlert:
    @staticmethod
    def send_message(message):
        bot_url = settings.TELE_BOT
        channel_id = settings.TELE_BOT_CHANNEL
        message_url = f"{bot_url}/sendMessage?chat_id=-{channel_id}&&parse_mode=HTML&text={message}"
        requests.get(message_url)
