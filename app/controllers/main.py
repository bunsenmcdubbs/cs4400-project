from flask import Blueprint, render_template, flash, request, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user

from datetime import datetime

from app.forms import LoginForm, RegisterUserForm, EditUserForm
from app.models import User, Course, Project, Application
from app.search import search

main = Blueprint('main', __name__)

@main.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('.login'))

    results = search()
    return render_template('index.html', results=results)

@main.route('/project/<project_name>', methods=['GET', 'POST'])
@login_required
def view_project(project_name):
    project = Project.find_by_name(project_name)
    if project is None:
        return abort(404)
    has_prev_application = Application.find(
        project_name=project_name,
        student_name=current_user.username,) is not None
    if request.method == 'POST':
        if has_prev_application:
            flash('You can only apply once to each project', 'danger')
        else:
            application = Application(
                project_name=project_name,
                student_name=current_user.username,
                application_date=datetime.now(),
                status='pending',
                is_new_application=True)
            application.save()
            flash('Application successfully submitted!', 'success')
    return render_template(
        'view_project.html',
        project=project,
        has_prev_application=has_prev_application)

@main.route('/course/<course_name>')
@login_required
def view_course(course_name):
    course = Course.find_by_name(course_name)
    if course is None:
        return abort(404)
    return render_template('view_course.html', course=course)

@main.route('/applications')
@login_required
def view_applications():
    my_apps = Application.find(student_name=current_user.username)
    return render_template('view_applications.html', applications=my_apps)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_username(username=form.username.data)
        login_user(user)
        flash('Welcome back %s!'%str(user.username), 'success')
        return redirect(request.args.get('next') or url_for('.home'))
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data
            )
        user.save()
        login_user(user)
        flash('Welcome %s!'%str(user.username), 'success')
        return redirect(request.args.get('next') or url_for('.home'))
    return render_template('register.html', form=form)

@main.route('/me', methods=['GET', 'POST'])
@login_required
def edit_user():
    form = EditUserForm()
    if form.validate_on_submit():
        current_user.year = form.year.data
        current_user.major = form.major.data
        current_user.save()
        flash('Successfully updated user details', 'success')
    elif request.method == 'GET':
        form.year.default = current_user.year
        form.major.default = current_user.major
        form.process()
    return render_template('edit_user.html', form=form)
