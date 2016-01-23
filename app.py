from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('app_config')


@app.route('/')
def index():
    return render_template('index.html', body_class="index")

if __name__ == '__main__':
    app.run(debug=True)
