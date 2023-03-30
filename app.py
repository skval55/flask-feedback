from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback

from forms import AddUser
from forms import LoginUser, AddFeedback

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)


# db.drop_all()
# db.create_all()

@app.route('/')
def redirect_to_register():
    """redirects to register page"""

    if "username" not in session:
        return redirect("/register")
    else:
        return redirect(f"/users/{session['username']}")


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
def user_page(username):
    """page for current user"""

    if User.authenticate(username):
        return redirect('/')
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
    """logout and clear session"""

    if "username" not in session:
        return redirect('/')

    session.pop('username')
    # session.clear()

    return redirect('/')

@app.route('/users/<username>/delete', methods=['POST'])
def delete(username):
    """delete user from db and clear session"""

    if User.authenticate(username):
        return redirect('/')
    
    session.pop('username')

    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')
    

@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    """form to add feedback"""

    if User.authenticate(username):
        return redirect('/')

    form = AddFeedback()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect('/')
    
    title= 'Add'

    return render_template('add-feedback.html', form=form, title=title)

@app.route('/feedback/<feedback_id>/update', methods=['GET','POST'])
def edit_feedback(feedback_id):
    """form to edit feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)

    if User.authenticate(feedback.username):
        return redirect('/')

    form = AddFeedback()

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()

        return redirect('/')
    
    title = 'Edit'

    return render_template('add-feedback.html', form=form, title=title)

@app.route('/feedback/<feedback_id>/delete', methods=['GET','POST'])
def delete_feedback(feedback_id):
    """delete feedback from db on authorized user"""
    feedback = Feedback.query.get_or_404(feedback_id)

    if User.authenticate(feedback.username):
        return redirect('/')

    db.session.delete(feedback)
    db.session.commit()


    return redirect('/')
    
    
    



