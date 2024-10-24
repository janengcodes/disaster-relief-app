"""
disaster_relief user view.

URLs include:
/
"""
import flask
import disaster_relief


@disaster_relief.app.route('/resources/')
def show_resources():
    """
    Show Explore: Display explore, showing users that haven't been followed.

    Route URL: /explore/
    HTTP Method: GET

    Parameters:
        None

    Returns:
        - If the user is not logged in, redirects to the 'login' route.
        - Otherwise, displays a list of users that haven't been followed.
    """
    # Connect to databaseg
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    connection = disaster_relief.model.get_db()
    # Query database
    logname = flask.session.get('username')
    # Query database for users that logname does not follow
    # Add database info to context
    context = {"logname": logname}
    return flask.render_template("resources.html", **context)
