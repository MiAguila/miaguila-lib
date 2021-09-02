"""
Settings using pydantic.
Mostly configured in .env for compatibility with docker.
"""

import os

from pydantic import BaseSettings

class AWSSettings(BaseSettings): # pylint: disable=too-few-public-methods
    """
    For Kinesis
    """
    aws_access_key: str = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key: str = os.getenv('AWS_SECRET_ACCESS_KEY')
    region: str = os.getenv('AWS_REGION')
    kinesis_name: str = os.getenv('KINESIS_NAME')
    kinesis_stream: str = os.getenv('KINESIS_STREAM')

class DatabaseSettings(BaseSettings): # pylint: disable=too-few-public-methods
    """
    For database
    """
    uri: str = os.getenv('DB_URI')

class LoggerSettings(BaseSettings): # pylint: disable=too-few-public-methods
    """
    For new relic
    """
    api_key: str = os.getenv('NEW_RELIC_LICENSE_KEY', '')
    new_relic_url: str = f'https://log-api.newrelic.com/log/v1?Api-Key={api_key}'

class Settings(BaseSettings): # pylint: disable=too-few-public-methods
    """
    All settings
    """
    app_name: str = os.getenv('APP_NAME', '')
    database: DatabaseSettings = DatabaseSettings()
    logger: LoggerSettings = LoggerSettings()
    aws: AWSSettings = AWSSettings()
    default_pagination_limit: int = 20

settings = Settings()
