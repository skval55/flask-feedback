
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, PasswordField
from wtforms.validators import InputRequired, Optional, AnyOf, URL, NumberRange

class AddUser(FlaskForm):
    """form for adding a user"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])



class LoginUser(FlaskForm):
    """form for adding a user"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class AddFeedback(FlaskForm):
    """form for adding feedback"""

    title = StringField('Title')
    content = StringField('Content')



# class AddAnimalForm(FlaskForm):
#     """form for adding an animal"""

#     name = StringField("Animal name",
#                        validators=[InputRequired()])
#     species = StringField("Species",
#                        validators=[InputRequired(), AnyOf(["cat", 'dog', 'porcupine'])])
#     photo_url = StringField("Photo URL", validators=[URL(), Optional()])
#     age = IntegerField('Age', validators=[NumberRange(min=0,max=30,message='age out of range')])
#     notes = StringField("Notes")