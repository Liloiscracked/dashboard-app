from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from app.run import app
from .forms import LoginForm
from .models import User


@app.route('/')
def hello():
    return 'Hello, World!'
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))