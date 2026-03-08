import os
from flask import Flask
from flask_babel import Babel
from flask_socketio import SocketIO
from .config import Config

# Extensions
babel = Babel()
socketio = SocketIO()

class OrionClient:
    def __init__(self, app=None):
        self.client = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        from .fiware import OrionClient as Client
        self.client = Client(app.config['ORION_BASE_URL'])
        app.orion_client = self.client

# Extensions
babel = Babel()
socketio = SocketIO()
orion = None  # Placeholder

def create_app(config_class=Config):
    global orion
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    babel.init_app(app)

    def get_locale():
        # Priority: query param > session > cookie > Accept-Language > default
        from flask import request, session
        locale = request.args.get('lang')
        if locale:
            session['lang'] = locale
            return locale

        locale = session.get('lang')
        if locale:
            return locale

        return request.accept_languages.best_match(['es', 'en']) or 'es'

    babel.localeselector = get_locale

    # Orion client
    from .fiware import OrionClient
    orion = OrionClient(app.config['ORION_BASE_URL'])
    app.orion_client = orion

    # Determine async mode
    async_mode = os.environ.get('SOCKETIO_ASYNC_MODE', 'threading')
    if async_mode == 'eventlet' and app.debug:
        # Auto-adjust to threading if running via Flask CLI
        async_mode = 'threading'
    socketio.init_app(app, async_mode=async_mode)

    # Bootstrap if enabled
    if app.config['AUTO_BOOTSTRAP']:
        from .fiware import bootstrap
        with app.app_context():
            bootstrap()

    # Register blueprints (to be added later)
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app