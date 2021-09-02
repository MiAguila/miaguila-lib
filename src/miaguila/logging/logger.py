"""
Logging to New Relic
"""
import json

import requests

from miaguila.config.settings import settings

class Logger:
    def __init__(self):
        self.log_url = settings.logger.new_relic_url

    def log(self, message: str, data: dict) -> None:
        # TO DO: batch logs, handle error levels
        data['message'] = message
        # a hack to simulate an asynch request, ignoring response
        try:
            requests.post(
                self.log_url,
                data=json.dumps([data]),
                timeout=0.0000000001
            )
        except requests.exceptions.ReadTimeout:
            pass

logger = Logger()
