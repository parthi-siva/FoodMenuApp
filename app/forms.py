from flask_wtf import FlaskForm
from wtforms import (StringField,
                    PasswordField,
                    SubmitField,
                    SelectField, IntegerField, validators)
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import DateField
from app.models import Employee, Items
import datetime

class LoginForm(FlaskForm):
    username = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Employee.query.filter_by(ename=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Employee.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ChoiceMenu(FlaskForm):
    foodoption = SelectField("Menu", validators=[DataRequired()],coerce=int)
    quantity = IntegerField("Quantity",validators=[DataRequired(),validators.NumberRange(min=1, max=10)])
    submit = SubmitField('Order')

class ReportForm(FlaskForm):
    startdate = DateField('Start Date', format='%d/%m/%Y')
    enddate = DateField('End Date', format='%d/%m/%Y')
    submit = SubmitField('Report')

    def validate_on_submit(self):
            result = super(ReportForm, self).validate()
            if (self.startdate.data>self.enddate.data):
                return False
            else:
                return result
