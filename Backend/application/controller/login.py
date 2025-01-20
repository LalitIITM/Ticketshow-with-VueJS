from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from application.data.database import db
from application.data.models import User
from application.data.forms import UserLoginForm, AdminLoginForm, RegistrationForm
from datetime import datetime
from functools import wraps
import bcrypt
from application.controller.login import *

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.is_admin != 1:
            return abort(403)
        return func(*args, **kwargs)
    return decorated_view

def user_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.is_admin == 1:
            return abort(403)
        return func(*args, **kwargs)
    return decorated_view

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    # Login logic
    return render_template('login.html',form=form, now=datetime.now())

@login_bp.route('/login/user', methods=['GET', 'POST'])
def user_login():
    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if not user:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login.register'))

        if not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('login.user_login'))
        
        if user.approved == 0:
            flash('Your registration is not approved , Pls wait', 'error')
            return redirect(url_for('login.user_login'))

        login_user(user)
        return redirect(url_for('routes.user_dashboard'))

    return render_template('user_login.html', form=form, now=datetime.now())

@login_bp.route('/login/admin', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if not user:
            flash('Invalid Username', 'error')
            return redirect(url_for('login.admin_login'))

        if not user.check_password(form.password.data):
            flash('Invalid password', 'error')
            return redirect(url_for('login.admin_login'))

        if user.role != 'admin':
            flash('You do not have permission to access this page', 'error')
            return redirect(url_for('login.admin_login'))

        login_user(user)
        return redirect(url_for('routes.admin_dashboard'))

    return render_template('admin_login.html', form=form, now=datetime.now())

@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        
        user = User(username=form.username.data,  password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('routes.home'))
    return render_template('register.html', title='Register', form=form, now=datetime.now())

@login_bp.route('/admin/register_approval', methods=['GET', 'POST'])
@admin_required

def register_approval():
    if current_user.role != 1:
        print('Unauthorised')
    if current_user.role == 1:
        print('authorised')
    print("register_approval function called")
    # Get all non-admin user registrations that need approval
    unapproved_users = User.query.filter((User.approved == 0) | (User.approved == None)).all()
    
    if request.method == 'POST':
        # Process form submission to approve user registrations
        for user in unapproved_users:
            print(user.username)
            if str(user.id) in request.form:
                # Approve user registration
                #user.approved = 1
                #db.session.commit()
                try:
                    user.approved = 1
                    db.session.commit()
                    flash('User registration approved!','success')
                    
                except Exception as e:
                    db.session.rollback()
                    flash('An error occurred while approving user registrations.', 'error')
            
        return redirect(url_for('routes.admin_dashboard'))
    return render_template('admin_dashboard.html', unapproved_users=unapproved_users, now=datetime.now())


@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))
