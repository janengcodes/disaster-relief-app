"""
disaster_relief accounts_ (main) view.

URLs include:
/
"""
import uuid
import os
import hashlib
import flask
from flask import request, abort
import disaster_relief


@disaster_relief.app.route('/accounts/', methods=['POST'])
def post_account():
    """Display /accounts/ route."""
    operation = request.form.get('operation')
    if operation == 'create':
        create()
    elif operation == 'delete':
        delete()
    elif operation == 'edit_account':
        edit_account()
    elif operation == 'update_password':
        update_password()
    elif operation == 'login':
        login()
    target = flask.request.args.get('target', '/')
    return flask.redirect(target)


def create():
    """Create a new user."""
    connection = disaster_relief.model.get_db()
    # Handle the login form submission
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('edit'))
    username = request.form.get('username')
    password = request.form.get('password')
    fullname = request.form.get('fullname')
    email = request.form.get('email')

    # Check if username already exists in database
    check_username = connection.execute('''
        SELECT COUNT(*)
        FROM users
        WHERE users.username = ?
    ''', (username,)).fetchall()
    if check_username[0]['COUNT(*)'] == 1:
        abort(409)

    # set session cookies
    # maybe move up
    flask.session['username'] = username

    # Check if any of fields are empty --> abort 404
    if len(username) == 0 or len(password) == 0:
        abort(404)
    if len(fullname) == 0 or len(email) == 0:
        abort(404)

    hash_obj = hashlib.new('sha512')
    salt = uuid.uuid4().hex
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_db_string = "$".join(['sha512', salt, hash_obj.hexdigest()])


    # Add to database
    connection.execute('''
        INSERT INTO users(username, password, fullname, email)
        VALUES (?, ?, ?, ?)
    ''', (username, password_db_string, fullname, email))

    return flask.redirect(flask.request.args.get('target', '/'))


def delete():
    """Delete a user."""
    connection = disaster_relief.model.get_db()
    # EC - If the user is not logged in, abort(403).
    if 'username' not in flask.session:
        abort(403)
    logname = flask.session.get('username')

    # delete old posts
    old_posts = connection.execute('''
            SELECT filename
            FROM posts
            WHERE posts.owner = ?
        ''', (logname,),).fetchall()

    for old_post in old_posts:
        path = disaster_relief.app.config["UPLOAD_FOLDER"]/old_post['filename']
        os.remove(path)
    connection.execute('''
        DELETE FROM users
        WHERE username = ?
    ''', (logname,))

    flask.session.clear()
    target = flask.request.args.get('target', '/')
    return flask.redirect(target)


def login():
    """Login a user."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    connection = disaster_relief.model.get_db()
    # Handle the login form submission
    username = request.form.get('username')
    password = request.form.get('password')

    # If the username or password fields are empty, abort(400).
    if len(username) == 0 or len(password) == 0:
        abort(400)

    # If username and password authentication fails, abort(403).

    # username authentification
    username_check = connection.execute('''
        SELECT COUNT(*)
        FROM users
        WHERE username = ?
    ''', (username,),).fetchone()
    # If username doesn't exist
    if username_check['COUNT(*)'] == 0:
        abort(403)
    # grab salt
    real_password = connection.execute('''
        SELECT password
        FROM users
        WHERE username = ?
    ''', (username,),).fetchone()
    parts = real_password['password'].split('$')
    salt = parts[1]
    algorithm = 'sha512'
    # salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    # if the password in the database doesn't match
    # inputted in the form, abort(403)
    # real_password['password'] is the password in the database
    # password_db_string is the password inputted in the form
    if password_db_string != real_password['password']:
        print(password_db_string, real_password['password'] )
        abort(403)

    # set a session cookie
    flask.session['username'] = username

    target = flask.request.args.get('target', '/')
    return flask.redirect(target)
    # Handle other cases (e.g., invalid login)


def update_password():
    """Update a user's password."""
    connection = disaster_relief.model.get_db()
    # If the user is not logged in, abort(403)
    if 'username' not in flask.session:
        abort(403)
    username = flask.session.get('username')
    password = request.form.get('password')
    new_password1 = request.form.get('new_password1')
    new_password2 = request.form.get('new_password2')
    # If any of the fields are empty, abort 404
    if not password or not new_password1 or not new_password2:
        abort(400)
    # store the passwords
    # If verification fails, abort(403).
    real_password = connection.execute('''
        SELECT password
        FROM users
        WHERE username = ?
    ''', (username,),).fetchone()

    # hash given password
    parts = real_password['password'].split('$')
    # everything btwn dollar sign
    salt = parts[1]

    # trying to hash the password inputted in the form
    hash_obj = hashlib.new('sha512')
    # getting the salted password (based on what was inputted in the form)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    # creating the salted password string (based on the inputted password)
    password_db_string = "$".join(['sha512', salt, hash_obj.hexdigest()])

    # if the password in the database doesn't match
    # inputted in the form, abort(403)
    # real_password['password'] is the password in the database
    # password_db_string is the password inputted in the form
    if password_db_string != real_password['password']:
        abort(403)

    # EC - if any of the above fields are empty, abort(400).
    if not password or not new_password1 or not new_password2:
        abort(404)
    # EC - verify both new passwords match.
    # If verification fails, abort(401).
    if new_password1 != new_password2:
        abort(401)
    # hash the new password
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new('sha512')
    password_salted_new = salt + new_password1
    hash_obj.update(password_salted_new.encode('utf-8'))
    password_hash_new = hash_obj.hexdigest()
    password_db_string_new = "$".join(['sha512', salt, password_hash_new])
    connection.execute('''
            UPDATE users
            SET password = ?
            WHERE username = ?
        ''', (password_db_string_new, username))

    target = flask.request.args.get('target', '/')
    return flask.redirect(target)


def edit_account():
    """Edit a user's account."""
    connection = disaster_relief.model.get_db()
    if 'username' not in flask.session:
        abort(403)

    logname = flask.session.get('username')
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    # If the fullname or email fields are empty, abort(400).

    if len(fullname) == 0 or len(email) == 0:
        abort(400)
    
    connection.execute('''
        UPDATE users
        SET fullname = ?, email = ?
        WHERE username = ?
    ''', (fullname, email, logname,),)

    target = flask.request.args.get('target', '/')
    return flask.redirect(target)
