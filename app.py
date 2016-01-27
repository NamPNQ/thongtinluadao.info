# -*- coding: utf-8 -*-
"""
    app
    ~~~

    TTLD app
"""

import os
from flask import Flask, render_template
from flask.ext.redis import FlaskRedis

redis_store = FlaskRedis()

app = Flask(__name__)
app.config.from_object('app_config')
if os.getenv('ENV_STAGE', 'dev') == 'test':
    app.config.from_object('tests.settings')

redis_store.init_app(app)


@app.route('/')
def index():
    return render_template('index.html', body_class="index")

if __name__ == '__main__':
    app.run(debug=True)
