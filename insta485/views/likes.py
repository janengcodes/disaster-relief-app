"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
from flask import request, abort
# import arrow
import insta485


@insta485.app.route('/likes/', methods=['POST'])
def likes():
    """Handle like functionaliity and redirection."""
    # Handle redirection
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    operation = request.form.get('operation')
    postid = request.form.get('postid')
    connection = insta485.model.get_db()
    logname = flask.session.get('username')
    # If someone tries to like a post they have already
    # liked or unlike a post they have not liked, then abort(409)
    liked = connection.execute('''
            SELECT COUNT(*)
            FROM likes
            WHERE likes.postid = ?
            AND likes.owner = ?
        ''', (postid, logname)).fetchone()
    if operation == 'like':
        if liked['COUNT(*)'] != 0:
            abort(409)
        connection.execute('''
            INSERT INTO likes(owner, postid)
            VALUES (?, ?)
        ''', (logname, postid))
    elif operation == 'unlike':
        if liked['COUNT(*)'] == 0:
            abort(409)
        connection.execute('''
            DELETE FROM likes
            WHERE owner = ? AND postid = ?
        ''', (logname, postid))
    target = flask.request.args.get('target', '/')
    return flask.redirect(target)
