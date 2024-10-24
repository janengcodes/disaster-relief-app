"""
disaster_relief user view.

URLs include:
/comments/
"""
import flask
from flask import request, abort
import disaster_relief


@disaster_relief.app.route('/comments/', methods=['POST'])
def comments():
    """
    Comments Route: Handles creating and deleting comments.

    Route URL: /comments/
    HTTP Method: POST

    Parameters:
        - 'operation': The type of operation to perform, create/delete.
        - 'postid': The ID of the post to which the comment belongs.
        - 'commentid': The ID of the comment to be deleted.
        - 'text': The text of the comment to be created.

    Returns:
        - If the user is not logged in, redirects to the 'login' route.
        - If the operation is 'create':
            - Validates the comment text and inserts it into the database.
        - If the operation is 'delete':
            - Checks if the logged-in user is comment owner before deleting.
        - Redirects to the specified target URL after completing the operation.
    """
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    logname = flask.session.get('username')
    print("logname ", logname)
    operation = request.form.get('operation')
    postid = request.form.get('postid')
    commentid = request.form.get('commentid')
    text = request.form.get('text')
    connection = disaster_relief.model.get_db()
    if operation == 'create':
        if len(text) == 0:
            abort(400)
        connection.execute('''
            INSERT INTO comments(owner, text, postid)
            VALUES (?, ?, ?)
        ''', (logname, text, postid))
    elif operation == 'delete':
        commentowner = connection.execute('''
            SELECT comments.owner
            FROM comments
            WHERE commentid = ?
        ''', (commentid,)).fetchone()
        if commentowner['owner'] is None:
            abort(403)
        if commentowner['owner'] != logname:
            abort(403)

        connection.execute('''
            DELETE FROM comments
            WHERE commentid = ?
        ''', (commentid,))
    target = flask.request.args.get('target', '/')
    return flask.redirect(target)
