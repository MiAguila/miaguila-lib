""" BaseRepository: Repository pattern ORM """
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_session():
    """
    Used for dependency injection in API.
    """
    engine = create_engine(settings.database.uri)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_local()
    try:
        yield session
    finally:
        session.close()

Base = declarative_base()

class BaseRepository:
    """
    Class with Repository Pattern for all the ORM transactions (Based on Django ORM).
    """
    session: Session = None
    i_class = None
    def __init__(self, i_class, session: Session):
        self.session = session
        self.i_class = i_class

    def get_queryset(self):
        """
        Return the queryset base for all transaction (Use it before all the ORM transactions).
        """
        return self.session.query(self.i_class)

    def get_by_id(self, id_val):
        """
        Search record by ID.
        """
        return self.__get_by_id(id_val).first()

    def get_all_paginated( # pylint: disable=dangerous-default-value
        self,
        page: int = 1,
        limit: int = settings.default_pagination_limit,
        filters: Optional[dict]={}
    ):
        """
        Search records using pagination.
        """
        skip = 0 if page == 1 else page * settings.default_pagination_limit
        query = self.get_queryset()
        for key in filters:
            query = query.filter( getattr(self.i_class, key) == filters[key] )
        query = query.offset(skip).limit(limit)
        return dict(
            records=query.all(),
            current_page= page,
            total_records=query.count(),
        )

    def create(self, item):
        """
        Create record query.
        """
        item = self.i_class(**item.dict())
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def update(self, id_val, item):
        """
        Update record query.
        """
        self.__get_by_id(id_val).update(item.dict())
        self.session.refresh(item)
        return item

    def destroy(self, id_val):
        """
        Destroy record query.
        """
        return self.__get_by_id(id_val).delete()

    def __get_by_id(self, id_val):
        return self.get_queryset().filter_by(id=id_val)
