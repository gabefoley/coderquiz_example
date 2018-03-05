from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, FileField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional
from form_validators import CheckThreshold, CheckMotifMatches, CheckAccuracyScore, CorrectAnswer, CheckNumberRange

class BIOL3014Quiz1(FlaskForm):
    q1a = StringField(
        'Q1a) Enter the threshold for the 10 base pair motif. (Enter to three decimal places - if your answer is 4.89367 enter 4.894)',
        validators=[CheckThreshold('4.936', '2.218'), Optional("Not completed")],
        filters=[lambda v: None if v == '' else v])
    q1b = StringField(
        'Q1b) Enter the threshold for the 11 base pair motif. (Enter to three decimal places - if your answer is 4.89367 enter 4.894)',
        validators=[CheckThreshold('4.752', '2.641'), Optional("Not completed")],
        filters=[lambda v: None if v == '' else v])
    q1c = StringField(
        'Q1c) Enter the threshold for the 12 base pair motif. (Enter to three decimal places - if your answer is 4.89367 enter 4.894)',
        validators=[CheckThreshold('5.587', '3.387'), Optional("Not completed")],
        filters=[lambda v: None if v == '' else v])

    q2a = StringField('Q2a) Enter the number of motif matches found for the 10 base pair motif.',
                      validators=[CheckMotifMatches('333', '149'), Optional("Not completed")],
                      filters=[lambda v: None if v == '' else v])
    q2b = StringField('Q2b) Enter the number of motif matches found for the 11 base pair motif.',
                      validators=[CheckMotifMatches('1176', '545'), Optional("Not completed")],
                      filters=[lambda v: None if v == '' else v])
    q2c = StringField('Q2c) Enter the number of motif matches found for the 12 base pair motif.',
                      validators=[CheckMotifMatches('593', '296'), Optional("Not completed")],
                      filters=[lambda v: None if v == '' else v])

    q3a = StringField(
        'Q3a) Enter the sensitivity for the 10 base pair motif. (Enter to three decimal places - if your answer is 4.89367 enter 4.894)',
        validators=[CheckAccuracyScore('0.756', '0.543', '0.717', 'Sensitivity'),
                    Optional("Not completed")], filters=[lambda v: None if v == '' else v])
    q3b = StringField(
        'Q3b) Enter the specificity for the 11 base pair motif. (Enter to three decimal places - if your answer is 4.89367 enter 4.894)',
        validators=[CheckAccuracyScore('0.985', '0.891', '0.968', 'Specificity'),
                    Optional("Not completed")], filters=[lambda v: None if v == '' else v])
    q3c = StringField(
        'Q3c) Enter the accuracy for the 12 base pair motif. (Enter to three decimal places - if your answer is 4.89367 enter 4.894)',
        validators=[CheckAccuracyScore('0.786', '0.087', '0.656', 'Accuracy'),
                    Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    check = SubmitField("Check  answers")

    submit = SubmitField("Submit answers")


class BIOL3014Quiz2(FlaskForm):
    q1 = StringField(
        'Q1) Which of Approach A or B would give you an answer to the scientific enquiry? Enter "A" or "B" ',
        validators=[CorrectAnswer('B'), Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    q2a = StringField(
        'Q2a) What number of DHS sites overlap with at least one Atoh1 peak and overlap with at least one Gli2 peak?',
        validators=[CorrectAnswer('3697'), Optional("Not completed")], filters=[lambda v: None if v == '' else v])
    q2b = StringField(
        'Q2b) For the DHS sites where both Atoh1 and Gli2 putatively bind, what is the average centre-to-centre distance between the Atoh1 and Gli2 peaks?',
        validators=[CheckNumberRange(80, 100), Optional("Not completed")], filters=[lambda v: None if v == '' else v])
    check = SubmitField("Check answers")
    submit = SubmitField("Submit answers")