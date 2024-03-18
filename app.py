
import os
import random

from flask import Flask, render_template, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

from forms import SignupForm, LoginForm
from models import db, connect_db, User

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///compliments'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")


connect_db(app)


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None



def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.username



def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


# Homepage route


@app.route('/', methods=["GET", "POST"])
def homepage():
    """Show homepage:"""


    if g.user:

        Compliment = ["You're amazing", "Wow! You're so smart", "You look marvelous today", "Good morning, beautiful", "You're so brave", "You're a goood person", "You look like a million bucks", "You're a hardworker", "Coding isn't that hard! You can do it", "You're a gem", "Great Job! You're winning"]

        Rand = random.randint(0, 10)

        return render_template('home.html', comp = Compliment[Rand], user = g.user)

    else:
        
        return redirect('/signup')
    


# User signup route    
    
@app.route('/signup', methods=["GET", "POST"])
def  signup():

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    
    form = SignupForm()

    if form.password.data != form.password2.data:
        flash("Passwords do not match", 'danger')
        return render_template('signup.html', form=form)

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                first_name = form.first_name.data,
                last_name = form.last_name.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already exist", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        flash("Thank you for signing up!", 'success')
        return redirect("/")

    else:
        return render_template('signup.html', form=form)
    

#Login form with bycrpt authentication


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)



# Log Out Routes
@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")


# Secret Message
@app.route('/secret')
def secret():
    """Secret Route"""

    if g.user:

        secret_msg = "Shhh, it's a secret message!"

        return render_template('home.html', comp = secret_msg, user = g.user)
    
    else:
        return redirect("/")
    

# Details Page
    

@app.route('/users/<user_username>')
def details(user_username):

    if g.user:

        return render_template('details.html', user = g.user)





#Permanently delete account

@app.route('/delete', methods=["GET", "POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")



    db.session.delete(g.user)
    db.session.commit()

    flash("Account Successfully Deleted", "success")

    return redirect("/signup")