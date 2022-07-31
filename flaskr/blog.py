from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

# The blog should list all posts, allow logged in users to create posts,
# and allow the author of a post to edit or delete it.
# (no 'url_prefix' --> all views in blog blueprint will be at '/{view}'.)
bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    """Index view shows all posts, most recent first."""
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
