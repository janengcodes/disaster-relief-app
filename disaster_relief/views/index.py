"""
disaster_relief index (main) view.

URLs include:
/
"""
import flask
from flask import abort, send_from_directory
import arrow
import disaster_relief


@disaster_relief.app.route('/uploads/<path:filename>')
def download_file(filename):
    """Upload images."""
    # Static File Permissions
    if 'username' not in flask.session:
        abort(403)
    return send_from_directory(disaster_relief.app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)


@disaster_relief.app.route('/')
def show_index():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    # Connect to databaseg
    connection = disaster_relief.model.get_db()
    # Query database
    logname = flask.session.get('username')
    cur2 = connection.execute(
        "SELECT p.* "
        "FROM posts p "
        "ORDER BY p.postid DESC"
    )

    posts_query = cur2.fetchall()
    posts = []
    for post in posts_query:
        post_id = post["postid"]
        comments, profile= \
            get_post_info(post["owner"], logname, post_id, connection)

        posts.append({
            "postid": post_id,
            "owner": post["owner"],
            "filename": post["filename"],
            "humanizedTS": arrow.get(post["created"]).humanize(),
            "comments": comments,
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
    # to get owner profile pic
    profile = connection.execute('''
        SELECT users.filename
        FROM users
        WHERE users.username = ?
    ''', (post_owner,)).fetchone()
    return comments, profile
