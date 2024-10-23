"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
from flask import abort, send_from_directory
import arrow
import insta485


@insta485.app.route('/uploads/<path:filename>')
def download_file(filename):
    """Upload images."""
    # Static File Permissions
    if 'username' not in flask.session:
        abort(403)
    return send_from_directory(insta485.app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)


@insta485.app.route('/')
def show_index():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    # Connect to databaseg
    connection = insta485.model.get_db()
    # Query database
    logname = flask.session.get('username')
    cur2 = connection.execute(
        "SELECT p.* "
        "FROM posts p "
        "WHERE p.owner = ? "
        "OR p.owner IN ( "
        "   SELECT username2 "
        "   FROM following "
        "   WHERE username1 = ? "
        ") "
        "ORDER BY p.postid DESC",
        (logname, logname)
    )

    posts_query = cur2.fetchall()
    posts = []
    for post in posts_query:
        post_id = post["postid"]
        comments, like_count, profile, liked = \
            get_post_info(post["owner"], logname, post_id, connection)

        posts.append({
            "postid": post_id,
            "owner": post["owner"],
            "profile_pic": profile,
            "filename": post["filename"],
            "humanizedTS": arrow.get(post["created"]).humanize(),
            "comments": comments,
            "likeCount": like_count,
            "ifLiked": liked['COUNT(*)']
        })
    # Add database info to context
    context = {"logname": logname, "posts": posts}
    return flask.render_template("index.html", **context)


def get_post_info(post_owner, logname, post_id, connection):
    """Get post information."""
    comments = connection.execute('''
        SELECT comments.text, comments.owner
        FROM comments
        WHERE comments.postid = ?
        ORDER BY comments.commentid ASC
    ''', (post_id,)).fetchall()

    # Fetch like counts for the current post
    like_count = connection.execute('''
        SELECT COUNT(*)
        FROM likes
        WHERE likes.postid = ?
    ''', (post_id,)).fetchone()

    # to get owner profile pic
    profile = connection.execute('''
        SELECT users.filename
        FROM users
        WHERE users.username = ?
    ''', (post_owner,)).fetchone()

    # get whether logged in user has liked post
    liked = connection.execute('''
        SELECT COUNT(*)
        FROM likes
        WHERE likes.postid = ?
        AND likes.owner = ?
    ''', (post_id, logname)).fetchone()
    return comments, like_count, profile, liked
