from flask_cors import CORS
from flask import Flask
from strawberry.flask.views import GraphQLView
from .query import schema

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view("graphql_view", schema=schema, graphiql=True)
    )

    return app
