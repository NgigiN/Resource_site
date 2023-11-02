from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
from flask_login import current_user

class LoginForm(FlaskForm):
    """class for each log in form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """Class for each sign up form."""

    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    admission_number = StringField('Admission', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_Rpt = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('SignUp')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class RepairsForm(FlaskForm):
    """Class for registering repairs."""

    device_brand = StringField('Device Brand', validators=[DataRequired()])
    serial_no = StringField('Serial Number', validators=[DataRequired()])
    issue_type = RadioField('Issue', choices=[(
        'Hardware', 'Hardware'), ('Software', 'Software')],
        validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=0, max=300)])
    submit = SubmitField('Submit')


class SessionForm(FlaskForm):
    """ Class for registering for sessions """

    course_name = StringField('Course', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    phone_number = StringField('Phone Number', validators=[DataRequired()])

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username')
