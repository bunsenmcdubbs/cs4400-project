from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from app.models import (
    Project,
    Course,
)
from app.forms import (
    AddProjectForm,
    AddCourseForm,
)

admin = Blueprint('admin', __name__,)

@admin.route('/')
def home():
    return render_template('admin/index.html')

@admin.route('/add_project', methods=['GET', 'POST'])
def add_project():
    form = AddProjectForm()
    if form.validate_on_submit():
        project = Project(
            name=form.name.data,
            description=form.description.data,
            advisor_name=form.advisor_name.data,
            advisor_email=form.advisor_email.data,
            est_num_students=form.est_num_students.data,
            designation_name=form.designation_name.data,
            categories=form.categories.data,
            requirements=form.requirements.data,
            is_new_project=True,
            )
        project.save()
        return redirect(url_for('.home'))
    return render_template('admin/add_project.html', form=form)

@admin.route('/add_course', methods=['GET', 'POST'])
def add_course():
    form = AddCourseForm()
    if form.validate_on_submit():
        print type(form.course_number.data)
        course = Course(
            course_number=form.course_number.data,
            name=form.name.data,
            instructor=form.instructor.data,
            est_num_students=form.est_num_students.data,
            designation_name=form.designation_name.data,
            categories=form.categories.data,
            is_new_course=True,
            )
        course.save()
        return redirect(url_for('.home'))
    return render_template('admin/add_course.html', form=form)
