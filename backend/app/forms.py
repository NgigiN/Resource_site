from flask_wtf import FlaskForm
from sqlalchemy import Boolean
from wtforms import BooleanField, StringField, PasswordField, SubmitField, RadioField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Regexp
from app.models import User


class LoginForm(FlaskForm):
    """class for each log in form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """Class for each sign up form."""

    firstname = StringField('Firstname', validators=[DataRequired(), Regexp(
        '^[A-Za-z]*$', message='First name must contain only alphabetical characters')])
    lastname = StringField('Lastname', validators=[DataRequired(), Regexp(
        '^[A-Za-z]*$', message='Last name must contain only alphabetical characters')])
    username = StringField('username', validators=[DataRequired()])
    admission_number = StringField('Admission', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(
        min=10, max=10, message='Phone number must be exactly 10 digits')])
    password = PasswordField('Password', validators=[DataRequired()])
    password_Rpt = PasswordField('Repeat Password', validators=[
                                 DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
                'Username already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(
                'Email address already in use. Please use a different one.')


class RepairsForm(FlaskForm):
    """Class for registering repairs."""

    device_brand = StringField('Device Brand', validators=[DataRequired()])
    serial_no = StringField('Serial Number', validators=[DataRequired()])
    issue_type = RadioField('Issue', choices=[('Hardware', 'Hardware'), ('Software', 'Software')],
                            validators=[DataRequired()])
    description = TextAreaField('Description', validators=[
                                DataRequired(), Length(min=1, max=300, message='Description must be between 1 and 300 characters')])
    status = SelectField('Status', choices=[('reported', 'Reported/Received'), ('in_progress', 'In Progress'), ('completed', 'Completed')],
                         validators=[DataRequired()])
    submit = SubmitField('Submit')


class SessionForm(FlaskForm):
    """ Class for registering for sessions """

    course_name = StringField('Course', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[
                        DataRequired(), Email(message='Invalid email address')])
    phone_number = StringField('Phone Number', validators=[DataRequired(),
                                                           Length(min=10, max=10, message='Phone number must be exactly 10 digits')])

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, original_username, username):
        if username.data != original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(
                    'Username already taken. Please choose a different one.')


class AdminForm(FlaskForm):
    username = StringField('Admin Username', validators=[DataRequired()])
    email = StringField('Admin Email', validators=[
                        DataRequired(), Email(message='Invalid email address')])
    password = PasswordField('Admin Password', validators=[DataRequired()])
    submit = SubmitField('Admin Login')
