import sqlite3

import pytest
from flaskr.db import get_db


# Within an application context, 'get_db' should return the same connection
# each time it is called. After the context, the connection should be closed.
def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


# The 'init_db' command should call the 'init_db' function and output a message
def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    # Uses Pytest's 'monkeypatch' fixture to replace the 'init-db' function
    # with one that records that it's been called.
    monkeypatch.setatrr('flaskr.db.init_db', fake_init_db)
    # 'runner' fixture from 'conftest.py' used to call 'init-db' by name.
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
