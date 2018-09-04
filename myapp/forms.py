from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import DataRequired, Email

class RegisterForm(FlaskForm):
    name = StringField(u'Your name')
    username = StringField(u'Username', validators=[DataRequired()])
    password = PasswordField(u'Your password', validators=[DataRequired()])
    email = StringField(u'Your email address', validators=[Email()])
    # birthday = DateField(u'Your birthday')
    #
    # a_float = FloatField(u'A floating point number')
    # a_decimal = DecimalField(u'Another floating point number')
    # a_integer = IntegerField(u'An integer')
    #
    # now = DateTimeField(u'Current time',
    #                     description='...for no particular reason')
    #
    # sample_file = FileField(u'Your favorite file')
    #
    # eula = BooleanField(u'I did not read the terms and conditions',
    #                     validators=[DataRequired('You must agree to not agree!')])

    submit = SubmitField(u'Register')

class LoginForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired()])
    password = PasswordField(u'Password', validators=[DataRequired()])
    submit = SubmitField(u'Login')

class PostForm(FlaskForm):
    title = StringField(u'Title', validators=[DataRequired()])
    body = TextAreaField(u'Body', validators=[DataRequired()])
    submit = SubmitField(u'Save')
