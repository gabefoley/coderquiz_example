from typing import Any
from flask import Flask, render_template, request, session, redirect, url_for, send_file
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from models import db, User, SubmissionPracticeQuiz, SubmissionSCIE2100Practical1
from forms import SignupForm, LoginForm, QueryForm, SubmissionForm, PracticeQuiz, EmailForm, PasswordForm
from forms_scie2100 import SCIE2100Practical1
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, DataError
from os.path import join
from io import BytesIO
import datetime
import pytz
import os
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from werkzeug.datastructures import FileStorage
from itsdangerous import URLSafeTimedSerializer
from flask import flash
from flask_mail import Mail, Message

application = Flask(__name__, static_url_path="")

application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///coderquiz2018'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
application.config['UPLOADED_IMAGES_DEST'] = os.getcwd() + "/static/uploads"
# application.config['UPLOADED_IMAGES_DEST'] =  "/static/uploads"

images = UploadSet('images', IMAGES)
configure_uploads(application, images)
patch_request_class(application)

db.init_app(application)

application.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'coderquiz@gmail.com',
    MAIL_PASSWORD = 'coderquiz2020',
))
mail = Mail(application)

application.secret_key = 'development-key'

BASE_ROUTE = '/coderquiz'

admin = ['40880084', '43558898', '123456789']

class SCIE2100_Exception(Exception):
    pass

def local(route: str) -> str:
	if BASE_ROUTE == '/':
		return route
	else:
		return join(BASE_ROUTE, route[1:])

def local_url_for(*args, **kwargs) -> str:
    new_url = local(url_for(*args, **kwargs))
    if new_url.count(BASE_ROUTE[1:]) == 1:
        fixed_url = new_url
        return new_url
    else:
        fixed_url = '/'.join(new_url.split('/')[2:])
    assert fixed_url.count(BASE_ROUTE[1:]) == 1, fixed_url
    return fixed_url

def url_for_static(filename):
    root = application.config.get('STATIC_ROOT', '')
    print (root)
    print (filename)

def local_redirect(*args, **kwargs) -> Any:
    return redirect(local_url_for(*args, **kwargs))

@application.route(local("/"))
def index():
    if 'studentno' in session:
        return render_template('landing.html', studentno=session['studentno'], url_for=url_for)
    else:
        return render_template("index.html", url_for=url_for)

@application.route(local("/signup"), methods=['GET', 'POST'])
def signup():
    if 'studentno' in session:
        return render_template('landing', url_for=url_for)

    form = SignupForm()

    if request.method == 'POST':
        try:
            if form.validate() == False:
                return render_template("signup.html", form=form, url_for=url_for, errors=[])
            else:
                newuser = User(form.first_name.data, form.last_name.data, form.studentno.data, form.email.data, form.password.data)
                db.session.add(newuser)
                db.session.commit()
                send_confirmation_email(newuser.email)
        except IntegrityError as e:
            if len(form.studentno.data) < 8:
                return render_template("signup.html", form=form, url_for=url_for, errors=['Please use all 8 digits for you student number'])
            else:
                return render_template("signup.html", form=form, url_for=url_for, errors=['This email is already taken.'])

        except DataError as e:
            return render_template("signup.html", form=form, url_for=url_for, errors=['Please provide a valid student number (integer).'])
        session['studentno'] = newuser.studentno

        print ('here')
        return render_template("landing.html", studentno=session['studentno'], url_for=url_for, first_time=True)

    elif request.method == 'GET':
        return render_template("signup.html", form=form, url_for=url_for, errors=[])

@application.route(local("/login"), methods=["GET", "POST"])
def login():
    if 'studentno' in session:
        return redirect(url_for('landing'))
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
                        return render_template("landing.html", studentno=session['studentno'], url_for=url_for)

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

@application.route(local("/logout"))
def logout():
    session.pop('studentno', None)
    return render_template('index.html')

