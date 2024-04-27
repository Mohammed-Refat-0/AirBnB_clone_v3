#!/usr/bin/python3
""" implementation of app_view blueprint for an API """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """"return 'status: OK' response"""

    return jsonify({"status": "OK"})
