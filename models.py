from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  studentno = db.Column(db.Integer)
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))
  email_confirmation_sent_on = db.Column(db.DateTime, nullable=True)
  email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
  email_confirmed_on = db.Column(db.DateTime, nullable=True)

  def __init__(self, firstname, lastname, studentno, email, password, email_confirmation_sent_on=None):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.studentno = studentno.title()
    self.email = email.lower()
    self.set_password(password)
    self.email_confirmation_sent_on = email_confirmation_sent_on
    self.email_confirmed = False
    self.email_confirmed_on = None
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

class SubmissionSCIE2100Practical1(db.Model):
    __tablename__ = "scie2100practical1"

    submissionid = db.Column(db.Integer, primary_key=True)
    studentno = db.Column(db.Integer)
    submissiontime = db.Column(db.DateTime(timezone=True))
    correct = db.Column(db.Boolean)
    incomplete = db.Column(db.Boolean)

    q1 = db.Column(db.String())
    q2a = db.Column(db.String())
    q2b = db.Column(db.String())
    q3a = db.Column(db.String())
    q3b = db.Column(db.String())
    q4a = db.Column(db.String())
    q4b = db.Column(db.String())
    q4_code = db.Column(db.LargeBinary)
    q5 = db.Column(db.String())
    q5_code = db.Column(db.LargeBinary)
    q6a = db.Column(db.String())
    q6b = db.Column(db.String())
    q6c_image = db.Column(db.String())
    q6d = db.Column(db.String())

    def __init__(self, studentno, submissiontime, correct, incomplete, q1, q2a, q2b, q3a, q3b, q4a, q4b, q4_code, q5, q5_code, q6a, q6b, q6c_image, q6d):
        self.studentno = studentno
        self.submissiontime = submissiontime
        self.correct = correct
        self.incomplete = incomplete
        self.q1 = q1
        self.q2a = q2a
        self.q2b = q2b
        self.q3a = q3a
        self.q3b = q3b
        self.q4a = q4a
        self.q4b = q4b
        self.q4_code = q4_code
        self.q5 = q5
        self.q5_code = q5_code
        self.q6a = q6a
        self.q6b = q6b
        self.q6c_image = q6c_image
        self.q6d = q6d

class SubmissionSCIE2100Practical2(db.Model):
    __tablename__ = "scie2100practical2"

    submissionid = db.Column(db.Integer, primary_key=True)
    studentno = db.Column(db.Integer)
    submissiontime = db.Column(db.DateTime(timezone=True))
    correct = db.Column(db.Boolean)
    incomplete = db.Column(db.Boolean)

    q1a = db.Column(db.String())
    q1b = db.Column(db.String())
    q1c = db.Column(db.String())
    q1d = db.Column(db.String())
    q2a = db.Column(db.String())
    q2b = db.Column(db.String())
    q2c = db.Column(db.String())
    q2d = db.Column(db.String())
    q3_code = db.Column(db.LargeBinary)
    q3b = db.Column(db.String())
    q3c = db.Column(db.String())
    q4a = db.Column(db.String())
    q4b = db.Column(db.String())
    q4c = db.Column(db.String())
    q4d = db.Column(db.String())



    def __init__(self, studentno, submissiontime, correct, incomplete, q1a, q1b, q1c, q1d, q2a, q2b, q2c, q2d, q3_code, q3b, q3c, q4a, q4b, q4c, q4d):
        self.studentno = studentno
        self.submissiontime = submissiontime
        self.correct = correct
        self.incomplete = incomplete
        self.q1a = q1a
        self.q1b = q1b
        self.q1c = q1c
        self.q1d = q1d
        self.q2a = q2a
        self.q2b = q2b
        self.q2c = q2c
        self.q2d = q2d
        self.q3_code = q3_code
        self.q3b = q3b
        self.q3c = q3c
        self.q4a = q4a
        self.q4b = q4b
        self.q4c = q4c
        self.q4d = q4d

class SubmissionSCIE2100Practical3(db.Model):
    __tablename__ = "scie2100practical3"

    submissionid = db.Column(db.Integer, primary_key=True)
    studentno = db.Column(db.Integer)
    submissiontime = db.Column(db.DateTime(timezone=True))
    correct = db.Column(db.Boolean)
    incomplete = db.Column(db.Boolean)

    q1 = db.Column(db.String())
    q2a = db.Column(db.String())
    q2b = db.Column(db.String())
    q2c = db.Column(db.String())
    q3a = db.Column(db.String())
    q3b_code = db.Column(db.LargeBinary)
    q3c = db.Column(db.String())
    q4a = db.Column(db.String())
    q4b_code = db.Column(db.LargeBinary)
    q5 = db.Column(db.String())



    def __init__(self, studentno, submissiontime, correct, incomplete, q1, q2a, q2b, q2c, q3a, q3b_code, q3c, q4a, q4b_code, q5):
        self.studentno = studentno
        self.submissiontime = submissiontime
        self.correct = correct
        self.incomplete = incomplete
        self.q1 = q1
        self.q2a = q2a
        self.q2b = q2b
        self.q2c = q2c
        self.q3a = q3a
        self.q3b_code = q3b_code
        self.q3c = q3c
        self.q4a = q4a
        self.q4b_code = q4b_code
        self.q5 = q5

