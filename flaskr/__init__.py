# contains the application factory.
# tells Python that the flaskr directory should be treated as a package.
import os

from flask import Flask


def create_app(test_config=None):
    """
    Application factory function
    """

    # create and configure the app:
    # __name__ is the name of the current Python module.
    # instance_relative_config=True says that config files are relative to
    # the instance folder. the instance folder is located outside the flaskr
    # package and can hold local data that shouldn't be committed to version
    # control (such as config secrets and the database file).
    app = Flask(__name__, instance_relative_config=True)

    # SECRET_KEY is used by Flask and extensions to keep data safe.
    # It’s set to 'dev' to provide a convenient value during development,
    # but it should be overridden with a random value when deploying.
    # DATABASE is the path where the SQLite database file will be saved.
    # It’s under app.instance_path, which is the path that Flask has chosen for
    # the instance folder.
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing.
        # Overridees default config w/ values from 'config.py' file
        # in the instance folder, if exists.
        # When deploying, can be used to set a real SECRET_KEY.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in.
        # Allows any tests to be configured independently of any dev values.
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, world!'

    # register app with the database
    from . import db
    db.init_app(app)

    # import and register blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    return app
