"""
disaster_relief user view.

URLs include:
/
"""
import flask
from flask import abort
import disaster_relief


@disaster_relief.app.route('/users/<username>/')
def show_user(username):
    """Render template for users."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))

    connect = disaster_relief.model.get_db()

    # username = "awdeorio"
    check_in_db(username, connect)
    # Query database for posts that owner = username
    posts = connect.execute(
        "SELECT p.* "
        "FROM posts p "
        "WHERE p.owner = ? ",
        (username,),).fetchall()
    # get user fullname
    fullname = connect.execute(
        "SELECT f.fullname "
        "FROM users f "
        "WHERE f.username = ?",
        (username,),).fetchall()


    # query database for whether logname is following username
    logname = flask.session.get('username')

    # Add database info to context
    context = {"username": username, "logname": logname, "posts": posts,
               "fullname": fullname, "total_posts": len(posts)}
    return flask.render_template("user.html", **context)


def check_in_db(username, connection):
    """CHECK: access DB -> if username is not in DB --> abort(404)."""
    if_in_db = connection.execute(
        "SELECT COUNT(*) "
        "FROM users "
        "WHERE username = ? ",
        (username,),).fetchone()

    if if_in_db['COUNT(*)'] != 1:
        abort(404)
