"""
Insta485 accounts_ (main) view.

URLs include:
/
"""
import os
import pathlib
import uuid
import flask
from flask import request, abort
import insta485


@insta485.app.route('/posts/', methods=['POST'])
def post_posts():
    """
    Post Posts Route: Handles creating and deleting user posts.

    Route URL: /posts/
    HTTP Method: POST

    Parameters:
        - 'operation' (str): 'create' or 'delete'.
        - 'file' (file): Image file to upload (for 'create' operation).
        - 'postid' (int): ID of the post to delete (for 'delete' operation).

    Returns: Redirects after completing the operation.
    """
    connection = insta485.model.get_db()
    operation = request.form.get('operation')
    username = flask.session.get('username')
    if operation == 'create':
        fileobj = flask.request.files["file"]
        # EC - If a user tries to create a post with an empty file,
        # then abort(400).
        if not fileobj:
            abort(400)
        filename = fileobj.filename
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"
        # Save to disk
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)
        # Add to database
        connection.execute('''
            INSERT INTO posts(filename, owner)
            VALUES (?, ?)
        ''', (uuid_basename, username,))

    elif operation == 'delete':
        # This endpoint only accepts POST requests. Create or delete a post
        # and immediately redirect to URL.
        # Use the operation and postid values from POST response form content.
        postid = request.form.get('postid')
        # If a user tries to delete a post that they do not own,
        # then abort(403).
        check_post = connection.execute('''
            SELECT COUNT(*)
            FROM posts
            WHERE posts.postid = ? AND posts.owner = ?
        ''', (postid, username,),).fetchone()
        if check_post['COUNT(*)'] == 0:
            abort(403)
        # If operation is delete,
        #  delete the image file for postid from the filesystem.
        delete_file = connection.execute('''
            SELECT filename
            FROM posts
            WHERE postid = ?
        ''', (postid,)).fetchone()
        path = insta485.app.config["UPLOAD_FOLDER"]/delete_file['filename']
        os.remove(path)
        # Delete everything in the database related to this post.
        connection.execute('''
            DELETE FROM posts
            WHERE postid = ?
        ''', (postid,))
    target = flask.request.args.get('target', '/')
    # If the value of ?target is not set, redirect to /users/<logname>/.
    if target == '/':
        return flask.redirect(flask.url_for('show_user', username=username))
    return flask.redirect(target)
