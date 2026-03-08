import os
from flask import Flask
from flask_babel import Babel
from flask_socketio import SocketIO
from .config import Config

# Extensions
babel = Babel()
socketio = SocketIO()

def create_app(config_class=Config):
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

    # Determine async mode
    async_mode = os.environ.get('SOCKETIO_ASYNC_MODE', 'threading')
    if async_mode == 'eventlet' and app.debug:
        # Auto-adjust to threading if running via Flask CLI
        async_mode = 'threading'
    socketio.init_app(app, async_mode=async_mode)

    # Register blueprints (to be added later)
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app