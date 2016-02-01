# -*- coding: utf-8 -*-
"""
    app
    ~~~

    TTLD app
"""

import os
from flask import Flask, render_template, request
from models import db, User

app = Flask(__name__)
app.config.from_object('app_config')
if os.getenv('ENV_STAGE', 'dev') == 'test':
    app.config.from_object('tests.settings')

db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html', body_class="index")


@app.route('/login')
def login():
    email = request.args.get('email', 'test@ttld.info')
    user = User.get_user_by_email(email)
    if user:
        return user['id']
    else:
        return 'Not found'


@app.route('/entry')
def entry():
    return render_template('entry.html', body_class="entry")

if __name__ == '__main__':
    app.run(debug=True)