class SubmissionSCIE2100Practical4(db.Model):
    __tablename__ = "scie2100practical4"

    submissionid = db.Column(db.Integer, primary_key=True)
    studentno = db.Column(db.Integer)
    submissiontime = db.Column(db.DateTime(timezone=True))
    correct = db.Column(db.Boolean)
    incomplete = db.Column(db.Boolean)

    q1a_code = db.Column(db.LargeBinary)
    q1b = db.Column(db.String())
    q1c = db.Column(db.String())
    q2a_code = db.Column(db.LargeBinary)
    q2b = db.Column(db.String())
    q3a_image = db.Column(db.String())
    q3b_code = db.Column(db.LargeBinary)
    q4a = db.Column(db.String())
    q4b = db.Column(db.String())



    def __init__(self, studentno, submissiontime, correct, incomplete, q1a_code, q1b, q1c, q2a_code, q2b, q3a_image, q3b_code, q4a, q4b):
        self.studentno = studentno
        self.submissiontime = submissiontime
        self.correct = correct
        self.incomplete = incomplete
        self.q1a_code = q1a_code
        self.q1b = q1b
        self.q1c = q1c
        self.q2a_code = q2a_code
        self.q2b = q2b
        self.q3a_image = q3a_image
        self.q3b_code = q3b_code
        self.q4a = q4a
        self.q4b = q4b

class SubmissionSCIE2100Practical5(db.Model):
    __tablename__ = "scie2100practical5"

    submissionid = db.Column(db.Integer, primary_key=True)
    studentno = db.Column(db.Integer)
    submissiontime = db.Column(db.DateTime(timezone=True))
    correct = db.Column(db.Boolean)
    incomplete = db.Column(db.Boolean)

    q1a = db.Column(db.String())
    q1b = db.Column(db.String())
    q1c = db.Column(db.String())
    q2a = db.Column(db.String())
    q2b = db.Column(db.String())
    q2c = db.Column(db.String())
    q2d = db.Column(db.String())
    q3a = db.Column(db.String())
    q3b = db.Column(db.String())
    q4a = db.Column(db.String())
    q4b = db.Column(db.String())



    def __init__(self, studentno, submissiontime, correct, incomplete, q1a, q1b, q1c, q2a, q2b, q2c, q2d, q3a, q3b, q4a, q4b):
        self.studentno = studentno
        self.submissiontime = submissiontime
        self.correct = correct
        self.incomplete = incomplete
        self.q1a = q1a
        self.q1b = q1b
        self.q1c = q1c
        self.q2a = q2a
        self.q2b = q2b
        self.q2c = q2c
        self.q2d = q2d
        self.q3a = q3a
        self.q3b = q3b
        self.q4a = q4a
        self.q4b = q4b



class SubmissionSCIE2100Practical6(db.Model):
    __tablename__ = "scie2100practical6"

    submissionid = db.Column(db.Integer, primary_key=True)
    studentno = db.Column(db.Integer)
    submissiontime = db.Column(db.DateTime(timezone=True))
    correct = db.Column(db.Boolean)
    incomplete = db.Column(db.Boolean)

    q1_code = db.Column(db.LargeBinary)
    q2 = db.Column(db.String())
    q3 = db.Column(db.String())
    q4 = db.Column(db.String())
    q5a1 = db.Column(db.String())
    q5a2 = db.Column(db.String())
    q5a3 = db.Column(db.String())
    q5a4 = db.Column(db.String())
    q5b = db.Column(db.String())
    q5c = db.Column(db.String())
    q5d = db.Column(db.String())
    q5e_code = db.Column(db.LargeBinary)
    q6a1 = db.Column(db.String())
    q6a2 = db.Column(db.String())
    q6a3 = db.Column(db.String())
    q6a4 = db.Column(db.String())
    q6a5 = db.Column(db.String())
    q6b1 = db.Column(db.String())
    q6b2 = db.Column(db.String())
    q6b3 = db.Column(db.String())
    q6b4 = db.Column(db.String())
    q6b5 = db.Column(db.String())
    q6c1 = db.Column(db.String())
    q6c2 = db.Column(db.String())
    q6c3 = db.Column(db.String())
    q6c4 = db.Column(db.String())
    q6c5 = db.Column(db.String())
    q6d_code = db.Column(db.LargeBinary)




    def __init__(self, studentno, submissiontime, correct, incomplete, q1_code, q2, q3, q4, q5a1, q5a2, q5a3, q5a4, q5b,
                  q5c, q5d, q5e_code, q6a1, q6a2, q6a3, q6a4, q6a5, q6b1, q6b2,
                 q6b3, q6b4, q6b5, q6c1, q6c2, q6c3, q6c4, q6c5, q6d_code):
        self.studentno = studentno
        self.submissiontime = submissiontime
        self.correct = correct
        self.incomplete = incomplete
        self.q1_code = q1_code
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.q5a1 = q5a1
        self.q5a2 = q5a2
        self.q5a3 = q5a3
        self.q5a4 = q5a4
        self.q5b = q5b
        self.q5c = q5c
        self.q5d = q5d
        self.q5e_code = q5e_code
        self.q6a1 = q6a1
        self.q6a2 = q6a2
        self.q6a3 = q6a3
        self.q6a4 = q6a4
        self.q6a5 = q6a5
        self.q6b1 = q6b1
        self.q6b2 = q6b2
        self.q6b3 = q6b3
        self.q6b4 = q6b4
        self.q6b5 = q6b5
        self.q6c1 = q6c1
        self.q6c2 = q6c2
        self.q6c3 = q6c3
        self.q6c4 = q6c4
        self.q6c5 = q6c5
        self.q6d_code = q6d_code


