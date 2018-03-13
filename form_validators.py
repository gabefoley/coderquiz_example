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

            correct_seqs = {'chr7:130602946-130603045', 'chr15:5089967-5090066', 'chr19:23226975-23227074'}
            user_seqs = set()

            regex = field.data

            try:
                tf = re.compile(regex)
                seqs = readFastaFile('chipseq.fa', DNA_Alphabet)
                for seq in seqs:
                    seqstr = ''.join(seq.sequence)
                    m = tf.match(seqstr)
                    if m:
                        user_seqs.add(seq.name)

                if correct_seqs == user_seqs:
                    return
                else:

                    raise ValidationError('Incorrect. Returning %s sequences %s' % (len(user_seqs), "" if len(
                        user_seqs) == 0 else "and they are " + str(user_seqs) if len(
                        user_seqs) < 6 else " and there are too many to list here."))
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

            if len(check_set) > len(correct_set):
                raise ValidationError("You have entered too many responses")

            if len(check_set) < len(correct_set):
                raise ValidationError("You haven't entered enough responses")

            if len(check_set - correct_set) > 0:
                # Get the original formatting of the response
                incorrect_responses = []
                for item in field.data.split(","):
                    if item.upper().strip() in check_set - correct_set:
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

            if field.data.strip().upper() != self.answer.strip().upper():
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
                valid = True
            except:
                pass
            if valid:
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
                            'You need to provide the {} score but you have provided the {} score'.format(self.wanted,self.scores_dict[field.data]))

                else:
                    continue
            raise ValidationError('This score is not correct')


class CheckSCIE2100Practical2SeqPairsCode(object):

    def __init__(self, answer):
        self.answer = answer

    def __call__(self, form, field):
        if field.data is not None:
            numSeqs = 20
            columns = 100
            if "=" not in field.data or "seqPairs" not in field.data:
                raise ValidationError("The format of your answer is incorrect. It should start with seqPairs =")
            try:
                seqPairs = eval(field.data.split("=")[1])
                if seqPairs != self.answer:
                    raise ValidationError("This answer is incorrect.")
            except ValidationError:
                raise ValidationError("This answer is incorrect.")
            except NameError:
                raise ValidationError("Make sure you have named your variables correctly")
            except (ValueError, SyntaxError, TypeError) as e:
                raise ValidationError( "There was an error in your code - " + repr(e))






class CheckSCIE2100Practical2AAPairsCode(object):

    def __init__(self, answer):
        self.answer = answer

    def __call__(self, form, field):
        if field.data is not None:
            seqPairs = 190
            columns = 100
            if "=" not in field.data or "aaPairs" not in field.data:
                raise ValidationError("The format of your answer is incorrect. It should start with aaPairs = ")

            try:
                check = eval(field.data.split("=")[1])
                if check != self.answer:
                    raise ValidationError("This answer is incorrect.")
            except ValidationError:
                raise ValidationError("This answer is incorrect.")
            except NameError:
                raise ValidationError("Make sure you have named your variables correctly")
            except (ValueError, SyntaxError, TypeError) as e:
                raise ValidationError( "There was an error in your code - " + repr(e))

class CheckSCIE2100Practical2ProbabilityCode(object):

    def __init__(self, answer, identical):
        self.answer = answer
        self.identical = identical

    def __call__(self, form, field):
        if field.data is not None:
            a = "A"
            b = "L"
            if self.identical:
                p = {"A": 0.14, "L": 0.14}
            else:
                p = {"A": 0.14, "L": 0.22}

            if "=" not in field.data or "eab" not in field.data:
                raise ValidationError("The format of your answer is incorrect. It should start with eab = ")

            elif "[" not in field.data:
                raise ValidationError("Are you indexing correctly?")
            elif "p" not in field.data or "b" not in field.data or "a" not in field.data:
                raise ValidationError("Make sure you're using the correct variable names")

            try:
                check = eval(field.data.split("=")[1])
                if check != self.answer:
                    raise ValidationError("This answer is incorrect.")
            except ValidationError:
                raise ValidationError("This answer is incorrect.")
            except NameError:
                raise ValidationError("Make sure you have named your variables correctly")
            except (ValueError, SyntaxError, TypeError) as e:
                raise ValidationError( "There was an error in your code - " + repr(e))




class CheckPalindrome(object):
    def __call__(self, form, field):
        if field.data is not None:
            cleaned_data = "".join(l for l in field.data.upper() if l not in string.punctuation)
            cleaned_data = cleaned_data.replace(" ", "")

            if cleaned_data == cleaned_data[::-1]:
                return
            else:
                raise ValidationError("That is not a palindrome")


class CheckDomainBoundaries(object):

    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def __call__(self, form, field):

        if field.data is not None:
            try:
                check_lower = float(field.data.split("-")[0])
                check_upper = float(field.data.split("-")[1])

                if check_upper < check_lower:
                    raise ValidationError("The upper boundary must be higher than the lower boundary")

                if check_upper - check_lower < 10:
                    raise ValidationError("That domain is too short")

                if check_upper - check_lower > 30:
                    raise ValidationError("That domain is too long")

            except IndexError:
                raise ValidationError("The format you've entered your answer in is incorrect")

            except ValueError as e:
                if str(e).startswith("could not convert string to float"):
                    raise ValidationError("Make sure you're only entering numbers and the - symbol")
                else:
                    raise ValidationError(e)

            if not (self.lower <= check_lower < check_upper <= self.upper):
                raise ValidationError("These are not the correct domain boundaries")

class CheckGapPenalty(object):

    def __call__(self, form, field):

        if field.data is not None:
            if "." in field.data:
                field.data = field.data.split(".")[0]
            check = int(field.data)
            if check >= 0:
                raise ValidationError("A score of zero or positive will lead to inaccurate, gappy alignments")
            if check == -1 or check == -2:
                raise ValidationError("A score this high would lead to an unusually high number of gaps")
            if check <= -8:
                raise ValidationError("A score this low will force a high number of mismatches in the alignment which is not ideal")


class Unique(object):
    def __init__(self, model, field, message=u'This element already exists.'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)