from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('main.html')

@app.route('/result/')
def result():
    return 'hi'


if __name__ == '__main__':
    app.run()
