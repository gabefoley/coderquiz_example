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

  def __init__(self, firstname, lastname, studentno, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.studentno = studentno.title()
    self.email = email.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

class Submission(db.Model):

  __tablename__ = "submissions"

  submissionid = db.Column(db.Integer, primary_key = True)
  studentno = db.Column(db.Integer)
  submissiontime = db.Column(db.DateTime(timezone=True))
  q1 = db.Column(db.String(255))
  q2 = db.Column(db.String(255))
  q3 = db.Column(db.String(255))
  file_upload = db.Column(db.LargeBinary)




  def __init__(self, studentno, submissiontime, q1, q2, q3, file_upload):
    self.studentno = studentno
    self.submissiontime = submissiontime
    self.q1 = q1
    self.q2 = q2
    self.q3 = q3
    self.file_upload = file_upload



