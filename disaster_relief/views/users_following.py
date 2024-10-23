"""
disaster_relief user view.

URLs include:
/
"""
import flask
import disaster_relief
from disaster_relief.views.user import check_in_db


@disaster_relief.app.route('/users/<username>/following/')
def show_following(username):
    """Render templates for users/.../following."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    # Connect to databaseg
    connection = disaster_relief.model.get_db()
    # Query database
    logname = flask.session.get('username')
    check_in_db(username, connection)
    following = []
    # query database for followers
    following_query = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 = ?",
        (username,),).fetchall()

    for followee in following_query:
        # username
        # to get user_img_url
        profile_pic = connection.execute('''
            SELECT filename
            FROM users
            WHERE username = ?
        ''', (followee['username2'],)).fetchone()
        # relationship: if logname follows follower
        # query database for whether logname is following username
        # (returns 0 if not following or 1 if following)
        is_following = connection.execute(
            "SELECT COUNT(*) "
            "FROM following "
            "WHERE username1 = ? "
            "AND username2 = ? ",
            (logname, followee['username2']),).fetchone()

        following.append({
            "username": followee['username2'],
            "user_img_url":  profile_pic['filename'],
            "logname_follows_username": is_following['COUNT(*)']
        })

    # Add database info to context
    context = {"username": username, "logname": logname,
               "following": following}
    return flask.render_template("following.html", **context)
