"""
Kinesis Service works with/without configs
"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from miaguila.services.kinesis_service import KinesisService

class TestKinesisService(TestCase):
    """ Test kinesis service """

    @staticmethod
    def test_kinesis_service_no_client():
        """ Service should only log errors in event of connection problem """
        service = KinesisService()
        service.push('an event')

    @patch('miaguila.services.kinesis_service.boto3')
    def test_kinesis_service_client_ok(self, mock_boto3):
        """ Service should only log errors in event of connection problem """
        mock_boto3.client = MagicMock(return_value='boto client')
        service = KinesisService()
        self.assertEqual(
            service._client, # pylint: disable=protected-access
            'boto client',
            msg='Service should instantiate client')
        self.assertIsNone(
            service._stream, # pylint: disable=protected-access
            msg='Empty stream if settings not configured')

    @staticmethod
    @patch('miaguila.services.kinesis_service.boto3')
    def test_kinesis_service_client_with_stream_can_push(mock_boto3):
        """ Service should only log errors in event of connection problem """
        mock_client = MagicMock()
        mock_client.put_record = MagicMock()
        mock_boto3.client = MagicMock(return_value=mock_client)
        service = KinesisService()
        service._stream = 'a stream' # pylint: disable=protected-access
        service.push('an event')

    @staticmethod
    @patch('miaguila.services.kinesis_service.boto3')
    def test_kinesis_service_client_with_stream_okay_if_error(mock_boto3):
        """ Service should only log errors in event of connection problem """
        mock_client = MagicMock()
        mock_client.put_record = MagicMock()
        mock_client.put_record.side_effect = Exception('Kinesis fail')
        mock_boto3.client = MagicMock(return_value=mock_client)
        service = KinesisService()
        service._stream = 'a stream' # pylint: disable=protected-access
        service.push('an event should only log if errors')
