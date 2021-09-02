# miaguila_lib

## TO DO

* Fix issue with new relic stats and test
* Move test to 100%
* Make logging async

## Install (PipEnv)

For now, library is publically available via github.

```
pipenv install git+https://git@github.com/MiAguila/miaguila-lib.git#egg=miaguila_lib
```

## Logs

Provides a logger for New Relic.

```
from miaguila.logging.logger import logger
logger.Log(message='something happened', data={'extra_data': 'something else'})
```

## Base Repository

Provides a basic SQL alchemy iterface, most useful as a parent class for business objects.  Underlying declarative_base is also provided.

```
from miaguila.base_repository import BaseRepository, get_session
get_session()
repo = BaseRepository()
BaseRepository.get_by_id(1)
```

### Inheritance Example

```
class UserRepository(BaseRepository):
    """ Repository for User entity """
    def __init__(self, session):
        super().__init__(User, session)

    def get_by_email(self, email):
        """ Search User by email """
        return self.get_queryset().filter_by(email=email).first()
```

### Interfaces

* get_by_id(id_val) -> item
* get_queryset() -> queryset base for transactions
* get_all_paginated(page=1, limit=1, filters={}) -> paginated queryset
* create(item) -> item
* update(id_val, item) -> item
* destroy(id_val) -> item


## Stats

Provides APM integration with New Relic and Kinesis.  If required, underlying Kinesis Service is also provided.

Note that you will need to set environment variables described in config/settings to connect to Kinesis.

```
from miaguila.stats import increment_stat
increment_stat('my_app.something_happened', send_to_newrelic=True, send_to_kinesis=True)
```

## Upgrade

After making changes, bump version in setup.cfg and rebuild distribution.

```
python3 -m pip install --upgrade build
python3 -m build
```

## Tests and Lint

Should run automatically with github actions, all changes should have 100% coverage.

```
pipenv shell
find . -type f | grep '.py$' | xargs pylint --extension-pkg-whitelist='pydantic' --jobs=0
python -m pytest --cov-config=.coveragec --cov=. ./src/ma_lib_tests/
```
