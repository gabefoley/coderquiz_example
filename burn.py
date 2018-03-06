from typing import Any
from flask import Flask, render_template, request, session, redirect, url_for, send_file, Markup
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

from models import db, User, SubmissionSCIE2100Practical1
from forms import SignupForm, LoginForm, AddressForm, QueryForm, SubmissionForm
from forms_scie2100 import SCIE2100Practical1
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
from base64 import b64encode


application = Flask(__name__, static_url_path="")

application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///coderquiz2018'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
application.config['UPLOADED_IMAGES_DEST'] = os.getcwd() + "/uploads"

images = UploadSet('images', IMAGES)
configure_uploads(application, images)
patch_request_class(application)

db.init_app(application)

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
        return render_template('landing.html', url_for=url_for)
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
        except IntegrityError as e:
            if len(form.studentno.data) < 8:
                return render_template("signup.html", form=form, url_for=url_for, errors=['Please use all 8 digits for you student number'])
            else:
                return render_template("signup.html", form=form, url_for=url_for, errors=['This email is already taken.'])

        except DataError as e:
            return render_template("signup.html", form=form, url_for=url_for, errors=['Please provide a valid student number (integer).'])
        session['studentno'] = newuser.studentno

        return render_template('landing.html', url_for=url_for)

    elif request.method == 'GET':
        return render_template("signup.html", form=form, url_for=url_for, errors=[])

@application.route(local("/login"), methods=["GET", "POST"])
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

@application.route(local("/logout"))
def logout():
    session.pop('studentno', None)
    return render_template('index.html')

@application.route(local("/landing"))
def landing():
    return render_template("landing.html")

@application.route(local("/scie2100_practical1"), methods=["GET", "POST"])
def scie2100_practical1():
    if 'studentno' not in session:
        return ('login')
    form = SCIE2100Practical1()
    questions = ['q1', 'q2a', 'q2b', 'q3a', 'q3b', 'q4a', 'q4b', 'q4_code', 'q5', 'q5_code', 'q6a', 'q6b', 'q6c_image', 'q6d']
    if request.method == "POST":
        if form.check.data and form.validate() == True:
            return render_template("scie2100practical1.html", questions = questions, form=form)
        elif form.submit.data:

            # elif form.submit.data and form.validate() == True:

            correct = form.validate()

            if form.q1.data:
                q1 = form.q1.data
            else:
                q1 = "INCORRECT"

            if form.q2a.data:
                q2a = form.q2a.data
            else:
                q2a = "INCORRECT"

            if form.q2b.data:
                q2b = form.q2b.data
            else:
                q2b = "INCORRECT"

            if form.q3a.data:
                q3a = form.q3a.data
            else:
                q3a = "INCORRECT"

            if form.q3b.data:
                q3b = form.q3b.data
            else:
                q3b = "INCORRECT"

            if form.q4a.data:
                q4a = form.q4a.data
            else:
                q4a = "INCORRECT"

            if form.q4b.data:
                q4b = form.q4b.data
            else:
                q4b = "INCORRECT"

            if form.q5.data:
                q5 = form.q5.data
            else:
                q5 = "INCORRECT"

            if form.q6a.data:
                q6a = form.q6a.data
            else:
                q6a = "INCORRECT"

            if form.q6b.data:
                q6b = form.q6b.data
            else:
                q6b = "INCORRECT"

            if form.q6d.data:
                q6d = form.q6d.data
            else:
                q6d = "INCORRECT"

            q4_code = request.files['q4_code']
            q5_code = request.files['q5_code']
            q6c_image = request.files['q6c_image']
            # q6c_filename = images.save(request.files['q6c_image'])
            q6c_filename = images.save(form.q6c_image.data)
            q6c_url = images.url(q6c_filename)

            print (q6c_filename)
            print (q6c_url)

            dt = datetime.datetime.now(pytz.timezone('Australia/Brisbane'))


            form_submission = SubmissionSCIE2100Practical1(session['studentno'], dt, correct, q1, q2a, q2b, q3a, q3b, q4a, q4b, q4_code.read(), q5, q5_code.read(), q6a, q6b, q6c_url, q6d)
            # form.populate_obj(form_submission)
            db.session.add(form_submission)
            db.session.commit()

            return render_template('success.html', url_for=url_for)

        else:
            return render_template("scie2100practical1.html", questions=questions, form=form)

    elif request.method == "GET":
        return render_template("scie2100practical1.html", questions=questions, form=form)

