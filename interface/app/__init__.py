from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile/<username>')
def profile(username):
    return('Hey there, %s!'%(username))

@app.route('/post/<int:post_id>')
def post(post_id):
    return('Hey there, %d!'%(post_id))


if __name__ == '__main__':
    app.run()
