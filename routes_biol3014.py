@application.route(local("/assessment1"), methods=["GET", "POST"])
def assessment1():
    if 'studentno' not in session:
        return ('login')
    form = BIOL3014Quiz1()
    if request.method == "POST":
        if form.check.data and form.validate() == True:
            return render_template("assessment1.html", form=form)
        elif form.submit.data and form.validate() == True:
            if form.q1a.data:
                q1a = form.q1a.data
            else:
                q1a = "INCORRECT"
            if form.q1b.data:
                q1b = form.q1b.data
            else:
                q1b = "INCORRECT"
            if form.q1c.data:
                q1c = form.q1c.data
            else:
                q1c = "INCORRECT"
            if form.q2a.data:
                q2a = form.q2a.data
            else:
                q2a = "INCORRECT"
            if form.q2b.data:
                q2b = form.q2b.data
            else:
                q2b = "INCORRECT"
            if form.q2c.data:
                q2c = form.q2c.data
            else:
                q2c = "INCORRECT"
            if  form.q3a.data:
                q3a = form.q3a.data
            else:
                q3a = "INCORRECT"
            if  form.q3b.data:
                q3b = form.q3b.data
            else:
                q3b = "INCORRECT"
            if  form.q3c.data:
                q3c = form.q3c.data
            else:
                q3c = "INCORRECT"

            dt = datetime.datetime.now(pytz.timezone('Australia/Brisbane'))
            form_submission = Submission(session['studentno'], dt, q1a, q1b, q1c, q2a, q2b, q2c, q3a, q3b, q3c)
            # form.populate_obj(form_submission)
            db.session.add(form_submission)
            db.session.commit()

            return render_template('success.html', url_for=url_for)

        else:
            return render_template("assessment1.html", form=form)

    elif request.method == "GET":
        return render_template("assessment1.html", form=form)

@application.route(local("/assessment2"), methods=["GET", "POST"])
def assessment2():
    if 'studentno' not in session:
        return ('login')
    form = BIOL3014Quiz2()
    if request.method == "POST":
        if form.check.data and form.validate() == True:
            return render_template("assessment2.html", form=form)
        elif form.submit.data and form.validate() == True:
            if form.q1.data:
                q1 = form.q1.data
            else:
                q1 = "INCORRECT"
            if form.q2a.data:
                q2a = form.q2a.data
            else:
                q2a = "INCORRECT"
            if  form.q2b.data:
                q2b = form.q2b.data
            else:
                q2b = "INCORRECT"

            dt = datetime.datetime.now(pytz.timezone('Australia/Brisbane'))
            form_submission = SubmissionBIOL3014_2(session['studentno'], dt, q1, q2a, q2b)
            db.session.add(form_submission)
            db.session.commit()

            return render_template('success.html', url_for=url_for)

        else:
            return render_template("assessment2.html", form=form)

    elif request.method == "GET":
        return render_template("assessment2.html", form=form)