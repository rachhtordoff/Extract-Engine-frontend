from skeleton_login_frontend import app
from skeleton_login_frontend.views import general, login, extract, user

def register_blueprints(app):
    """
    Adds all blueprint objects into the app.
    """
    app.register_blueprint(general.general)
    app.register_blueprint(login.login)
    app.register_blueprint(extract.extract)
    app.register_blueprint(user.user)

    # All done!
    app.logger.info("Blueprints registered")
