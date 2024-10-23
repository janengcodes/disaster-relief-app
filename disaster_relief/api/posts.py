"""REST API for posts."""
import flask
import disaster_relief

from disaster_relief.api.exceptions import AuthException
from disaster_relief.api.exceptions import check_auth


@disaster_relief.app.route('/api/v1/posts/')
def get_posts():
    """Get all posts from logged in user or those they follow."""
    # Each post is made by a user which the logged in user follows or
    # belongs to the user
    connection = disaster_relief.model.get_db()
    # If user is logged in, set logname
    logname = check_auth()

    # Get latest postid, to be default if postid_lte not specified in url
    latest_postid = connection.execute('''
        SELECT MAX(postid)
        FROM posts
        WHERE (posts.owner = ? OR posts.owner IN (
            SELECT username2
            FROM following
            WHERE username1 = ?)
        )
    ''', (logname, logname)).fetchone()

    latest_postid = latest_postid['MAX(postid)']
    postid_lte = flask.request.args.get('postid_lte',
                                        default=latest_postid, type=int)

    size = flask.request.args.get("size", default=10, type=int)

    page = flask.request.args.get("page", default=0, type=int)
    json_posts = []
    if latest_postid is None:
        # there are no posts to load
        context = {
            "next": "",
            "results": json_posts,
            "url": "/api/v1/posts/"
        }
        return flask.jsonify(**context)

    if postid_lte < 0 or size <= 0 or page < 0:
        raise AuthException('Bad Request', status_code=400)
    # Get the specificied number of posts from the database
    size_posts = connection.execute('''
        SELECT posts.postid
        FROM posts
        WHERE (posts.postid <= ? AND (posts.owner = ? OR posts.owner IN (
            SELECT username2
            FROM following
            WHERE username1 = ?)))
        ORDER BY posts.postid DESC
        LIMIT ?
        OFFSET ?
    ''', (postid_lte, logname, logname, size, (size * page))).fetchall()
    # [{'postid': 4}, {'postid': 3}]
    filtered_posts = [post['postid'] for post in size_posts]
    # print(filtered_posts)

    for post in filtered_posts:
        # postid = str(post)
        new_post = {"postid": post,
                    "url": ("/api/v1/posts/" + str(post) + "/")}
        json_posts.append(new_post)
    #  if flask.request.query_string:
    #  If there are query parameters, construct the URL without a
    #  question mark
    #     full_url = url + '?' + flask.request.query_string.decode('utf-8')
    # else:
    #     # If there are no query parameters, use the base URL
    #     without a question mark
    #     full_url = url

    if len(json_posts) < size:
        next_str = ""
    else:
        # size=1&page=2&postid_lte=2
        next_str = ("/api/v1/posts/?size=" + str(size) + "&page=" +
                    str(page + 1) + "&postid_lte=" + str(postid_lte))
    if flask.request.query_string:
        url = flask.request.full_path
    else:
        url = "/api/v1/posts/"

    context = {
        "next": next_str,
        "results": json_posts,
        "url": url
    }
    return flask.jsonify(**context)


@disaster_relief.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post(postid_url_slug):
    """Return post on postid."""
    # Post IDs that are out of range should return a 404 error.
    # Select the post from the database
    connection = disaster_relief.model.get_db()
    logname = check_auth()
    post = connection.execute('''
        SELECT *
        FROM posts
        WHERE postid = ?
    ''', (postid_url_slug,)).fetchone()
    # If post doesn't exist, return 404
    if post is None:
        raise AuthException('Not Found', status_code=404)
    likes = connection.execute('''
        SELECT owner, likeid
        FROM likes
        WHERE postid = ?
    ''', (postid_url_slug, )).fetchall()

    logname_liked = False
    logname_like_obj = None
    for like in likes:
        # print("like ", like['likeid'])
        if like['owner'] == logname:
            logname_liked = True
            logname_like_obj = like
            break

    # Select the comments from the database for that postid
    comments = connection.execute('''
        SELECT *
        FROM comments
        WHERE postid = ?
    ''', (postid_url_slug,)).fetchall()

    # Loop through comments and apprend to a list
    json_comments = []
    for comment in comments:
        logname_owns_this = comment['owner'] == logname

        new_comment = {
            "commentid": comment['commentid'],
            "lognameOwnsThis": logname_owns_this,
            "owner": comment['owner'],
            "ownerShowUrl": flask.url_for('show_user',
                                          username=comment['owner']),
            "text": comment['text'],
            "url": "/api/v1/comments/" + str(comment['commentid']) + "/"
        }
        json_comments.append(new_comment)
    owner_img_url = connection.execute('''
        SELECT filename
        FROM users
        WHERE username = ?
    ''', (post['owner'],)).fetchone()

    context = {
        "comments": json_comments,
        "comments_url": "/api/v1/comments/?postid=" + str(postid_url_slug),
        "created": post['created'],
        "imgUrl": "/uploads/" + post['filename'],
        "likes": {
            "lognameLikesThis": logname_liked,
            "numLikes": len(likes),
            "url": f"/api/v1/likes/{str(logname_like_obj['likeid'])}/"
            if logname_liked else None
        },
        "owner": post['owner'],
        "ownerImgUrl": "/uploads/" + owner_img_url['filename'],
        "ownerShowUrl": f"/users/{post['owner']}/",
        "postShowUrl": f"/posts/{postid_url_slug}/",
        "postid": postid_url_slug,
        "url": flask.request.path,
    }
    return flask.jsonify(**context)
