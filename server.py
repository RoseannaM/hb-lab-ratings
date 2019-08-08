"""Movie Ratings."""
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, url_for, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""
    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/register", methods=["GET", "POST"])
def register():
    """register new user"""

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        pass_hash = generate_password_hash(password)
        user = User.query.filter_by(email=email).first()
        
        if user is None:
            print('user not found, add')
            user = User(email=email, password=pass_hash)
            db.session.add(user)
            db.session.commit()

        else:
            flash('Please login')
            return redirect("/login")

        return redirect("/")

    return render_template('register.html')


@app.route("/login", methods=["POST", "GET"])
def user_login():
    """add user login """
    
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        pass_hash = check_password_hash(user.password,password)
        
        if pass_hash:
            session["id"] = user.user_id
            flash('You were successfully logged in')
            return redirect("/")

        else:
             flash('wrong password, try again')


    return render_template("/login.html")

@app.route("/logout", methods=["POST", "GET"])
def user_logout():

    """remove user from session"""
    
    session.pop("id", None)
    flash('You were successfully logged out')
    return redirect("/")

    


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
