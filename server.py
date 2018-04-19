import re
from flask import Flask, session, request, redirect, render_template, flash, url_for
from db.data_layer import get_user_by_email, get_user_by_id, create_user
import sqlalchemy

app = Flask(__name__)
app.secret_key = 'garbage'

EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authenticate')
def authenticate():
    if ('user_id' in session):
        redirect(url_for('index'))
    return render_template('authenticate.html')

@app.route('/register', methods=['POST'])
def register():
    is_valid = True
    for field in ['html_email', 'html_username', 'html_password']:
        if (len(request.form[field]) <= 0):
            flash('{} cannot be empty!'.format(field[5:]))
            is_valid = False
    if (request.form['html_password'] != request.form['html_confirm']):
            flash('passwords do not match!')
            is_valid = False
    if (not is_valid):
        return redirect('authenticate')
    user = None
    try:
        user = create_user(request.form['html_email'], request.form['html_username'], request.form['html_password'])
    except sqlalchemy.exc.IntegrityError:
        pass
    except Exception as ex:
        print(ex)
    if (user is None):
        flash('email address already registered!')
        return redirect(url_for('authenticate'))
    session['user_id'] = user.id
    session['username'] = user.name
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    user = None
    try:
        user = get_user_by_email(request.form['html_email'])
    except sqlalchemy.orm.exc.NoResultFound:
        pass
    except Exception as ex:
        print(ex)
    if (user is not None and request.form['html_password'] == user.password):
        session['user_id'] = user.id
        session['username'] = user.name
        return redirect(url_for('index'))
    flash('invalid login attempt')
    return redirect(url_for('authenticate'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

app.run(debug=True)

