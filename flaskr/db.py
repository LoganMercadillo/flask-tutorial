import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
# 'g' is a special object that is unique for each request.
# It is used to store data that might be accessed by multiple functions
# during the request.
# The connection is stored and reused instead of creating a new connection
# if 'get_db()' is called a second time in the same request.

# 'current_app' is another special object, it points to the Flask application
# that is handling the request.
# Because 'get_db()' will be called when the application has been created
# and is handling a request, 'current_app' can be used.

# 'sqlite3.connect()' establishes a connection to the file pointed at by
# the DATABASE configuration key.

# sqlite3.Row tells the connection to return the rows that behave like dicts.
# this allows accessing of columns by name.


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Checks if a connection was created by checking if 'g.db' was set.
    If the connection exists, it is closed.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()
