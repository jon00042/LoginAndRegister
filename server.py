import re
from flask import Flask, session, request, redirect, render_template, flash, url_for
from db.data_layer import get_user_by_email, get_user_by_id, create_user

app = Flask(__name__)


EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')

@app.route('/')
def index():
    return render_template('index.html')

app.run(debug=True)