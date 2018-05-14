from random import randrange

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, FileField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional, Required

from static.python.phylo import *
from static.python.sequence import Sequence
from models import User

from form_validators import CorrectAnswer, Unique, CheckList, CheckPalindrome




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






class PracticeQuiz(FlaskForm):
    q1 = StringField(
        'Question 1: Type the following word - bioinformatics',
        validators=[CorrectAnswer('bioinformatics'), DataRequired("You haven't answered this yet."),
],
        filters=[lambda v: None if v == '' else v])

    q2 = StringField(
            "Question 2: Type the following four words - cat, hamster, baboon, and armadillo. Separate each word with a"
            " comma. <br><br>Note that you can write them in any order, with any amount of space between then, and even with a "
            "mixture of uppercase and lowercase letters. <br><br> Try typing Hamster, BABOON, cat, ARMadILLo and you "
            "will see that it accepts it as an answer <br><br> Then try typing an incorrect answer, or too many or too few responses",
    validators=[CheckList(
            'cat,hamster,baboon,armadillo'),
            DataRequired("You haven't answered this yet.")],

        filters=[lambda v: None if v == '' else v])

    q3 = StringField("Question 3: Coder Quiz is designed to accept a wide range of answers. Try typing a palindrome in as your answer. A "
                     "palindrome is a phrase that spells the same thing backwards and forwards, for example - "
                     "'Oozy rat in a sanitary zoo' or 'Was it a car or a cat I saw?'. This quiz ignores any punctuation"
                     " but validates any palindrome. Find a palindrome and try it out", validators=[CheckPalindrome(),
                                                                                                    DataRequired(
                                                                                                        "You haven't answered this yet.")],
                     filters=[lambda v: None if v == '' else v])

    check = SubmitField("Check  answers")

    submit = SubmitField("Submit answers")

    questions = ['q1', 'q2', 'q3']


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
                                  choices = [('SubmissionSCIE2100Practical1', 'SCIE2100 Practical 1'),
                                             ('SubmissionSCIE2100Practical2', 'SCIE2100 Practical 2'),
                                             ('SubmissionSCIE2100Practical3', 'SCIE2100 Practical 3'),
                                             ('SubmissionSCIE2100Practical4', 'SCIE2100 Practical 4'),
                                             ('SubmissionSCIE2100Practical5', 'SCIE2100 Practical 5'),

                                             ('SubmissionSCIE2100PracticalAssessment1', ' SCIE2100 Practical Assessment 1'),
                                             ('SubmissionSCIE2100PracticalAssessment2',
                                              ' SCIE2100 Practical Assessment 2'),
                                             ('SubmissionPracticeQuiz', 'Practice Quiz')],
                                  validators = [DataRequired()])
    records = RadioField('Do you want the latest submission or all submissions?',
                         choices=[('Latest', 'Latest'), ('All', 'All')], default='Latest', validators = [DataRequired()])
    submit = SubmitField("Get student's submission")
    # download = SubmitField("Download Question 2 code")
    # download2 = SubmitField("Download Question 3 code")

class MarkingForm(FlaskForm):
    assessment_item = SelectField('Which assessment item do you want?',
                                  choices = [('SubmissionSCIE2100Practical1', 'SCIE2100 Practical 1'),
                                             ('SubmissionSCIE2100Practical2', 'SCIE2100 Practical 2'),
                                             ('SubmissionSCIE2100Practical3', 'SCIE2100 Practical 3'),
                                             ('SubmissionSCIE2100Practical4', 'SCIE2100 Practical 4'),
                                             ('SubmissionSCIE2100Practical5', 'SCIE2100 Practical 5'),

                                             ('SubmissionSCIE2100PracticalAssessment1',
                                              ' SCIE2100 Practical Assessment 1'),
                                             ('SubmissionSCIE2100PracticalAssessment2',
                                              ' SCIE2100 Practical Assessment 2'),

                                             ('SubmissionPracticeQuiz', 'Practice Quiz')],
                                  validators = [DataRequired()])

    submit = SubmitField("Generate marking summary")


class SubmissionForm(FlaskForm):
    assessment_item = SelectField('Which assessment item do you want?',
                                  choices = [('SubmissionSCIE2100Practical1', 'SCIE2100 Practical 1'),
                                             ('SubmissionSCIE2100Practical2', 'SCIE2100 Practical 2'),
                                             ('SubmissionSCIE2100Practical3', 'SCIE2100 Practical 3'),
                                             ('SubmissionSCIE2100Practical4', 'SCIE2100 Practical 4'),
                                             ('SubmissionSCIE2100Practical5', 'SCIE2100 Practical 5'),

                                             ('SubmissionSCIE2100PracticalAssessment1',
                                              ' SCIE2100 Practical Assessment 1'),
                                             ('SubmissionSCIE2100PracticalAssessment2',
                                              ' SCIE2100 Practical Assessment 2'),

                                             ('SubmissionPracticeQuiz', 'Practice Quiz')],
                                  validators = [DataRequired()])
    records = RadioField('Do you want your latest submission or all submissions?',
                         choices=[('Latest', 'Latest'), ('All', 'All')], default='Latest', validators = [DataRequired()])
    submit = SubmitField("Get your submission")


class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])