@application.route(local("/landing"))
def landing():
    if 'studentno' in session:

        return render_template("landing.html", studentno=session['studentno'], url_for=url_for)

@application.route(local("/practice"), methods=["GET", "POST"])
def practice():
    if 'studentno' not in session:
        return redirect(url_for('login'))
    form = PracticeQuiz()
    questions = ['q1', 'q2', 'q3']
    if request.method == "POST":
        if form.check.data and form.validate() == True:
            return render_template("practice.html", questions = questions, form=form)
        elif form.submit.data:

            # elif form.submit.data and form.validate() == True:

            correct = form.validate()

            incomplete = False

            if form.q1.data:
                q1 = form.q1.data
            else:
                q1 = "INCORRECT"
                incomplete = True

            if form.q2.data:
                q2 = form.q2.data
            else:
                q2 = "INCORRECT"
                incomplete = True


            if form.q3.data:
                q3 = form.q3.data
            else:
                q3 = "INCORRECT"
                incomplete = True


            dt = datetime.datetime.now(pytz.timezone('Australia/Brisbane'))


            form_submission = SubmissionPracticeQuiz(session['studentno'], dt, correct, incomplete, q1, q2, q3)
            # form.populate_obj(form_submission)
            db.session.add(form_submission)
            db.session.commit()

            return render_template('success.html', incomplete=incomplete, correct=correct, url_for=url_for)

        else:
            return render_template("practice.html", questions=questions, form=form)

    elif request.method == "GET":
        return render_template("practice.html", questions=questions, form=form)

@application.route(local("/scie2100_practical1"), methods=["GET", "POST"])
def scie2100_practical1():
    if 'studentno' not in session:
        return redirect(url_for('login'))
    form = SCIE2100Practical1()
    questions = ['q1', 'q2a', 'q2b', 'q3a', 'q3b', 'q4a', 'q4b', 'q4_code', 'q5', 'q5_code', 'q6a', 'q6b', 'q6c_image', 'q6d']
    if request.method == "POST":
        if form.check.data and form.validate() == True:
            return render_template("scie2100practical1.html", questions = questions, form=form)
        elif form.submit.data:
            print ('here we go')

            # elif form.submit.data and form.validate() == True:

            correct = form.validate()
            incomplete = False

            if form.q1.data:
                q1 = form.q1.data
            else:
                q1 = "INCORRECT"
                incomplete = True

            if form.q2a.data:
                q2a = form.q2a.data
            else:
                q2a = "INCORRECT"
                incomplete = True


            if form.q2b.data:
                q2b = form.q2b.data
            else:
                q2b = "INCORRECT"
                incomplete = True


            if form.q3a.data:
                q3a = form.q3a.data
            else:
                q3a = "INCORRECT"
                incomplete = True


            if form.q3b.data:
                q3b = form.q3b.data
            else:
                q3b = "INCORRECT"
                incomplete = True


            if form.q4a.data:
                q4a = form.q4a.data
            else:
                q4a = "INCORRECT"
                incomplete = True


            if form.q4b.data:
                q4b = form.q4b.data
            else:
                q4b = "INCORRECT"
                incomplete = True


            if form.q5.data:
                q5 = form.q5.data
            else:
                q5 = "INCORRECT"
                incomplete = True


            if form.q6a.data:
                q6a = form.q6a.data
            else:
                q6a = "INCORRECT"
                incomplete = True


            if form.q6b.data:
                q6b = form.q6b.data
            else:
                q6b = "INCORRECT"
                incomplete = True


            if form.q6d.data:
                q6d = form.q6d.data
            else:
                q6d = "INCORRECT"
                incomplete = True


            if form.q4_code.data:
                q4_code = request.files['q4_code']
            else:
                q4_code = FileStorage()

            if form.q5_code.data:
                q5_code = request.files['q5_code']
                print (type(q5_code))
            else:
                q5_code = FileStorage()

            if form.q6c_image.data:
                q6c_filename = images.save(form.q6c_image.data)
                q6c_url = images.url(q6c_filename)
            else:
                q6c_url = ""

            print (q6c_url)


            dt = datetime.datetime.now(pytz.timezone('Australia/Brisbane'))


            form_submission = SubmissionSCIE2100Practical1(session['studentno'], dt, correct, incomplete, q1, q2a, q2b, q3a, q3b, q4a, q4b, q4_code.read(), q5, q5_code.read(), q6a, q6b, q6c_url, q6d)
            # form.populate_obj(form_submission)
            db.session.add(form_submission)
            db.session.commit()

            return render_template('success.html', url_for=url_for, correct=correct, incomplete=incomplete)

        else:
            return render_template("scie2100practical1.html", questions=questions, form=form)

    elif request.method == "GET":
        return render_template("scie2100practical1.html", questions=questions, form=form)

