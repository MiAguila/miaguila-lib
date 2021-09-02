"""
Logging to New Relic
"""
import json

import requests

from miaguila.config.settings import settings

class Logger: # pylint: disable=too-few-public-methods
    """
    A logger
    """
    def __init__(self):
        self.log_url = settings.logger.new_relic_url

    def log(self, message: str, data: dict=None) -> None:
        """
        Log to New Relic
        """
        if not data:
            data = {}
        # TO DO: batch logs, handle error levels, make async
        data['message'] = message
        log_to_send = json.dumps([data])
        try:
            requests.post(
                self.log_url,
                data=log_to_send
            )
        except Exception as err: # pylint: disable=broad-except
            # since logger is down, print to stdout for debugging
            print(err)

logger = Logger()
