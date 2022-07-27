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

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# Create a blueprint named 'auth', defined in __name__ (auth.py),
# and prepends '/auth' to all the URLs associated with this blueprint.
bp = Blueprint('auth', __name__, url_prefix='/auth')