@application.route(local("/submissiondynamic"), methods=["GET", "POST"])
def submissiondynamic():
    form = SubmissionForm()
    if request.method == "POST":
        studentno = str(session['studentno'])
        item = form.assessment_item.data
        request_name = item[10:]
        questions = eval(request_name + '.questions')
        if form.records.data == 'Latest':
            results = eval('[' + item + '.query.filter_by(studentno=studentno).order_by(desc("submissiontime")).limit(1).first()]')
            if (results[0] == None):
                return render_template("submissiondynamic.html", form=form,
                                       errors="You haven't submitted this assessment item")

            edited_results = build_results(results, questions)


            return render_template("submissiondynamic.html", form=form, studentno=studentno, results=edited_results)

        elif form.records.data == 'All':
            results = eval(item + '.query.filter_by(studentno=studentno).order_by(desc("submissiontime"))')
            print (type(results))
            if not results.count():
                return render_template("submissiondynamic.html", form=form,
                                       errors="You haven't submitted this assessment item")

            edited_results = build_results(results, questions)

            return render_template("submissiondynamic.html", form=form, studentno=studentno, results=edited_results)


        else:
            return render_template("submissiondynamic.html", form=form)



    if 'studentno' not in session:
        return redirect(url_for('login'))
    else:
        return render_template("submissiondynamic.html", form=form)

def build_results(results, questions):
    """
    Take a list of submissions and return an edited list of dictionaries that seperates the different information
    :param results: The list of submissions
    :return: A list of dictionaries with the edited results
    """
    edited_results = []
    for result in results:
        correct = result.correct
        incomplete = result.incomplete
        submission_time = str(result.submissiontime).split(".")[0]
        joined_list = []
        code_list = []
        image_list = []
        for question in questions:
            answer = eval('result.' + question)
            if 'image' in question:
                filepath = "/uploads/" + answer.split("/")[-1]
                print (filepath)
                image_list.append([question, filepath])
            elif type(answer) == str:
                joined_list.append([question, answer])
            elif 'code' in question:
                code_list.append([question, highlight(answer, PythonLexer(), HtmlFormatter())])
        edited_result = {"results": joined_list, "submission_time": submission_time, "correct": correct, "incomplete" : incomplete, "code_list": code_list,
             "image_list": image_list}
        edited_results.append(edited_result)

    return edited_results



