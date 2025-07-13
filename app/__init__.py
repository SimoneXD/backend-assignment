from flask_cors import CORS
from flask import Flask
from strawberry.flask.views import GraphQLView
from config import Config
from .query import schema

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view("graphql_view", schema=schema, graphiql=True)
    )

    return app
