"""REST API for comments."""
from flask import make_response
import flask
import disaster_relief


from disaster_relief.api.exceptions import AuthException
from disaster_relief.api.exceptions import check_auth


@disaster_relief.app.route('/api/v1/comments/', methods=['POST'])
def post_comments():
    """Post comments."""
    logname = check_auth()
    postid = flask.request.args.get("postid", type=int)
    connection = disaster_relief.model.get_db()
    # Post IDs that are out of range should return a 404 error.
    if postid is None:
        raise AuthException('Not Found', status_code=404)
    text = flask.request.json.get('text')
    # Add one comment to a post.
    connection.execute('''
        INSERT INTO comments (owner, postid, text)
        VALUES (?, ?, ?)
    ''', (logname, postid, text))
    # Include the ID of the new comment in the return data.
    new_comment_id = connection.execute('''
                                        SELECT last_insert_rowid()
                                        ''').fetchone()
    new_comment_id = new_comment_id['last_insert_rowid()']
    # Return 201 on success.
    context = {
        "commentid": str(new_comment_id),
        "lognameOwnsThis": True,
        "owner": logname,
        "ownerShowUrl": flask.url_for('show_user', username=logname),
        "text": text,
        "url": "/api/v1/comments/" + str(new_comment_id) + "/"
    }
    return flask.jsonify(**context), 201


@disaster_relief.app.route('/api/v1/comments/<int:commentid>/', methods=['DELETE'])
def delete_comment(commentid):
    """Delete a comment."""
    logname = check_auth()
    connection = disaster_relief.model.get_db()

    comment = connection.execute('''
        SELECT owner
        FROM comments
        WHERE commentid = ?
    ''', (commentid,)).fetchone()

    if comment is None:
        raise AuthException('Not Found', status_code=404)
    if comment['owner'] != logname:
        raise AuthException('Forbidden', status_code=403)

    connection.execute('''
        DELETE
        FROM comments
        WHERE commentid = ?
    ''', (commentid,))

    response = make_response('', 204)
    return response
