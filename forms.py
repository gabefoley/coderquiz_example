from random import randrange

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, FileField
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
        if not( self.lower <= float(field.data)  <= self.upper):
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

class CheckThreshold(object):
    def __init__(self, answer, incorrect):
        self.answer = answer
        self.incorrect = incorrect
    def __call__(self, form, field):

        if field.data is not None:


            if '.' not in field.data:
                raise ValidationError("Your answer is not to three decimal places")

            elif len(field.data.split('.')[1]) != 3:
                raise ValidationError("Your answer is not to three decimal places")

            if field.data == self.answer:
                return
            elif field.data == self.incorrect:
                raise ValidationError("It looks like you've taken the maximum and minimum scores and divided by two. This isn't correct.")
            else:
                raise ValidationError("That isn't the correct threshold")
                # else:
                #     raise ValidationError('This threshold is not correct')
            # except:
            #     raise ValidationError("That isn't the correct threshold")

class CheckMotifMatches(object):
    def __init__(self, answer, incorrect):
        self.answer = answer
        self.incorrect = incorrect

    def __call__(self, form, field):

        if field.data is not None:
            if field.data == self.answer:
                return
            elif field.data == self.incorrect:
                raise ValidationError("This answer is incorrect. It looks like you only considered one strand")
            else:
                raise ValidationError("This answer is incorrect")


class CheckAccuracyScore(object):
    def __init__(self, sens, spec, accur, wanted):
        scores_dict = {}
        scores_dict[sens] = 'Sensitivity'
        scores_dict[spec] = 'Specificity'
        scores_dict[accur] = 'Accuracy'
        self.scores_dict = scores_dict
        self.wanted = wanted

    def __call__(self, form, field):

        if field.data is not None:

            if '.' not in field.data:
                raise ValidationError("Your answer is not to three decimal places")

            elif len(field.data.split('.')[1]) != 3:
                raise ValidationError("Your answer is not to three decimal places")

            for score in self.scores_dict.keys():
                if field.data == score:
                    if self.scores_dict[field.data] == self.wanted:
                        return
                    else:
                        raise ValidationError('You need to provide the {} score but you have provided the {} score'.format(self.wanted, self.scores_dict[field.data]))

                else:
                    continue
            raise ValidationError('This score is not correct')




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


class BIOL3014Quiz1(FlaskForm):
    q1a = StringField('Q1a) Enter the threshold for the 10 base pair motif. (Enter to three decimal places - if your answer is 4.89367 enter 4.894)',
                      validators=[CheckThreshold('4.936', '2.218'), Optional("Not completed")], filters =[lambda v: None if v == '' else v])
    q1b = StringField('Q1b) Enter the threshold for the 11 base pair motif. (Enter to three decimal places - if your answer is 4.89367 enter 4.894)',
                      validators=[CheckThreshold('4.752', '2.641'), Optional("Not completed")], filters =[lambda v: None if v == '' else v])
    q1c = StringField('Q1c) Enter the threshold for the 12 base pair motif. (Enter to three decimal places - if your answer is 4.89367 enter 4.894)',
                      validators=[CheckThreshold('5.587', '3.387'), Optional("Not completed")], filters =[lambda v: None if v == '' else v])

    q2a = StringField('Q2a) Enter the number of motif matches found for the 10 base pair motif.',
                      validators=[CheckMotifMatches('333', '149'), Optional("Not completed")], filters =[lambda v: None if v == '' else v])
    q2b = StringField('Q2b) Enter the number of motif matches found for the 11 base pair motif.',
                      validators=[CheckMotifMatches('1176', '545'), Optional("Not completed")], filters =[lambda v: None if v == '' else v])
    q2c = StringField('Q2c) Enter the number of motif matches found for the 12 base pair motif.',
                      validators=[CheckMotifMatches('593', '296'), Optional("Not completed")], filters =[lambda v: None if v == '' else v])

    q3a = StringField('Q3a) Enter the sensitivity for the 10 base pair motif. (Enter to three decimal places - if your answer is 4.89367 enter 4.894)',
                      validators=[CheckAccuracyScore('0.756', '0.543', '0.717', 'Sensitivity'),
                                  Optional("Not completed")], filters =[lambda v: None if v == '' else v])
    q3b = StringField('Q3b) Enter the specificity for the 11 base pair motif. (Enter to three decimal places - if your answer is 4.89367 enter 4.894)',
                      validators=[CheckAccuracyScore('0.985', '0.891', '0.968', 'Specificity'),
                                  Optional("Not completed")], filters =[lambda v: None if v == '' else v])
    q3c = StringField('Q3c) Enter the accuracy for the 12 base pair motif. (Enter to three decimal places - if your answer is 4.89367 enter 4.894)',
                      validators=[CheckAccuracyScore('0.786', '0.087', '0.656', 'Accuracy'),
                                  Optional("Not completed")], filters =[lambda v: None if v == '' else v])

    check = SubmitField("Check  answers")

    submit = SubmitField("Submit answers")

class BIOL3014Quiz2(FlaskForm):
	q1 = StringField('Q1) Which of Approach A or B would give you an answer to the scientific enquiry? Enter "A" or "B" ', validators=[CorrectAnswer('B'), Optional("Not completed")], filters=[lambda v: None if v == '' else v])
 
	q2a = StringField('Q2a) What number of DHS sites overlap with at least one Atoh1 peak and overlap with at least one Gli2 peak?', validators=[CorrectAnswer('3697'), Optional("Not completed")], filters=[lambda v: None if v == '' else v])
	q2b = StringField('Q2b) For the DHS sites where both Atoh1 and Gli2 putatively bind, what is the average centre-to-centre distance between the Atoh1 and Gli2 peaks?', validators=[CheckNumberRange(80, 100), Optional("Not completed")], filters=[lambda v: None if v == '' else v]) 
	check = SubmitField("Check answers")
	submit = SubmitField("Submit answers")

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
    records = RadioField('Do you want the latest submission or all submissions?', choices=[('Latest','Latest'),('All','All')])
    submit = SubmitField("Get student's submission")
    #download = SubmitField("Download Question 2 code")
   # download2 = SubmitField("Download Question 3 code")

class SubmissionForm(FlaskForm):
	records = RadioField('Do you want your latest submission or all submissions?', choices=[('Latest','Latest'),('All','All')])
	submit = SubmitField("Get your submission")



