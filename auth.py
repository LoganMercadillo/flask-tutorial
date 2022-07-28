# NOTE:
# A "view function" is the code that you write in order to respond to requests
# to your application.
#
# Flask uses patterns to match an incoming request URL to the view that should
# handle it. The view returns data, and Flask transforms that data into an
# outgoing response.
#
# Flask can also go the other way and generate a URL to a view based on
# the view's name and arguments.
#
# ############################################################################
#
# A "Blueprint" is a way to organize a group of related views and other code
# that respond to a group of related requests.
#
# Rather than registering views and other code directly with an application,
# they are registered with a blueprint.
#
# Then, within the factory function, this blueprint is registered with an
# application after the application is created/declared in the function.
#
# ############################################################################
#
# Flaskr has two blueprints, one for handling authentication functions
# and another for handling blog post functions.
#
# TLDR: THIS IS THE AUTHENTICATION BLUEPRINT.

import functools
from sqlite3 import IntegrityError

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# Create a blueprint named 'auth', defined in __name__ (auth.py),
# and prepends '/auth' to all the URLs associated with this blueprint.
bp = Blueprint('auth', __name__, url_prefix='/auth')


# REGISTER VIEW
# associate URL "/register" with the register view function (register())
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    f'INSERT INTO user (username, password) VALUES (?, ?)',
                    (username, generate_password_hash(password))
                )
                db.commit()
            # db.IntegrityError occurs when username already exists
            except db.IntegrityError:
                error = f'User {username} is already registered.'
            else:
                return redirect(url_for('auth.login'))

        # if validation fails, show user
        flash(error)

    # initial display ('GET' request) or validation error
    return render_template('auth/register.html')


# LOGIN VIEW
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            # session is a dict that stores data across requests.
            # if validation success, store user id in a new session.
            session.clear()
            session['user_id'] = user['id']
            # now that user id is stored in the session, it is available
            # to be used for subsequent requests.
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# At the BEGINNING of each request (for any URL and before any other action),
# if user is logged in then their info should be loaded
# and be made available to other views.
@bp.before_app_request
def load_logged_in_user():
    """
    Check if a user id is stored in session, and if so, stores it in g.user.
    g.user lasts the length of the request.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
