"""
Insta485 accounts_get (main) view.

URLs include:
/
"""

import flask
from flask import abort
import insta485

insta485.app.secret_key = insta485.app.config['SECRET_KEY']


@insta485.app.route('/accounts/login/', methods=['GET'])
def login():
    """Display the login page."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    # Render the login form
    return '''
        <form action="/accounts/?target=/" method="post"
        enctype="multipart/form-data">
            <input type="text" name="username"
            required placeholder = "username"/>
            <input type="password" name="password"
            required placeholder = "password"/>
            <input type="submit" value="login"/>
            <input type="hidden" name="operation" value="login"/>
        </form>
    Don't have an account?
    <a href="/accounts/create/">Sign up</a>
    '''


@insta485.app.route('/accounts/create/', methods=['GET'])
def create():
    """Display /accounts/create route."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('edit'))
    # if 'username' in flask.session:
    #     return flask.redirect(flask.url_for('login'))
    # Render the login form
    # http://localhost:8000/accounts/create/accounts/?target=/
    return '''
        <!-- DO NOT CHANGE THIS (aside from styling) -->
        <form action="/accounts/?target=/" method="post"
        enctype="multipart/form-data">
            <input type="file" name="file" required/>
            <input type="text" name="fullname" required
            placeholder="Full Name"/>
            <input type="text" name="username" required
            placeholder="username"/>
            <input type="text" name="email" required
            placeholder="email"/>
            <input type="password" name="password" required
            placeholder="password"/>
            <input type="submit" name="signup" value="sign up"/>
            <input type="hidden" name="operation" value="create"/>
        </form>
        <p>Have an account? <a href="/accounts/login/">Login</a></p>
    '''


@insta485.app.route('/accounts/delete/', methods=['GET'])
def delete():
    """Display /accounts/delete route."""
    # Render the login form
    # If the user is not logged in, abort(403).
    # Delete all post files created by this user.
    # Delete user icon file. Delete all related entries in all tables.
    # Hint: database tables set up properly with
    # primary/foreign key relationships
    # and ON DELETE CASCADE will do this automatically.
    # Upon successful submission, clear the users session,
    # and redirect to URL.
    if 'username' not in flask.session:  # ?
        # abort(403)?
        return flask.redirect(flask.url_for('login'))
    username = flask.session.get('username')
    # Run a unit test for operation: delete.
    return f'''
    <p>{username}</p>
    <form action="/accounts/?target=/accounts/create/"
    method="post" enctype="multipart/form-data">
        <input type="submit" name="delete"
        value="confirm delete account"/>
        <input type="hidden" name="operation" value="delete"/>
    </form>
'''


@insta485.app.route('/accounts/edit/', methods=['GET'])
def edit():
    """Display /accounts/edit route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    connection = insta485.model.get_db()
    logname = flask.session.get('username')
    photo = connection.execute(
            "SELECT f.filename "
            "FROM users f "
            "WHERE f.username = ?",
            (logname,),).fetchall()

    # get user fullname
    fullname = connection.execute(
            "SELECT f.fullname "
            "FROM users f "
            "WHERE f.username = ?",
            (logname,),).fetchall()

    # get email
    email = connection.execute(
            "SELECT f.email "
            "FROM users f "
            "WHERE f.username = ?",
            (logname,),).fetchall()

    context = {
        "logname": logname,
        "photo": photo[0]['filename'],
        "fullname": fullname[0]['fullname'],
        "email": email[0]['email']
    }
    # Query database
    return flask.render_template("edit.html", **context)


@insta485.app.route('/accounts/password/', methods=['GET'])
def password():
    """Display /accounts/password route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    # Render the login form
    return '''
        <form action="/accounts/?target=/accounts/edit/"
        method="post" enctype="multipart/form-data">
        <input type="password" name="password" required
        placeholder="old passy"/>
        <input type="password" name="new_password1" required
        placeholder="new passy" />
        <input type="password" name="new_password2" required
        placeholder="new passy again" />
        <input type="submit" name="update_password" value="submit"/>
        <input type="hidden" name="operation" value="update_password"/>
        </form>
        <a href="/accounts/edit/">Back to edit account</a>
    '''


@insta485.app.route('/accounts/auth/')
def auth():
    """Display /accounts/auth route."""
    # FIX: Return a 200 status code with no content
    # (i.e. an empty response) if the user is logged in.
    # abort(403) if the user is not logged in. This route is
    # only used when you deploy the app to AWS.
    if 'username' not in flask.session:
        abort(403)
    else:
        return '', 200
        # return flask.Response(status=200)
