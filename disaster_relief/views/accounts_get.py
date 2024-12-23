"""
disaster_relief accounts_get (main) view.

URLs include:
/
"""

import flask
from flask import abort, render_template
import disaster_relief

disaster_relief.app.secret_key = disaster_relief.app.config['SECRET_KEY']




@disaster_relief.app.route('/accounts/login/', methods=['GET'])
def login():
    """Display the login page."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    return render_template('login.html')


@disaster_relief.app.route('/accounts/create/', methods=['GET'])
def create():
    """Display /accounts/create route."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('edit'))
    return render_template('create.html')


@disaster_relief.app.route('/accounts/delete/', methods=['GET'])
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
    context = {
        "username": username,
    }
    # Query database
    return flask.render_template("delete.html", **context)



@disaster_relief.app.route('/accounts/edit/', methods=['GET'])
def edit():
    """Display /accounts/edit route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    connection = disaster_relief.model.get_db()
    logname = flask.session.get('username')

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
        "fullname": fullname[0]['fullname'],
        "email": email[0]['email']
    }
    # Query database
    return flask.render_template("edit.html", **context)


@disaster_relief.app.route('/accounts/password/', methods=['GET'])
def password():
    """Display /accounts/password route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    username = flask.session.get('username')
    # Render the login form
    context = {
        "username": username
    }
    return flask.render_template("changepassword.html", **context)


@disaster_relief.app.route('/accounts/auth/')
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
