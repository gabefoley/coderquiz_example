from wtforms.validators import ValidationError
from static.python.sequence import Sequence
from static.python.phylo import *

from random import randrange
import re
import sre_constants
from static.python.sequence import *
from static.python.phylo import *
import string


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



class CheckList(object):
    """
    Custom validator for WTForms to check
    if the correct list was submitted
    """

    def __init__(self, correct_list):
        self.correct_list = []
        for item in correct_list.split(","):
            self.correct_list.append(item.upper().strip())

    def __call__(self, form, field):
        if field.data is not None:
            check_list = []
            for item in field.data.split(","):
                check_list.append(item.upper().strip())
            check_set = set(check_list)
            correct_set = set(self.correct_list)

            if (len(check_set) > len(correct_set)):
                raise ValidationError("You have entered too many responses")

            if (len(check_set) < len(correct_set)):
                raise ValidationError("You haven't entered enough responses")

            if (len(check_set - correct_set) > 0):
                # Get the original formatting of the response
                incorrect_responses = []
                for item in field.data.split(","):
                    if (item.upper().strip() in check_set - correct_set):
                        incorrect_responses.append(item.strip())

                raise ValidationError('The following responses are not correct - {}'.format(', '.join([x for x in incorrect_responses])))

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
            if not (self.lower <= float(field.data) <= self.upper):
                raise ValidationError("Not in correct range")


class CheckAlphabet(object):
    def __call__(self, form, field):

        if field.data is not None:

            valid = False

            invalids = ['B', 'J' 'O', 'Z']

            valids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                      'W', 'X', 'Y', '-']

            if any(x in field.data for x in invalids):
                raise ValidationError("Incorrect: Your answer shouldn't contain a B, J, O, or Z")

            if any(x for x in field.data if x not in valids):
                raise ValidationError(
                    "Incorrect: Your answer should only contain uppercase alphabetic characters or a gap symbol")

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
                raise ValidationError(
                    "It looks like you've taken the maximum and minimum scores and divided by two. This isn't correct.")
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
                        raise ValidationError(
                            'You need to provide the {} score but you have provided the {} score'.format(self.wanted,
                                                                                                         self.scores_dict[
                                                                                                             field.data]))

                else:
                    continue
            raise ValidationError('This score is not correct')


class CheckPalindrome(object):
    def __call__(self, form, field):
        if field.data is not None:
            cleanedData = "".join(l for l in field.data.upper() if l not in string.punctuation)
            cleanedData = cleanedData.replace(" ", "")

            if cleanedData == cleanedData[::-1]:
                return
            else:
                raise ValidationError("That is not a palindrome")

class Unique(object):
    def __init__(self, model, field, message=u'This element already exists.'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)