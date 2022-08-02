import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

# Contains setup functions called fixtures that each test will use.
#
# Tests are in Python modules that start with 'test_',
# and each test function in those modules also starts with 'test_'.
#
# Pytest uses fixtures by matching their function names with the names of
# arguments in the test functions.
#
# For example, the 'test_hello' function takes a 'client' argument.
# Pytest matches that with the 'client' fixture function, calls it, and
# then passes the returned value to the test function.


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


# The 'app' fixture will call the factory and pass 'test_config' to configure
# the application & database for testing instead of using the local dev config.
@pytest.fixture
def app():
    # Create and open a temporary file, returns file descriptor and path to it.
    db_fd, db_path = tempfile.mkstemp()

    # Overrides the database path to point to this temp file instead of the
    # instance folder.
    # 'TESTING" tells the app that it's in test mode.
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # After testing is over, temp file is closed and removed.
    os.close(db_fd)
    os.unlink(db_path)


# Tests will use the client to make requests to the application
# WITHOUT running the server.
@pytest.fixture
def client(app):
    return app.test_client()


# Creates a runner that can call the Click commands registered with the app.
@pytest.fixture
def runner(app):
    return app.test_cli_runner()