@application.route(local("/submissiondynamic"), methods=["GET", "POST"])
def submissiondynamic():
    form = SubmissionForm()
    if request.method == "POST":
        studentno = str(session['studentno'])
        records = form.records.data
        item = form.assessment_item.data
        request_name = item[10:]
        questions = eval(request_name + '.questions')
        if form.records.data == 'Latest':
            results = eval('[' + item + '.query.filter_by(studentno=studentno).order_by(desc("submissiontime")).limit(1).first()]')
            correct = results[0].correct
            submission_time = str(results[0].submissiontime).split(".")[0]

        elif form.records.data == 'All':
            # code_output = []
            results = eval(item + '.query.filter_by(studentno=studentno).order_by(desc("submissiontime"))')
            edited_results = []
            for result in results:
                correct = result.correct
                submission_time = str(result.submissiontime).split(".")[0]

                joined_list = []
                code_list = []
                image_list = []
                for question in questions:
                    answer = eval('result.' + question)
                    if 'image' in question:
                        filepath = answer
                        image_list.append([question, filepath])
                    elif type(answer) == str:
                        joined_list.append([question, answer])
                    elif 'code' in question:
                        code_list.append([question, highlight(answer, PythonLexer(), HtmlFormatter())])


            return render_template("submissiondynamic.html", form=form, studentno=studentno,
                                       submission_time=submission_time, records=records, correct=correct,
                                       result=joined_list, code_list=code_list, image_list=image_list)

                # for result in results:
                # code_output.append(highlight(result.file_upload, PythonLexer(), HtmlFormatter()))
        else:
            return render_template("submissiondynamic.html", form=form)

        if (results[0] == None):
            return render_template("submissiondynamic.html", form=form, errors = "You haven't submitted this assessment item")

        joined_list = []
        code_list = []
        image_list = []
        for result in range(0,len(results)):
            for question in questions:
                print (question)
                answer = eval('results[result].' + question)
                if 'image' in question:
                    filepath = answer
                    print (filepath)
                    image_list.append([question, filepath ])
                elif type(answer) == str:
                    joined_list.append([question, answer])
                elif 'code' in question:
                    code_list.append([question, highlight(answer, PythonLexer(), HtmlFormatter())])
        edited_results = {"results" : joined_list, "submission_time" : submission_time, "correct" : correct, "code_list" : code_list, "image_list" : image_list}

        return render_template("submissiondynamic.html", form=form, studentno=studentno, submission_time=submission_time, records=records, correct= correct, result=joined_list, code_list= code_list, image_list = image_list)

    if 'studentno' not in session:
        return ('login')
    else:
        return render_template("submissiondynamic.html", form=form)

@application.route(local("/query"), methods=["GET", "POST"])
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
                results = [SubmissionBIOL3014_2.query.filter_by(studentno=studentno).order_by(desc('submissiontime')).limit(1).first()]
               # code_output = [highlight(results[0].file_upload, PythonLexer(), HtmlFormatter())]

            else:
                #code_output = []
                results = SubmissionBIOL3014_2.query.filter_by(studentno=studentno).order_by(desc('submissiontime'))
                #for result in results:
                 #   code_output.append(highlight(result.file_upload, PythonLexer(), HtmlFormatter()))

            return render_template("query.html", form=form, studentno=studentno, records=records, result=results)



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
    application.run(debug=True)
