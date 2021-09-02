"""
Test get session
"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from sqlalchemy import Column, Integer, String

from miaguila import base_repository

class TestUser(base_repository.Base): # pylint: disable=too-few-public-methods
    """
    A sample user for testing
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)

class TestBaseRepository(TestCase):
    """
    Test common methods for ORM class
    """

    @patch('miaguila.base_repository.sessionmaker')
    @patch('miaguila.base_repository.create_engine')
    def test_get_session(self, mock_engine, mock_sessionmaker):
        """
        Get session should an iterator with a single DB session
        """
        # should work without erroring regardless of availability of DB
        session = MagicMock()
        session.close = MagicMock()
        mock_engine.return_value = 'db_engine'
        mock_sessionmaker.return_value = MagicMock(return_value = session)
        session_iterator = base_repository.get_session()
        session_result = next(session_iterator)
        # gets one session
        self.assertEqual(
            session_result,
            session,
            msg='The received session was not the expected one'

        )
        # will error
        with self.assertRaises(
            StopIteration,
            msg='Session iterator should be exhausted'
        ):
            next(session_iterator)

    def test_get_queryset(self):
        """ Get queryset ok """
        session = MagicMock()
        session.query = MagicMock(return_value='a queryset')
        repo = base_repository.BaseRepository(i_class=None, session=session)
        self.assertEqual(
            repo.get_queryset(),
            'a queryset',
            msg='a queryset should be returned')

    def test_get_by_id(self):
        """ Get by ID okay """
        session = MagicMock()
        queryset = MagicMock()
        queryset_filter = MagicMock()
        queryset_filter.first = MagicMock(return_value='an item')
        queryset.filter_by = MagicMock(return_value=queryset_filter)
        session.query = MagicMock(return_value=queryset)
        repo = base_repository.BaseRepository(i_class=None, session=session)
        self.assertEqual(
            repo.get_by_id(1),
            'an item',
            msg='an item should be returned')

    def test_all_paginated(self):
        """ Base repository can get paginated sets with filters """
        expected_response = 'a limited query result'
        filters = {
            'email': 'a_value'
        }
        session = MagicMock()
        query = MagicMock()
        filtered_query = MagicMock()
        offset_query = MagicMock()
        limited_query = MagicMock()

        limited_query.all = MagicMock(return_value=expected_response)
        offset_query.limit = MagicMock(return_value=limited_query)
        filtered_query.offset = MagicMock(return_value=offset_query)
        query.filter = MagicMock(return_value=filtered_query)
        session.query = MagicMock(return_value=query)

        response = base_repository.BaseRepository(
            TestUser, session).get_all_paginated(1, 10, filters)
        self.assertEqual(
            expected_response,
            response['records'],
            msg=(
                'The returned response was expected to be equal '
                f'to {expected_response}'
            )
        )

    def test_create_returns_item_with_expected_attribute_assigned(self):
        """ Base repository can create things """
        expected_email = 'someone@example.com'
        item_dict = {
            'email': expected_email
        }
        item = MagicMock()
        item.dict = MagicMock(return_value=item_dict)

        session = MagicMock()
        session.add = MagicMock()
        session.commit = MagicMock()
        session.refresh = MagicMock()
        returned_object = base_repository.BaseRepository(TestUser, session).create(item)
        self.assertEqual(
            expected_email,
            returned_object.email,
            msg=(
                'create() should have returned an object with '
                f'an email attribute equals to {expected_email}'
            )
        )

    def test_update_returns_the_same_object(self):
        """ Base repository can update things """
        item_dict = {
            'email': 'a_value'
        }
        item = MagicMock()
        item.dict = MagicMock(return_value=item_dict)

        query_set = MagicMock()
        query_set.filter_by = MagicMock(return_value={'email': 'old_email'})
        session = MagicMock()
        session.refresh = MagicMock()
        session.query = MagicMock(return_value=query_set)
        response = base_repository.BaseRepository(TestUser, session).update(1, item)
        self.assertEqual(
            response,
            item,
            msg='update() should have returned the same item'
        )

    def test_destroy(self):
        """ Base repository can destroy things """
        expected_response = 'item was deleted'
        deleter = MagicMock()
        deleter.delete = MagicMock(return_value=expected_response)
        query_set = MagicMock()
        query_set.filter_by = MagicMock(return_value=deleter)
        session = MagicMock()
        session.query = MagicMock(return_value=query_set)
        response = base_repository.BaseRepository(TestUser, session).destroy(1)
        self.assertEqual(
            expected_response,
            response,
            msg=(
                'The returned response was expected to be equal '
                f'to {expected_response}'
            )
        )
