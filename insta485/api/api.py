"""This module provides the API functionality for the Insta485 project.

This module contains classes and functions for interacting
with the API of the Insta485
application. It handles various API endpoints and provides
exceptions for error handling.

"""

import flask
import insta485


@insta485.app.route('/api/v1/')
def get_services():
    """Return list of services."""
    context = {
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)