@application.route(local("/query"), methods=["GET", "POST"])
def query():
    if 'studentno' not in session:
        return redirect(url_for('login'))

    if str(session['studentno']) not in admin:
        return redirect(url_for('landing'))
    form = QueryForm()

    if request.method == "POST" and not form.studentno.data:
        return render_template("query.html", form=form)

    elif request.method == "POST" and form.submit.data:
        studentno = form.studentno.data
        item = form.assessment_item.data
        request_name = item[10:]
        questions = eval(request_name + '.questions')
        if form.records.data == 'Latest':
            results = eval(
                '[' + item + '.query.filter_by(studentno=studentno).order_by(desc("submissiontime")).limit(1).first()]')
            if (results[0] == None):
                return render_template("query.html", form=form,
                                       errors="This student hasn't submitted this assessment item")

            edited_results = build_results(results, questions)

            return render_template("query.html", form=form, studentno=studentno, results=edited_results)

        elif form.records.data == 'All':
            results = eval(item + '.query.filter_by(studentno=studentno).order_by(desc("submissiontime"))')
            if not results.count():
                return render_template("query.html", form=form,
                                       errors="This student hasn't submitted this assessment item")

            edited_results = build_results(results, questions)

            return render_template("query.html", form=form, studentno=studentno, results=edited_results)


        else:
            return render_template("query.html", form=form)



    # ## BELOW WAS FOR DOWNLOADING FILES
    # elif request.method == "POST" and form.download.data:
    #     studentno = form.studentno.data
    #     file_data = Submission.query.filter_by(studentno=studentno).order_by(desc('submissiontime')).limit(1).first()
    #     return send_file(BytesIO(file_data.file_upload), attachment_filename=studentno + "_Q2.py", as_attachment=True)
    #
    #
    # elif request.method == "POST" and form.download2.data:
    #     studentno = form.studentno.data
    #     file_data = Submission.query.filter_by(studentno=studentno).order_by(desc('submissiontime')).limit(1).first()
    #     return send_file(BytesIO(file_data.file_upload), attachment_filename=studentno + "_Q3.py", as_attachment=True)


    if 'studentno' not in session:
        return redirect(url_for('login'))
    else:
        return render_template("query.html", form=form)


def send_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(application.config['SECRET_KEY'])

    confirm_url = url_for(
        'confirm_email',
        token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
        _external=True)

    html = render_template(
        'emailconfirmation.html',
        confirm_url= confirm_url)

    send_email('Confirm Your Email Address', [user_email], "", html)

def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    msg.sender = "Coder Quiz"
    mail.send(msg)


@application.route(local('/confirm/<token>'))
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(application.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except:
        return render_template("confirmationerror.html", registration_message='The confirmation link is invalid or has expired.')

    user = User.query.filter_by(email=email).first()

    if user.email_confirmed:
        return render_template("confirmation.html", registration_message='Account already confirmed.')
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()

    return render_template("confirmation.html", registration_message = 'Thank you for confirming your email address!')


def send_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(application.config['SECRET_KEY'])

    password_reset_url = url_for(
        'reset_with_token',
        token=password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
        _external=True)

    html = render_template(
        'email_password_reset.html',
        password_reset_url=password_reset_url)

    send_email('Password Reset Requested', [user_email], "", html)


@application.route(local('/reset'), methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first_or_404()
        except:
            return render_template('password_reset_email.html', form=form, error="Invalid email address")

        if user.email_confirmed:
            send_password_reset_email(user.email)
            return render_template('password_reset_email.html', form=form, error="Please check your email for a password request")
        else:
            return render_template('password_reset_email.html', form=form, error="Your email address must be confirmed before attempting a password reset.")

    return render_template('password_reset_email.html', form=form)


@application.route(local('/reset/<token>'), methods=["GET", "POST"])
def reset_with_token(token):
    form = PasswordForm()

    try:
        password_reset_serializer = URLSafeTimedSerializer(application.config['SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        return render_template('reset_password_with_token.html', form=form, token=token, error="The password reset link is invalid or has expired'")
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=email).first_or_404()
        except:
            return render_template('reset_password_with_token.html', form=form, token=token,
                                   error="Invalid email address'")
        user.set_password(form.password.data)
        db.session.commit()
        return render_template('reset_password_with_token.html', form=form, token=token, error="Your password has been updated!'")


    return render_template('reset_password_with_token.html', form=form, token=token, error="")

if __name__ == "__main__":
    application.run(debug=True)
