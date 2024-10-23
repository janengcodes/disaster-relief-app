"""
Insta485 logout view.

URLs include:
/login/
"""
import flask
import insta485


@insta485.app.route('/accounts/logout/', methods=['POST'])
def logout():
    """
    Display Logout Route: Handles logout by clearing & redirect.

    Route URL: /accounts/logout/
    HTTP Methods: POST
    Parameters: None
    Returns: Redirection to the 'login' route.
    """
    if 'username' in flask.session:
        flask.session.clear()
    return flask.redirect(flask.url_for('login'))
