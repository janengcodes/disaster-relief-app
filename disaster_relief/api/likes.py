"""REST API for likes."""
import flask
import disaster_relief

from disaster_relief.api.exceptions import AuthException
from disaster_relief.api.exceptions import check_auth


@disaster_relief.app.route('/api/v1/likes/', methods=['POST'])
def api_likes():
    """Likes."""
    logname = check_auth()

    postid = flask.request.args.get("postid", type=int)

    connection = disaster_relief.model.get_db()
    # Post IDs that are out of range should return a 404 error.
    post_id_check = connection.execute('''
        SELECT *
        FROM posts
        WHERE postid = ?
    ''', (postid,)).fetchone()

    if post_id_check is None:
        raise AuthException('Not Found', status_code=404)
    # If the like already exists, return the like object with a 200 response.
    like_exists = connection.execute('''
        SELECT likeid
        FROM likes
        WHERE owner = ?
        AND postid = ?
    ''', (logname, postid,)).fetchone()
    # Check if the like already exists
    already_exists = False
    if like_exists:
        already_exists = True
        likeid = like_exists['likeid']
    if not already_exists:
        # Create one like for a specific post. Return 201 on success. Example:
        connection.execute('''
            INSERT INTO likes (owner, postid)
            VALUES (?, ?)
        ''', (logname, postid))
        # get the likeid for newest like
        new_likeid = connection.execute('''
            SELECT likeid
            FROM likes
            WHERE owner = ?
            AND postid = ?
        ''', (logname, postid,)).fetchone()
        likeid = new_likeid['likeid']
    context = {
        "likeid": likeid,
        "url": "/api/v1/likes/" + str(likeid) + "/"
    }
    if already_exists:
        return flask.jsonify(**context), 200
    return flask.jsonify(**context), 201


@disaster_relief.app.route('/api/v1/likes/<likeid>/', methods=['DELETE'])
def api_likes_delete(likeid):
    """Delete a like."""
    logname = check_auth()
    # Find the like
    connection = disaster_relief.model.get_db()
    like_exists = connection.execute('''
        SELECT COUNT(*)
        FROM likes
        WHERE likeid = ?
    ''', (likeid,)).fetchone()
    # Error checking: If the likeid does not exist, return 404.
    if like_exists['COUNT(*)'] == 0:
        raise AuthException('Not Found', status_code=404)
    # Error checking: If the user does not own the like, return 403
    like_owner = connection.execute('''
        SELECT owner
        FROM likes
        WHERE likeid = ?
    ''', (likeid,)).fetchone()
    if logname != like_owner['owner']:
        raise AuthException('Forbidden', status_code=403)
    # Delete one like. Return 204 on success.
    connection.execute('''
        DELETE FROM likes
        WHERE likeid = ?
    ''', (likeid,))
    response = flask.make_response('', 204)
    return response
