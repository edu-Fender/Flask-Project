## -- Script inicial do módulo website --
## Não é necessário alterar nada nesse arquivo

from flask import Flask

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey'

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app