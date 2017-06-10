from typing import Any
from flask import Flask, render_template, request, session, redirect, url_for, send_file, Markup
from models import db, User, Submission
from forms import SignupForm, LoginForm, AddressForm, QueryForm, SubmissionForm, SimpleQuiz
from sqlalchemy import desc, exc
from sqlalchemy.exc import IntegrityError, DataError
from os.path import join
from io import BytesIO
import datetime
import pytz
import os
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///quiz'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db.init_app(application)

application.secret_key = 'development-key'

BASE_ROUTE = '/SCIE2100'

admin = ['40880084', '43558898', '123456789']

@application.route("/")
def index():
    if 'studentno' in session:
        return render_template('landing.html', url_for=url_for)
    else:
        return render_template("index.html", url_for=url_for)

@application.route("/signup", methods=['GET', 'POST'])
def signup():
    if 'studentno' in session:
        return render_template('landing', url_for=url_for)

    form = SignupForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template("signup.html", form=form, url_for=url_for, errors=[])
        else:
            newuser = User(form.first_name.data, form.last_name.data, form.studentno.data, form.email.data, form.password.data)
            db.session.add(newuser)
            try:
                db.session.commit()
            except IntegrityError as e:
                return render_template("signup.html", form=form, url_for=url_for, errors=['This email is already taken.'])
            except DataError as e:
                return render_template("signup.html", form=form, url_for=url_for, errors=['Please provide a valid student number (integer).'])
            session['studentno'] = newuser.studentno

            return render_template('landing.html', url_for=url_for)

    elif request.method == 'GET':
        return render_template("signup.html", form=form, url_for=url_for, errors=[])

@application.route("/login", methods=["GET", "POST"])
def login():
    if 'studentno' in session:
        return ('landing')
    form = LoginForm()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                studentno = form.studentno.data
                password = form.password.data

                if studentno == "":
                    return render_template('login.html', form=form, studentnoerror = "Student number cannot be blank")

                if password == "":
                    return render_template('login.html', form=form,
                                           passworderror="Password cannot be blank")

                if User.query.filter_by(studentno=studentno).first():
                    user = User.query.filter_by(studentno=studentno).first()
                    check_pass = user.check_password(password)
                    if check_pass == True:
                        session['studentno'] = form.studentno.data
                        return render_template("landing.html")

                    else:
                        return render_template('login.html', form=form, passworderror="Password is incorrect")

                else:
                    return render_template("login.html", form=form, url_for=url_for, studentnoerror="No such student number is registered")


            else:
                return render_template('login.html', form=form)

        except DataError as e:
            return render_template('login.html', form=form, studentnoerror="Please provide a valid student number (integer).")



    elif request.method == "GET":
        return render_template('login.html', form=form)


    # if request.method == "POST":
    #     if form.validate() == False:
    #         return render_template("login.html", form=form, url_for=url_for, studentnoerror="No such student number is registered")
    #     else:
    #         studentno = form.studentno.data
    #         password = form.password.data
    #
    #         user = User.query.filter_by(studentno=studentno).first()
    #         if user is not None and user.check_password(password):
    #             session['studentno'] = form.studentno.data
    #             return render_template("landing.html")
    #         else:
    #             return render_template('login.html', form=form, passworderror=["Password is incorrect"])
    # elif request.method == "GET":
    #     return render_template('login.html', form=form)

@application.route("/logout")
def logout():
    session.pop('studentno', None)
    return render_template('index.html')

@application.route("/landing")
def landing():
    return render_template("landing.html")

@application.route("/assessment1", methods=["GET", "POST"])
def assessment1():
    if 'studentno' not in session:
        return ('login')
    form = SimpleQuiz()
    if request.method == "POST":
        if form.check.data and form.validate() == True:
            return render_template("assessment1.html", form=form)
        elif form.submit.data and form.validate() == True:
            if form.q1.data:
                q1 = form.q1.data
            else:
                q1 = "INCORRECT"
            if form.q2.data:
                q2 = form.q2.data
            else:
                q2 = "INCORRECT"
            if  form.q3.data:
                q3 = form.q3.data
            else:
                q3 = "INCORRECT"

            file = request.files['file_upload']

            dt = datetime.datetime.now(pytz.timezone('Australia/Brisbane'))
            form_submission = Submission(session['studentno'], dt, q1, q2, q3, file.read())
            # form.populate_obj(form_submission)
            db.session.add(form_submission)
            db.session.commit()

            return render_template('success.html', url_for=url_for)

        else:
            return render_template("assessment1.html", form=form)

    elif request.method == "GET":
        return render_template("assessment1.html", form=form)


@application.route("/submissiondynamic", methods=["GET", "POST"])
def submissiondynamic():
    form = SubmissionForm()
    if request.method == "POST":
        studentno = str(session['studentno'])
        records = form.records.data
        if form.records.data == 'Latest':
            results = [
                Submission.query.filter_by(studentno=studentno).order_by(desc('submissiontime')).limit(1).first()]
            code_output = [highlight(results[0].file_upload, PythonLexer(), HtmlFormatter())]
        else:
            code_output = []
            results = Submission.query.filter_by(studentno=studentno).order_by(desc('submissiontime'))
            for result in results:
                code_output.append(highlight(result.file_upload, PythonLexer(), HtmlFormatter()))
        return render_template("submissiondynamic.html", form=form, studentno=studentno, records=records, result=results, code_output = code_output)

    if 'studentno' not in session:
        return ('login')
    else:
        return render_template("submissiondynamic.html", form=form)

@application.route("/query", methods=["GET", "POST"])
def query():
    if str(session['studentno'])  not in admin:
        return ('index')
    form = QueryForm()

    if request.method == "POST" and not form.studentno.data:
        return render_template("query.html", form=form)

    elif request.method == "POST" and form.submit.data:
            studentno = form.studentno.data
            records = form.records.data

            # lexer = get_lexer_by_name("python", stripall=True)
            # formatter = HtmlFormatter(linenos=True, cssclass="source")
            # code = "def __init__(self, model, field, message=u'This element already exists.'):"
            # code_output = Markup(highlight(code, PythonLexer(), HtmlFormatter()))

            if form.records.data == 'Latest':
                results = [Submission.query.filter_by(studentno=studentno).order_by(desc('submissiontime')).limit(1).first()]
                code_output = [highlight(results[0].file_upload, PythonLexer(), HtmlFormatter())]

            else:
                code_output = []
                results = Submission.query.filter_by(studentno=studentno).order_by(desc('submissiontime'))
                for result in results:
                    code_output.append(highlight(result.file_upload, PythonLexer(), HtmlFormatter()))

            return render_template("query.html", form=form, studentno=studentno, records=records, result=results, code_output=code_output)



    elif request.method == "POST" and form.download.data:
        studentno = form.studentno.data
        file_data = Submission.query.filter_by(studentno=studentno).order_by(desc('submissiontime')).limit(1).first()
        return send_file(BytesIO(file_data.file_upload), attachment_filename=studentno + "_Q2.py", as_attachment=True)


    elif request.method == "POST" and form.download2.data:
        studentno = form.studentno.data
        file_data = Submission.query.filter_by(studentno=studentno).order_by(desc('submissiontime')).limit(1).first()
        return send_file(BytesIO(file_data.file_upload), attachment_filename=studentno + "_Q3.py", as_attachment=True)


    if 'studentno' not in session:
        return ('login')
    else:
        return render_template("query.html", form=form)




if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0')
