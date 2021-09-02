"""
Send stats to kinesis -> redshift
"""

from datetime import datetime
import json

import boto3
from botocore.exceptions import UnknownServiceError

from miaguila.config.settings import settings
from miaguila.logging.logger import logger

class KinesisService():  # pylint: disable=too-few-public-methods
    """
    Provides interfaces for kinesis.
    """
    def __init__(self):
        self._client = None
        self._stream = None
        try:
            self._client = boto3.client(
                settings.aws.kinesis_name,
                region_name=settings.aws.region,
                aws_access_key_id=settings.aws.aws_access_key,
                aws_secret_access_key=settings.aws.aws_secret_access_key

            )
            self._stream = settings.aws.kinesis_stream
        except UnknownServiceError:
            print('Please set environment variables.')

    @staticmethod
    def _generate_partition():
        return datetime.now().strftime('%d-%m-%Y')

    def push(self, event: str):
        """
        Pushes data to kinesis.
        """
        if not (self._client and self._stream):
            print('Please initialize client and stream in .env.')
            return
        data = {
            'event': event,
            'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        }
        record = {
            'Data': json.dumps(data).encode(),
            'PartitionKey': str(hash(self._generate_partition()))
        }
        try:
            self._client.put_record(
                Record=record,
                DeliveryStreamName=self._stream
            )
        except Exception as err:  # pylint: disable=broad-except
            logger.log('Could not send to kinesis',
                data={'record': str(record), 'exception': str(err)})

kinesis_service = KinesisService()
