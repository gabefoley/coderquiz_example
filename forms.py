from random import randrange

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, FileField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional, Required

from static.python.phylo import *
from static.python.sequence import Sequence
from models import User

from form_validators import CorrectAnswer, Unique




class SignupForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
    last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
    studentno = StringField('Student number', validators=[DataRequired("Please enter your student number."),
                                                          Unique(User, User.studentno,
                                                                 message="There is already an account with that student number.")])
    email = StringField('Email', validators=[DataRequired("Please enter your email address."),
                                             Email("Please enter your email address."), Unique(User, User.email,
                                                                                               message="There is already an account with that email.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password."),
                                                     Length(min=6, message="Passwords must be 6 characters or more.")])
    submit = SubmitField('Sign up')








class SimpleQuiz(FlaskForm):
    q1 = StringField(
        'Question 1: Type the word "horse"',
        validators=[CorrectAnswer('horse'), Optional("Not completed")],
        filters=[lambda v: None if v == '' else v])
    q2 = StringField(
        'Question 1: Type the word "cat"',
        validators=[CorrectAnswer('cat'), Optional("Not completed")],
        filters=[lambda v: None if v == '' else v])

    q3 = StringField(
        'Question 1: Type the word "dragon"',
        validators=[CorrectAnswer('dragon'), Optional("Not completed")],
        filters=[lambda v: None if v == '' else v])

    file_upload = FileField(
        'Upload your Python code',
        validators=[DataRequired("Please upload your Python code.")])

    check = SubmitField("Check  answers")

    submit = SubmitField("Submit answers")


class LoginForm(FlaskForm):
    studentno = StringField('Student number', validators=[DataRequired("Please enter your student number.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
    submit = SubmitField("Sign in")


class AddressForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired("Please enter an address")])
    submit = SubmitField("Search")


class QueryForm(FlaskForm):
    studentno = StringField("Enter student number")
    assessment_item = SelectField('Which assessment item do you want?',
                                  choices = [('SubmissionSCIE2100Practical1', 'SCIE2100 Practical 1')],
                                  validators = [DataRequired()])
    records = RadioField('Do you want the latest submission or all submissions?',
                         choices=[('Latest', 'Latest'), ('All', 'All')], default='Latest', validators = [DataRequired()])
    submit = SubmitField("Get student's submission")
    # download = SubmitField("Download Question 2 code")
    # download2 = SubmitField("Download Question 3 code")


class SubmissionForm(FlaskForm):
    assessment_item = SelectField('Which assessment item do you want?',
                                  choices = [('SubmissionSCIE2100Practical1', 'SCIE2100 Practical 1')],
                                  validators = [DataRequired()])
    records = RadioField('Do you want your latest submission or all submissions?',
                         choices=[('Latest', 'Latest'), ('All', 'All')], default='Latest', validators = [DataRequired()])
    submit = SubmitField("Get your submission")



