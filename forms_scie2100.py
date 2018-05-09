from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional
from form_validators import CheckList, CheckAlphabet, CorrectAnswer, CheckNewick, CheckRegex, CheckNumberRange, \
    CheckDomainBoundaries, CheckSCIE2100Practical2SeqPairsCode, CheckSCIE2100Practical2AAPairsCode, \
    CheckSCIE2100Practical2ProbabilityCode, CheckGapPenalty, CompareNumbers, CheckTripletAlignGlobal, \
    CheckPoissonDistance, CheckSelectField
import math, numpy


class SCIE2100Practical1(FlaskForm):
    q1 = StringField(
        'Question 1: List the standard alphabets defined in sym.py (e.g. Bool_Alphabet). Please ensure your spelling is correct and your answers are separated by a comma (,). ',
        validators=[CheckList(
            'Bool_Alphabet, DNA_Alphabet, DNA_Alphabet_wN, RNA_Alphabet, Protein_Alphabet, Protein_Alphabet_wX, DSSP_Alphabet, DSSP3_Alphabet, Protein_Alphabet_wSTOP, RNA_Alphabet_wN'),
            DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q2a = StringField(
        "Question 2A: List the 'special' functions (e.g.  __len__(self)) from the sequence class",
        validators=[CheckList(
            '__len__(self), __str__(self), __iter__(self), __contains__(self, item),__getitem__(self, ndx)'),
            DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q2b = TextAreaField(
        "Question 2B: Provide an example of the use of each function from Question 2A",
        validators=[DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])
    q3a = StringField(
        "Question 3A: How many different identifiers are assocated with the sequences in mystery2.fa? To answer this, submit the first two letters common to the identifiers.",
        validators=[CheckList('XP,NP'),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q3b = StringField(
        "Question 3B: Which databases do the identifiers from Question 3A map to?",
        validators=[DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q4a = StringField(
        "Question 4A: How many entries are in sigpep_at.fa?",
        validators=[CheckNumberRange(1000, 1500),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q4b = StringField(
        "Question 4B: How many entries are in lipmet_at.fa?",
        validators=[CheckNumberRange(70, 100),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q4_code = FileField(
        'Question 4 Code: Submit the code you wrote to answer Question 4B.',
        validators=[DataRequired("Please attach your code for Question 4B.")],
        filters=[lambda v: None if v == '' else v])

    q5 = StringField(
        "Question 5: How many TAG lipases did you find?",
        validators=[CheckNumberRange(2, 10),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q5_code = FileField(
        'Question 5 Code: Submit the code you wrote to answer Question 5.',
        validators=[DataRequired("Please attach your code for Question 5.")],
        filters=[lambda v: None if v == '' else v])

    q6a = TextAreaField(
        "Question 6A: Describe the physico-chemical properties represented by each default colour used in the alignment (including the white/uncoloured amino acids).",
        validators=[DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])
    q6b = TextAreaField(
        "Question 6B: Show your own 'hydrophobic' colour scheme (as a list of affected amino acids)",
        validators=[DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q6c_image = FileField(
        "Question 6C: Upload an image of your GPCR alignment with updated 'hydrophobic' colour scheme",
        validators=[DataRequired("Please attach an image of your GPCR alignment")],
        filters=[lambda v: None if v == '' else v])

    q6d = StringField(
        "Question 6D: Provide the rough boundaries of the fifth transmembrane domain. Enter your boundaries in the following format : 10 - 30",
        validators=[CheckDomainBoundaries(280, 320),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    check = SubmitField("Check  answers")

    submit = SubmitField("Submit answers")

    questions = ['q1', 'q2a', 'q2b', 'q3a', 'q3b', 'q4a', 'q4b', 'q4_code', 'q5', 'q5_code', 'q6a', 'q6b', 'q6c_image',
                 'q6d']


class SCIE2100Practical2(FlaskForm):
    q1a = StringField("Question 1A: Provide the answer to your calculation of e<sub>aa</sub>",
                      validators=[CheckNumberRange(0.0195, 0.0197), DataRequired(
                          "You must supply an answer to each question or you will not pass this Practical")],
                      filters=[lambda v: None if v == '' else v])

    q1b = StringField("Question 1B: Provide the answer to your calculation of e<sub>ab</sub>",
                      validators=[CheckNumberRange(0.0615, 0.0617), DataRequired(
                          "You must supply an answer to each question or you will not pass this Practical")],
                      filters=[lambda v: None if v == '' else v])

    q1c = StringField("Question 1C: Provide the answer to your calculation of s<sub>ab</sub>",
                      validators=[CheckNumberRange(-0.603, -0.601, hint="Make sure you're calculating 2 x log base 2"),
                                  DataRequired(
                                      "You must supply an answer to each question or you will not pass this Practical")],
                      filters=[lambda v: None if v == '' else v])

    q1d = TextAreaField("Question 1D: Provide an explanation for how the calculation of substitution scores works",
                        validators=[DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q2a = StringField(
        "Question 2A: Enter your Python code for calculating seqPairs. This should be submitted to Coder Quiz in the format seqPairs = MY_ANSWER",
        validators=[CheckSCIE2100Practical2SeqPairsCode(190),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q2b = StringField(
        "Question 2B: Enter your Python code for calculating aaPairs. This should be submitted to Coder Quiz in the format aaPairs = MY_ANSWER",
        validators=[CheckSCIE2100Practical2AAPairsCode(19000),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q2c = StringField(
        "Question 2C: Enter your Python code for calculating e<sub>ab</sub>  where a == b . This should be submitted to Coder Quiz in the format eab = MY_ANSWER",
        validators=[CheckSCIE2100Practical2ProbabilityCode(0.027777777777777776, identical=True),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q2d = StringField(
        "Question 2D: Enter your Python code for calculating e<sub>ab</sub> where a!= b. This should be submitted to Coder Quiz in the format eab = MY_ANSWER",
        validators=[CheckSCIE2100Practical2ProbabilityCode(0.09375, identical=False),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q3_code = FileField(
        'Question 3 Code: Submit the code with additional comments describing the traceback process. Don’t submit the '
        'entire functions, just the traceback sections (i.e., the part you completed.',
        validators=[DataRequired("Please attach your code for Question 3.")],
        filters=[lambda v: None if v == '' else v])

    q3b = StringField(
        "Question 3B: Submit the alignment if the gap penalty is set to -8 . To differentiate the two rows of the "
        "alignment separate them by a comma e.g. MADMAN,MAD-AM.",
        validators=[CheckList('THISLINE-,ISALIGNED'),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q3c = StringField(
        "Question 3C: Submit the alignment if the gap penalty is set to -4 . To differentiate the two rows of the "
        "alignment separate them by a comma e.g. MADMAN,MAD-AM.",
        validators=[CheckList('THIS-LI-NE-,--ISALIGNED'),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q4a = TextAreaField("Question 4A: Explain why it took so long for the alignment to be computed",
                        validators=[DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q4b = StringField(
        "Question 4B: If you leave the DNA substitution matrix untouched, what is a biologically sensible gap penalty? ",
        validators=[CheckGapPenalty(),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q4c = TextAreaField("Question 4C: What steps did you take to determine 4B?",
                        validators=[DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q4d = StringField(
        "Question 4D: Given the original DNA substitution matrix and a gap penalty of -5, at what position"
        " is the first ATG codon in reading frame +2 of seqB (JX416721.1)?",
        validators=[CorrectAnswer(["92"]),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    check = SubmitField("Check  answers")

    submit = SubmitField("Submit answers")

    questions = ['q1a', 'q1b', 'q1c', 'q1d', 'q2a', 'q2b', 'q2c', 'q2d', 'q3_code', 'q3b', 'q3c', 'q4a', 'q4b', 'q4c',
                 'q4d']


class SCIE2100Practical3(FlaskForm):
    q1 = StringField(
        "Question 1: Report the time it took to run the tripletAlignGlobal function, and the time to run global "
        "alignment? Enter the times with tripletAlignGlobal first, followed by global alignment and seperated by a "
        "comma, for example 1.04, 2.01",
        validators=[CompareNumbers("greater"),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q2a = SelectField("Question 2A: What is the difference in the time it takes to complete the alignment after doubling the size "
                      "of the sequences?", choices=[('Time did not change considerably', 'Time did not change considerably'),
                                                    ('Time increases by roughly a factor of two (doubled)', 'Time increases by roughly a factor of two (doubled)'),
                                                    ('Time increases by roughly a factor of five', 'Time increases by roughly a factor of five'),
                                                    ('Time increases by roughly a factor of eight', 'Time increases by roughly a factor of eight'),
                                                    ], validators=[CheckSelectField('Time increases by roughly a factor of eight'), DataRequired(
                          "You must supply an answer to each question or you will not pass this Practical")],
                      filters=[lambda v: None if v == '' else v])

    q2b = StringField(
        "Question 2B:  Describe, with code that is runnable in Python, the number of steps involved in completing the score "
        "matrix of tripletAlignGlobal, in terms of the sequence lengths. (Let  N  be the length of each sequence) "
        "(Your answer should follow this format: matrix_size = my_formula",

        validators=[CheckTripletAlignGlobal(9261, 20),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q2c = StringField("Question 2C: Assuming three sequences of length  N=30 took 1 second to align and three "
                        "sequences of length  N=60  OR  2N took 8 seconds to align, how many seconds would it "
                        "take to align three sequences if you double the lengths again, i.e.  N=120  OR  4N base "
                        "pairs long?",
                        validators=[CorrectAnswer(["64", "64 seconds"]),DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q3a = StringField(
        "Question 3A: Use your getConsensus to provide the consensus sequence for the five sequences above.",
        validators=[CorrectAnswer(["AGFDTVT-AISWSLMYLVTNPRVQRKIQ"]),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q3b_code = FileField(
        'Question 3B Code: Submit the code for your implementation of getConsensus.(Copy your getConsensus function to a new file and submit it)',
        validators=[DataRequired("Please attach your code for Question 3B.")],
        filters=[lambda v: None if v == '' else v])



    q3c = StringField(
        "Question 3C: Report the first 3 columns where multiple symbols might have been included in the consensus sequence of the Epoxide Hydrolase alignment .",
        validators=[CheckList('1, 2, 9'),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q4a = StringField(
        "Question 4A: Submit the formula for calculating the Poisson distance in the format dist = my_formula. Your code should be runnable in Python",
        validators=[CheckPoissonDistance(0.35667494393873245, 0.3),
                    DataRequired("You must supply an answer to each question or you will not pass this Practical")],
        filters=[lambda v: None if v == '' else v])

    q4b_code = FileField(
        'Question 4B Code: Submit the calcDistances method with your comments, including code for calculating the Poisson distance.',
        validators=[DataRequired("Please attach your code for Question 4B.")],
        filters=[lambda v: None if v == '' else v])

    q5 = TextAreaField("Question 5: Describe the two groups you saw in your heatmap",
                        validators=[DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    check = SubmitField("Check  answers")

    submit = SubmitField("Submit answers")

    questions = ['q1', 'q2a', 'q2b', 'q2c', 'q3a', 'q3b_code', 'q3c', 'q4a', 'q4b_code', 'q5' ]


class SCIE2100Practical4(FlaskForm):
    q1a_code = FileField(
        'Question 1A Code: Submit your code with comments included',
        validators=[DataRequired("Please attach your code for Question 1A.")],
        filters=[lambda v: None if v == '' else v])

    q1b = StringField("Question 1B: The consensus sequence for mammals",
                        validators=[CorrectAnswer(["AGFDTVTTAISWSLMYLVTNPRVQRKIQEELDAFILETFRHSSFILFGLGKRKCCIGETIGRLEVF"]
                                                  ),DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q1c = StringField("Question 1C: The consensus sequence for fish",
                      validators=[CorrectAnswer(["AGFDTISTALSWSVMYLVAYPEIQERLYQEIKAFILEIFRHSSFMVFGMGKRRCCIGEVIARNEVF",
                                                 "AGFDTVSTALSWSVMYLVAYPEIQERLYQEIKAFILEIFRHSSFMVFGMGKRRCCIGEVIARNEVF"]),
                                  DataRequired("You must supply an answer to each question or you will not pass this "
                                               "Practical")],
                        filters=[lambda v: None if v == '' else v])

    q2a_code = FileField(
        'Question 2A Code: Submit your code with comments included',
        validators=[DataRequired("Please attach your code for Question 2A.")],
        filters=[lambda v: None if v == '' else v])


    q2b = StringField("Question 2B: The number of sequences selected",
                        validators=[CorrectAnswer(["31"]),DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q3a_image = FileField(
        "Question 3A: Upload an image of the MalS tree with tips labeled with the names of the sequences",
        validators=[DataRequired("Please attach an image of your MalS tree")],
        filters=[lambda v: None if v == '' else v])

    q3b_code = FileField(
        'Question 3B Code: Submit the code required to generate a Newick string of the MalS tree where the tips are labeled with the sequence at positions 65-70.',
        validators=[DataRequired("Please attach your code for Question 3B.")],
        filters=[lambda v: None if v == '' else v])

    q4a = StringField("Question 4A: The root sequence from the targeted_reconstruction",
                        validators=[CorrectAnswer(["FTAGLVGDE"]),DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q4b = TextAreaField("Question 4B: A few sentences describing any similarities or differences between the "
                        "reconstructions of the key columns, why it has or hasn't changed and the significance of your "
                        "observations.", validators=[DataRequired("You must supply an answer to each question or you "
                                                                  "will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])


    check = SubmitField("Check  answers")

    submit = SubmitField("Submit answers")

    questions = ['q1a_code', 'q1b', 'q1c', 'q2a_code', 'q2b', 'q3a_image', 'q3b_code', 'q4a', 'q4b']

class SCIE2100PracticalAssessment1(FlaskForm):
    q1 = StringField(
        'Question 1: Give one example of a sequence composed of uppercase letters, that does not contain J, Z, or O, for which the Sequence class could not automatically assign a predefined alphabet.',
        validators=[CheckAlphabet(), Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    q2a = StringField(
        'Question 2A: Which sequence has the greater number of valines? Type either P53_EQUAS or P53_HUMAN.',
        validators=[CorrectAnswer(['P53_HUMAN']), Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    q2b = StringField(
        'Question 2B: Which sequence has the greater number of valines as a proportion of the total protein length? Type either P53_EQUAS or P53_HUMAN.',
        validators=[CorrectAnswer(['P53_EQUAS']), Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    q2c = StringField(
        'Question 2C: What percentage of the P53_EQUAS was valine? Enter a percentage to three decimal places (do not include the % sign)',
        validators=[CorrectAnswer(['5.797']), Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    q3 = StringField('Question 3: How many of the sequences in Staphylococcus.fasta have the RAFKPS target sequence?',
                     validators=[CorrectAnswer(['17']), Optional("Not completed")],
                     filters=[lambda v: None if v == '' else v])

    q4a = StringField(
        "Question 4A: Paste the aligned mystery_seq1 here (Include only protein symbols and gap characters)",
        validators=[CorrectAnswer(
            ['KFLKVSSLFVATLT-TATLVSSPAANALSSKAMDNHPQQ-SQS-SKQ-QTPKIQKGGNLKPLEQREHAN-V-ILPNNDRHQITDTTNGHY-A--P-VT-YI-Q--VE---APTGTFIASGVVVG-KDTLLTNKHVVDATHG-DPHAL-K---A--F--PS-AINQDNY-PNGGFTAEQ-ITKYSGEGDLAIVKFSPNEQ-NKHIGEVVKPATMSNNAETQV-N-QN-ITVTGYPGDKPVATMWESKGKITY-L-KGEAMQY-DLSTTGGNS-GSPVFNEKNEVIGIHWGGVPNEFNGAVFINE']),
            Optional()], filters=[lambda v: None if v == '' else v])

    q4b = StringField(
        "Question 4B: Paste the aligned mystery_seq2 here (Include only protein symbols and gap characters)",
        validators=[CorrectAnswer(
            ['EFKKAPKVNVSNLTDNKNFVASE--DKLK-KISD--PSAASKIVDKNFVVPE-SKLGNIVP-EYKEINNRVNVATNNPASQQVD--K-HFVAKGPEVNRFITQNKVNHHFITTQTHYKK-VITSYKSTHV-HKHVNHATDSINKHFIVKPSEAPRYTHPSQSLMINHYFAVPGYHAHKFVTP--GHASIKINHFCVVPQINS-F-KVIPPYG-HNSHRMHVPSFQNNTTAT-HQNAK-VNKAYDYKYFYSYKVVKG-VKKYFSFSQSNGYKIGKPSLNIKN-V-NYQYA-VPS-YSPTNYVPE']),
            Optional()], filters=[lambda v: None if v == '' else v])

    q4_code = FileField('Question 4C: Upload your alignLocal function',
                        validators=[DataRequired("Please attach your code for Question 4.")])

    check = SubmitField("Check  answers")

    submit = SubmitField("Submit answers")

    questions = ["q1", "q2a", "q2b", "q2c", "q3", "q4a", "q4b", "q4_code"]


class SCIE2100PracticalAssessment2(FlaskForm):
    q1 = StringField(
        'Question 1 [2 Marks]: What is the Newick string that would represent the above phylogenetic tree, including distances?',
        validators=[CheckNewick('(((A:0.1,B:0.2):0.2,C:0.1):0.2,(D:0.3,(E:0.2,F:0.1):0.4):0.3)'),
                    Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    q2 = StringField(
        'Question 2 [3 Marks]: What is the Gamma distance between the two sequences in eh.aln? Your submitted answer should be rounded to three decimal places, e.g. 1.241525 would be 1.242',
        validators=[CorrectAnswer(['1.507']), Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    q3 = StringField(
        'Question 3 [5 Marks]: What is the node label for the closest common ancestor for nodes A0A1A8AU08 and G3PS36?',
        validators=[CorrectAnswer(['N_6X5OCZ']), Optional("Not completed")],
        filters=[lambda v: None if v == '' else v])

    q2_code = FileField('Upload the code for the extended version of calcDistances that you wrote for Question 2',
                            validators=[DataRequired("Please attach your code for Question 2.")])

    q3_code = FileField('Upload the code for identifying the common ancestor that you wrote for Question 3',
                             validators=[DataRequired("Please attach your code for Question 3.")])

    check = SubmitField("Check answers")

    submit = SubmitField("Submit answers")

    questions = ["q1", "q2", "q3", "q2_code", "q3_code"]


class PracticalAssessment3Form(FlaskForm):
    q1 = StringField('Question 1 [4 Marks]: Submit your predicted secondary structure.', validators=[
        CorrectAnswer(['CCCEEEEEHCHEEEEHCEHCECEEECEEEHCHHEHCECCCECEECHEECECCCHHHEEHCHHHEEHCECHHECEEECHHEHEHECE'])],
                     filters=[lambda v: None if v == '' else v])

    q2a = StringField('Question 2A [1 Marks]: Submit the sensitivity of class E to two decimal places.', validators=[
        CorrectAnswer(['0.58'])],
                      filters=[lambda v: None if v == '' else v])

    q2b = StringField('Question 2B [1 Marks]: Submit the specificity of class E to two decimal places.', validators=[
        CorrectAnswer(['0.64'])],
                      filters=[lambda v: None if v == '' else v])

    q2_code = FileField(
        'Question 2 Code [2 Marks]: Submit the code you wrote to calculate sensitivity and specificity.',
        validators=[DataRequired("Please attach your code for Question 2.")],
        filters=[lambda v: None if v == '' else v])

    q3 = StringField(
        'Question 3 [2 Marks]: Please submit your regular expression. You only need to provide your regular expression, e.g. only paste in something in this format - [AC]C[AT]AT.[AT] ',
        validators=[CheckRegex()], filters=[lambda v: None if v == '' else v])

    check = SubmitField("Check answers")

    submit = SubmitField("Submit answers")
