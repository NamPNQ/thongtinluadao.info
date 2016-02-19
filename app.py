# -*- coding: utf-8 -*-
"""
    app
    ~~~

    TTLD app
"""

import os
from flask import Flask, render_template, request, session, url_for, redirect
from models import db, User
from flask_oauth import OAuth

app = Flask(__name__)
app.config.from_object('app_config')
if os.getenv('ENV_STAGE', 'dev') == 'test':
    app.config.from_object('tests.settings')

oauth = OAuth()
db.init_app(app)

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=app.config['GOOGLE_CLIENT_ID'],
                          consumer_secret=app.config['GOOGLE_CLIENT_SECRET'])


@app.route('/social/login/google')
def google_login():
    return google.authorize(callback=url_for('google_authorized', _external=True))


@app.route('/social/google/authorized')
@google.authorized_handler
def google_authorized(resp):
    access_token = resp['access_token']
    session['g_access_token'] = access_token, ''
    return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
    return session.get('g_access_token')


@app.route('/')
def index():
    if session.get('g_access_token'):
        print google.get('https://www.googleapis.com/oauth2/v1/userinfo').data
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
