"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
from flask import abort, request
import insta485


@insta485.app.route('/following/', methods=['POST'])
def post_following():
    """Display / route."""
    # Connect to databaseg
    connection = insta485.model.get_db()
    # Query database
    logname = flask.session.get('username')
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    operation = request.form.get('operation')

    if operation == 'follow':
        logname = flask.session.get('username')
        username = request.form.get('username')
        # EC - if user tries to follow user they already follower, abort 409
        check_follow = connection.execute('''
            SELECT COUNT(*)
            FROM following
            WHERE following.username1 = ? AND following.username2 = ?
        ''', (logname, username,),).fetchone()

        if check_follow['COUNT(*)'] == 1:
            abort(409)

        connection.execute('''
            INSERT INTO following(username1, username2)
            VALUES (?, ?)
        ''', (logname, username,),)

    elif operation == 'unfollow':
        logname = flask.session.get('username')
        username = request.form.get('username')
        # EC - if user tries to follow user they already follower, abort 409
        check_unfollow = connection.execute('''
            SELECT COUNT(*)
            FROM following
            WHERE following.username1 = ? AND following.username2 = ?
        ''', (logname, username,),).fetchone()

        if check_unfollow['COUNT(*)'] == 0:
            abort(409)

        connection.execute('''
            DELETE FROM following
                WHERE username1 = ? AND username2 = ?
            ''', (logname, username))

    target = flask.request.args.get('target', '/')
    return flask.redirect(target)
