from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

from forms import AddUser
from forms import LoginUser

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

db.drop_all()
db.create_all()

@app.route('/')
def redirect_to_register():
    """redirects to register page"""

    return redirect('/register')

@app.route('/register', methods=["GET",'POST'])
def register_page():
    """form to register user"""

    form = AddUser()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()

        session['username'] = user.username
        return redirect(f'/users/{user.username}')

    return render_template('register.html', form=form)

@app.route('/users/<username>')
def secret_page(username):

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")
    elif session['username'] != username:
        flash("not your account!")
        return redirect(f"/users/{session['username']}")
    else:
        user = User.query.get_or_404(username)
        return render_template('user.html', user=user)

@app.route('/login', methods=["GET",'POST'])
def login_page():
    """form to register user"""

    form = LoginUser()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.login(username=username, password=password)
        
        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Bad name/password"]


    return render_template('login.html', form=form)

@app.route('/logout')
def logout():

    if "username" not in session:
        return redirect('/')

    session.pop('username')
    # session.clear()

    return redirect('/')