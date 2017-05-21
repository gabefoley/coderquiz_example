from random import randrange

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional

from static.python.phylo import *
from static.python.sequence import Sequence
from models import User


class CorrectAnswer(object):
    """
    Custom validator for WTForms to check
    if the correct answer was submitted
    """
    def __init__(self, answer):
        self.answer = answer

    def __call__(self, form, field):
        # List of error messages that are selected by random
        error_messages = ['Sorry, that\'s not the correct answer.',
                          'Try that again...',
                          'Incorrect answer.',
                          'Please check this answer...',
                          'Oops! Try again...',
                          'Nope! Sorry... try again!',
                          'No, not quite... try again!',
                          'Hmmm, not exactly right...']
        num = randrange(0, len(error_messages))
        message = error_messages[num]

        if field.data is not None:


          if field.data != self.answer:
              raise ValidationError(message)

class CheckNumberRange(object):

     

    def __init__(self, lower, upper):
      self.lower = lower
      self.upper = upper

    def __call__(self, form, field):

      if field.data is not None:


        if not( self.lower <= int(field.data)  <= self.upper):
          raise ValidationError("Not in correct range")



class CheckAlphabet(object):

  def __call__(self, form, field):

    if field.data is not None:

        valid = False

        invalids = ['B', 'J' 'O', 'Z']

        valids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', '-']

        if any(x in field.data for x in invalids):
            raise ValidationError("Incorrect: Your answer shouldn't contain a B, J, O, or Z")

        if any(x for x in field.data if x not in valids):
            raise ValidationError("Incorrct: Your answer should only contain uppercase alphabetic characters or a gap symbol")


        try:
            seq1 = Sequence(field.data.upper())
            valid = True;
        except:
            pass
        if (valid):
            raise ValidationError("Incorrect: This is a valid sequence")

class CheckNewick(object):

    def __init__(self, answer):
        self.answer = answer
    def __call__(self, form, field):

        if field.data is not None:
            try:
                field.data.replace(" ", "")
                newick = parseNewick(field.data)
                newick.canonise()
                if str(newick) != self.answer:
                    raise ValidationError("This Newick string is not correct.")
            except:
                raise ValidationError("This Newick string is not correct.")

class Unique(object):
    def __init__(self, model, field, message=u'This element already exists.'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)

class SignupForm(FlaskForm):
  first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
  last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
  studentno = StringField('Student number', validators=[DataRequired("Please enter your student number."), Unique(User, User.studentno, message="There is already an account with that student number.")])
  email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address."), Unique(User, User.email, message="There is already an account with that email.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
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
    records = RadioField('Do you want the latest submission or all submissions?', choices=[('Latest','Latest'),('All','All')])
    submit = SubmitField("Get student's submission")
    download = SubmitField("Download Question 2 code")
    download2 = SubmitField("Download Question 3 code")

class SubmissionForm(FlaskForm):
	records = RadioField('Do you want your latest submission or all submissions?', choices=[('Latest','Latest'),('All','All')])
	submit = SubmitField("Get your submission")



