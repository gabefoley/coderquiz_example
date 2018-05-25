from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional
from form_validators import CheckList, CheckAlphabet, CorrectAnswer, CheckNewick, CheckRegex, CheckNumberRange, \
    CheckDomainBoundaries, CheckSCIE2100Practical2SeqPairsCode, CheckSCIE2100Practical2AAPairsCode, \
    CheckSCIE2100Practical2ProbabilityCode, CheckGapPenalty, CompareNumbers, CheckTripletAlignGlobal, \
    CheckPoissonDistance, CheckSelectField, CheckSCIE2100Practical5Threshold, CheckSCIE2100Practical5GoTerms, \
    CheckBasedOnDropDown
import os


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

    q4a = StringField(
        'Question 4A: How many cells would the S matrix (in the alignGlobal function) contain when aligning HQ659871.1 and JX416721.1? ',
        validators=[CorrectAnswer(['2,345,868', '2345868']), Optional("Not completed")], filters=[lambda v: None if v == '' else v])

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

class SCIE2100Practical5(FlaskForm):

    q1a = StringField("Question 1A: How many columns did the Abf1 PWM contain?",
                        validators=[CorrectAnswer(["16"]),DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q1b = TextAreaField("Question 1B: What is stored in the instance variable m? (Your response must be more detailed "
                        "than just 'a matrix')", validators=[DataRequired("You must supply an answer to each question "
                                                                          "or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q1c = StringField("Question 1C: What is the log likelihood of seeing the symbol G at position 7?",
                        validators=[CorrectAnswer(["0.11", "+0.11", "+ 0.11", ".11", "+.11", "+ .11"]),DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q2a = StringField("Question 2A: The number of promoter sequences in yeast_promoters.fa.",
                        validators=[CorrectAnswer(["5880"]),DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q2b = StringField("Question 2B: The length of the shortest promoter sequence in yeast_promoters.fa.",
                        validators=[CorrectAnswer(["0", "zero"]),DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q2c = StringField("Question 2C: Report the number of yeast promoter sequences that have length equal to the Abf1 motif or greater.",
                        validators=[CorrectAnswer(["5839"]),DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q2d = TextAreaField("Question 2D: Cite a source that reports the number of expected genes in yeast and whether it matches the number of promoters in the provided file."
                        , validators=[DataRequired("You must supply an answer to each question or you "
                                                                  "will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q3a = StringField("Question 3A: The threshold you have chosen, entered to at least one decimal place",
                        validators=[CheckSCIE2100Practical5Threshold(8.10, 8.5), DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q3b = TextAreaField("Question 3B: A brief description of how you selected this threshold."
                        , validators=[DataRequired("You must supply an answer to each question or you "
                                                                  "will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q4a = StringField("Question 4A: A list of GO terms that have an E-value smaller than 50.0. Submit only the "
                      "identifier (e.g. GO:1234567) and not the full description in a list like this - GO:1234567, GO:7654321",
                        validators=[CheckSCIE2100Practical5GoTerms(['GO:0008152', 'GO:0003674', 'GO:0016021',
                                                                    'GO:0055085', 'GO:0008150', 'GO:0006414',
                                                                    'GO:0055114', 'GO:0016491', 'GO:0006310',
                                                                    'GO:0007059', 'GO:0016779', 'GO:0003887',
                                                                    'GO:0004540', 'GO:0004190', 'GO:0004523',
                                                                    'GO:0015074', 'GO:0003964', 'GO:0006278',
                                                                    'GO:0000943', 'GO:0032196', 'GO:0032197', 'GO:0090501']),DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q4b = TextAreaField("Question 4B: Do any of your enriched GO terms support a known role you've discovered Abf1 to "
                        "play in Saccharomyces cerevisiae?", validators=[DataRequired("You must supply an answer to each question or you "
                                                                  "will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    check = SubmitField("Check  answers")

    submit = SubmitField("Submit answers")

    questions = ['q1a', 'q1b', 'q1c', 'q2a', 'q2b', 'q2c', 'q2d', 'q3a', 'q3b', 'q4a', 'q4b']

class SCIE2100Practical6(FlaskForm):

    q1_code = FileField(
        'Question 1 Code: Submit your code for your function getScoresWithForLoop',
        validators=[DataRequired("Please attach your code for Question 1.")],
        filters=[lambda v: None if v == '' else v])

    q2 = SelectField("Question 2: True or false: the PDB structure corresponding to the provided protein sequence is helical", choices=[('True', 'True'),
                                                    ('False', 'False'),
                                                    ], validators=[CheckSelectField('True'), DataRequired(
                          "You must supply an answer to each question or you will not pass this Practical")],
                      filters=[lambda v: None if v == '' else v])

    q3 = TextAreaField("Question 3: Describe, in your own words, the process of applying the Chou-Fasman prediction "
                       "rules for alpha-helices and beta-strands"
                        , validators=[DataRequired("You must supply an answer to each question or you "
                                                                  "will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q4 = StringField("Question 4: Give your base-line accuracy calculations.",
                        validators=[CorrectAnswer(["0.33", "1/3", "33%", "33", "one third"]),DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q5a1 = SelectField("Question 5A: Select your chosen protein", choices=[('0', '1EVH'),
                                                    ('1', '1WN2'), ('2', '2EEI')
                                                    ], validators=[DataRequired(
                          "You must supply an answer to each question or you will not pass this Practical")],
                      filters=[lambda v: None if v == '' else v])

    q5a2 = StringField("Question 5A: Enter the amino acid sequence for your protein.",
                        validators=[CheckBasedOnDropDown("q5a1", ["SEQSICQARAAVMVYDDANKKWVPAGGSTGFSRVHIYHHTGNNTFRVVGRKIQDHQVVINCAIPKGLKYNQATQTFHQWRDARQVYGLNFGSKEDANVFASAMMHALEVLN", "MFKYKQVIVARADLKLSKGKLAAQVAHGAVTAAFEAYKKKREWFEAWFREGQKKVVVKVESEEELFKLKAEAEKLGLPNALIRDAGLTEIPPGTVTVLAVGPAPEEIVDKVTGNLKLL", "GSSGSSGQPRLCYLVKEGGSYGFSLKTVQGKKGVYMTDITPQGVAMRAGVLADDHLIEVNGENVEDASHEEVVEKVKKSGSRVMFLLVDKETDKRHVEQKSGPSSG"]),DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q5a3 = StringField("Question 5A: Enter the DSSP secondary structure for your protein",
                        validators=[CheckBasedOnDropDown("q5a1", ["CEEEEEEEEEEEEEEECCCCEEEEHHHCCCCEEEEEEEECCCCEEEEEEEECCCCCEEEEEEECCCCCCECCCCCEEEEECCCCEEEEEECCHHHHHHHHHHHHHHHHHHC", "CCCEEEEEEEECCCCCCHHHHHHHHHHHHHHHHHHHHHHCHHHHHHHHHCCCCEEEEEECCHHHHHHHHHHHHHCCCCEEEEECCCCCCCCCCCEEEEEEEEEEHHHHHHHHCCCEEC", "CCCCCCCCCEEEEEECCCCCCCCCEECCCCCCCCEECCCCCCCHHHHHCCCCCEEEEEECCEECCCCCHHHHHHHHHHHCCEEEEEECCCCCCCCCCCCCCCCCCC"]),DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q5a4 = StringField("Question 5A: Enter the predicted secondary structure using the Chou-Fasman algorithm for your protein.",
                        validators=[CheckBasedOnDropDown("q5a1", ["HEEEEEEEEEEEEEEEEEHHHHHHHHCCCCEEEEEEEEEECHEEEEEEEEEEEEEEEEEEEEEEHEEEEEEEEEEEEEEEEEEHHHHHHHHHHHHHHHHHHHHHHHHHHHH", "EEEEEEEEEEEEHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHEEEEEEEEEHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHEEEEEEEEEEEHHHEEEEEEEEEEEEEE", "CCCCCCCEEEEEEEEEEHHEEEEEEEEEEEEEEEEEEEEEEEEEEEEHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHEEEEEEEEEEEHHHHHHHHHHHHCCCC"]),DataRequired(
                            "You must supply an answer to each question or you will not pass this Practical")],
                        filters=[lambda v: None if v == '' else v])

    q5b = StringField("Question 5B: Enter the percent accuracy for alpha-helix predictions for your protein. Enter as a percent to two decimal places, i.e. 0.5438654 would be entered as 54.39%",
                      validators=[CheckBasedOnDropDown("q5a1", [
                          "81.98%",
                          "69.49%",
                          "64.15%"]),
                                  DataRequired(
                                      "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])


    q5c = StringField("Question 5C: Enter the percent accuracy for beta-strand predictions for your protein. Enter as a percent to two decimal places, i.e. 0.5438654 would be entered as 54.39%",
                      validators=[CheckBasedOnDropDown("q5a1", [
                          "70.27%",
                          "73.73%",
                          "61.32%"]),
                                  DataRequired(
                                      "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])



    q5d = StringField("Question 5D: Enter the percent accuracy for both alpha-helix and beta-strand predictions together for your protein. Enter as a percent to two decimal places, i.e. 0.5438654 would be entered as 54.39%",
                      validators=[CheckBasedOnDropDown("q5a1", [
                          "76.13%",
                          "71.61%",
                          "62.74%"]),
                                  DataRequired(
                                      "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])

    q5e_code = FileField(
        'Question 5E Code: Submit the code you wrote for the percent accuracy calculation.',
        validators=[DataRequired("Please attach your code for Question 1A.")],
        filters=[lambda v: None if v == '' else v])

    q6a1 = StringField("Question 6A: True positives for alpha-helices",
                       validators=[CorrectAnswer(["126459"]), DataRequired(
                           "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])

    q6a2 = StringField("Question 6A: True negatives for alpha-helices",
                       validators=[CorrectAnswer(["261152"]), DataRequired(
                           "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])

    q6a3 = StringField("Question 6A: False positives for alpha-helices",
                       validators=[CorrectAnswer(["152226"]), DataRequired(
                           "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])

    q6a4 = StringField("Question 6A: False negatives for alpha-helices",
                       validators=[CorrectAnswer(["105063"]), DataRequired(
                           "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])

    q6a5 = StringField("Question 6A: Accuracy for alpha-helices. Enter as a percent to two decimal places, i.e. 0.5438654 would be entered as 54.39%",
                       validators=[CorrectAnswer(["60.1%", "60.10", "60.10%", "60.1"]), DataRequired(
                           "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])

    q6b1 = StringField("Question 6B: True positives for beta-strands",
                       validators=[CorrectAnswer(["98670"]), DataRequired(
                           "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])

    q6b2 = StringField("Question 6B: True negatives for beta-strands",
                       validators=[CorrectAnswer(["277492"]), DataRequired(
                           "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])

    q6b3 = StringField("Question 6B: False positives for beta-strands",
                       validators=[CorrectAnswer(["221513"]), DataRequired(
                           "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])

    q6b4 = StringField("Question 6B: False negatives for beta-strands. ",
                       validators=[CorrectAnswer(["47225"]), DataRequired(
                           "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])

    q6b5 = StringField("Question 6B: Accuracy for beta-strands. Enter as a percent to two decimal places, i.e. 0.5438654 would be entered as 54.39% ",
                       validators=[CorrectAnswer(["58.33%", "58.33", "58.33%", "58.33"]), DataRequired(
                           "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])

    q6c1 = StringField("Question 6C: True positives for combined (alpha-helices and beta-strands)",
                       validators=[CorrectAnswer(["225129"]), DataRequired(
                           "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])

    q6c2 = StringField("Question 6C: True negatives for combined (alpha-helices and beta-strands)",
                       validators=[CorrectAnswer(["538644"]), DataRequired(
                           "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])

    q6c3 = StringField("Question 6C: False positives for combined (alpha-helices and beta-strands)",
                       validators=[CorrectAnswer(["373739"]), DataRequired(
                           "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])

    q6c4 = StringField("Question 6C: False negatives for combined (alpha-helices and beta-strands)",
                       validators=[CorrectAnswer(["152288"]), DataRequired(
                           "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])

    q6c5 = StringField("Question 6C: Accuracy for combined (alpha-helices and beta-strands together). Enter as a percent to two decimal places, i.e. 0.5438654 would be entered as 54.39%",
                       validators=[CorrectAnswer(["59.22%", "59.22", "59.22%", "59.22"]), DataRequired(
                           "You must supply an answer to each question or you will not pass this Practical")],
                       filters=[lambda v: None if v == '' else v])

    q6d_code = FileField(
        'Question 6D Code: Submit the code you wrote for Question 6 (inner/new loops only).',
        validators=[DataRequired("Please attach your code for Question 6D.")],
        filters=[lambda v: None if v == '' else v])


    check = SubmitField("Check  answers")

    submit = SubmitField("Submit answers")

    questions = ['q1_code', 'q2', 'q3', 'q4', 'q5a1', 'q5a2', 'q5a3', 'q5a4', 'q5b', 'q5c',
                  'q5d', 'q5e_code', 'q6a1', 'q6a2', 'q6a3', 'q6a4', 'q6a5', 'q6b1', 'q6b2',
                 'q6b3', 'q6b4', 'q6b5', 'q6c1', 'q6c2', 'q6c3', 'q6c4', 'q6c5', 'q6d_code']


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
        'Question 1: What is the Newick string that would represent the phylogenetic tree, including distances?',
        validators=[CheckNewick('(((A:0.1,B:0.2):0.2,C:0.1):0.2,(D:0.3,(E:0.2,F:0.1):0.4):0.3)'),
                    Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    q2 = StringField(
        'Question 2: What is the Gamma distance between the two sequences in eh.aln? Your submitted answer should be rounded to three decimal places, e.g. 1.241525 would be 1.242',
        validators=[CorrectAnswer(['1.507']), Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    q3 = StringField(
        'Question 3: What is the node label for the closest common ancestor for nodes A0A1A8AU08 and G3PS36?',
        validators=[CorrectAnswer(['N_6X5OCZ']), Optional("Not completed")],
        filters=[lambda v: None if v == '' else v])

    q2_code = FileField('Upload the code for the extended version of calcDistances that you wrote for Question 2',
                            validators=[DataRequired("Please attach your code for Question 2.")])

    q3_code = FileField('Upload the code for identifying the common ancestor that you wrote for Question 3',
                             validators=[DataRequired("Please attach your code for Question 3.")])

    check = SubmitField("Check answers")

    submit = SubmitField("Submit answers")

    questions = ["q1", "q2", "q3", "q2_code", "q3_code"]


class SCIE2100PracticalAssessment3(FlaskForm):
    q1 = StringField('Question 1: Submit your predicted secondary structure.', validators=[
        CorrectAnswer(['CCCEEEEEHCHEEEEHCEHCECEEECEEEHCHHEHCECCCECEECHEECECCCHHHEEHCHHHEEHCECHHECEEECHHEHEHECE']), Optional("Not completed")],
                     filters=[lambda v: None if v == '' else v])

    q2a = StringField('Question 2A: Submit the sensitivity of class E to two decimal places.', validators=[
        CorrectAnswer(['0.58']), Optional("Not completed")],
                      filters=[lambda v: None if v == '' else v])

    q2b = StringField('Question 2B: Submit the specificity of class E to two decimal places.', validators=[
        CorrectAnswer(['0.64']), Optional("Not completed")],
                      filters=[lambda v: None if v == '' else v])

    q2_code = FileField(
        'Question 2 Code: Submit the code you wrote to calculate sensitivity and specificity.',
        validators=[DataRequired("Please attach your code for Question 2.")],
        filters=[lambda v: None if v == '' else v])

    q3 = StringField(
        'Question 3: Please submit your regular expression. You only need to provide your regular expression, e.g. only paste in something in this format - [AC]C[AT]AT.[AT] ',
        validators=[CheckRegex(['chr7:130602946-130603045,', 'chr15:5089967-5090066,', 'chr19:23226975-23227074,'], os.getcwd() + "/static/python/files/chipseq.fa", "match"), Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    q4 = StringField(
        'Question 4: Please submit your regular expression. You only need to provide your regular expression, e.g. only paste in something in this format - [AC]C[AT]AT.[AT] ',
        validators=[CheckRegex(['RPL6B', 'SRM1', 'TAF2', 'GAT2', 'YER064C', 'SUB1', 'SNO4', 'RPL28', 'MUB1', 'DOT1'], os.getcwd() + "/static/python/files/yeast_promoters.fa", 'search'), Optional("Not completed")], filters=[lambda v: None if v == '' else v])

    q4_code = FileField(
        'Question 4 Code: Submit the code you wrote to load the files and extract the sequences to build the regular expression',
        validators=[DataRequired("Please attach your code for Question 2.")],
        filters=[lambda v: None if v == '' else v])

    questions = ["q1", "q2a", "q2b", "q2_code", "q3", "q4", "q4_code"]

    interview_questions = ["Test question", "Second question"]

    check = SubmitField("Check answers")

    submit = SubmitField("Submit answers")
