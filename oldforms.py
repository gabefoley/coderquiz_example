from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, RadioField, FileField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional
from random import randrange
# import sym
from sequence import *
from phylo import *
import re
import sre_constants


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

class CheckRegex(object):


    def __call__(self, form, field):

        if field.data is not None:

            correctSeqs = {'chr7:130602946-130603045', 'chr15:5089967-5090066', 'chr19:23226975-23227074'}
            userSeqs = set()

            regex = field.data

            try:
                tf = re.compile(regex)
                seqs = readFastaFile('chipseq.fa', DNA_Alphabet)
                for seq in seqs:
                    seqstr = ''.join(seq.sequence)
                    m = tf.match(seqstr)
                    if m:
                        userSeqs.add(seq.name)

                if correctSeqs == userSeqs:
                    return
                else:

                    raise ValidationError('Incorrect. Returning %s sequences %s' % (len(userSeqs), "" if len(
                        userSeqs) == 0 else "and they are " + str(userSeqs) if len(
                        userSeqs) < 6 else " and there are too many to list here."))
            except sre_constants.error:
                raise ValidationError("The provided regular expression is not valid. Try checking your brackets.")


class SignupForm(FlaskForm):
  first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
  last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
  studentno = StringField('Student number', validators=[DataRequired("Please enter your student number.")])
  email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
  submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
	studentno = StringField('Student number', validators=[DataRequired("Please enter your student number.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
	submit = SubmitField("Sign in")

class AddressForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired("Please enter an address")])
    submit = SubmitField("Search")

class PracticalAssessmentForm(FlaskForm):
    q1 = StringField('Question 1: Give one example of a sequence which is composed of uppercase letters and does not contain B,J,Z, or O for which the Sequence class could not work out what the alphabet is.', validators=[CheckAlphabet(), Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    q2a = StringField('Question 2A: Which sequence has the greater number of valines? Type either P53_EQUAS or P53_HUMAN.', validators=[CorrectAnswer('P53_HUMAN'), Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    q2b = StringField('Question 2B: Which sequence has the greater number of valines as a proportion of the total protein length? Type either P53_EQUAS or P53_HUMAN.', validators=[CorrectAnswer('P53_EQUAS'), Optional("Not completed")], filters=[lambda v: None if v == '' else v])
    
    q2c = StringField('Question 2C: What percentage of the P53_EQUAS was valine? Enter a percentage to three decimal places (do not include the % sign)', validators=[CorrectAnswer('5.797'), Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    q3 = StringField('Question 3: How many of the sequences in Staphylococcus.fasta have the RAFKPS target sequence?', validators=[CorrectAnswer('17'), Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    q4a = StringField("Question 4A: Paste the aligned mystery_seq1 here (Include only protein symbols and gap characters)", validators=[CorrectAnswer('KFLKVSSLFVATLT-TATLVSSPAANALSSKAMDNHPQQ-SQS-SKQ-QTPKIQKGGNLKPLEQREHAN-V-ILPNNDRHQITDTTNGHY-A--P-VT-YI-Q--VE---APTGTFIASGVVVG-KDTLLTNKHVVDATHG-DPHAL-K---A--F--PS-AINQDNY-PNGGFTAEQ-ITKYSGEGDLAIVKFSPNEQ-NKHIGEVVKPATMSNNAETQV-N-QN-ITVTGYPGDKPVATMWESKGKITY-L-KGEAMQY-DLSTTGGNS-GSPVFNEKNEVIGIHWGGVPNEFNGAVFINE'), Optional()], filters=[lambda v: None if v == '' else v])

    q4b = StringField("Question 4B: Paste the aligned mystery_seq2 here (Include only protein symbols and gap characters)", validators=[CorrectAnswer('EFKKAPKVNVSNLTDNKNFVASE--DKLK-KISD--PSAASKIVDKNFVVPE-SKLGNIVP-EYKEINNRVNVATNNPASQQVD--K-HFVAKGPEVNRFITQNKVNHHFITTQTHYKK-VITSYKSTHV-HKHVNHATDSINKHFIVKPSEAPRYTHPSQSLMINHYFAVPGYHAHKFVTP--GHASIKINHFCVVPQINS-F-KVIPPYG-HNSHRMHVPSFQNNTTAT-HQNAK-VNKAYDYKYFYSYKVVKG-VKKYFSFSQSNGYKIGKPSLNIKN-V-NYQYA-VPS-YSPTNYVPE'), Optional()], filters=[lambda v: None if v == '' else v])
    
   # q4c = FileField('Question 4C: Upload your alignLocal function')

    check = SubmitField("Check  answers")

    submit = SubmitField("Submit answers")


class PracticalAssessment2Form(FlaskForm):
    q1 = StringField(
        'Question 1 [2 Marks]: What is the Newick string that would represent the above phylogenetic tree, including distances?',
    validators=[CheckNewick('(((A:0.1,B:0.2):0.2,C:0.1):0.2,(D:0.3,(E:0.2,F:0.1):0.4):0.3)'), Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    q2 = StringField(
        'Question 2 [3 Marks]: What is the Gamma distance between the two sequences in eh.aln? Your submitted answer should be rounded to three decimal places, e.g. 1.241525 would be 1.242',
        validators=[CorrectAnswer('1.507'), Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    q3 = StringField('Question 3 [5 Marks]: What is the node label for the closest common ancestor for nodes A0A1A8AU08 and G3PS36?',
                     validators=[CorrectAnswer('N_6X5OCZ'), Optional("Not completed")],
                     filters=[lambda v: None if v == '' else v])


    file_upload = FileField('Upload the code for the extended version of calcDistances that you wrote for Question 2', validators=[DataRequired("Please attach your code for Question 2.")])

    file_upload2 = FileField('Upload the code for identifying the common ancestor that you wrote for Question 3', validators=[DataRequired("Please attach your code for Question 3.")])

    check = SubmitField("Check answers")

    submit = SubmitField("Submit answers")

class PracticalAssessment3Form(FlaskForm):
    q1 = StringField('Question 1 [4 Marks]: Submit your predicted secondary structure.', validators=[CorrectAnswer('CCCEEEEEHCHEEEEHCEHCECEEECEEEHCHHEHCECCCECEECHEECECCCHHHEEHCHHHEEHCECHHECEEECHHEHEHECE')], filters=[lambda v: None if v == '' else v])

    q2a = StringField('Question 2A [1 Marks]: Submit the sensitivity of class E to two decimal places.', validators=[
        CorrectAnswer('0.58')],
                     filters=[lambda v: None if v == '' else v])

    q2b = StringField('Question 2B [1 Marks]: Submit the specificity of class E to two decimal places.', validators=[
        CorrectAnswer('0.64')],
                     filters=[lambda v: None if v == '' else v])

    q2_code = FileField('Question 2 Code [2 Marks]: Submit the code you wrote to calculate sensitivity and specificity.', validators=[DataRequired("Please attach your code for Question 2.")],
                     filters=[lambda v: None if v == '' else v])

    q3 = StringField('Question 3 [2 Marks]: Please submit your regular expression. You only need to provide your regular expression, e.g. only paste in something in this format - [AC]C[AT]AT.[AT] ', validators=[CheckRegex()], filters=[lambda v: None if v == '' else v])

    check = SubmitField("Check answers")

    submit = SubmitField("Submit answers")

class QueryForm(FlaskForm):
    studentno = StringField("Enter student number")
    records = RadioField('Do you want the latest submission or all submissions?', choices=[('Latest','Latest'),('All','All')])
    submit = SubmitField("Get student's submission")
    download = SubmitField("Download Question 2 code")
    download2 = SubmitField("Download Question 3 code")

class SubmissionForm(FlaskForm):
	records = RadioField('Do you want your latest submission or all submissions?', choices=[('Latest','Latest'),('All','All')])
	submit = SubmitField("Get your submission")



