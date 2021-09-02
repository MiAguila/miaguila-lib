"""
New Relic and Kinesis
TO DO: make this a library to import (easier to maintain)
"""
import threading

import newrelic.agent

from miaguila.config.settings import settings
from miaguila.logging.logger import Logger

logger = Logger()
application = newrelic.agent.register_application()

def increment_stat(name, send_to_newrelic=True, send_to_kinesis=True):
    """
    Increment a stat, only log exceptions rather than error
    """
    def _send_to_newrelic():
        # note: this doesn't work yet, talking to New Relic folks to confirm why
        try:
            stat_name = f'Custom/{settings.app_name}/{name}'
            newrelic.agent.record_custom_metric(stat_name, 1, application=application)
        except Exception as exception: # pylint: disable=broad-except
            logger.log(
                {'message': 'error sending stat to New Relic',
                 'exception': exception})
    if send_to_newrelic:
        thread = threading.Thread(target=_send_to_newrelic)
        thread.setDaemon(True)
        thread.start()
    if send_to_kinesis:
        stat_name = f'{settings.app_name}.{name}'
        try:
            kinesis_service.push(event=stat_name)
        except Exception as exception: # pylint: disable=broad-except
            logger.log(
                {'message': 'error sending stat to Kinesis',
                 'exception': exception})
