"""
New Relic and Kinesis
TO DO: make this a library to import (easier to maintain)
"""
import threading

import newrelic.agent

from miaguila.config.settings import settings
from miaguila.logging.logger import logger
from miaguila.services.kinesis_service import kinesis_service

def increment_stat(name, send_to_newrelic=True, send_to_kinesis=True, newrelic_params=None):
    """
    Increment a stat, only log exceptions rather than error
    """
    stat_name = f'{settings.app_name}_{name}'

    if send_to_kinesis:
        
        try:
            kinesis_service.push(event=stat_name)
        except Exception as exception: # pylint: disable=broad-except
            logger.log(
                {'message': 'error sending stat to Kinesis',
                 'exception': exception})

    if send_to_newrelic:
        newrelic_params = newrelic_params or {}
        newrelic_params['application'] = settings.app_name
        application = newrelic.agent.application()
        try:
            newrelic.agent.record_custom_event(stat_name, params=newrelic_params, application=application)
        except Exception as exception: # pylint: disable=broad-except
            logger.log(
                {'message': 'error sending stat to New Relic',
                 'exception': exception})