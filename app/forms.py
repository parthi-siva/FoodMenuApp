from flask_wtf import FlaskForm
from wtforms import (StringField,
                    PasswordField,
                    SubmitField,
                    SelectField, IntegerField, validators)
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from wtforms.fields.html5 import DateField
from app.models import Employee, Items, EmplyeeMaster
import datetime
from datetime import date

class LoginForm(FlaskForm):
    username = StringField('Employee ID',
                        validators=[DataRequired(),])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    emp_id = StringField('Employee ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_emp_id(self, emp_id):
        already_user = Employee.query.filter_by(emp_id=emp_id.data).first()
        valid_user = EmplyeeMaster.query.filter_by(employee_id=emp_id.data).first()
        if already_user is not None:
            raise ValidationError('Employee ID already exists.')
        elif valid_user is None:
            raise ValidationError('Please Enter Valid Employee ID.')

class ChoiceMenu(FlaskForm):
    foodoption = SelectField("Menu", validators=[DataRequired()],coerce=int)
    quantity = IntegerField("Quantity",validators=[DataRequired(),validators.NumberRange(min=1, max=10)])
    submit = SubmitField('Order')

class ReportForm(FlaskForm):
    startdate = DateField('Start Date', default=date.today)
    enddate = DateField('End Date', default=date.today)
    submit = SubmitField('Report')

    def validate_on_submit(self):
        result = super(ReportForm, self).validate()
        if (self.startdate.data > self.enddate.data):
            return False
        else:
            return result
