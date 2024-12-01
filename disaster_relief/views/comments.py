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
    operation = request.form.get('operation')
    postid = request.form.get('postid')
    commentid = request.form.get('commentid')
    text = request.form.get('text')
    connection = disaster_relief.model.get_db()
    if operation == 'create':
        if text != '':
            cur = connection.execute(
                "INSERT INTO comments (owner, text, postid) VALUES (?, ?, ?)",
                (logname, postid, text)
            )
            connection.commit()
        else:
            return abort(400)
    elif operation == 'delete':
        cur = connection.execute(
            "SELECT * FROM comments WHERE commentid = ? AND owner = ?",
            (commentid, logname)
        )
        is_your_comment = cur.fetchone()
        print("owner", is_your_comment)
        if is_your_comment is not None:
            cur = connection.execute(
                "DELETE FROM comments WHERE commentid = ?",
                (commentid,)
            )
            connection.commit()
        else:
            return abort(403)

    target = flask.request.args.get('target', '/')
    return flask.redirect(target)