class SubmissionPracticeQuiz(db.Model):

    __tablename__ = "practice"

    submissionid = db.Column(db.Integer, primary_key=True)
    studentno = db.Column(db.Integer)
    submissiontime = db.Column(db.DateTime(timezone=True))
    correct = db.Column(db.Boolean)
    incomplete = db.Column(db.Boolean)

    q1 = db.Column(db.String())
    q2 = db.Column(db.String())
    q3 = db.Column(db.String())

    def __init__(self, studentno, submissiontime, correct, incomplete, q1, q2, q3):
        self.studentno = studentno
        self.submissiontime = submissiontime
        self.correct = correct
        self.incomplete = incomplete
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3

class SubmissionSCIE2100PracticalAssessment1(db.Model):

  __tablename__ = "scie2100practicalassessment1"

  submissionid = db.Column(db.Integer, primary_key = True)
  studentno = db.Column(db.Integer)
  submissiontime = db.Column(db.DateTime(timezone=True))
  correct = db.Column(db.Boolean)
  incomplete = db.Column(db.Boolean)
  q1 = db.Column(db.String())
  q2a = db.Column(db.String())
  q2b = db.Column(db.String())
  q2c = db.Column(db.String())
  q3 = db.Column(db.String())
  q4a = db.Column(db.String())
  q4b = db.Column(db.String())
  q4_code = db.Column(db.LargeBinary)

  def __init__(self, studentno, submissiontime, correct, incomplete, q1, q2a, q2b, q2c, q3, q4a, q4b, q4_code):
    self.studentno = studentno
    self.submissiontime = submissiontime
    self.correct = correct
    self.incomplete = incomplete
    self.q1 = q1
    self.q2a = q2a
    self.q2b = q2b
    self.q2c = q2c
    self.q3 = q3
    self.q4a = q4a
    self.q4b = q4b
    self.q4_code = q4_code

class SubmissionBIOL3014_2 (db.Model):
	__tablename__ = "submissions2"
	submissionid = db.Column(db.Integer, primary_key = True)
	studentno = db.Column(db.Integer)
	submissiontime = db.Column(db.DateTime(timezone=True))
	q1 = db.Column(db.String())
	q2a = db.Column(db.String())
	q2b = db.Column(db.String())

	def __init__(self, studentno, submissiontime, q1, q2a, q2b):
		self.studentno = studentno
		self.submissiontime = submissiontime
		self.q1 = q1
		self.q2a = q2a
		self.q2b = q2b



class SubmissionSCIE2100PracticalAssessment2(db.Model):

  __tablename__ = "scie2100practicalassessment2"

  submissionid = db.Column(db.Integer, primary_key = True)
  studentno = db.Column(db.Integer)
  submissiontime = db.Column(db.DateTime(timezone=True))
  correct = db.Column(db.Boolean)
  incomplete = db.Column(db.Boolean)
  q1 = db.Column(db.String())
  q2 = db.Column(db.String())
  q3 = db.Column(db.String())
  q2_code = db.Column(db.LargeBinary)
  q3_code = db.Column(db.LargeBinary)

  def __init__(self, studentno, submissiontime, correct, incomplete, q1, q2, q3, q2_code, q3_code):
    self.studentno = studentno
    self.submissiontime = submissiontime
    self.correct = correct
    self.incomplete = incomplete
    self.q1 = q1
    self.q2 = q2
    self.q3 = q3
    self.q2_code = q2_code
    self.q3_code = q3_code