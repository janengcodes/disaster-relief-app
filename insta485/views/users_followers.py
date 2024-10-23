"""
Insta485 user view.

URLs include:
/
"""
import flask
import insta485
from insta485.views.user import check_in_db


@insta485.app.route('/users/<username>/followers/')
def show_followers(username):
    """Show Followers Route."""
    connection = insta485.model.get_db()
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    # Query database
    logname = flask.session.get('username')

    # CHECK: access DB -> if username is not in DB --> abort(404)
    check_in_db(username, connection)

    followers = []
    # query database for followers
    follower_query = connection.execute(
        "SELECT username1 "
        "FROM following "
        "WHERE username2 = ?",
        (username,),).fetchall()

    for follower in follower_query:
        # username
        # to get user_img_url
        profile_pic = connection.execute('''
            SELECT filename
            FROM users
            WHERE username = ?
        ''', (follower['username1'],)).fetchone()
        # relationship: if logname follows follower
        # query database for whether logname is following username
        # (returns 0 if not following or 1 if following)
        is_following = connection.execute(
            "SELECT COUNT(*) "
            "FROM following "
            "WHERE username1 = ? "
            "AND username2 = ? ",
            (logname, follower['username1']),).fetchone()

        followers.append({
            "username": follower['username1'],
            "user_img_url": profile_pic['filename'],
            "logname_follows_username": is_following['COUNT(*)']
        })

    # Add database info to context
    context = {"username": username, "logname": logname,
               "followers": followers}
    return flask.render_template("followers.html", **context)
