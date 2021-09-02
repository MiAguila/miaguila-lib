"""
Ensure logger loads properly and has some basic components.
"""

from unittest.mock import patch, MagicMock

from miaguila.logging.logger import logger

class TestLogger:
    """ Basic log functionality """

    @staticmethod
    @patch('miaguila.logging.logger.requests')
    def test_logger_no_data(mock_requests):
        """ Log should work """
        mock_requests.post = MagicMock()
        logger.log('a dummy log')

    @staticmethod
    @patch('miaguila.logging.logger.requests')
    def test_logger_some_data(mock_requests):
        """ Log should work """
        mock_requests.post = MagicMock()
        logger.log('a dummy log', data={'some_item': 'some_log'})

    @staticmethod
    @patch('miaguila.logging.logger.requests')
    def test_logger_error_does_nothing(mock_requests):
        """ Log should work """
        mock_post = MagicMock()
        mock_post.side_effect = Exception('post did not work')
        mock_requests.post = mock_post
        logger.log('a dummy log that does not error')
