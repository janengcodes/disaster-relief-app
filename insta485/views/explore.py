"""
Insta485 user view.

URLs include:
/
"""
import flask
import insta485


@insta485.app.route('/explore/')
def show_explore():
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
    connection = insta485.model.get_db()
    # Query database
    logname = flask.session.get('username')
    # Query database for users that logname does not follow
    not_following = connection.execute(
        "SELECT u.* "
        "FROM users u "
        "WHERE u.username NOT IN ( "
        "   SELECT username2 "
        "   FROM following "
        "   WHERE username1 = ? "
        ") "
        "AND u.username != ? ",
        (logname, logname),).fetchall()
    len_not_following = len(not_following)
    # Add database info to context
    context = {"logname": logname,
               "not_following": not_following,
               "len_not_following": len_not_following}
    return flask.render_template("explore.html", **context)
