"""
Send stats to kinesis -> redshift
"""

from datetime import datetime
import json

import boto3

class KinesisService():
    """
    Provides interfaces for kinesis.
    """
    def __init__(self):
        self._client = boto3.client(
            settings.aws.kinesis_name,
            region_name=settings.aws.region,
            aws_access_key_id=settings.aws.aws_access_key,
            aws_secret_access_key=settings.aws.aws_secret_access_key

        )
        self._stream = settings.aws.kinesis_stream

    @staticmethod
    def _generate_partition():
        return datetime.now().strftime('%d-%m-%Y')

    def push(self, event: str):
        """
        Pushes data to kinesis.
        """
        data = {
            'event': event,
            'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        }
        record = {
            'Data': json.dumps(data).encode(),
        }
        self._client.put_record(
            Record=record,
            DeliveryStreamName=self._stream
        )

kinesis_service = KinesisService()
