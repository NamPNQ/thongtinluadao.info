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

REDIRECT_URI = '/oauth2callback'

app = Flask(__name__)
app.config.from_object('app_config')
if os.getenv('ENV_STAGE', 'dev') == 'test':
    app.config.from_object('tests.settings')

app.secret_key = app.config['SECRET_KEY']
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
def social_login():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('google_login'))

    access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError

    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
        print res
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('google_login'))
        return res.read()

    return res.read()

@app.route('/google_login')
def google_login():
    return google.authorize(callback=url_for('google_authorized', _external=True))

@app.route('/social/google/authorized')
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))

@google.tokengetter
def get_access_token():
    return session.get('access_token')


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
