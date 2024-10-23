"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import arrow
import insta485
from insta485.views.index import get_post_info


@insta485.app.route('/posts/<postid>/')
def show_post(postid):
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    # Connect to databaseg
    profile = insta485.model.get_db()
    # Query database
    logname = flask.session.get('username')

    # QUERY DATabase with postid
    post = profile.execute(
        "SELECT p.* "
        "FROM posts p "
        "WHERE p.postid = ? ",
        (postid,)).fetchone()
    comments, like_count, profile, liked = \
        get_post_info(post["owner"], logname, postid, profile)
    # Add database info to context
    context = {
        "humanizedTS": arrow.get(post["created"]).humanize(),
        "profile_pic": profile,
        "logname": logname,
        "postid": postid,
        "owner": post["owner"],
        "filename": post["filename"],
        "comments": comments,
        "likeCount": like_count['COUNT(*)'],
        "ifLiked": liked['COUNT(*)']
    }
    return flask.render_template("post.html", **context)
