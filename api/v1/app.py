#!/usr/bin/python3
"""instance of api app"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import environ


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """terminate current session"""
    storage.close()


@app.errohandlr(404)
def error_404(error):
    """return a json reponse on 404 error"""
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
