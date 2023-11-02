from flask import render_template, url_for, flash, redirect, request
from app.forms import LoginForm, RegistrationForm, RepairsForm, SessionForm, EditProfileForm
from flask_login import login_required, logout_user, current_user, login_user
from app import app, db
from app.models import User, Repair, Session
from datetime import datetime


@app.before_request
def before_request():
    """ This function due to its decorator is executed before the view function.
    It takes the time the user logs in the site"""
   
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("landing.html", title="DITA Resource Site")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    """ This is a function logsout the user """
    logout_user()
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', title='Profile Page')

@app.route('/repairs', methods=['GET', 'POST'])
@login_required
def repairs():
    form = RepairsForm()
    if form.validate_on_submit():
        repair = Repair(
                device_brand=form.device_brand.data,
                serial_no=form.serial_no.data,
                issue_type=form.issue_type.data,
                description=form.description.data,
                user_id=current_user.id
                )
        db.session.add(repair)
        db.session.commit()
        flash('Your repair has been successfully submitted')
        return redirect(url_for('home'))
    return render_template('repair.html', title='Repair Registration', form=form)


@app.route('/sessions', methods=['GET', 'POST'])
@login_required
def sessions():
    form = SessionForm()
    if form.validate_on_submit():
        course_name = Session(course=form.course_name.data)
        db.session.add(course)
        db.session.commit()
        flash('Session registered')
        return redirect(url_for('home'))
    return render_template('sessions.html', title='Session Registration', form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
    return render_template('edit_profile.html', title='Edit Profile', form=form)


if __name__ == '__main__':
    app.run(debug=True)
