import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
# NOTE: Nearly all comments are stolen/modified from
# https://flask.palletsprojects.com/en/2.1.x/tutorial/database/.


# First thing to do when working with databases: create a connection to it.
# Any queries or operations performed on the database will be performed
# using this connection, and the connection will close after the work is done.

# The connection is created at some point when handling a request,
# and it is closed before the response to the request is sent.


# ############### #
# GET_DB() NOTES: #
# ############### #
# 'g' is a special object that is unique for each request.
# It is used to store data that might be accessed by multiple functions
# during the request.
# The connection is stored and reused instead of creating a new connection
# if 'get_db()' is called a second time in the same request.

# 'sqlite3.connect()' establishes a connection to the file pointed at by
# the DATABASE configuration key.

# 'current_app' is another special object, it points to the Flask application
# that is handling the request.
# (Because 'get_db()' will be called when the application has been created
# and is handling a request, 'current_app' can be used.)

# 'sqlite3.Row' tells the connection to return the rows that behave like dicts.
# This allows accessing of columns by name.
def get_db():
    """
    Called when the application has been created and is handling a request.

    Returns: a Connection object to the database
    """
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


def init_db():
    """
    Connects to database and executes commands from 'schema.sql',
    which creates fresh 'user' and 'post' tables.
    """
    # get a database connection and use it to execute commands from schema.sql.
    db = get_db()

    # 'open_resource' opens a file RELATIVE to the 'flaskr' package.
    # This is useful because schema.sql's location won't necessarily be known
    # when deploying.
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# 'click.command()' defines a command line command called init-db
# that calls the init_db function and shows a success message to the user.
@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Clear the existing data and create new tables.
    """
    init_db()
    click.echo('Initialized the database.')


# The 'close_db()' and 'init_db_command()' functions need to be registered with
# the application instance, or else they won't be used by the application.
# HOWEVER, we are using a factory function to create the app (create_app()),
# an application instance isn't available when writing the functions.
# Instead, have a  function take an app instance and do the registration.

def init_app(app):
    # tell flask to call 'close_db' when cleaning up after returning a response
    app.teardown_appcontext(close_db)
    # add new command that can be called with the flask command
    app.cli.add_command(init_db_command)
