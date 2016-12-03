from flask_wtf import FlaskForm as Form
from wtforms import (
    TextField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    IntegerField
)
from wtforms import validators

from app.models import User, Year, Major, Category, Designation, Requirement

_coerce_unicode = lambda x: unicode(x) if x != 'None' else None

class LoginForm(Form):
    username = TextField(u'username', validators=[validators.required()])
    password = PasswordField(u'password', validators=[validators.required()])

    def validate(self):
        if not super(LoginForm, self).validate():
            return False
        user = User.find_by_username(self.username.data)
        if not user:
            self.username.errors.append('Invalid username or password')
            return False
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password')
            return False
        return True

class RegisterUserForm(Form):
    username = TextField(u'username', validators=[validators.required()])
    email = TextField(u'email', validators=[validators.required(), validators.email()])
    password = PasswordField(u'password', validators=[validators.required()])

    confirm_password = PasswordField(u'confirm_password', validators=[validators.required()])

    def validate(self):
        if not super(RegisterUserForm, self).validate():
            return False
        if self.password.data != self.confirm_password.data:
            self.password.errors.append('Passwords do not match')
            return False
        user = User.find_by_username(self.username.data)
        if user:
            self.username.errors.append('Username already in use')
            return False
        return True

class EditUserForm(Form):
    major = SelectField(u'major', choices=[(m['name'], m['name']) for m in Major.get_all()], coerce=_coerce_unicode)
    year = SelectField(u'year', choices=[(y['year'], y['name']) for y in Year.get_all()], coerce=lambda x: int(x) if x else None)

    def validate(self):
        # validating with SelectField is hard?
        # if not super(EditUserForm, self).validate():
        #     return False
        return True

class AddProjectForm(Form):
    name = TextField(u'name', validators=[validators.required()])
    description = TextField(u'description', validators=[validators.required()])
    advisor_name = TextField(u'advisor_name', validators=[validators.required()])
    advisor_email = TextField(u'advisor_email', validators=[validators.required(), validators.email()])
    est_num_students = IntegerField(u'est_num_students', validators=[validators.required()])
    designation_name = SelectField(u'designation_name', choices=[(d['name'], d['name']) for d in Designation.get_all()])
    categories = SelectMultipleField(u'categories', choices=[(c['name'], c['name']) for c in Category.get_all()])
    requirement_year = SelectField(u'requirement_year', choices=[(r['requirement_name'], r['requirement_name']) for r in Requirement.get_all_year()], coerce=_coerce_unicode)
    requirement_major = SelectField(u'requirement_major', choices=[(r['requirement_name'], r['requirement_name']) for r in Requirement.get_all_major()], coerce=_coerce_unicode)
    requirement_department = SelectField(u'requirement_department', choices=[(r['requirement_name'], r['requirement_name']) for r in Requirement.get_all_department()], coerce=_coerce_unicode)
    
    def validate(self):
        if not super(AddProjectForm, self).validate():
            return False
        return True

class AddCourseForm(Form):
    course_number = TextField(u'course_number', validators=[validators.required()])
    name = TextField(u'name', validators=[validators.required()])
    instructor = TextField(u'instructor', validators=[validators.required()])
    est_num_students = IntegerField(u'est_num_students', validators=[validators.required()])
    designation_name = SelectField(u'designation_name', choices=[(d['name'], d['name']) for d in Designation.get_all()])
    categories = SelectMultipleField(u'categories', choices=[(c['name'], c['name']) for c in Category.get_all()])

    def validate(self):
        # if not super(AddCourseForm, self).validate():
        #     return False
        return True
